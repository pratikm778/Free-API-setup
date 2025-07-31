#!/usr/bin/env python3
"""
Test script to verify individual provider functionality
"""
import sys
from cascade import CascadingAPIClient
from providers import get_all_providers, get_available_providers
from utils import setup_logging, format_usage_display

# Setup logging for tests
setup_logging()

def test_individual_providers():
    """Test each provider individually"""
    print("[INFO] Testing Individual API Providers")
    print("=" * 40)

    all_providers = get_all_providers()
    working_providers = []
    failed_providers = []

    for provider in all_providers:
        if not provider.is_available:
            print(f"[WARN] {provider.name}: No API key provided (skipping)")
            continue

        print(f"[INFO] Testing {provider.name}...", end=" ", flush=True)

        try:
            # Create client with just this provider
            client = CascadingAPIClient([provider])

            # Simple test message
            response = client.chat_completion([
                {"role": "user", "content": "Say 'Hello from' followed by your model name"}
            ], max_tokens=50)

            print("[OK] Working")
            print(f"   [INFO] Response: {response[:80]}{'...' if len(response) > 80 else ''}")
            working_providers.append(provider.name)

        except Exception as e:
            print("[FAIL] Failed")
            print(f"   [WARN] Error: {str(e)}")
            failed_providers.append((provider.name, str(e)))

    # Summary
    print(f"\n[INFO] Individual Provider Test Results:")
    print(f"[OK] Working: {len(working_providers)} providers")
    for name in working_providers:
        print(f"   - {name}")

    print(f"[FAIL] Failed: {len(failed_providers)} providers")
    for name, error in failed_providers:
        print(f"   - {name}: {error}")

    return len(working_providers) > 0

def test_cascading_functionality():
    """Test the cascading functionality"""
    print("\n[INFO] Testing Cascading Functionality")
    print("=" * 35)

    try:
        available_providers = get_available_providers()

        if not available_providers:
            print("[FAIL] No providers available for cascading test")
            return False

        client = CascadingAPIClient()
        print(f"[INFO] Initialized with {len(client.providers)} providers")

        # Test with a standard question
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Be concise."},
            {"role": "user", "content": "What is 2+2? Answer in one sentence."}
        ]

        response = client.chat_completion(messages, max_tokens=100)
        print(f"[OK] Cascading test successful")
        print(f"[INFO] Response: {response}")

        # Show usage stats
        stats = client.get_usage_stats()
        print(f"\n{format_usage_display(stats)}")

        return True

    except Exception as e:
        print(f"[FAIL] Cascading test failed: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n[INFO] Testing Error Handling")
    print("=" * 25)

    try:
        client = CascadingAPIClient()

        # Test with empty messages (should fail gracefully)
        try:
            response = client.chat_completion([])
            print("[WARN] Empty messages test: Unexpectedly succeeded")
        except Exception as e:
            print("[OK] Empty messages test: Failed gracefully")

        # Test with very high token request (might hit limits)
        try:
            response = client.chat_completion([
                {"role": "user", "content": "Tell me about AI"}
            ], max_tokens=10000)  # High token count
            print("[OK] High token test: Handled appropriately")
        except Exception as e:
            print(f"[OK] High token test: Failed gracefully - {str(e)[:50]}...")

        return True

    except Exception as e:
        print(f"[FAIL] Error handling test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests comprehensively"""
    print("[INFO] Comprehensive Provider Test Suite")
    print("=" * 50)

    test_results = []

    # Test 1: Individual providers
    print("\n[INFO] Test 1: Individual Provider Functionality")
    individual_test = test_individual_providers()
    test_results.append(("Individual Providers", individual_test))

    if not individual_test:
        print("\n[FAIL] No providers working. Skipping remaining tests.")
        print("\n[INFO] Troubleshooting:")
        print("   1. Check your .env file has valid API keys")
        print("   2. Verify API keys on provider websites")
        print("   3. Ensure internet connection is stable")
        return False

    # Test 2: Cascading functionality
    print("\n[INFO] Test 2: Cascading Functionality")
    cascading_test = test_cascading_functionality()
    test_results.append(("Cascading", cascading_test))

    # Test 3: Error handling
    print("\n[INFO] Test 3: Error Handling")
    error_test = test_error_handling()
    test_results.append(("Error Handling", error_test))

    # Final summary
    print("\n" + "=" * 50)
    print("[INFO] FINAL TEST SUMMARY")
    print("=" * 50)

    passed_tests = 0
    for test_name, result in test_results:
        status = "[OK] PASSED" if result else "[FAIL] FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed_tests += 1

    print(f"\n[INFO] Overall: {passed_tests}/{len(test_results)} tests passed")

    if passed_tests == len(test_results):
        print("\n[INFO] All tests passed! Your setup is perfect.")
        print("\n[INFO] Next steps:")
        print("   • Run 'python example.py' for usage examples")
        print("   • Import CascadingAPIClient in your projects")
        print("   • Check logs in cascade_api.log")
    elif passed_tests > 0:
        print("\n[INFO] Some tests passed. Basic functionality works.")
        print("   • Check failed tests and fix any issues")
        print("   • You can still use working providers")
    else:
        print("\n[FAIL] All tests failed. Please check your setup.")
        print("\n[INFO] Setup help:")
        print("   • Review setup_guide.md")
        print("   • Check API keys in .env file")
        print("   • Verify internet connection")

    return passed_tests > 0

def main():
    """Main test function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--quick', '-q']:
        # Quick test mode
        test_individual_providers()
    else:
        # Comprehensive test mode
        run_comprehensive_test()

if __name__ == "__main__":
    main()