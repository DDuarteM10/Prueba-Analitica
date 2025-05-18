from librerias.lib import *

#st.set_page_config(page_title="Home", layout="wide")  # Solo si es primera instrucción

def show_home():
    with st.container():
        st.markdown("<h1 style='text-align: center;'>EUC PARCE</h1>", unsafe_allow_html=True)
        st.subheader("Plataforma Abierta para el Razonamiento Creativo y Exploración de datos")
        st.write("¡Bienvenido a EUC PARCE! Esta es una herramienta con el propósito de analizar movimientos y saldos en las cuentas de los negocios. "
                 "Permitiendo a los usuarios obtener información valiosa de manera rápida y eficiente.")
    st.markdown("---")
    with st.container():
        st.subheader("¿Como utilizar parce?")
        st.markdown("""
        1. En la ruta <b>data</b>, se cargan automáticamente los datos de un archivo Excel.<br>
        2. La herramienta extrae información valiosa de los negocios para la construcción de filtros.<br>
        &emsp;• Filtros por negocio, por fecha y por documento.<br>
        3. Dentro del menú <b>Dashboard</b>, se pueden visualizar estadísticas generales de los datos y gráficos de los mismos.<br>
        &emsp;• Si el usuario en algún momento necesita descargar la información, es posible en formato CSV.
        """, unsafe_allow_html=True)
    st.markdown("---")    
    st.subheader("Recursos utilizados")

    items = ["Menu de navegacion: https://pypi.org/project/streamlit-navigation-bar/",
             "Menu de navegacion: https://github.com/gabrieltempass/streamlit-navigation-bar/wiki/Multipage#recommended-structure",
             "Configuracion de los temas: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config",
             "Configuracion de tabs: https://discuss.streamlit.io/t/multiple-tabs-in-streamlit/1100/9",
             "Ayuda con container: https://docs.streamlit.io/develop/api-reference/layout/st.container",
             "Configuracion de los temas: https://docs.streamlit.io/develop/concepts/configuration/theming",
             "Configuracion: https://docs.streamlit.io/develop/concepts/configuration/options"]
    cont=st.container()
    with cont:
        for item in items:
            st.write(f"- {item}")





