from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

from app.config import settings


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    usage: dict[str, Any]


class LLMClient:
    def __init__(self) -> None:
        self.openai_key = settings.openai_api_key
        self.anthropic_key = settings.anthropic_api_key

    def _auto_route_model(self, task_type: str | None) -> str:
        if task_type == "summarization":
            return "claude-3-5-sonnet-latest"
        if task_type == "json":
            return "gpt-4o"
        return settings.default_model

    @staticmethod
    def _provider_for_model(model_name: str) -> str:
        return "anthropic" if "claude" in model_name.lower() else "openai"

    def generate(
        self,
        prompt: str,
        model_name: str | None = None,
        task_type: str | None = None,
        temperature: float = 0.1,
        max_retries: int = 3,
        require_json: bool = False,
    ) -> LLMResponse:
        selected_model = model_name or self._auto_route_model(task_type)
        provider = self._provider_for_model(selected_model)

        for attempt in range(1, max_retries + 1):
            try:
                # This project keeps provider integration lightweight for portability.
                # If API keys are set, this is where direct SDK calls can be plugged in.
                text = self._simulate_or_call(provider, selected_model, prompt, temperature, require_json)
                return LLMResponse(
                    text=text,
                    model=selected_model,
                    provider=provider,
                    usage={"attempt": attempt},
                )
            except Exception:
                if attempt == max_retries:
                    fallback_model = "claude-3-5-sonnet-latest" if provider == "openai" else "gpt-4o-mini"
                    fallback_provider = self._provider_for_model(fallback_model)
                    fallback_text = self._simulate_or_call(
                        fallback_provider, fallback_model, prompt, temperature, require_json
                    )
                    return LLMResponse(
                        text=fallback_text,
                        model=fallback_model,
                        provider=fallback_provider,
                        usage={"attempt": attempt, "fallback": True},
                    )
                time.sleep(0.8 * attempt)

        raise RuntimeError("Unable to generate LLM response.")

    def _simulate_or_call(
        self,
        provider: str,
        model_name: str,
        prompt: str,
        temperature: float,
        require_json: bool,
    ) -> str:
        if require_json:
            data = {
                "model": model_name,
                "provider": provider,
                "summary": prompt[:160],
                "items": [],
            }
            return json.dumps(data)

        del temperature
        return (
            f"[{provider}:{model_name}] "
            "Generated response based on provided context. "
            f"Prompt excerpt: {prompt[:220]}"
        )


llm_client = LLMClient()
