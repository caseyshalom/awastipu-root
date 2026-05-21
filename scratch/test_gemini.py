import asyncio
import os
import sys

# Hardcode path to backend
backend_path = r'c:\Users\HP\OneDrive\Documents\my-project\JuaraVibeCoding\awastipu-root\backend'
sys.path.append(backend_path)

from dotenv import load_dotenv
load_dotenv(os.path.join(backend_path, '.env'))

from app.services.ai_agent import simulate_chat

async def main():
    print("=== STARTING SIMULATION ===")
    r1 = await simulate_chat("phishing", user_message=None)
    session_id = r1["session_id"]
    print(f"Scammer: {r1['scammer_message']}")
    print(f"Red Flags: {r1['red_flags']}")
    print(f"Tip: {r1['tip']}")
    
    print("\n=== USER SENDS REPLY ===")
    user_reply = "Boleh kirim foto paketnya kak?"
    print(f"User: {user_reply}")
    r2 = await simulate_chat("phishing", user_message=user_reply, session_id=session_id)
    print(f"Scammer: {r2['scammer_message']}")
    print(f"Red Flags: {r2['red_flags']}")
    print(f"Tip: {r2['tip']}")

    print("\n=== USER SENDS SECOND REPLY ===")
    user_reply_2 = "Tapi HP saya Android. Kok bit.ly linknya?"
    print(f"User: {user_reply_2}")
    r3 = await simulate_chat("phishing", user_message=user_reply_2, session_id=session_id)
    print(f"Scammer: {r3['scammer_message']}")
    print(f"Red Flags: {r3['red_flags']}")
    print(f"Tip: {r3['tip']}")

if __name__ == "__main__":
    asyncio.run(main())
