from librerias.lib import *
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title="EUC PARCE",
    page_icon="fig/Rm.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None  # Esto oculta el menú de navegación de páginas
)
styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "center",  # <-- Aquí el cambio para centrar
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "black",
        "font-weight": "normal",
        "padding": "14px",
    }
}
pages = ["Home", "Dashboard","Desarrollador","GitHub"]  # O ["Home", "Data"] si cambias el nombre en tu código
urls = {"GitHub": "https://github.com/DDuarteM10"}
options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=None,  # O tu SVG si tienes uno
    urls=urls,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_home,
    "Dashboard": pg.show_data,  # O "Data": pg.show_data si cambias el nombre
    "Desarrollador": pg.show_Info,
}

go_to = functions.get(page)
if go_to:
    go_to()
