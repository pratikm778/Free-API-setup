"""
Main cascading API client for reliable AI API access
"""
import logging
from typing import List, Dict, Optional

try:
    from openai import OpenAI
    import openai
except ImportError:
    print("OpenAI package not found. Install with: pip install openai")
    exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not found. Using system environment variables.")

from config import settings
from providers import ProviderConfig, get_available_providers
from usage_tracker import UsageTracker
from utils import setup_logging, exponential_backoff, adapt_request_params

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class CascadingAPIClient:
    """Main cascading API client with automatic provider fallback"""

    def __init__(self, providers: List[ProviderConfig] = None):
        """
        Initialize the cascading API client

        Args:
            providers: List of provider configurations. If None, uses all available providers.
        """
        self.providers = providers or get_available_providers()
        self.usage_tracker = UsageTracker()
        self.clients = {}

        if not self.providers:
            raise ValueError("No API providers available. Please set up your API keys.")

        # Initialize OpenAI clients for each provider
        for provider in self.providers:
            try:
                self.clients[provider.name] = OpenAI(
                    base_url=provider.base_url,
                    api_key=provider.api_key
                )
                logger.debug(f"Initialized client for {provider.name}")
            except Exception as e:
                logger.error(f"Failed to initialize client for {provider.name}: {e}")

        logger.info(f"Initialized cascading client with {len(self.providers)} providers")

    def _make_request(self, provider: ProviderConfig, messages: List[Dict], **kwargs) -> Optional[str]:
        """Make a request to a specific provider"""
        if provider.name not in self.clients:
            logger.error(f"No client available for {provider.name}")
            return None

        if not self.usage_tracker.check_limits(provider):
            return None

        client = self.clients[provider.name]

        try:
            # Prepare request parameters
            request_params = {
                "model": provider.model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", settings.DEFAULT_MAX_TOKENS),
                "temperature": kwargs.get("temperature", settings.DEFAULT_TEMPERATURE),
                "stream": kwargs.get("stream", False)
            }

            # Adapt parameters for specific providers
            request_params = adapt_request_params(provider.name, request_params)

            # Make the API call
            response = client.chat.completions.create(**request_params)

            # Update usage tracking
            tokens_used = response.usage.total_tokens if response.usage else 0
            self.usage_tracker.update_usage(provider.name, requests=1, tokens=tokens_used)

            logger.info(f"[OK] Success with {provider.name} - Tokens used: {tokens_used}")
            return response.choices[0].message.content

        except openai.RateLimitError as e:
            logger.warning(f"[WARN] Rate limit hit for {provider.name}: {e}")
            return None
        except openai.APIError as e:
            logger.error(f"[ERROR] API error with {provider.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"[FATAL] Unexpected error with {provider.name}: {e}")
            return None

    def chat_completion(self, messages: List[Dict], max_retries: int = None, **kwargs) -> str:
        """
        Get chat completion with automatic provider fallback

        Args:
            messages: List of message dictionaries
            max_retries: Maximum retries per provider (defaults to settings)
            **kwargs: Additional parameters for the API call

        Returns:
            Response content as string

        Raises:
            Exception: If all providers fail
        """
        if max_retries is None:
            max_retries = settings.DEFAULT_MAX_RETRIES

        for provider in self.providers:
            logger.info(f"[INFO] Trying {provider.name}...")

            for retry in range(max_retries + 1):
                result = self._make_request(provider, messages, **kwargs)

                if result:
                    return result

                if retry < max_retries:
                    exponential_backoff(retry)

            logger.warning(f"[FAIL] {provider.name} failed after {max_retries + 1} attempts")

        # If we get here, all providers failed
        error_msg = f"All {len(self.providers)} API providers failed"
        logger.error(error_msg)
        raise Exception(error_msg)

    def get_usage_stats(self) -> Dict:
        """Get usage statistics for all providers"""
        return self.usage_tracker.get_usage_stats(self.providers)

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [p.name for p in self.providers]