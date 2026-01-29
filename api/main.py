from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import json
from fastapi.responses import FileResponse # Importa esto
import os


app = FastAPI()

@app.get("/")
def read_index():
    # Usamos .. para salir de la carpeta /api y buscar en la raíz
    path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    return FileResponse(path)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ph = PasswordHasher()

# Cargar usuarios desde environment
user1 = os.getenv("USER")
hash_password = os.getenv("PASSWORD")

class LoginData(BaseModel): 
    username: str
    password: str

@app.post("/api/login")
def login(datos: LoginData):

       # 1. Validar primero el usuario (¡Muy importante!)
    if datos.username != user1:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Comparar password con hash
    try:
        ph.verify(hash_password, datos.password)
        
        # ✅ Login exitoso
        return {
            "success": True,
            "mensaje": "Login exitoso",
            "username": user1
        }
        
    except VerifyMismatchError:
        # ❌ Contraseña incorrecta
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )
