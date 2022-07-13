from asyncio.log import logger
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JOSEError
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from app.utils.configuration import Config
from app.utils.error_handler import AuthException, OpsException

security = HTTPBearer()
config = Config()


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    if not token:
        raise AuthException(code=401, message="No authorization token provided")

    try:
        payload = jwt.decode(
            token,
            config.jwt_secret,
            algorithms=[config.hash_algorithm],
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
                "verify_sub": False,
            },
        )
        return payload
    except ExpiredSignatureError:
        raise AuthException(code=401, message="Authorization token expired")
    except JOSEError as e:
        logger.exception(e.args, exc_info=e)
        raise AuthException(code=401, message=str(e))
    except Exception:
        raise AuthException(code=401, message="Unable to parse authorization token")
