import hashlib
import hmac
import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# KHQR Configuration
KHQR_PROFILE_ID = os.getenv("KHQR_PROFILE_ID", "cEo4uXMQVGYb0PovjrdgBDlER5775BdX")
KHQR_SECRET_KEY = os.getenv("KHQR_SECRET_KEY", "luDfx5f5JXpyCdA4j4g9u1FssYSp2Uc0")
KHQR_GATEWAY_URL = os.getenv("KHQR_GATEWAY_URL", "https://khqr.cc/api/payment/request")
KHQR_VERIFY_URL = os.getenv("KHQR_VERIFY_URL", f"https://khqr.cc/api/{KHQR_PROFILE_ID}/payment-gateway/v1/payments/check-trans")

# Mock mode for testing when KHQR is unavailable
MOCK_PAYMENT_MODE = os.getenv("MOCK_PAYMENT_MODE", "true").lower() == "true"

def generate_payment_url(transaction_id: str, amount: float, success_url: str, remark: str) -> str:
    """
    Generate KHQR payment URL
    Hash generation: sha1(secret_key + transaction_id + amount + success_url + remark)
    """
    if MOCK_PAYMENT_MODE:
        # Return mock payment URL for testing
        return f"https://mock-payment.example.com/pay?transaction_id={transaction_id}&amount={amount}&success_url={success_url}"
    
    # Format amount to 2 decimal places
    formatted_amount = "{:.2f}".format(amount)
    
    # Generate hash using SHA1 as per documentation
    raw_string = f"{KHQR_SECRET_KEY}{transaction_id}{formatted_amount}{success_url}{remark}"
    hash_value = hashlib.sha1(raw_string.encode()).hexdigest()
    
    # Build payment URL with query parameters
    params = {
        "transaction_id": transaction_id,
        "amount": formatted_amount,
        "success_url": success_url,
        "remark": remark,
        "hash": hash_value
    }
    
    # Build query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    payment_url = f"{KHQR_GATEWAY_URL}/{KHQR_PROFILE_ID}?{query_string}"
    
    return payment_url

async def verify_payment(transaction_id: str) -> Dict[str, Any]:
    """Verify payment with KHQR API"""
    # Generate hash for verification: sha1(secret_key + transaction_id)
    raw_string = f"{KHQR_SECRET_KEY}{transaction_id}"
    hash_value = hashlib.sha1(raw_string.encode()).hexdigest()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                KHQR_VERIFY_URL,
                data={
                    "transaction_id": transaction_id,
                    "hash": hash_value
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "responseCode": 1,
                    "responseMessage": f"Verification failed: HTTP {response.status_code}"
                }
        except Exception as e:
            print(f"Payment verification error: {e}")
            return {
                "responseCode": 1,
                "responseMessage": str(e)
            }

def verify_webhook_signature(req_time: str, transaction_id: str, amount: str, signature: str) -> bool:
    """
    Verify webhook signature from KHQR
    Hash formula: sha256(secret + req_time + transaction_id + amount + "SUCCESS")
    """
    # Create the raw string for verification
    raw_string = f"{KHQR_SECRET_KEY}{req_time}{transaction_id}{amount}SUCCESS"
    
    # Calculate expected signature
    expected_signature = hashlib.sha256(raw_string.encode()).hexdigest()
    
    # Compare signatures (case-insensitive)
    return hmac.compare_digest(expected_signature.lower(), signature.lower())

def is_payment_successful(verification_response: Dict[str, Any]) -> bool:
    """Check if payment was successful"""
    # Check response code and status
    if verification_response.get("responseCode") == 0:
        data = verification_response.get("data", {})
        status = data.get("status", "").lower()
        return status == "success"
    return False