import os
from dotenv import load_dotenv
load_dotenv()
from tools import record_on_chain
import json

def test_blockchain():
    print("=== Testing Blockchain Recording ===")
    dummy_data = {
        "report": "This is a test report.",
        "audit_result": "APPROVED",
        "status": "VERIFIED"
    }
    
    result = record_on_chain.invoke(json.dumps(dummy_data))
    print(f"Result: {result}")

if __name__ == "__main__":
    test_blockchain()
