#!/usr/bin/env python3
"""Diagnose the aider -> litellm -> GitHub Models connection.

Sends one tiny request the same way aider does (litellm, provider "openai",
OPENAI_API_BASE / OPENAI_API_KEY from env) with litellm debug logging on,
so the job log shows the exact URL, headers (key masked) and raw response.
"""
import os
import sys

import litellm

litellm._turn_on_debug()
model = sys.argv[1] if len(sys.argv) > 1 else "openai/openai/gpt-4o"
print(f"model={model} api_base={os.environ.get('OPENAI_API_BASE')}")
try:
    r = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=5,
        num_retries=0,
    )
    print("ANSWER:", r.choices[0].message.content)
except Exception as e:  # noqa: BLE001 - we want every failure printed
    print(f"FAILED: {type(e).__name__}: {e}")
    sys.exit(1)
