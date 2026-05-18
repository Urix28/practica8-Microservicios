from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI(title="Microservicio de Catálogo", version="1.0")

# Este es el único lugar donde existe la base de datos (diccionario)
INVENTARIO = {
    "Fundamentos de Programación": 30,
    "Matemáticas Discretas": 15,
    "Cálculo": 25,
    "Álgebra Lineal": 18,
    "Ecuaciones Diferenciales": 10,
    "Algoritmos y Estructuras de Datos": 12,
    "Bases de Datos": 8,
    "Sistemas Operativos": 5,
    "Redes de Computadoras": 7,
    "Compiladores": 3,
    "Teoría de la Computación": 4,
    "Arquitectura de Computadoras": 6,
    "Diseño de Sistemas Digitales": 9,
    "Tecnologías para el Desarrollo de Aplicaciones Web": 14,
    "Análisis y Diseño de Algoritmos": 5,
    "Procesamiento Digital de Señales": 2
}

cerrojo_inventario = asyncio.Lock()

class PeticionLibro(BaseModel):
    titulo: str

@app.get("/api/catalogo")
def ver_catalogo():
    """Expone el inventario al exterior"""
    return INVENTARIO

@app.post("/api/catalogo/restar")
async def restar_libro(peticion: PeticionLibro):
    """Ruta interna de uso exclusivo para otros microservicios"""
    titulo = peticion.titulo.strip()
    
    # SECCIÓN CRÍTICA AISLADA
    async with cerrojo_inventario:
        if titulo in INVENTARIO:
            if INVENTARIO[titulo] > 0:
                INVENTARIO[titulo] -= 1
                return {"exito": True, "quedan": INVENTARIO[titulo]}
            else:
                return {"exito": False, "motivo": "Agotado"}
        
        raise HTTPException(status_code=404, detail="No existe")