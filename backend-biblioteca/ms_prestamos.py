from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Microservicio de Préstamos", version="1.0")

# Permisos para que la PWA pueda consumir este microservicio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PeticionLibro(BaseModel):
    titulo: str

# URL de nuestro otro microservicio
URL_CATALOGO = "practica8-microservicios.railway.internal"

@app.get("/api/catalogo")
async def obtener_catalogo():
    """
    Actúa como API Gateway: La PWA pide el catálogo aquí, 
    y este microservicio va y se lo pide al MS de Catálogo.
    """
    print("🔄 [MS Préstamos] Pidiendo el catálogo al MS interno...")
    async with httpx.AsyncClient() as client:
        try:
            # Hace la petición HTTP al otro microservicio
            respuesta = await client.get(f"{URL_CATALOGO}/api/catalogo")
            # Le devuelve el JSON intacto a la PWA
            return respuesta.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Error: El Microservicio de Catálogo está inaccesible.")
        
@app.post("/api/prestar")
async def procesar_prestamo(peticion: PeticionLibro):
    """Recibe la orden de la PWA y negocia con el MS de Catálogo"""
    titulo = peticion.titulo.strip()
    print(f"🔄 [MS Préstamos] Gestionando solicitud para: '{titulo}'")
    
    # Iniciamos la comunicación HTTP hacia el Microservicio de Catálogo
    async with httpx.AsyncClient() as client:
        try:
            # Le mandamos el JSON al otro microservicio
            respuesta = await client.post(
                f"{URL_CATALOGO}/api/catalogo/restar",
                json={"titulo": titulo}
            )
            
            # Si el catálogo dice que el libro no existe (Error 404)
            if respuesta.status_code == 404:
                raise HTTPException(status_code=404, detail="Libro no encontrado en el catálogo.")
                
            # Extraemos el JSON que nos contestó el catálogo
            datos_catalogo = respuesta.json()
            
            # Formateamos la respuesta final para la PWA
            if datos_catalogo["exito"]:
                return {
                    "estado": "aprobado",
                    "mensaje": f"Préstamo exitoso. Quedan {datos_catalogo['quedan']} copias.",
                    "titulo": titulo
                }
            else:
                return {
                    "estado": "rechazado",
                    "mensaje": f"El libro '{titulo}' está {datos_catalogo['motivo']}."
                }
                
        except httpx.RequestError:
            # Si el microservicio de catálogo está apagado o caído
            raise HTTPException(status_code=503, detail="Error interno: El Microservicio de Catálogo no está disponible.")