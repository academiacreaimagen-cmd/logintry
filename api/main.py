from fastapi import FastAPI, HTTPException, Response, Cookie, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import json
import os


app = FastAPI()

@app.get("/")
def read_index():
    # Usamos .. para salir de la carpeta /api y buscar en la raíz
    path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    return FileResponse(path)

@app.get("/dashboard")
def read_dashboard(session_user: Optional[str] = Cookie(None)):
    if not session_user:
        return RedirectResponse(url="/", status_code=303)
    
    # Servir el dashboard desde la raíz
    path = os.path.join(os.path.dirname(__file__), '..', 'dashboard.html')
    return FileResponse(path)

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_user")
    return response

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
def login(datos: LoginData, response: Response):
    # 1. Validar primero el usuario (¡Muy importante!)
    if datos.username != user1:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Comparar password con hash
    try:
        ph.verify(hash_password, datos.password)
        
        # ✅ Login exitoso: Seteamos la cookie
        response.set_cookie(
            key="session_user", 
            value=user1, 
            httponly=True, 
            samesite="lax"
        )
        
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
