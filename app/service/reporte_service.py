from sqlalchemy.orm import Session
from app.repository.reporte_repository import ReporteRepository
from fastapi import HTTPException

class ReporteService:
    def __init__(self):
        self.reporte_repo = ReporteRepository()
    
    def crear_reporte(self, db: Session, id_tipo_reporte: int, descripcion: str, 
                     imagen_url: str, id_concesionaria: int, id_usuario: int):
        if not descripcion.strip():
            raise HTTPException(status_code=400, detail="La descripción es requerida")
        
        reporte = self.reporte_repo.crear_reporte(
            db, id_tipo_reporte, descripcion, imagen_url, id_concesionaria, id_usuario
        )
        return {"mensaje": "Reporte creado exitosamente", "reporte_id": reporte.id_reporte}
    
    def obtener_reporte(self, db: Session, id_reporte: int):
        reporte = self.reporte_repo.obtener_reporte_por_id(db, id_reporte)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return reporte
    
    def obtener_reportes_usuario(self, db: Session, id_usuario: int):
        reportes = self.reporte_repo.obtener_reportes_por_usuario(db, id_usuario)
        return {"reportes": reportes}
    
    def obtener_reportes_concesionaria(self, db: Session, id_concesionaria: int):
        reportes = self.reporte_repo.obtener_reportes_por_concesionaria(db, id_concesionaria)
        return {"reportes": reportes}
    
    def actualizar_estado(self, db: Session, id_reporte: int, id_estado: int):
        reporte = self.reporte_repo.actualizar_estado_reporte(db, id_reporte, id_estado)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return {"mensaje": "Estado actualizado exitosamente"}
    
    def obtener_tipos_reporte(self, db: Session):
        tipos = self.reporte_repo.obtener_tipos_reporte(db)
        return {"tipos_reporte": tipos}
    
    def obtener_estados(self, db: Session):
        estados = self.reporte_repo.obtener_estados(db)
        return {"estados": estados}