from librerias.lib import *

def show_home():
    with st.container():
        #st.title("EUC PARCE",align="center")    
        st.markdown("<h1 style='text-align: center;'>EUC PARCE</h1>", unsafe_allow_html=True)
        st.subheader("Plataforma Abierta para el Razonamiento Creativo y Exploracion de datos")
        st.write("¡Bienvenido a EUC PARCE! , esta es una herramienta con el proposito de ")
        # Cargar datos
    archivo = "data/datos.xlsx"
        #df_mov = pd.read_excel(archivo, sheet_name="movimientos")
        #df_sal = pd.read_excel(archivo, sheet_name="saldos")

        #st.subheader("Vista de Movimientos")
        #st.dataframe(df_mov)

        #st.subheader("Vista de Saldos")
        #st.dataframe(df_sal)
