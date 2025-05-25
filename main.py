import streamlit as st
import pandas as pd
import os
import io
import matplotlib.pyplot as plt

# ----------------- Funciones clave ------------------

def evaluar_alerta(nombre, valor):
    reglas = {
        "Liquidez corriente": (1.5, 2.5),
        "Prueba ácida": (1.0, 1.5),
        "Endeudamiento": (0, 0.5),
        "ROE": (0.15, 0.25),
        "ROA": (0.05, 0.15),
        "Margen neto": (0.10, 0.20),
        "Margen operativo": (0.12, 0.25),
        "EBITDA margen": (0.10, 0.20),
        "Deuda / EBITDA": (0, 3)
    }
    if nombre not in reglas:
        return "🟢 Bueno"
    bajo, alto = reglas[nombre]
    if valor < bajo:
        return "🔴 Riesgoso"
    elif bajo <= valor <= alto:
        return "🟡 Aceptable"
    else:
        return "🟢 Bueno"

def sugerir_accion(ratio, alerta):
    if alerta == "🔴 Riesgoso":
        sugerencias = {
            "Liquidez corriente": "Revisar ciclo de cobros, reducir pasivos a corto plazo, buscar financiamiento a largo plazo.",
            "Prueba ácida": "Disminuir inventarios o aumentar caja disponible.",
            "Endeudamiento": "Refinanciar deuda, aumentar capital propio, reducir activos ineficientes.",
            "ROE": "Mejorar utilidad neta o eficiencia operativa, reducir costos.",
            "ROA": "Mejorar utilización de activos, eliminar activos improductivos.",
            "Margen neto": "Optimizar estructura de costos, renegociar precios con proveedores.",
            "Margen operativo": "Revisar gastos operativos, automatizar procesos.",
            "EBITDA margen": "Reducir costos indirectos o mejorar ingresos operativos.",
            "Deuda / EBITDA": "Aumentar EBITDA o refinanciar deuda para reducir presión financiera."
        }
        return sugerencias.get(ratio, "Analizar situación con mayor profundidad.")
    elif alerta == "🟡 Aceptable":
        return "Monitorear periódicamente, buscar mejoras graduales."
    else:
        return "No requiere acción inmediata."

def svg_alerta(alerta):
    if "🔴" in alerta:
        return """<svg height="20" width="20"><circle cx="10" cy="10" r="8" stroke="red" stroke-width="2" fill="red" /></svg>"""
    elif "🟡" in alerta:
        return """<svg height="20" width="20"><circle cx="10" cy="10" r="8" stroke="orange" stroke-width="2" fill="orange" /></svg>"""
    elif "🟢" in alerta:
        return """<svg height="20" width="20"><circle cx="10" cy="10" r="8" stroke="green" stroke-width="2" fill="green" /></svg>"""
    return ""

def mostrar_tabla_con_svg(df):
    html = """
    <style>
        table {width:100%; border-collapse: collapse;}
        th, td {border-bottom: 1px solid #ccc; padding: 8px; text-align:left;}
        th {background-color: #f2f2f2;}
    </style>
    """
    html += "<table>"
    html += "<tr><th>Ratio</th><th>Valor</th><th>Indicador</th><th>Alerta</th><th>Acción sugerida</th></tr>"
    for idx, row in df.iterrows():
        html += "<tr>"
        html += f"<td>{idx}</td>"
        html += f"<td>{row['Valor']:.2f}</td>"
        html += f"<td>{row['Indicador visual']}</td>"
        html += f"<td>{row['Alerta']}</td>"
        html += f"<td>{row['Acción sugerida']}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

def exportar_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Historial')
    output.seek(0)
    return output

# ----------------- Seguridad -----------------

st.sidebar.title("🔐 Seguridad")
empresa_input = st.sidebar.text_input("Empresa:", value="Mi Empresa S.A.")
clave_input = st.sidebar.text_input("Clave de acceso:", type="password")

usuarios_autorizados = {
    "Mi Empresa S.A.": "1234",
    "Empresa X": "abcd",
    "Constructora Z": "2025"
}

if empresa_input not in usuarios_autorizados or clave_input != usuarios_autorizados[empresa_input]:
    st.warning("🔒 Ingresa una clave válida para acceder al análisis.")
    st.stop()

empresa = empresa_input
st.title(f"📊 Análisis financiero - {empresa}")

anio = st.number_input("Año del análisis:", min_value=2000, max_value=2100, step=1, value=2025)

st.header("📥 Ingresar datos financieros")

datos = {
    "Liquidez corriente": 1.2,
    "Prueba ácida": 0.9,
    "Endeudamiento": 0.55,
    "ROE": 0.12,
    "ROA": 0.08,
    "Margen neto": 0.09,
    "Margen operativo": 0.11,
    "EBITDA margen": 0.14,
    "Deuda / EBITDA": 3.2
}

ratios = datos
alertas = {nombre: evaluar_alerta(nombre, valor) for nombre, valor in ratios.items()}
acciones = {nombre: sugerir_accion(nombre, alertas[nombre]) for nombre in ratios.keys()}

df_resultados = pd.DataFrame({
    "Valor": ratios,
    "Alerta": alertas,
    "Acción sugerida": acciones
})
df_resultados["Indicador visual"] = df_resultados["Alerta"].apply(svg_alerta)

st.header("🔍 Filtro por alerta")
opcion_filtro = st.radio(
    "Seleccionar tipo de alerta:",
    ("Todos", "🔴 Riesgoso", "🟡 Aceptable", "🟢 Bueno")
)

if opcion_filtro != "Todos":
    df_filtrado = df_resultados[df_resultados["Alerta"] == opcion_filtro]
else:
    df_filtrado = df_resultados

mostrar_tabla_con_svg(df_filtrado)

import os
historial_path = "historial_ratios.csv"

df_to_save = df_resultados.copy()
df_to_save["Empresa"] = empresa
df_to_save["Año"] = anio
df_to_save["Ratio"] = df_to_save.index
cols_order = ["Empresa", "Año", "Ratio", "Valor", "Alerta", "Acción sugerida"]
df_to_save = df_to_save[cols_order]

if st.button("💾 Guardar resultados en historial"):
    try:
        if os.path.exists(historial_path):
            df_to_save.to_csv(historial_path, mode='a', header=False, index=False)
        else:
            df_to_save.to_csv(historial_path, mode='w', header=True, index=False)
        st.success("✅ Resultados guardados en historial.")
    except Exception as e:
        st.error(f"❌ Error guardando historial: {e}")

st.header("📂 Historial guardado")
if os.path.exists(historial_path):
    historial_df = pd.read_csv(historial_path)
    empresas_disponibles = historial_df["Empresa"].unique()
    empresa_sel = st.selectbox("Seleccionar empresa para historial:", empresas_disponibles, index=list(empresas_disponibles).index(empresa))
    anios_disponibles = historial_df[historial_df["Empresa"] == empresa_sel]["Año"].unique()
    anio_sel = st.selectbox("Seleccionar año para historial:", sorted(anios_disponibles, reverse=True))
    filtro_hist = (historial_df["Empresa"] == empresa_sel) & (historial_df["Año"] == anio_sel)
    df_hist_filtrado = historial_df[filtro_hist]
    st.dataframe(df_hist_filtrado)
    excel_data = exportar_excel(df_hist_filtrado)
    st.download_button(
        label="📥 Descargar historial filtrado como Excel",
        data=excel_data,
        file_name=f"historial_{empresa_sel}_{anio_sel}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
