"""
Provider configurations for free AI API services
"""
import os
from dataclasses import dataclass
from typing import List

@dataclass
class ProviderConfig:
    """Configuration for an AI API provider"""
    name: str
    base_url: str
    api_key: str
    model: str
    daily_limit: int
    token_limit: int
    requests_per_minute: int = 60

    def __post_init__(self):
        """Validate provider configuration"""
        if not self.api_key:
            print(f"Warning: No API key found for {self.name}")

    @property
    def is_available(self) -> bool:
        """Check if provider has valid API key"""
        return bool(self.api_key and self.api_key.strip())

def get_all_providers() -> List[ProviderConfig]:
    """Get all configured providers in priority order"""
    return [
        ProviderConfig(
            name="Groq",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY", ""),
            model="llama-3.3-70b-versatile",
            daily_limit=1000,
            token_limit=6000,
            requests_per_minute=30
        ),
        ProviderConfig(
            name="Cerebras",
            base_url="https://api.cerebras.ai/v1",
            api_key=os.environ.get("CEREBRAS_API_KEY", ""),
            model="llama-3.3-70b-instruct",
            daily_limit=1000,
            token_limit=60000,
            requests_per_minute=60
        ),
        ProviderConfig(
            name="OpenRouter",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            model="meta-llama/llama-3.3-70b-instruct:free",
            daily_limit=200,
            token_limit=20000,
            requests_per_minute=20
        ),
        ProviderConfig(
            name="Together",
            base_url="https://api.together.ai/v1",
            api_key=os.environ.get("TOGETHER_API_KEY", ""),
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            daily_limit=500,
            token_limit=50000,
            requests_per_minute=10
        ),
        ProviderConfig(
            name="Mistral",
            base_url="https://api.mistral.ai/v1",
            api_key=os.environ.get("MISTRAL_API_KEY", ""),
            model="mistral-7b-instruct",
            daily_limit=200,
            token_limit=20000,
            requests_per_minute=20
        ),
        ProviderConfig(
            name="HuggingFace",
            base_url="https://api-inference.huggingface.co/models",
            api_key=os.environ.get("HUGGINGFACE_API_KEY", ""),
            model="meta-llama/Llama-3.3-70B-Instruct",
            daily_limit=1000,
            token_limit=10000,
            requests_per_minute=10
        ),
        ProviderConfig(
            name="Fireworks",
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=os.environ.get("FIREWORKS_API_KEY", ""),
            model="accounts/fireworks/models/llama-v3p3-70b-instruct",
            daily_limit=500,
            token_limit=10000,
            requests_per_minute=5
        )
    ]

def get_available_providers() -> List[ProviderConfig]:
    """Get only providers with valid API keys"""
    return [p for p in get_all_providers() if p.is_available]
