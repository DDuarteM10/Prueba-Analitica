from librerias.lib import *
import pages as pg
from streamlit_option_menu import option_menu
#nombre pagina web
#Plataforma Abierta para el Razonamiento Creativo y Exploracion de datos xD
st.set_page_config(page_title="EUC PARCE",page_icon="fig/logo.png",layout="wide") 


# selected = option_menu(
#     menu_title=None,
#     options=["home", "Data"],
#     icons=["house", "file-earmark-text"],
#     default_index=0,
#     orientation="horizontal",
    
# )
# if selected == "home":
#     st.title("home")
    
v_menu=["Home", "Data"]
#menu vertical
with st.sidebar:
    st.header("Menu")

    selected = option_menu(
        menu_title=None,  # required
        options=v_menu,  # required
        icons=['house', 'gear'],  # optional
        menu_icon="menu-down",  # optional
        default_index=0,  # optional
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#eee","font-weight": "bold","color": "black"},
        }
    )

if selected == "Home":
    pg.show_home()
if selected == "Data":
    pg.show_data()
# home = st.Page("pages/home.py", title="home", icon=":material/home:")
# Data = st.Page("pages/AnalisisDatos.py", title="Data", icon=":material/delete:")
# pg = st.navigation([home, Data])
# pg.run()
