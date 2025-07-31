# 🚀 Cascading Free AI API Flow

A robust Python system that automatically switches between multiple free AI API providers for reliable chat completions and text generation. Never worry about rate limits or downtime again!

## ✨ Features

- **🔄 Automatic Fallback**: Seamlessly switches providers when one fails or hits limits
- **📊 Usage Tracking**: Monitors daily usage across all providers  
- **⚡ Exponential Backoff**: Smart retry logic to handle temporary failures
- **🔧 Modular Design**: Clean, maintainable code split across multiple files
- **📈 Real-time Stats**: Monitor API consumption and performance
- **🛡️ Robust Error Handling**: Comprehensive logging and graceful failures

## 🎯 Supported Free Providers (2025)

| Provider | Daily Limit | Speed | Models |
|----------|-------------|-------|--------|
| **Groq** | 1,000 requests | ⚡ Fastest | Llama 3.3 70B |
| **Cerebras** | 1M tokens | 🚀 High throughput | Llama 3.3 70B |
| **OpenRouter** | 200 requests | 🔀 Multi-model | Various free |
| **Together AI** | 500 requests | 🤝 Open source | Llama variants |
| **Mistral** | 200 requests | 🇫🇷 European | Mistral 7B |
| **HuggingFace** | 1,000 requests | 🤗 Community | Llama 3.3 70B |
| **Fireworks** | 500 requests | 🎆 Fast inference | Llama variants |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Test Your Setup
```bash
python test_providers.py
```

### 4. Run Examples
```bash
python example.py
```

## 📁 Project Structure

```
cascading-ai-flow/
├── cascade.py          # Main cascading API client
├── providers.py        # Provider configurations
├── usage_tracker.py    # Usage tracking functionality
├── utils.py           # Utility functions
├── config.py          # Settings and configuration
├── example.py         # Usage examples
├── test_providers.py  # Provider testing script
├── requirements.txt   # Dependencies
├── .env.example      # Environment variables template
└── README.md         # This file
```

## 🔧 Basic Usage

```python
from cascade import CascadingAPIClient

# Initialize client (uses all available providers)
client = CascadingAPIClient()

# Send a message
messages = [
    {"role": "user", "content": "What is machine learning?"}
]

response = client.chat_completion(messages)
print(response)
```

## 🔑 API Keys Setup

Get free API keys from these providers:

| Provider | Signup Link | Notes |
|----------|-------------|-------|
| **Groq** | [console.groq.com](https://console.groq.com) | Fastest inference |
| **Cerebras** | [inference.cerebras.ai](https://inference.cerebras.ai) | High throughput |
| **OpenRouter** | [openrouter.ai](https://openrouter.ai) | Multiple models |
| **Together AI** | [api.together.ai](https://api.together.ai) | Open source focus |
| **Mistral** | [console.mistral.ai](https://console.mistral.ai) | European provider |
| **HuggingFace** | [huggingface.co](https://huggingface.co) | Community models |
| **Fireworks** | [fireworks.ai](https://fireworks.ai) | Fast inference |

> 💡 **Tip**: You don't need all keys! Start with 2-3 providers and add more later.

## 🧪 Testing

```bash
# Test all providers
python test_providers.py

# Quick test (individual providers only)
python test_providers.py --quick
```

## 📊 Advanced Usage

```python
from cascade import CascadingAPIClient

client = CascadingAPIClient()

# Custom parameters
response = client.chat_completion(
    messages=messages,
    max_tokens=500,
    temperature=0.8,
    max_retries=3
)

# Get usage statistics
stats = client.get_usage_stats()
print(stats)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Logging levels and file locations
- Default API parameters
- Retry and backoff settings
- Usage tracking options

## 📈 Monitoring

The system automatically:
- Tracks daily usage in `usage_tracking.json`
- Logs all activity to `cascade_api.log`
- Resets usage counters daily
- Provides real-time statistics

## 🐛 Troubleshooting

**No providers available**
- Check API keys in `.env` file
- Run `python test_providers.py` to verify setup

**Rate limit errors**
- System handles automatically with backoff
- Check usage with `client.get_usage_stats()`

**API errors**
- Check `cascade_api.log` for detailed errors
- Verify model names are correct

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - use freely in your projects!

## 🙏 Acknowledgments

Thanks to all AI providers offering free tiers and the developer community for inspiration.

---

⭐ **Star this repo if it helps you!** ⭐
