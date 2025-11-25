from tools import token_manager, record_on_chain
import json

def test_token_economy():
    print("=== Testing Token Economy ===")
    
    # Check initial balance
    print(f"Initial SystemDAO Balance: {token_manager.get_balance('SystemDAO')}")
    print(f"Initial Analyst Balance: {token_manager.get_balance('AnalystAgent')}")
    
    # Simulate Reward
    print("\nSimulating Reward...")
    msg = token_manager.reward_agent("AnalystAgent", 50, "Test Reward")
    print(msg)
    
    # Check new balance
    print(f"\nNew Analyst Balance: {token_manager.get_balance('AnalystAgent')}")
    print(f"New SystemDAO Balance: {token_manager.get_balance('SystemDAO')}")

if __name__ == "__main__":
    test_token_economy()
