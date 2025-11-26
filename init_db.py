from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models.models import TipoDeReporte, Estado

def init_database():
    create_tables()
    
    db = SessionLocal()
    
    # Crear tipos de reporte si no existen
    if not db.query(TipoDeReporte).first():
        tipos_reporte = [
            TipoDeReporte(tipo_reporte="Problema de Calidad"),
            TipoDeReporte(tipo_reporte="Servicio al Cliente"),
            TipoDeReporte(tipo_reporte="Infraestructura"),
            TipoDeReporte(tipo_reporte="Otros")
        ]
        db.add_all(tipos_reporte)
    
    # Crear estados si no existen
    if not db.query(Estado).first():
        estados = [
            Estado(estado="Pendiente"),
            Estado(estado="En Proceso"),
            Estado(estado="Resuelto"),
            Estado(estado="Cerrado")
        ]
        db.add_all(estados)
    
    db.commit()
    db.close()
    print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_database()