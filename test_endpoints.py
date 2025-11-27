import requests
import json

BASE_URL = "http://localhost:8002"

def test_crear_reporte():
    data = {
        "tipo": "higiene",
        "detalle": "Encontré comida en mal estado en la vitrina",
        "concesionario": {
            "numAutorizado": "1062",
            "dependencia": "Facultad de Estudios Superiores Acatlán",
            "localidad": "C",
            "autorizado": "Grupo Mondainz 8, S.A. de C.V.",
            "horario": "Lunes a viernes de 8:00 a 20:30 horas"
        },
        "usuario_id": 1
    }
    response = requests.post(f"{BASE_URL}/reportes/crear", json=data)
    print("Crear reporte:", response.json())

def test_obtener_todos():
    response = requests.get(f"{BASE_URL}/reportes/todos")
    print("Obtener todos:", response.json())

def test_obtener_por_concesionario():
    response = requests.get(f"{BASE_URL}/reportes/por-concesionario/1062")
    print("Obtener por concesionario:", response.json())

def test_obtener_por_tipo():
    response = requests.get(f"{BASE_URL}/reportes/por-tipo/higiene")
    print("Obtener por tipo:", response.json())

if __name__ == "__main__":
    print("Probando endpoints del MS-Reportes...")
    print("Asegúrate de que el servidor esté ejecutándose en localhost:8002")
    print()
    
    try:
        test_crear_reporte()
        test_obtener_todos()
        test_obtener_por_concesionario()
        test_obtener_por_tipo()
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
    except Exception as e:
        print(f"Error: {e}")