# Challenge-Telecom-X-caor
Challenge Telecom X caor

---

## 🚀 Tecnologías utilizadas

- Python 3
- Pandas
- Seaborn
- Matplotlib

---

## 🔍 Pasos del Análisis

### 1. 📥 Extracción
Los datos se descargan directamente desde un archivo `.json` alojado en GitHub.

### 2. 🔧 Transformación
- Normalización de columnas anidadas.
- Limpieza de nombres y valores nulos.
- Conversión de fechas y tipos.
- Preparación de la variable `churn` como binaria (1 = sí, 0 = no).

### 3. 📊 Carga y Análisis
- Exportación a CSV.
- Análisis de distribución de churn.
- Visualización de correlaciones.
- Gráficos por tipo de plan, producto o servicio.

---

## 📈 Resultados Destacados

- Se identificó la proporción de clientes que cancelan el servicio (`churn`).
- Se analizaron factores potenciales asociados al churn (tipo de plan, duración del servicio, etc).
- Se generaron visualizaciones para facilitar la comprensión.

---

## 💡 Cómo usar este proyecto

1. Clona el repositorio o descarga los archivos.
2. Instala las dependencias:
   ```bash
   pip install pandas seaborn matplotlib

