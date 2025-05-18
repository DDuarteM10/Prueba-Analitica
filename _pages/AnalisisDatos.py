from librerias.lib import *
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

# Menú principal
v_menu = ["Movimientos", "Saldos"]

def cargar_datos():
    archivo = "docs/data.xlsx"
    try:
        df_mov = pd.read_excel(archivo, sheet_name="movimientos")
        df_sal = pd.read_excel(archivo, sheet_name="saldos")
        df_mov["fecha"] = pd.to_datetime(df_mov["fecha"].astype(str), format="%Y%m%d", errors="coerce").dt.date
        df_sal["fecha"] = pd.to_datetime(df_sal["fecha"].astype(str), format="%Y%m%d", errors="coerce").dt.date
        df_mov["documento"] = df_mov["documento"].astype(str)
        return df_mov, df_sal
    except FileNotFoundError:
        st.error("El archivo `data.xlsx` no se encontró en la carpeta `docs`.")
        return None, None

def filtrosXTabla(dataFrame, clave_key="filtro"):
    col1A, col2A,col3A = st.columns(3)
    with col1A:
        negocios = dataFrame['negocio'].dropna().unique()
        negocios_sel = st.multiselect(
            "Selecciona uno o más negocios:",
            options=sorted(negocios),
            default=sorted(negocios)[:1],
            key=f"neg_{clave_key}"
        )
    with col2A:
        # Filtrar el DataFrame según los negocios seleccionados
        df_filtrado_negocios = dataFrame[dataFrame['negocio'].isin(negocios_sel)]

        # Extraer las cuentas únicas solo para esos negocios
        cuentas = sorted(df_filtrado_negocios['cuenta'].dropna().unique())
        opciones_cuentas = ["Todas"] + cuentas  # Agrega opción "Todas"

        # Selector múltiple para elegir cuentas
        cuentas_sel = st.multiselect(
            "Selecciona una o más cuentas:",
            options=opciones_cuentas,
            default=["Todas"],
            key=f"cta_{clave_key}"
        )

        # Lógica para determinar las cuentas filtradas
        if "Todas" in cuentas_sel or not cuentas_sel:
            cuentas_filtradas = cuentas
        else:
            cuentas_filtradas = cuentas_sel
    with col3A:
        # Filtrar el DataFrame según los negocios seleccionados
        df_filtrado_negocios = dataFrame[dataFrame['negocio'].isin(negocios_sel)]
        # Extraer las cuentas únicas solo para esos negocios
        terceros = sorted(df_filtrado_negocios['tercero'].dropna().unique())
        opciones_terceros = ["Todas"] + terceros  # Agrega opción "Todas"
         # Selector múltiple para elegir cuentas
        terceros_sel = st.multiselect(
            "Selecciona una o más terceros:",
            options=opciones_terceros,
            default=["Todas"],
            key=f"ter_{clave_key}"
        )

        # Lógica para determinar las cuentas filtradas
        if "Todas" in terceros_sel or not terceros_sel:
            terceros_filtradas = terceros
        else:
            terceros_filtradas = terceros_sel

    col1B, col2B = st.columns(2)
    with col1B:
        st.subheader("📆 Filtro por fecha")
        fecha_ini = st.date_input(
            "Fecha inicial:",
            value=pd.to_datetime(dataFrame["fecha"]).min(),
            key=f"fecha_ini_{clave_key}"
        )
        
    with col2B:
        st.subheader("")
        fecha_fin = st.date_input(
            "Fecha final:",
            value=pd.to_datetime(dataFrame["fecha"]).max(),
            key=f"fecha_fin_{clave_key}"
        )
    
    return negocios_sel, fecha_ini, fecha_fin,cuentas_filtradas,terceros_filtradas

def show_data():
    st.header("📊 Análisis de Datos Financieros")
    
    # Cargar los datos
    df_mov, df_sal = cargar_datos()
    if df_mov is None or df_sal is None:
        return

    # Filtros globales (para ambas tablas)
    st.subheader("🎯 Filtros generales")
    df_union = pd.concat([df_mov[['negocio', 'cuenta', 'fecha','tercero']], df_sal[['negocio', 'cuenta', 'fecha','tercero']]])
    negocios_sel, fecha_ini, fecha_fin, cuentas_sel,terceros_sel = filtrosXTabla(df_union, clave_key="global")

    # Aplicar filtros a ambos DataFrames
    df_mov_filtrado = df_mov[
        (df_mov["negocio"].isin(negocios_sel)) &
        (df_mov["fecha"] >= fecha_ini) &
        (df_mov["fecha"] <= fecha_fin) &
        (df_mov["cuenta"].isin(cuentas_sel)) &
        (df_mov["tercero"].isin(terceros_sel)) 
    ]

    df_sal_filtrado = df_sal[
        (df_sal["negocio"].isin(negocios_sel)) &
        (df_sal["fecha"] >= fecha_ini) &
        (df_sal["fecha"] <= fecha_fin) &
        (df_sal["cuenta"].isin(cuentas_sel)) &
        (df_mov["tercero"].isin(terceros_sel)) 
    ]

    # Tabs de análisis
    tab1, tab2 = st.tabs(["📈 Movimientos", "💰 Saldos"])

    with tab1:
        st.subheader("📋 Tabla de Movimientos")
        st.dataframe(df_mov_filtrado)

        

    with tab2:
        st.subheader("📋 Tabla de Saldos")
        st.dataframe(df_sal_filtrado.style.applymap(color_saldo, subset=["saldo"]))
    
    # Sección SEPARADA para las gráficas (por fuera de los tabs anteriores)
    if not df_mov_filtrado.empty or not df_sal_filtrado.empty:
        st.markdown("---")
        st.header("📊 Gráficas de Análisis")
        tabGraf1, tabGraf2 = st.tabs(["📉 Débitos/Créditos", "📈 Saldos"])

        with tabGraf1:
            col1, col2 = st.columns(2)

            with col1:
                df_pivot1 = df_mov_filtrado.groupby(["fecha", "negocio"])["debitos"].sum().unstack()
                fig1, ax1 = plt.subplots(figsize=(8, 4))
                df_pivot1.plot(ax=ax1, marker='o', title="Débitos por fecha y negocio")
                ax1.set_xlabel("Fecha")
                ax1.set_ylabel("Débitos")
                ax1.grid(True)
                ax1.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig1)

            with col2:
                df_pivot2 = df_mov_filtrado.groupby(["fecha", "negocio"])["creditos"].sum().unstack()
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                df_pivot2.plot(ax=ax2, marker='o', title="Créditos por fecha y negocio")
                ax2.set_xlabel("Fecha")
                ax2.set_ylabel("Créditos")
                ax2.grid(True)
                ax2.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig2)

    with tabGraf2:
        df_pivot = df_sal_filtrado.groupby(["fecha", "negocio"])["saldo"].sum().unstack()
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        df_pivot.plot(ax=ax3, marker='o', title="Saldo por fecha y negocio")
        ax3.set_xlabel("Fecha")
        ax3.set_ylabel("Saldo")
        ax3.grid(True)
        ax3.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        st.pyplot(fig3)
        
def color_saldo(val):
    color = "green" if val > 0 else "red" if val < 0 else "black"
    return f"color: {color}"

# Aplica el estilo y muéstralo

        
