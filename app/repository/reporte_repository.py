from sqlalchemy.orm import Session
from app.models.models import Reporte, TipoDeReporte, Estado
from datetime import datetime

class ReporteRepository:
    
    def crear_reporte(self, db: Session, id_tipo_reporte: int, descripcion: str, 
                     imagen_url: str, id_concesionaria: int, id_usuario: int):
        db_reporte = Reporte(
            id_tipo_reporte=id_tipo_reporte,
            descripcion=descripcion,
            imagen_url=imagen_url,
            fecha_hora=datetime.now(),
            id_estado=1,  # Estado inicial "Pendiente"
            id_concesionaria=id_concesionaria,
            id_usuario=id_usuario
        )
        db.add(db_reporte)
        db.commit()
        db.refresh(db_reporte)
        return db_reporte
    
    def obtener_reporte_por_id(self, db: Session, id_reporte: int):
        return db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    
    def obtener_reportes_por_usuario(self, db: Session, id_usuario: int):
        return db.query(Reporte).filter(Reporte.id_usuario == id_usuario).all()
    
    def obtener_reportes_por_concesionaria(self, db: Session, id_concesionaria: int):
        return db.query(Reporte).filter(Reporte.id_concesionaria == id_concesionaria).all()
    
    def actualizar_estado_reporte(self, db: Session, id_reporte: int, id_estado: int):
        reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
        if reporte:
            reporte.id_estado = id_estado
            db.commit()
            db.refresh(reporte)
        return reporte
    
    def obtener_tipos_reporte(self, db: Session):
        return db.query(TipoDeReporte).all()
    
    def obtener_estados(self, db: Session):
        return db.query(Estado).all()