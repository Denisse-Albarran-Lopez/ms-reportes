from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import base64
from datetime import datetime
from typing import Optional, List

app = FastAPI(title="MS-Reportes", description="Microservicio de reportes")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de archivos
REPORTES_DIR = r"C:\Users\Denisse Albarrán Lpz\OneDrive\Escritorio\Ingeniería de Software\Pruebas\MS-Reportes"
REPORTES_FILE = os.path.join(REPORTES_DIR, "reportes.txt")
IMAGENES_DIR = os.path.join(REPORTES_DIR, "imagenes")

# Crear directorios si no existen
os.makedirs(REPORTES_DIR, exist_ok=True)
os.makedirs(IMAGENES_DIR, exist_ok=True)

# Modelos Pydantic
class Concesionario(BaseModel):
    numAutorizado: str
    dependencia: str
    localidad: str
    autorizado: str
    horario: str

class ReporteCreate(BaseModel):
    tipo: str
    detalle: str
    concesionario: Concesionario
    usuario_id: Optional[int] = None
    imagen_base64: Optional[str] = None

class ReporteResponse(BaseModel):
    id: int
    tipo: str
    detalle: str
    concesionario: Concesionario
    timestamp: str
    usuario_id: Optional[int]
    imagen_path: Optional[str]

# Funciones auxiliares
def load_reportes():
    if not os.path.exists(REPORTES_FILE):
        return []
    try:
        with open(REPORTES_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return [json.loads(line) for line in content.split('\n') if line.strip()]
    except:
        return []

def save_reporte(reporte_data):
    with open(REPORTES_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(reporte_data, ensure_ascii=False) + '\n')

def save_image_from_base64(base64_data: str, reporte_id: int) -> str:
    try:
        # Remover el prefijo data:image/jpeg;base64, si existe
        if base64_data.startswith('data:image'):
            base64_data = base64_data.split(',')[1]
        
        # Decodificar base64
        image_data = base64.b64decode(base64_data)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_{reporte_id}_{timestamp}.jpg"
        filepath = os.path.join(IMAGENES_DIR, filename)
        
        # Guardar imagen
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

# Endpoints
@app.get("/")
async def root():
    return {"mensaje": "MS-Reportes - Microservicio de reportes"}

@app.post("/reportes/crear")
async def crear_reporte(reporte: ReporteCreate):
    reportes = load_reportes()
    nuevo_id = len(reportes) + 1
    
    # Guardar imagen si se proporciona
    imagen_filename = None
    if reporte.imagen_base64:
        imagen_filename = save_image_from_base64(reporte.imagen_base64, nuevo_id)
    
    reporte_data = {
        "id": nuevo_id,
        "tipo": reporte.tipo,
        "detalle": reporte.detalle,
        "concesionario": reporte.concesionario.dict(),
        "timestamp": datetime.now().isoformat(),
        "usuario_id": reporte.usuario_id,
        "imagen_path": imagen_filename
    }
    
    save_reporte(reporte_data)
    
    return {
        "mensaje": "Reporte creado exitosamente",
        "reporte_id": nuevo_id,
        "imagen_guardada": imagen_filename is not None
    }

@app.post("/reportes/crear-con-imagen")
async def crear_reporte_con_imagen(
    tipo: str = Form(...),
    detalle: str = Form(...),
    concesionario_json: str = Form(...),
    usuario_id: Optional[int] = Form(None),
    imagen: UploadFile = File(...)
):
    try:
        concesionario_data = json.loads(concesionario_json)
        concesionario = Concesionario(**concesionario_data)
    except:
        raise HTTPException(status_code=400, detail="Datos de concesionario inválidos")
    
    reportes = load_reportes()
    nuevo_id = len(reportes) + 1
    
    # Guardar imagen
    imagen_filename = None
    if imagen:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = imagen.filename.split('.')[-1] if '.' in imagen.filename else 'jpg'
        imagen_filename = f"reporte_{nuevo_id}_{timestamp}.{extension}"
        imagen_path = os.path.join(IMAGENES_DIR, imagen_filename)
        
        with open(imagen_path, 'wb') as f:
            content = await imagen.read()
            f.write(content)
    
    reporte_data = {
        "id": nuevo_id,
        "tipo": tipo,
        "detalle": detalle,
        "concesionario": concesionario.dict(),
        "timestamp": datetime.now().isoformat(),
        "usuario_id": usuario_id,
        "imagen_path": imagen_filename
    }
    
    save_reporte(reporte_data)
    
    return {
        "mensaje": "Reporte creado exitosamente",
        "reporte_id": nuevo_id,
        "imagen_guardada": imagen_filename is not None
    }

@app.get("/reportes/todos")
async def obtener_todos_reportes():
    reportes = load_reportes()
    return {"reportes": reportes}

@app.get("/reportes/{reporte_id}")
async def obtener_reporte(reporte_id: int):
    reportes = load_reportes()
    reporte = next((r for r in reportes if r['id'] == reporte_id), None)
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte

@app.get("/reportes/por-concesionario/{num_autorizado}")
async def obtener_reportes_por_concesionario(num_autorizado: str):
    reportes = load_reportes()
    reportes_filtrados = [
        r for r in reportes 
        if r.get('concesionario', {}).get('numAutorizado') == num_autorizado
    ]
    return {"reportes": reportes_filtrados}

@app.get("/reportes/por-tipo/{tipo}")
async def obtener_reportes_por_tipo(tipo: str):
    reportes = load_reportes()
    reportes_filtrados = [r for r in reportes if r.get('tipo') == tipo]
    return {"reportes": reportes_filtrados}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)