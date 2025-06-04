# ETL completo con análisis exploratorio y visualizaciones
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. EXTRACCIÓN
url = "https://github.com/alura-cursos/challenge2-data-science-LATAM/raw/main/TelecomX_Data.json"
df_raw = pd.read_json(url)

print("✅ Datos cargados correctamente")
print(f"Dimensiones originales: {df_raw.shape}")
print(df_raw.head())

# 2. TRANSFORMACIÓN

# 2.1 Limpieza de nombres de columnas
df = df_raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 2.2 Normalización de columnas anidadas (si existen)
for col in df.columns:
    if isinstance(df[col].iloc[0], dict):
        nested_df = pd.json_normalize(df[col])
        nested_df.columns = [f"{col}_{subcol}" for subcol in nested_df.columns]
        df = df.drop(columns=[col])
        df = pd.concat([df, nested_df], axis=1)

# 2.3 Conversión de columnas de fecha
date_columns = [col for col in df.columns if 'fecha' in col]
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# 2.4 Eliminación de valores nulos críticos
if 'id_cliente' in df.columns:
    df = df.dropna(subset=['id_cliente'])

# 2.5 Revisión general
print("\n📊 Información general del dataframe:")
print(df.info())
print(df.describe(include='all'))

# 3. CARGA Y ANÁLISIS EXPLORATORIO

# Guardar datos limpios (opcional)
df.to_csv("TelecomX_clean.csv", index=False)

# 3.1 Conversión segura de la columna 'churn' a valores numéricos
if 'churn' in df.columns:
    df['churn_numerico'] = df['churn'].astype(str).str.lower().map({
        'si': 1, 'sí': 1, 'true': 1, '1': 1,
        'no': 0, 'false': 0, '0': 0
    })

    # Verificar distribución de churn
    if df['churn_numerico'].notna().any():
        print("\n🎯 Distribución de churn:")
        print(df['churn_numerico'].value_counts(normalize=True))

        # Visualización de churn
        sns.countplot(data=df, x='churn_numerico')
        plt.title("Distribución de Clientes: Churn vs No Churn")
        plt.xlabel("¿Cliente se dio de baja? (1 = Sí, 0 = No)")
        plt.ylabel("Cantidad")
        plt.show()

        # Cálculo de tasa general
        churn_rate = df['churn_numerico'].mean()
        print(f"✔ Tasa general de churn: {churn_rate:.2%}")
    else:
        print("⚠ No se pudieron convertir los valores de 'churn' a numéricos.")
else:
    print("⚠ No se encontró la columna 'churn'.")

# 3.2 Mapa de calor de correlación (si hay columnas numéricas)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
    plt.title("Mapa de Calor - Correlación entre variables numéricas")
    plt.show()

# 3.3 Análisis de otras variables por churn (si existen)
for col in ['tipo_plan', 'producto', 'servicio']:
    if col in df.columns:
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x=col, hue='churn_numerico')
        plt.title(f"Distribución de '{col}' por Churn")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# 4. INFORME FINAL

print("\n📄 INFORME FINAL")
print(f"✔ Total de registros: {len(df)}")
print(f"✔ Columnas del dataset: {df.columns.tolist()}")
print("✔ Porcentaje de valores nulos por columna:")
print((df.isnull().mean() * 100).round(2).sort_values(ascending=False))
