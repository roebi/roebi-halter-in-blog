#!/usr/bin/env python3
"""Check the LLM connection aider will use (aider talks to models via litellm).

Sends one tiny request through litellm and fails unless a real, non-empty
chat answer comes back. API keys come from the environment
(e.g. GROQ_API_KEY). Set LITELLM_DEBUG=1 to log the exact request/response.
Usage: litellm-debug.py <litellm-model>   e.g. groq/openai/gpt-oss-120b
"""
import os
import sys

import litellm

if os.environ.get("LITELLM_DEBUG") == "1":
    litellm._turn_on_debug()

model = sys.argv[1]
print(f"model={model}")
try:
    r = litellm.completion(
        model=model,
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
