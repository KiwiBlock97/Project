from os import environ
from dotenv import load_dotenv
load_dotenv()

class Var:
    DB_HOST:str = environ.get("DB_HOST", "127.0.0.1")
    DB_USERNAME:str = environ.get("DB_USERNAME", "root")
    DB_PASSWORD:str = environ.get("DB_PASSWORD", "mysql")
    DB_NAME:str = environ.get("DB_NAME", "bus")
    DB_PORT:int = int(environ.get("DB_PORT", 3306))
    PORT:int = int(environ.get("PORT", 8080))
    HOST:str = environ.get("HOST", "0.0.0.0")
    FQDN:str = environ.get("FQDN", HOST)
    HAS_SSL=environ.get("HAS_SSL", False)
    NO_PORT=environ.get("NO_PORT", False)
    URL:str = "http{}://{}{}".format("s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":"+str(PORT))
    CF_CLIENTID: str = environ.get("CF_CLIENTID")
    CF_CLIENTSECRET: str = environ.get("CF_CLIENTSECRET")
    CF_VERSION: str = environ.get("CF_VERSION", "2023-08-01")
    BREVO_API: str = environ.get("BREVO_API", None)