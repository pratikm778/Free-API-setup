#!/usr/bin/env python3
"""
Example usage of the Cascading AI API Flow system
"""
import sys
from cascade import CascadingAPIClient
from utils import format_usage_display

def basic_example():
    """Basic usage example"""
    print("[INFO] Basic Cascading AI API Example")
    print("=" * 40)

    try:
        # Initialize the client (automatically uses all available providers)
        client = CascadingAPIClient()
        print(f"[OK] Initialized with providers: {', '.join(client.get_available_providers())}")

        # Simple chat completion
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]

        response = client.chat_completion(messages)
        print(f"\n[INFO] AI Response:\n{response}")

        # Show usage stats
        stats = client.get_usage_stats()
        print(f"\n{format_usage_display(stats)}")

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    return True

def advanced_example():
    """Advanced usage with custom parameters"""
    print("\n[INFO] Advanced Example with Custom Parameters")
    print("=" * 45)

    try:
        client = CascadingAPIClient()

        # More complex conversation
        messages = [
            {"role": "system", "content": "You are a creative writing assistant. Keep responses engaging but concise."},
            {"role": "user", "content": "Write a short story about a robot who learns to paint."}
        ]

        # Custom parameters
        response = client.chat_completion(
            messages=messages,
            max_tokens=300,
            temperature=0.8,
            max_retries=3
        )

        print(f"[INFO] Creative AI Response:\n{response}")

        # Show updated stats  
        stats = client.get_usage_stats()
        print(f"\n{format_usage_display(stats)}")

    except Exception as e:
        print(f"[FAIL] Advanced example failed: {e}")
        return False

    return True

def interactive_chat():
    """Interactive chat session"""
    print("\n[INFO] Interactive Chat Session")
    print("=" * 30)
    print("Type 'quit', 'exit', or 'q' to end the session")

    try:
        client = CascadingAPIClient()
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Keep responses concise and friendly."}
        ]

        while True:
            user_input = input("\n[USER] You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("[INFO] Goodbye!")
                break

            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                response = client.chat_completion(messages, max_tokens=200)
                print(f"[AI] AI: {response}")
                messages.append({"role": "assistant", "content": response})

            except Exception as e:
                print(f"[FAIL] Error getting response: {e}")
                break

    except KeyboardInterrupt:
        print("\n[INFO] Chat ended by user")
    except Exception as e:
        print(f"[FAIL] Chat session error: {e}")

def main():
    """Main example function"""
    print("[INFO] Cascading AI API Flow - Examples")
    print("=" * 50)

    # Run basic example
    if not basic_example():
        print("\n[FAIL] Basic example failed. Check your API keys and setup.")
        sys.exit(1)

    # Run advanced example
    if not advanced_example():
        print("\n[WARN] Advanced example failed, but basic functionality works.")

    # Ask for interactive chat
    while True:
        choice = input("\n[CHOICE] Would you like to try interactive chat? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_chat()
            break
        elif choice in ['n', 'no']:
            print("[INFO] Skipping interactive chat.")
            break
        else:
            print("Please enter 'y' or 'n'")

    print("\n[INFO] Examples completed! Check the logs and usage_tracking.json for details.")

if __name__ == "__main__":
    main()