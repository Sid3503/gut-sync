import requests
import time
import sys
import uuid

API_URL = "http://127.0.0.1:8000/webhook/incoming"
HEALTH_URL = "http://127.0.0.1:8000/health"

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Gut Health API - Interactive Client")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Targeting: {API_URL}\n")

    # 1. Check if API is running
    try:
        requests.get(HEALTH_URL, timeout=2)
        print("✅ API is online and healthy.")
    except requests.exceptions.ConnectionError:
        print("❌ API is NOT running.")
        print("Please run this command in a separate terminal:")
        print("   uvicorn src.web.api:app --reload")
        sys.exit(1)

    print("\nType your symptoms below (or 'quit' to exit).")
    
    while True:
        try:
            print("\n" + "─" * 40)
            user_input = input("User > ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Exiting.")
                break
            
            if not user_input:
                continue

            print(" [Sending to API...] ", end="", flush=True)
            start_t = time.perf_counter()
            
            payload = {
                "user_id": f"cli_user_{str(uuid.uuid4())[:8]}",
                "message": user_input,
                "source": "web"
            }
            
            response = requests.post(API_URL, json=payload, timeout=60)
            
            elapsed = time.perf_counter() - start_t
            print(f"Done ({elapsed:.2f}s)!\n")

            if response.status_code == 200:
                data = response.json()
                print("🤖 Agent Response:\n")
                print(data["report"])
                print(f"\n[Processing Time: {data['processing_time_ms']}ms]")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"\n❌ Client Error: {e}")

if __name__ == "__main__":
    main()
