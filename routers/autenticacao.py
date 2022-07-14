from fastapi import FastAPI, Depends, status, APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from utilidades import utilidades, configuracao
from database import schemas, database, models
from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = configuracao.settings.secret_key_jwt
ALGORITHM = configuracao.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = configuracao.settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="/login"
)

@router.post("/", response_model= schemas.Token)
def criar_usuario(dados_usuario: schemas.UserCreate, db: Session = Depends(database.get_db)):

    dados_usuario_bd = db.query(models.User).filter(models.User.email == dados_usuario.email).first()
    if not dados_usuario_bd:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Credenciais invalidas")
    if not utilidades.verifica(dados_usuario.senha, dados_usuario_bd.senha):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Credenciais invalidas")

    access_token = create_access_token(data = {"user_id": dados_usuario_bd.id})
    return {"access_token":access_token, "token_type": "Bearer"}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não foi possivel validar o usuario",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
