from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TipoDeReporte(Base):
    __tablename__ = "tipo_de_reporte"
    
    id_tipo_reporte = Column(Integer, primary_key=True, index=True)
    tipo_reporte = Column(String, nullable=False)
    
    reportes = relationship("Reporte", back_populates="tipo_reporte")

class Estado(Base):
    __tablename__ = "estado"
    
    id_estado = Column(Integer, primary_key=True, index=True)
    estado = Column(String, nullable=False)
    
    reportes = relationship("Reporte", back_populates="estado")

class Reporte(Base):
    __tablename__ = "reporte"
    
    id_reporte = Column(Integer, primary_key=True, index=True)
    id_tipo_reporte = Column(Integer, ForeignKey("tipo_de_reporte.id_tipo_reporte"))
    descripcion = Column(String, nullable=False)
    imagen_url = Column(String)
    fecha_hora = Column(DateTime, nullable=False)
    id_estado = Column(Integer, ForeignKey("estado.id_estado"))
    id_concesionaria = Column(Integer, nullable=False)
    id_usuario = Column(Integer, nullable=False)
    
    tipo_reporte = relationship("TipoDeReporte", back_populates="reportes")
    estado = relationship("Estado", back_populates="reportes")