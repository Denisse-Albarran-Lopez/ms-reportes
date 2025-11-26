from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.reporte_controller import router as reporte_router
from app.database import create_tables

app = FastAPI(title="MS-Reportes", description="Microservicio de reportes para CaFES Check")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reporte_router, prefix="/reportes", tags=["Reportes"])

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "MS-Reportes - Microservicio de Reportes"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)