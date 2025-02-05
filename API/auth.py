import os

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests

KEYCLOAK_URL = os.getenv('KEYCLOAK_URL',"http://localhost:8080")
KEYCLOAK_PUBLIC_KEY = None
ALGORITHM = "RS256"
REQUIRED_ROLE = "prothetic_user"

security = HTTPBearer()


def get_public_key():
    global KEYCLOAK_PUBLIC_KEY
    if not KEYCLOAK_PUBLIC_KEY:
        response = requests.get(f"{KEYCLOAK_URL}/realms/reports-realm/protocol/openid-connect/certs")
        jwks = response.json()
        if "keys" in jwks:
            KEYCLOAK_PUBLIC_KEY = f"-----BEGIN CERTIFICATE-----\n{jwks['keys'][0]['x5c'][0]}\n-----END CERTIFICATE-----"
    return KEYCLOAK_PUBLIC_KEY


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    public_key = get_public_key()

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHM],
        )
        roles = payload.get("realm_access", {}).get("roles", [])

        if REQUIRED_ROLE not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
