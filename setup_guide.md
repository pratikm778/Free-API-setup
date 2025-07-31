# 📋 Detailed Setup Guide

This comprehensive guide will walk you through setting up the Cascading Free AI API Flow system step by step.

## 🎯 What You'll Build

By the end of this guide, you'll have:
- A robust AI API system that never fails
- Automatic switching between 7+ free AI providers
- Usage tracking and monitoring
- Professional logging and error handling

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Internet connection** for API calls
- **Terminal/Command Prompt** access
- **Text editor** (VS Code, PyCharm, etc.)

## 🔧 Step 1: Installation

### Download the Project

```bash
# Option 1: Clone from GitHub
git clone https://github.com/pratikm778/Free-API-setup.git
cd Free-API-setup

# Option 2: Download and extract ZIP file
# Then navigate to the extracted folder
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues, try:
```bash
pip install --upgrade pip
pip install openai python-dotenv
```

## 🔑 Step 2: API Key Setup

### 2.1 Create Environment File

Copy the example file:
```bash
cp .env.example .env
```

### 2.2 Get Your API Keys

Visit each provider and sign up for free accounts:

#### 🚀 Groq (Priority 1 - Fastest)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with email
3. Navigate to "API Keys" in the dashboard
4. Click "Create API Key"
5. Copy the key and add to `.env`:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

#### 🧠 Cerebras (Priority 2 - High Throughput)
1. Visit [inference.cerebras.ai](https://inference.cerebras.ai)
2. Create account
3. Go to dashboard and find "API Keys"
4. Generate new key
5. Add to `.env`:
   ```
   CEREBRAS_API_KEY=csk_your_key_here
   ```

#### 🔀 OpenRouter (Priority 3 - Multi-Model)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up and verify email
3. Dashboard → "Keys" → "Create Key"
4. Add to `.env`:
   ```
   OPENROUTER_API_KEY=sk_or_your_key_here
   ```

#### 🤝 Together AI (Priority 4 - Open Source)
1. Visit [api.together.ai](https://api.together.ai)
2. Create account
3. API Keys section in dashboard
4. Add to `.env`:
   ```
   TOGETHER_API_KEY=your_together_key_here
   ```

#### 🇫🇷 Mistral (Priority 5 - European)
1. Go to [console.mistral.ai](https://console.mistral.ai)
2. Sign up for free account
3. Generate API key
4. Add to `.env`:
   ```
   MISTRAL_API_KEY=your_mistral_key_here
   ```

#### 🤗 HuggingFace (Priority 6 - Community)
1. Go to [huggingface.co](https://huggingface.co)
2. Create account
3. Settings → Access Tokens → New Token
4. Add to `.env`:
   ```
   HUGGINGFACE_API_KEY=hf_your_key_here
   ```

#### 🎆 Fireworks (Priority 7 - Fast Inference)
1. Visit [fireworks.ai](https://fireworks.ai)
2. Sign up for account
3. Get API key from dashboard
4. Add to `.env`:
   ```
   FIREWORKS_API_KEY=fw_your_key_here
   ```

### 2.3 Your Complete .env File

Your `.env` file should look like this:
```bash
# Primary providers (recommended to have at least these)
GROQ_API_KEY=gsk_your_groq_key_here
CEREBRAS_API_KEY=csk_your_cerebras_key_here
OPENROUTER_API_KEY=sk_or_your_openrouter_key_here

# Additional providers (optional but recommended)
TOGETHER_API_KEY=your_together_key_here
MISTRAL_API_KEY=your_mistral_key_here
HUGGINGFACE_API_KEY=hf_your_huggingface_key_here
FIREWORKS_API_KEY=fw_your_fireworks_key_here
```

> 💡 **Pro Tip**: You don't need ALL keys! Start with 2-3 providers and add more later.

## 🧪 Step 3: Testing Your Setup

### 3.1 Quick Test

Run the example:
```bash
python cascade.py
```

Expected output:
```
2025-07-31 10:30:15 - CascadingAPIClient - INFO - Initialized with 3 providers
2025-07-31 10:30:15 - CascadingAPIClient - INFO - 🔄 Trying Groq...
2025-07-31 10:30:16 - CascadingAPIClient - INFO - ✅ Success with Groq - Tokens used: 245

🤖 AI Response:
Quantum computing is a revolutionary approach to computation that harnesses the principles of quantum mechanics...

📊 Usage Statistics:
  Groq: 1/1000 requests (0.1%)
  OpenRouter: 0/200 requests (0.0%)
```

### 3.2 Test Each Provider

Create a test script `test_providers.py`:

```python
from cascade import CascadingAPIClient, PROVIDERS

def test_individual_providers():
    for provider_config in PROVIDERS:
        if not provider_config.api_key:
            print(f"❌ {provider_config.name}: No API key")
            continue

        try:
            client = CascadingAPIClient([provider_config])
            response = client.chat_completion([
                {"role": "user", "content": "Say hello"}
            ])
            print(f"✅ {provider_config.name}: Working")
        except Exception as e:
            print(f"❌ {provider_config.name}: {e}")

if __name__ == "__main__":
    test_individual_providers()
```

Run it:
```bash
python test_providers.py
```

## 🔧 Step 4: Customization

### 4.1 Modify Provider Order

Edit `cascade.py` to change the provider priority:

```python
# Move your preferred provider to the top
PROVIDERS = [
    ProviderConfig(
        name="YourFavoriteProvider",
        # ... config
    ),
    # ... other providers
]
```

### 4.2 Adjust Limits

Update daily limits based on your needs:

```python
ProviderConfig(
    name="Groq",
    daily_limit=500,  # Reduce if you want to save quota
    # ... other config
)
```

### 4.3 Add Custom Provider

```python
PROVIDERS.append(
    ProviderConfig(
        name="NewProvider",
        base_url="https://api.newprovider.com/v1",
        api_key=os.environ.get("NEW_PROVIDER_API_KEY", ""),
        model="new-model-name",
        daily_limit=1000,
        token_limit=50000,
        requests_per_minute=30
    )
)
```

## 📊 Step 5: Monitoring and Maintenance

### 5.1 Check Usage

View your usage tracking file:
```bash
cat usage_tracking.json
```

### 5.2 Monitor Logs

Check the log file for issues:
```bash
tail -f cascade_api.log
```

### 5.3 Reset Usage (New Day)

Usage automatically resets daily, but you can manually reset:
```bash
rm usage_tracking.json
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### "No API providers available"
- **Problem**: No valid API keys found
- **Solution**: Check your `.env` file and verify keys are correct

#### "Rate limit hit immediately"
- **Problem**: Already exceeded daily limits
- **Solution**: Wait for reset or add more providers

#### "All API providers failed"
- **Problem**: Network issues or all providers down
- **Solution**: Check internet connection and provider status pages

#### Import errors
- **Problem**: Missing dependencies
- **Solution**: Run `pip install -r requirements.txt`

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verify API Keys

Test individual keys:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.groq.com/openai/v1/models
```

## 🔄 Updates and Maintenance

### Keeping Limits Updated

Providers change their limits. Check these resources monthly:
- [Analytics Vidhya AI APIs](https://www.analyticsvidhya.com/blog/2025/02/top-free-apis-for-ai-development/)
- Provider documentation pages
- Community forums

### Adding New Providers

When new free providers emerge:
1. Add to `PROVIDERS` list
2. Add API key to `.env`
3. Test with the test script
4. Update documentation

## 🎉 You're All Set!

Your cascading AI API system is now ready! You have:
- ✅ Multiple free AI providers configured
- ✅ Automatic fallback system
- ✅ Usage tracking and monitoring
- ✅ Professional error handling
- ✅ Comprehensive logging

## 🚀 Next Steps

1. **Integrate into your project**: Import and use the `CascadingAPIClient`
2. **Monitor usage**: Check logs and usage stats regularly  
3. **Scale up**: Add more providers as needed
4. **Optimize**: Adjust provider order based on your use patterns

## 🆘 Need Help?

- Check the logs: `cascade_api.log`
- Test individual providers: `python test_providers.py`
- Verify API keys on provider websites
- Check provider status pages for outages

Happy coding! 🎉
