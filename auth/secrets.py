from google.cloud import secretmanager

import os

def load_secret(secret_name, env_var_name=None, project_id=1084246205015, version_id="latest", set_env=True):
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
        ("stripe_test", "STRIPE_API_KEY", 1),
        ("openai", "OPENAI_API_KEY", 1),
        ("secret_key", "SECRET_KEY", 1),
        ("teller_certificate", "TELLER_CERT", 4),
        ("teller_private_key", "TELLER_CERT_KEY", 4),
        ("smtp_password", "SMTP_PASSWORD", 1)
    ]
    
    for (secret_name, env_var_name, version_id) in ESSENTIAL_SECRETS:
        load_secret(secret_name, env_var_name, version_id=version_id)