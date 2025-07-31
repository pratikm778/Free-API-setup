"""
Usage tracking functionality for API providers
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

from config import settings

logger = logging.getLogger(__name__)

class UsageTracker:
    """Track API usage across providers"""

    def __init__(self, usage_file: str = None):
        self.usage_file = Path(usage_file or settings.USAGE_TRACKING_FILE)
        self.usage_data = self._load_usage()

    def _load_usage(self) -> Dict:
        """Load usage data from file"""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                # Reset daily counters if it's a new day
                current_date = datetime.now().strftime('%Y-%m-%d')
                for provider in data:
                    if data[provider].get('date') != current_date:
                        data[provider] = {
                            'date': current_date, 
                            'requests': 0, 
                            'tokens': 0
                        }
                return data
            except Exception as e:
                logger.error(f"Error loading usage data: {e}")
        return {}

    def _save_usage(self):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")

    def get_usage(self, provider_name: str) -> Dict:
        """Get current usage for a provider"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if provider_name not in self.usage_data:
            self.usage_data[provider_name] = {
                'date': current_date, 
                'requests': 0, 
                'tokens': 0
            }
        return self.usage_data[provider_name]

    def update_usage(self, provider_name: str, requests: int = 0, tokens: int = 0):
        """Update usage for a provider"""
        usage = self.get_usage(provider_name)
        usage['requests'] += requests
        usage['tokens'] += tokens
        self._save_usage()
        logger.debug(f"Updated usage for {provider_name}: +{requests} requests, +{tokens} tokens")

    def check_limits(self, provider) -> bool:
        """Check if provider has exceeded limits"""
        usage = self.get_usage(provider.name)

        if usage['requests'] >= provider.daily_limit:
            logger.warning(f"{provider.name} has exceeded daily request limit ({usage['requests']}/{provider.daily_limit})")
            return False

        # Rough daily token limit check (token_limit is typically per minute)
        daily_token_limit = provider.token_limit * 1440  # minutes in a day
        if usage['tokens'] >= daily_token_limit:
            logger.warning(f"{provider.name} has exceeded estimated daily token limit")
            return False

        return True

    def get_usage_stats(self, providers) -> Dict:
        """Get usage statistics for all providers"""
        stats = {}
        for provider in providers:
            usage = self.get_usage(provider.name)
            stats[provider.name] = {
                "requests_used": usage['requests'],
                "requests_limit": provider.daily_limit,
                "requests_remaining": max(0, provider.daily_limit - usage['requests']),
                "utilization_percent": round((usage['requests'] / provider.daily_limit) * 100, 2)
            }
        return stats
