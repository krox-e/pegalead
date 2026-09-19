import httpx
import re
import json
from urllib.parse import quote

# Test mobile number detection and instagram bio check
sample_numbers = [
    "(11) 96901-7740", # Mobile / WhatsApp
    "(11) 3223-6162",  # Landline
    "(11) 91094-3443", # Mobile / WhatsApp
    "(19) 99908-8825", # Mobile / WhatsApp
    "(21) 3742-2729",  # Landline
    "(31) 99831-1567", # Mobile / WhatsApp
]

def is_whatsapp_number(phone_str):
    if not phone_str:
        return False
    # Strip non-digits
    digits = re.sub(r'\D', '', phone_str)
    # Check if +55
    if digits.startswith("55"):
        digits = digits[2:]
    # Must be 11 digits: DDD (2 digits) + 9 + 8 digits
    if len(digits) == 11 and digits[2] == '9':
        return True
    return False

for num in sample_numbers:
    print(f"{num}: WhatsApp? {is_whatsapp_number(num)}")
