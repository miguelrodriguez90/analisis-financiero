import streamlit as st
import json

# --- Cargar usuarios desde archivo JSON ---
def cargar_usuarios():
    with open("usuarios.json", "r") as f:
        data = json.load(f)
        return data["usuarios"]

# --- Autenticación simple ---
def autenticar(usuario, clave, usuarios):
    if usuario in usuarios and usuarios[usuario]["clave"] == clave:
        return usuarios[usuario]["rol"]
    return None

# --- Login UI ---
def login():
    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 30px">
            <img src="https://raw.githubusercontent.com/miguelrodriguez90/analisis-financiero/main/logo.png" width="180">
            <h2 style="margin-top: 10px;">🔐 Iniciar sesión en Finanlytix</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Clave", type="password")
        submit = st.form_submit_button("Ingresar")

    if submit:
        usuarios = cargar_usuarios()
        rol = autenticar(usuario.strip(), clave.strip(), usuarios)
        if rol:
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = rol
            st.success("¡Acceso concedido! Redireccionando...")
            st.stop()
        else:
            st.error("Usuario o clave incorrectos")

    st.markdown(
        """
        <div style="text-align:center; margin-top: 50px; color: gray; font-size: 14px;">
            Proyecto desarrollado por <b>Miguel Rodríguez</b> – 2025 © Finanlytix. Todos los derechos reservados.
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Página principal ---
def pagina_principal():
    st.title("📊 Panel de Análisis Financiero")
    st.write(f"Bienvenido, **{st.session_state['usuario']}**")
    st.success("Aquí irá tu análisis financiero según el rol del usuario")

# --- Main ---
def main():
    st.set_page_config(page_title="Finanlytix - Análisis Financiero", page_icon="📈")
    if "usuario" not in st.session_state:
        login()
    else:
        pagina_principal()
# --- Función para calcular EBITDA ---
def calcular_ebitda(utilidad_neta, intereses, impuestos, depreciacion, amortizacion):
    return utilidad_neta + intereses + impuestos + depreciacion + amortizacion

# --- Funciones para calcular ratios ---
def calcular_ratios(datos):
    ebitda = datos['EBITDA']
    ventas = datos['Ventas']
    deuda = datos['Deuda']
    patrimonio = datos['Patrimonio']
    utilidad_neta = datos['Utilidad_neta']

    ratios = {}
    ratios['EBITDA Margen'] = ebitda / ventas if ventas else 0
    ratios['Deuda / EBITDA'] = deuda / ebitda if ebitda else 0
    ratios['ROE'] = utilidad_neta / patrimonio if patrimonio else 0
    return ratios

# --- Mostrar alertas según rangos ---
def mostrar_alertas(ratios):
    deuda_ebitda = ratios.get('Deuda / EBITDA', 0)
    if deuda_ebitda > 3:
        st.error(f"⚠️ Alerta: Deuda/EBITDA alta: {deuda_ebitda:.2f}")
    elif deuda_ebitda > 1.5:
        st.warning(f"⚠️ Atención: Deuda/EBITDA moderada: {deuda_ebitda:.2f}")
    else:
        st.success(f"✅ Deuda/EBITDA en zona segura: {deuda_ebitda:.2f}")

# --- Interfaz principal ---
def main():
    st.set_page_config(page_title="Finanlytix", page_icon="💼", layout="centered")

    st.title("Finanlytix - Análisis Financiero")

    usuarios = cargar_usuarios()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("🔒 Iniciar sesión")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Clave", type="password")
        if st.button("Ingresar"):
            rol = autenticar(usuario, clave, usuarios)
            if rol:
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.session_state.rol = rol
                st.experimental_rerun()
            else:
                st.error("Usuario o clave incorrectos")
    else:
        st.sidebar.write(f"👤 Usuario: **{st.session_state.usuario}** - Rol: **{st.session_state.rol}**")
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.logged_in = False
            st.experimental_rerun()

        # Formulario datos financieros
        st.header("Ingrese los datos financieros")

        utilidad_neta = st.number_input("Utilidad Neta", min_value=0.0, step=1000.0, format="%.2f")
        intereses = st.number_input("Gastos por Intereses", min_value=0.0, step=1000.0, format="%.2f")
        impuestos = st.number_input("Impuestos", min_value=0.0, step=1000.0, format="%.2f")
        depreciacion = st.number_input("Gastos por Depreciación", min_value=0.0, step=1000.0, format="%.2f")
        amortizacion = st.number_input("Gastos por Amortización", min_value=0.0, step=1000.0, format="%.2f")

        ventas = st.number_input("Ventas", min_value=0.0, step=1000.0, format="%.2f")
        deuda = st.number_input("Deuda", min_value=0.0, step=1000.0, format="%.2f")
        patrimonio = st.number_input("Patrimonio", min_value=0.0, step=1000.0, format="%.2f")
        utilidad_neta = utilidad_neta  # ya definida
        capital = st.number_input("Capital", min_value=0.0, step=1000.0, format="%.2f")

        # Calcular EBITDA automáticamente
        ebitda = calcular_ebitda(utilidad_neta, intereses, impuestos, depreciacion, amortizacion)
        st.markdown(f"### EBITDA calculado: **{ebitda:,.2f}**")

        datos = {
            'EBITDA': ebitda,
            'Ventas': ventas,
            'Deuda': deuda,
            'Patrimonio': patrimonio,
            'Utilidad_neta': utilidad_neta,
            'Capital': capital
        }

        if st.button("Calcular Ratios"):
            ratios = calcular_ratios(datos)
            st.write("#### Ratios calculados:")
            for nombre, valor in ratios.items():
                st.write(f"- **{nombre}**: {valor:.2f}")

            mostrar_alertas(ratios)

        # Aquí podés agregar más funcionalidades para admin, p.ej.:
        if st.session_state.rol == "admin":
            st.sidebar.markdown("---")
            st.sidebar.write("⚙️ Funciones Admin")
            # Por ejemplo: gestión usuarios, historial, etc.

        st.sidebar.markdown("© 2025 Finanlytix. Todos los derechos reservados.")

if __name__ == "__main__":
    main()
