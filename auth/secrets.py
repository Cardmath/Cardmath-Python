import os
import logging
from google.cloud import secretmanager

logging.basicConfig(level=logging.INFO)

def load_secret(secret_name, env_var_name=None, project_id=1084246205015, version_id=1, set_env=True):
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "cardmath-llc")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version_id}"
    
    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")
    if set_env:
        os.environ[env_var_name] = secret_payload
    return secret_payload

def load_essential_secrets():
    ESSENTIAL_SECRETS = [
        ("openai", "OPENAI_API_KEY"),
        ("secret_key", "SECRET_KEY"),
        ("teller_certificate", "TELLER_CERT"),
        ("teller_private_key", "TELLER_CERT_KEY"),
        ("smtp_password", "SMTP_PASSWORD")
    ]
    
    for secret_name, env_var_name in ESSENTIAL_SECRETS:
        load_secret(secret_name, env_var_name)