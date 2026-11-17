#!/usr/bin/env python3
"""Check the LLM connection aider will use (aider talks to models via litellm).

Sends one tiny request through litellm and fails unless a real, non-empty
chat answer comes back. API keys come from the environment
(e.g. GROQ_API_KEY). Set LITELLM_DEBUG=1 to log the exact request/response.

With --need-tokens N it also reads the provider's rate-limit headers
(x-ratelimit-remaining-tokens / x-ratelimit-reset-tokens, Groq: tokens per
minute) and, if fewer than N tokens are left, waits until the window resets
(max 65 s) so the following aider call is not rate limited.

Usage: litellm-debug.py <litellm-model> [--need-tokens N]
       e.g. litellm-debug.py groq/openai/gpt-oss-120b --need-tokens 7000
"""
import argparse
import os
import re
import sys
import time

MAX_WAIT_SECONDS = 65  # tokens-per-minute window is 60 s


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
    """Find a provider header, plain or with litellm's 'llm_provider-' prefix."""
    lowered = {str(k).lower(): v for k, v in (headers or {}).items()}
    return lowered.get(name) or lowered.get(f"llm_provider-{name}")


def seconds_to_wait(headers: dict, need_tokens: int) -> float:
    """0 if enough tokens are left in the window, else seconds until reset (capped)."""
    remaining = header(headers, "x-ratelimit-remaining-tokens")
    if remaining is None:
        return 0.0
    if int(float(remaining)) >= need_tokens:
        return 0.0
    reset = parse_duration(header(headers, "x-ratelimit-reset-tokens") or "")
    return min(reset + 1, MAX_WAIT_SECONDS) if reset else MAX_WAIT_SECONDS


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
        headers = (getattr(r, "_hidden_params", None) or {}).get("additional_headers") or {}
        remaining = header(headers, "x-ratelimit-remaining-tokens")
        if remaining is None:
            print("::notice::no rate-limit headers from provider, not waiting")
            return
        wait = seconds_to_wait(headers, args.need_tokens)
        print(f"tokens left this minute: {remaining}, needed: {args.need_tokens}")
        if wait:
            print(f"waiting {wait:.0f}s for the tokens-per-minute window to reset")
            time.sleep(wait)


if __name__ == "__main__":
    main()
