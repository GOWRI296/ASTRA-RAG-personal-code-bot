from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key found: {api_key}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"First 10 chars: {api_key[:10] if api_key else 'None'}")