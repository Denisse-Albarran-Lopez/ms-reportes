from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.service.reporte_service import ReporteService
from app.database import get_db

router = APIRouter()
reporte_service = ReporteService()

class CrearReporteRequest(BaseModel):
    id_tipo_reporte: int
    descripcion: str
    imagen_url: str = None
    id_concesionaria: int
    id_usuario: int

class ActualizarEstadoRequest(BaseModel):
    id_estado: int

@router.post("/crear")
def crear_reporte(request: CrearReporteRequest, db: Session = Depends(get_db)):
    return reporte_service.crear_reporte(
        db, request.id_tipo_reporte, request.descripcion, 
        request.imagen_url, request.id_concesionaria, request.id_usuario
    )

@router.get("/reporte/{id_reporte}")
def obtener_reporte(id_reporte: int, db: Session = Depends(get_db)):
    return reporte_service.obtener_reporte(db, id_reporte)

@router.get("/usuario/{id_usuario}")
def obtener_reportes_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return reporte_service.obtener_reportes_usuario(db, id_usuario)

@router.get("/concesionaria/{id_concesionaria}")
def obtener_reportes_concesionaria(id_concesionaria: int, db: Session = Depends(get_db)):
    return reporte_service.obtener_reportes_concesionaria(db, id_concesionaria)

@router.put("/estado/{id_reporte}")
def actualizar_estado_reporte(id_reporte: int, request: ActualizarEstadoRequest, db: Session = Depends(get_db)):
    return reporte_service.actualizar_estado(db, id_reporte, request.id_estado)

@router.get("/tipos-reporte")
def obtener_tipos_reporte(db: Session = Depends(get_db)):
    return reporte_service.obtener_tipos_reporte(db)

@router.get("/estados")
def obtener_estados(db: Session = Depends(get_db)):
    return reporte_service.obtener_estados(db)