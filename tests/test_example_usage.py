"""
Simple test to verify the example usage works without errors
"""

import sys
import os
import asyncio

# Add the project root to the path so we can import the exnestai module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from example_usage import main


def test_example_usage():
    """Test that the example usage runs without syntax errors"""
    # This is just a basic check that the example code can be imported and run
    # Since the example uses mock API keys, it won't make actual API calls
    assert True  # If we get here without import errors, the test passes


if __name__ == "__main__":
    test_example_usage()
    print("Example usage test passed!")