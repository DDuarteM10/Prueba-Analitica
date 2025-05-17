from librerias.lib import *
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
v_menu=["Movimientos", "Saldos"]
#objetos:


def cargar_datos():
    archivo = "docs/data.xlsx"
    try:
        df_mov = pd.read_excel(archivo, sheet_name="movimientos")
        df_sal = pd.read_excel(archivo, sheet_name="saldos")
        df_mov["fecha"] = pd.to_datetime(df_mov["fecha"].astype(str), format="%Y%m%d", errors="coerce").dt.date
        df_sal["fecha"] = pd.to_datetime(df_sal["fecha"].astype(str), format="%Y%m%d", errors="coerce").dt.date
        return df_mov, df_sal
    except FileNotFoundError:
        st.error("El archivo `datos.xlsx` no se encontró en la carpeta `data`.")
        return None, None
    
def show_data(): #funcion main
        cargar_datos()
        with st.container():
            st.header("🔍 Análisis de Datos")
            st.write("Aquí puedes cargar, procesar y analizar los datos de `movimientos` y `saldos`.")

            df_mov, df_sal = cargar_datos()

            if df_mov is not None and df_sal is not None:
                selected = option_menu(
                    menu_title=None,  # required
                    options=v_menu,  # required
                    icons=['house', 'gear'],  # optional
                    menu_icon="menu-down",  # optional
                    default_index=0,  # optional
                    orientation="horizontal",
                    styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#eee","font-weight": "bold","color": "black"},
                    }
                )
                
                
                
                if selected == "Movimientos":
                    negocios_sel,fecha_inicio,fecha_fin=filtrosXTabla(df_mov)
                    st.subheader("📊 Tabla de Movimientos")
                    #st.dataframe(df_mov)
                    df_filtrado = df_mov[
                        (df_mov["negocio"].isin(negocios_sel)) &
                        (df_mov["fecha"] >= fecha_inicio) &
                        (df_mov["fecha"] <= fecha_fin)
                    ]
                    st.dataframe(df_filtrado)
                    graf1, graf2 = st.columns(2)
                    with graf1:
                        # Agrupar y pivotear para graficar fácilmente
                        df_pivot1 = df_filtrado.groupby(["fecha", "negocio"])["debitos"].sum().unstack()

                        # Graficar directamente con pandas
                        ax = df_pivot1.plot(figsize=(10, 5), marker='o', title="debitos y creditos por fecha")
                        ax.set_xlabel("Fecha")
                        ax.set_ylabel("debitos y creditos")
                        ax.grid(True)
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                        
                    with graf2:

                        df_pivot2 = df_filtrado.groupby(["fecha", "negocio"])["creditos"].sum().unstack()

                        # Graficar directamente con pandas
                        ax = df_pivot2.plot(figsize=(10, 5), marker='o', title="debitos y creditos por fecha")
                        ax.set_xlabel("Fecha")
                        ax.set_ylabel("debitos y creditos")
                        ax.grid(True)
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                     # Agrupar y pivotear para graficar fácilmente
                    

                elif selected == "Saldos":
                    negocios_sel,fecha_inicio,fecha_fin=filtrosXTabla(df_sal)
                    st.subheader("📊 Tabla de Saldos")
                    df_filtrado = df_sal[
                        (df_sal["negocio"].isin(negocios_sel)) &
                        (df_sal["fecha"] >= fecha_inicio) &
                        (df_sal["fecha"] <= fecha_fin)
                    ]
                    st.dataframe(df_filtrado)
                    #graficas
                    if negocios_sel: #verifica si hay negocios 
                        #df_filtrado = df_sal[df_sal["negocio"].isin(negocios_sel)]

                        # Agrupar y pivotear para graficar fácilmente
                        df_pivot = df_filtrado.groupby(["fecha", "negocio"])["saldo"].sum().unstack()

                        # Graficar directamente con pandas
                        ax = df_pivot.plot(figsize=(10, 5), marker='o', title="Saldo por fecha")
                        ax.set_xlabel("Fecha")
                        ax.set_ylabel("Saldo")
                        ax.grid(True)
                        plt.xticks(rotation=45)
                        st.pyplot(plt)

def filtrosXTabla(dataFrame):
    #objeto de filtro 
    col1A, col2A = st.columns(2)
    with col1A:
        negocios = dataFrame['negocio'].dropna().unique()
        negocios_sel = st.multiselect(
            "Selecciona uno o más negocios:",
            options=sorted(negocios),
            default=sorted(negocios)[:1],  # Opcional: puedes seleccionar el primero por defecto
            key="neg_saldos"
        )
    with col2A:
        st.subheader("📌 Hola x2")

    
    col1B, col2B = st.columns(2)
    with col1B:
        st.subheader("📆 Filtro por fecha")
        fecha_ini = st.date_input("Fecha inicial:", value=pd.to_datetime(dataFrame["fecha"]).min())
        fecha_fin = st.date_input("Fecha final:", value=pd.to_datetime(dataFrame["fecha"]).max())
    with col2B:
        st.subheader("📌 Hola x2")
    return negocios_sel,fecha_ini,fecha_fin