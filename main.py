import streamlit as st
import pandas as pd

st.title("⛽ Análisis de Impuestos en Combustible")

# Carga de datos
df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQB04QQYWbQeOMF_OrwpAuFTF7OPnA4fovZc5H7Yl12oYVcf9t_4Afxq8iuE56DCAVPQvlTmtSNlGgX/pub?gid=0&single=true&output=tsv",
    sep="\t",
    decimal=","
)

# Parsear fecha
df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)

# Cálculos base
df["totalxcombustible"] = df["litros"] * df["precioxlitro"]
df["totalximpuestos"] = df["iva"] + df["impuesto combustibles"]
df["totalapagar"] = df["totalxcombustible"] + df["totalximpuestos"]

# Cuánto pagás de impuestos por cada 1 litro
df["impuestos_por_litro"] = df["totalximpuestos"] / df["litros"]

# Precio final real por litro (lo que sale de tu bolsillo)
df["precio_final_por_litro"] = df["totalapagar"] / df["litros"]

# Porcentaje de carga tributaria (qué % del total son impuestos)
df["porcentaje_impuestos"] = (df["totalximpuestos"] / df["totalapagar"]) * 100

# Mostrar métricas resumen del último ticket
st.subheader("Resumen delúltimo ticket")
ultimo_ticket = df.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Precio Final/Litro", f"${ultimo_ticket['precio_final_por_litro']:.2f}")
col2.metric("Impuestos/Litro", f"${ultimo_ticket['impuestos_por_litro']:.2f}")
col3.metric("Carga Tributaria", f"{ultimo_ticket['porcentaje_impuestos']:.1f}%")

st.subheader("Desglose por carga")
st.dataframe(df[["fecha", "combustible", "precio_final_por_litro", "impuestos_por_litro", "porcentaje_impuestos"]])

# Visualización de la evolución
st.subheader("Evolución del peso de los impuestos")
st.line_chart(df.set_index("fecha")[["porcentaje_impuestos"]])