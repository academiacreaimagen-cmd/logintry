from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import json
import os


app = FastAPI()

# Servir archivos estáticos
app.mount("/css", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "js")), name="js")

# Configuración de Sesiones con Cookies Firmadas
secret_key = os.getenv("SECRET_KEY")
app.add_middleware(SessionMiddleware, secret_key=secret_key)

@app.get("/")
def read_index():
    # Usamos .. para salir de la carpeta /api y buscar en la raíz
    path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    return FileResponse(path)

@app.get("/dashboard")
def read_dashboard(request: Request):
    # Verificamos la sesión firmada
    if not request.session.get("session_user"):
        return RedirectResponse(url="/", status_code=303)
    
    # Servir el dashboard desde la raíz
    path = os.path.join(os.path.dirname(__file__), '..', 'dashboard.html')
    return FileResponse(path)

@app.get("/logout")
def logout(request: Request):
    # Limpiamos la sesión firmada
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

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
def login(datos: LoginData, request: Request):
    # 1. Validar primero el usuario (¡Muy importante!)
    if datos.username != user1:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Comparar password con hash
    try:
        ph.verify(hash_password, datos.password)
        
        # ✅ Login exitoso: Seteamos la sesión firmada
        request.session["session_user"] = user1
        
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
