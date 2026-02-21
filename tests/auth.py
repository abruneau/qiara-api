import base64
import hashlib
import hmac
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("QIARA_BASE_URL", "https://api.qiara.co/api/v1")
CUSTOMER_ID = int(os.getenv("QIARA_CUSTOMER_ID", "0"))
SECRET_KEY = os.getenv("QIARA_SECRET_KEY", "")  # The HMAC key — find this in the APK


def generate_response(challenge: str, key: str) -> str:
    try:
        # Decode Base64 inputs
        key_bytes = base64.b64decode(key)
        hashed = hmac.new(key_bytes, challenge.encode("utf-8"), hashlib.sha1)

        # The response is usually the hex digest of the HMAC
        return hashed.hexdigest()
    except Exception as e:
        raise ValueError(f"Error generating response: {e}")


def get_session_id() -> str:
    """Full auth flow: get challenge → compute response → get session."""

    # Step 1: get challenge
    r = requests.get(f"{BASE_URL}/login/challenge", verify=False)
    r.raise_for_status()
    challenge = r.json()["challenge"]

    # Step 2: compute HMAC-SHA256
    # Adjust this based on how the APK computes it
    challenge_rsp = generate_response(challenge, SECRET_KEY)

    # Step 3: create session
    r = requests.post(
        f"{BASE_URL}/login/new",
        json={
            "cust_id": CUSTOMER_ID,
            "challenge_rsp": challenge_rsp,
        },
        verify=False,
    )
    r.raise_for_status()
    return r.json()["session"]


if __name__ == "__main__":
    session = get_session_id()
    print(f"Session ID: {session}")
