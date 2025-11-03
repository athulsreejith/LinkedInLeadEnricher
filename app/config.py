import os
from dotenv import load_dotenv
load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:29092")
SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM") or None
SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME") or None
SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD") or None

INPUT_TOPIC  = os.getenv("INPUT_TOPIC", "salesforce_myleads")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "salesforce_icebreakers")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SERPAPI_KEY    = os.getenv("SERPAPI_API_KEY")

