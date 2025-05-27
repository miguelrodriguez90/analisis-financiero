
import streamlit as st
from PIL import Image
import json
import os

def aplicar_estilos():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .stButton>button {
            background-color: #0f4c81;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #105a99;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def guardar_historial(datos):
    archivo = "historial.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []

    historial.append(datos)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4)

def mostrar_historial():
    archivo = "historial.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)

        st.subheader("📚 Historial de análisis")
        empresas = sorted(set(item["empresa"] for item in historial))
        anios = sorted(set(item["anio"] for item in historial))

        filtro_empresa = st.selectbox("Filtrar por empresa", ["Todas"] + empresas)
        filtro_anio = st.selectbox("Filtrar por año", ["Todos"] + anios)

        for item in historial:
            if (filtro_empresa == "Todas" or item["empresa"] == filtro_empresa) and                (filtro_anio == "Todos" or item["anio"] == filtro_anio):
                st.markdown(f"### {item['empresa']} - {item['anio']}")
                for k, v in item["resultados"].items():
                    st.write(f"**{k}:** {v:.2%}" if isinstance(v, float) else f"{v}")

def main():
    aplicar_estilos()

    # Mostrar logo
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png")
        st.image(logo, width=150)

    st.title("📊 Sistema de Análisis Financiero")

    # Entrada de datos
    st.subheader("📥 Ingreso de datos financieros")
    empresa = st.text_input("Nombre de la empresa")
    anio = st.number_input("Año del análisis", step=1, value=2025)
    EBITDA = st.number_input("EBITDA", step=1000)
    ventas = st.number_input("Ventas", step=1000)
    deuda = st.number_input("Deuda total", step=1000)
    activo_total = st.number_input("Activo total", step=1000)
    patrimonio = st.number_input("Patrimonio", step=1000)
    utilidad_neta = st.number_input("Utilidad neta", step=1000)
    capital = st.number_input("Capital invertido", step=1000)

    if st.button("📈 Calcular Ratios"):
        if empresa and ventas > 0 and capital > 0 and EBITDA > 0:
            margen_ebitda = EBITDA / ventas
            deuda_ebitda = deuda / EBITDA
            ROE = utilidad_neta / patrimonio if patrimonio else 0
            ROA = utilidad_neta / activo_total if activo_total else 0
            rotacion_activo = ventas / activo_total if activo_total else 0
            margen_utilidad = utilidad_neta / ventas if ventas else 0
            dupont = ROA * (patrimonio / capital) if capital else 0

            resultados = {
                "Margen EBITDA": margen_ebitda,
                "Deuda / EBITDA": deuda_ebitda,
                "ROE": ROE,
                "ROA": ROA,
                "Rotación del Activo": rotacion_activo,
                "Margen de Utilidad": margen_utilidad,
                "Modelo Dupont": dupont
            }

            st.success("✅ Resultados financieros")
            for k, v in resultados.items():
                st.write(f"**{k}:** {v:.2%}")

            # Guardar historial
            guardar_historial({
                "empresa": empresa,
                "anio": anio,
                "usuario": "miguelrodriguez90",
                "resultados": resultados
            })
        else:
            st.warning("❗Por favor, completa todos los campos con valores válidos.")

    mostrar_historial()

    # Pie de página con copyright
    st.markdown(
        """
        <hr style="margin-top: 50px; margin-bottom: 10px;">
        <div style="text-align: center; color: gray; font-size: 0.9em;">
            © 2025 <strong>Finanlytix</strong>. Todos los derechos reservados.
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
