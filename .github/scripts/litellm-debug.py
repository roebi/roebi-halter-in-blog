#!/usr/bin/env python3
"""Check the LLM connection aider will use (aider talks to models via litellm).

Sends one tiny request through litellm and fails unless a real, non-empty
chat answer comes back. API keys come from the environment
(e.g. GROQ_API_KEY). Set LITELLM_DEBUG=1 to log the exact request/response.

With --need-tokens N (Groq models only) it then makes one direct request to
the Groq API, because litellm does not pass the rate-limit headers through.
From x-ratelimit-remaining-tokens / x-ratelimit-reset-tokens (tokens per
minute) it waits until the window resets if fewer than N tokens are left,
and on HTTP 429 it waits as long as retry-after says. At most 3 probes and
65 s per wait, so the following aider call starts with a full token budget.

Usage: litellm-debug.py <litellm-model> [--need-tokens N]
       e.g. litellm-debug.py groq/openai/gpt-oss-120b --need-tokens 7000
Env:   GROQ_API_BASE overrides https://api.groq.com/openai/v1 (for tests)
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

MAX_WAIT_SECONDS = 65  # tokens-per-minute window is 60 s
MAX_PROBES = 3
GROQ_API_BASE = "https://api.groq.com/openai/v1"


def parse_duration(value: str) -> float:
    """Parse rate-limit reset values like '7.66s', '2m59.56s', '120ms'."""
    value = (value or "").strip()
    if not value:
        return 0.0
    try:
        return float(value)  # plain seconds
    except ValueError:
        pass
    total = 0.0
    for number, unit in re.findall(r"([\d.]+)(ms|h|m|s)", value):
        total += float(number) * {"ms": 0.001, "s": 1, "m": 60, "h": 3600}[unit]
    return total


def header(headers: dict, name: str) -> str | None:
    """Case-insensitive header lookup."""
    lowered = {str(k).lower(): v for k, v in (headers or {}).items()}
    return lowered.get(name)


def seconds_to_wait(headers: dict, need_tokens: int) -> float:
    """0 if enough tokens are left in the window, else seconds until reset (capped)."""
    remaining = header(headers, "x-ratelimit-remaining-tokens")
    if remaining is None:
        return 0.0
    if int(float(remaining)) >= need_tokens:
        return 0.0
    reset = parse_duration(header(headers, "x-ratelimit-reset-tokens") or "")
    return min(reset + 1, MAX_WAIT_SECONDS) if reset else MAX_WAIT_SECONDS


def groq_probe(model_id: str, api_key: str, base: str) -> tuple[int, dict]:
    """One tiny direct chat request; returns (HTTP status, response headers)."""
    body = json.dumps(
        {"model": model_id, "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 16}
    ).encode()
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "blog-workflow-token-check",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {})


def wait_for_groq_tokens(model: str, need_tokens: int, sleep=time.sleep, probe=groq_probe) -> None:
    """Probe Groq directly and wait until need_tokens fit into the TPM window."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    base = os.environ.get("GROQ_API_BASE", GROQ_API_BASE).rstrip("/")
    model_id = model.split("/", 1)[1]  # groq/openai/gpt-oss-120b -> openai/gpt-oss-120b
    for attempt in range(1, MAX_PROBES + 1):
        status, headers = probe(model_id, api_key, base)
        if status == 429:
            wait = min(parse_duration(header(headers, "retry-after") or "") + 1, MAX_WAIT_SECONDS)
            wait = wait if wait > 1 else MAX_WAIT_SECONDS
            print(f"token probe {attempt}: rate limited (429), waiting {wait:.0f}s")
            sleep(wait)
            continue
        if status != 200:
            print(f"::warning::token probe got HTTP {status}, not waiting")
            return
        remaining = header(headers, "x-ratelimit-remaining-tokens")
        if remaining is None:
            print("::notice::no rate-limit headers from Groq, not waiting")
            return
        wait = seconds_to_wait(headers, need_tokens)
        print(f"token probe {attempt}: {remaining} tokens left this minute, needed: {need_tokens}")
        if not wait:
            return
        print(f"waiting {wait:.0f}s for the tokens-per-minute window to reset")
        sleep(wait)
        return  # window has reset, aider can start
    print(f"::warning::still rate limited after {MAX_PROBES} probes, aider will retry by itself")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model")
    parser.add_argument("--need-tokens", type=int, default=0)
    args = parser.parse_args()

    import litellm

    if os.environ.get("LITELLM_DEBUG") == "1":
        litellm._turn_on_debug()

    print(f"model={args.model}")
    try:
        r = litellm.completion(
            model=args.model,
            messages=[{"role": "user", "content": "Say OK"}],
            # reasoning models (e.g. gpt-oss) spend tokens on thinking first;
            # a tiny limit would end before any answer text is written
            max_tokens=300,
            num_retries=0,
        )
        answer = (r.choices[0].message.content or "").strip()
    except Exception as e:  # noqa: BLE001 - we want every failure printed
        print(f"::error::LLM call failed: {type(e).__name__}: {e}")
        sys.exit(1)

    if not answer:
        print("::error::LLM returned an empty answer")
        sys.exit(1)
    print(f"LLM reachable, answer: {answer!r}")

    if args.need_tokens:
        if args.model.startswith("groq/"):
            wait_for_groq_tokens(args.model, args.need_tokens)
        else:
            print("::notice::token wait is only implemented for groq/ models")


if __name__ == "__main__":
    main()
