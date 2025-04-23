from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> dict[str, str]:
    print("[TransformerFunctions:HashPassword] Hashing password.")
    return pwd_context.hash(password)