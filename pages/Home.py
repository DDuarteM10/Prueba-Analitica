
from librerias.lib import *
import os
#st.set_page_config(page_title="Home", layout="wide")  # Solo si es primera instrucción

def show_home():
    with st.container():
        col1, col2,col3 = st.columns([1, 4 ,1])
        with col1:
            st.image("fig/Loguito.svg", width=80)
        with col2:
            st.markdown("""
            <div style='text-align: center;'>
                <h1 style='margin-top: 10px;'>EUC PARCE</h1>
            </div>
            """, unsafe_allow_html=True)
        st.subheader("Plataforma Abierta para el Razonamiento Creativo y Exploración de datos")
        st.write("¡Bienvenido a EUC PARCE! Esta es una herramienta con el propósito de analizar movimientos y saldos en las cuentas de los negocios. "
                 "Permitiendo a los usuarios obtener información valiosa de manera rápida y eficiente.")
    st.markdown("---")
    with st.container():
        st.subheader("¿Como utilizar parce?")
        st.markdown("""
        1. En la ruta <b>data</b>, se cargan automáticamente los datos de un archivo Excel.<br>
        2. La herramienta extrae información valiosa de los negocios para la construcción de filtros.<br>
        &emsp;• Filtros por negocio, por fecha y por documento, en este caso el filtro mas optimo es por fecha, ya que no se puede relacionar correctamente los documentos en la tabla saldos<br>
        3. Dentro del menú <b>Dashboard</b>, se pueden visualizar estadísticas generales de los datos y gráficos de los mismos.<br>
        &emsp;• Si el usuario en algún momento necesita descargar la información, es posible en formato CSV.
        """, unsafe_allow_html=True)
    st.markdown("---")    
    st.subheader("Recorre los avances del desarrollo")
    Zcol1, Zcol2, Zcol3 = st.columns([1, 2, 1])
    with Zcol2:
        img_folder = os.path.join(os.getcwd(), "Recorrido avances")
        images = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(".png")]
        images.sort()  # Asegura orden si es importante

        if "img_index" not in st.session_state:
            st.session_state.img_index = 0

        if images:
            st.image(images[st.session_state.img_index], use_column_width=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Anterior") and st.session_state.img_index > 0:
                    st.session_state.img_index -= 1
            with col3:
                if st.button("Siguiente ➡️") and st.session_state.img_index < len(images) - 1:
                    st.session_state.img_index += 1
        else:
            st.warning("No se encontraron imágenes en la carpeta 'Recorrido avances'.")
    st.markdown("---")    
    st.subheader("Recursos utilizados")

    items = ["Menu de navegacion: https://pypi.org/project/streamlit-navigation-bar/",
             "Menu de navegacion: https://github.com/gabrieltempass/streamlit-navigation-bar/wiki/Multipage#recommended-structure",
             "Configuracion de los temas: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config",
             "Configuracion de tabs: https://discuss.streamlit.io/t/multiple-tabs-in-streamlit/1100/9",
             "Ayuda con container: https://docs.streamlit.io/develop/api-reference/layout/st.container",
             "Configuracion de los temas: https://docs.streamlit.io/develop/concepts/configuration/theming",
             "Configuracion: https://docs.streamlit.io/develop/concepts/configuration/options",
             "Recorrido Imagenes: https://discuss.streamlit.io/t/automatic-slideshow/38342/5"]
    cont=st.container()
    with cont:
        for item in items:
            st.write(f"- {item}")





