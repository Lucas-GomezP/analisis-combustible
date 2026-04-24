import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("⛽ Análisis de Impuestos en Combustible")

# Carga de datos
df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQB04QQYWbQeOMF_OrwpAuFTF7OPnA4fovZc5H7Yl12oYVcf9t_4Afxq8iuE56DCAVPQvlTmtSNlGgX/pub?gid=0&single=true&output=tsv",
    sep="\t",
    decimal=","
)

df["iva_x_litro"] = df["iva"] / df["litros"]
df["imp_comb_x_litro"] = df["impuesto combustibles"] / df["litros"]

df["total_x_litro"] = df["precioxlitro"] + df["iva_x_litro"] + df["imp_comb_x_litro"]

df["pct_combustible"] = df["precioxlitro"] / df["total_x_litro"] * 100
df["pct_iva"] = df["iva_x_litro"] / df["total_x_litro"] * 100
df["pct_imp_comb"] = df["imp_comb_x_litro"] / df["total_x_litro"] * 100


for i, row in df.iterrows():
    fig, ax = plt.subplots()

    valores = [
        row["pct_combustible"],
        row["pct_iva"],
        row["pct_imp_comb"]
    ]

    labels = ["Combustible", "IVA", "ICL/IDC"]

    ax.pie(valores, labels=labels, autopct="%1.1f%%")
    ax.set_title(f'{row["fecha"]} - {row["combustible"]}')

    st.pyplot(fig)

df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)
df = df.sort_values("fecha")

fig, ax = plt.subplots()

ax.plot(df["fecha"], df["precioxlitro"], marker="o", label="Precio x litro")
ax.plot(df["fecha"], df["imp_comb_x_litro"], marker="o", label="Imp. Combustible x litro")

ax.set_xlabel("Fecha")
ax.set_ylabel("ARS")
ax.set_title("Evolución Precio vs ICL/IDC")

ax.legend()
ax.grid(True)

st.pyplot(fig)

df["precio_idx"] = df["precioxlitro"] / df["precioxlitro"].iloc[0] * 100
df["imp_idx"] = df["imp_comb_x_litro"] / df["imp_comb_x_litro"].iloc[0] * 100

fig, ax = plt.subplots()

ax.plot(df["fecha"], df["precio_idx"], marker="o", label="Precio (base 100)")
ax.plot(df["fecha"], df["imp_idx"], marker="o", label="ICL/IDC (base 100)")

ax.set_title("Evolución relativa (base 100)")
ax.legend()
ax.grid(True)


st.pyplot(fig)
st.dataframe(df)
# # Parsear fecha
# df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)

# # Cálculos base
# df["totalxcombustible"] = df["litros"] * df["precioxlitro"]
# df["totalximpuestos"] = df["iva"] + df["impuesto combustibles"]
# df["totalapagar"] = df["totalxcombustible"] + df["totalximpuestos"]

# # Cuánto pagás de impuestos por cada 1 litro
# df["impuestos_por_litro"] = df["totalximpuestos"] / df["litros"]

# # Precio final real por litro (lo que sale de tu bolsillo)
# df["precio_final_por_litro"] = df["totalapagar"] / df["litros"]

# # Porcentaje de carga tributaria (qué % del total son impuestos)
# df["porcentaje_impuestos"] = (df["totalximpuestos"] / df["totalapagar"]) * 100

# # Mostrar métricas resumen del último ticket
# st.subheader("Resumen delúltimo ticket")
# ultimo_ticket = df.iloc[-1]
# col1, col2, col3 = st.columns(3)
# col1.metric("Precio Final/Litro", f"${ultimo_ticket['precio_final_por_litro']:.2f}")
# col2.metric("Impuestos/Litro", f"${ultimo_ticket['impuestos_por_litro']:.2f}")
# col3.metric("Carga Tributaria", f"{ultimo_ticket['porcentaje_impuestos']:.1f}%")

# st.subheader("Desglose por carga")
# st.dataframe(df[["fecha", "combustible", "precio_final_por_litro", "impuestos_por_litro", "porcentaje_impuestos"]])

# # Visualización de la evolución
# st.subheader("Evolución del peso de los impuestos")
# st.line_chart(df.set_index("fecha")[["porcentaje_impuestos"]])

# st.markdown("---")
# df["porcentaje_imp_comb_sobre_base"] = (
#     df["impuesto combustibles"] / df["totalxcombustible"]
# ) * 100

# df["porcentaje_imp_comb_sobre_total"] = (
#     df["impuesto combustibles"] / df["totalapagar"]
# ) * 100

# df["base_imponible"] = df["iva"] / 0.21
# df["precio_base"] = df["base_imponible"] - df["impuesto combustibles"]

# df["porcentaje_imp_comb_real"] = (
#     df["impuesto combustibles"] / df["precio_base"]
# ) * 100

# st.write(df[[
#     "fecha",
#     "porcentaje_imp_comb_sobre_total",
#     "porcentaje_imp_comb_sobre_base"
# ]])
