from librerias.lib  import *
import _pages as pg
from streamlit_option_menu import option_menu
from streamlit_navigation_bar import st_navbar
import os
logo_path = os.path.abspath("fig/Loguito.svg")


#Plataforma Abierta para el Razonamiento Creativo y Exploracion de datos xD
st.set_page_config(
    page_title="EUC PARCE",
    page_icon="fig/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None  # Esto oculta el menú de navegación de páginas
)


    
# v_menu=["Home", "Data"]
# #menu vertical
# with st.sidebar:
#     st.header("Menu")

#     selected = option_menu(
#         menu_title=None,  # required
#         options=v_menu,  # required
#         icons=['house', 'gear'],  # optional
#         menu_icon="menu-down",  # optional
#         default_index=0,  # optional
#         orientation="horizontal",
#         styles={
#         "container": {"padding": "0!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"}, 
#         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#eee","font-weight": "bold","color": "black"},
#         }
#     )

# if selected == "Home":
#     pg.show_home()
# if selected == "Data":
#     pg.show_data()

#intento de menu horizontal

pages = ["Home", "Data"]
styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
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
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": True,
    "show_sidebar": False,
}
page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=None,
    styles=styles,
    options=options,
)
functions = {
    "Home": pg.show_home,
    "Data": pg.show_data,
}
go_to = functions.get(page)
if go_to:
    go_to()