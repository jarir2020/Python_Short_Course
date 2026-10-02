"""Password hashing and signed OAuth2 bearer-token helpers."""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from .config import Settings


# PasswordHash.recommended() selects the recommended Argon2 configuration when
# the argon2 extra is installed. Only this hash, never the plaintext password,
# belongs in the users table.
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(subject: str, settings: Settings) -> str:
    """Create a signed, expiring JWT; signing does not encrypt its contents."""

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_minutes
    )
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str, settings: Settings) -> str:
    """Verify signature/expiry and return the user subject."""

    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise jwt.InvalidTokenError("Token subject is missing")
    return subject
