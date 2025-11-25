import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

load_dotenv()

def test_deepseek():
    print("Testing DeepSeek API...")
    try:
        llm = ChatOpenAI(
            model='deepseek-chat', 
            openai_api_key=os.environ.get("DEEPSEEK_API_KEY"), 
            openai_api_base='https://api.deepseek.com',
            max_tokens=100
        )
        response = llm.invoke("Hello, are you working?")
        print(f"DeepSeek Response: {response.content}")
        print("DeepSeek API: OK")
    except Exception as e:
        print(f"DeepSeek API Error: {e}")

def test_tavily():
    print("\nTesting Tavily API...")
    try:
        tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
        response = tavily_client.search("Bitcoin price", search_depth="basic")
        print(f"Tavily Response: Found {len(response.get('results', []))} results.")
        print("Tavily API: OK")
    except Exception as e:
        print(f"Tavily API Error: {e}")

if __name__ == "__main__":
    test_deepseek()
    test_tavily()
