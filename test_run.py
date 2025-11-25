import os
from dotenv import load_dotenv
# Load environment variables first
load_dotenv()

from langchain_core.messages import HumanMessage
from main import app

def run_test():
    print("=== Running FinChain-Agent Test ===")
    query = "Analyze the recent performance of Bitcoin and Ethereum in the last week."
    print(f"Query: {query}")
    
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    print("\nProcessing...")
    try:
        for event in app.stream(initial_state, {"recursion_limit": 50}):
            for key, value in event.items():
                print(f"\n--- Node: {key} ---")
                if key in ["analyst_a", "analyst_b", "analyst_c"]:
                    print(f"  Report Generated.")
                elif key == "auditor":
                    print(f"  Winner: {value.get('winner')}")
                    print(f"  Reason: {value.get('audit_reason')[:100]}...")
                elif key == "blockchain":
                    print(f"  Block Hash: {value.get('block_hash')}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_test()
