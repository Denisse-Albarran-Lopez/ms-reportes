# MS-Reportes - Microservicio de Reportes

Microservicio para manejo de reportes de incidentes del sistema CaFES Check.

## Características

- Creación de reportes con imágenes
- Almacenamiento de reportes en archivo de texto
- Guardado de imágenes en carpeta dedicada
- Consultas por concesionario, tipo y fecha
- API REST compatible con FastAPI

## Endpoints Disponibles

### Creación de Reportes
- `POST /reportes/crear` - Crear reporte con imagen en base64
- `POST /reportes/crear-con-imagen` - Crear reporte con archivo de imagen

### Consultas
- `GET /reportes/todos` - Obtener todos los reportes
- `GET /reportes/{reporte_id}` - Obtener reporte específico
- `GET /reportes/por-concesionario/{num_autorizado}` - Reportes por concesionario
- `GET /reportes/por-tipo/{tipo}` - Reportes por tipo de incidente

## Instalación

1. Ejecutar `instalar_dependencias.bat` o:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el servidor:
   ```bash
   python run.py
   ```

3. El servidor estará disponible en `http://localhost:8002`

## Estructura de Datos

Los reportes se almacenan en formato JSON en el archivo `reportes.txt`:

```json
{
  "id": 1,
  "tipo": "higiene",
  "detalle": "Descripción del problema",
  "concesionario": {
    "numAutorizado": "1062",
    "dependencia": "Facultad de Estudios Superiores Acatlán",
    "localidad": "C",
    "autorizado": "Grupo Mondainz 8, S.A. de C.V.",
    "horario": "Lunes a viernes de 8:00 a 20:30 horas"
  },
  "timestamp": "2024-01-01T12:00:00",
  "usuario_id": 1,
  "imagen_path": "reporte_1_20240101_120000.jpg"
}
```

## Tipos de Incidentes

- `higiene` - Malas prácticas de higiene
- `comida-mal-estado` - Comida en mal estado
- `trato-inadecuado` - Trato inadecuado
- `precios-injustos` - Precios injustos
- `productos-caducados` - Productos caducados
- `malas-condiciones` - Malas condiciones en instalaciones
- `uso-areas-no-designadas` - Uso de áreas no designadas
- `maquinas-expendedoras` - Máquinas expendedoras
- `seguridad-proteccion-civil` - Falta de seguridad y protección civil
- `porciones-inadecuadas` - Porciones inadecuadas

## Integración con Frontend

Este microservicio se integra con el frontend caFES-Check:

- Las imágenes se envían en formato base64 desde el canvas del navegador
- Los reportes incluyen datos del usuario y concesionario
- Se almacenan tanto los datos como las imágenes de evidencia
