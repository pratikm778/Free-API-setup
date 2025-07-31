"""
Utility functions for the cascading API system
"""
import logging
import time
from typing import Dict, Any

from config import settings

logger = logging.getLogger(__name__)

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def exponential_backoff(retry_count: int, max_delay: int = None) -> None:
    """Implement exponential backoff"""
    if max_delay is None:
        max_delay = settings.MAX_BACKOFF_DELAY

    delay = min(settings.BASE_BACKOFF_DELAY ** retry_count, max_delay)
    logger.info(f"Waiting {delay} seconds before retry...")
    time.sleep(delay)

def adapt_request_params(provider_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt request parameters for specific providers"""
    if provider_name == "Google AI Studio":
        # Google's API might have different parameter names
        # This is a placeholder - adjust based on actual requirements
        return params
    elif provider_name == "HuggingFace":
        # HuggingFace might need parameter adjustments
        return params

    return params

def format_usage_display(stats: Dict) -> str:
    """Format usage statistics for display"""
    lines = ["📊 Usage Statistics:"]
    for provider, data in stats.items():
        if data['requests_used'] > 0:
            lines.append(f"  🎯 {provider}: {data['requests_used']}/{data['requests_limit']} requests ({data['utilization_percent']}%)")
        else:
            lines.append(f"  ⚪ {provider}: 0/{data['requests_limit']} requests (0%)")
    return "\n".join(lines)
