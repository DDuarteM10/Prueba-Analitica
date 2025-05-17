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
    col1A, col2A = st.columns(2)
    with col1A:
        negocios = dataFrame['negocio'].dropna().unique()
        negocios_sel = st.multiselect(
            "Selecciona uno o más negocios:",
            options=sorted(negocios),
            default=sorted(negocios)[:1],
            key=f"neg_{clave_key}"
        )
    with col2A:
        st.subheader("⚙️ Puedes incluir otros filtros aquí")

    col1B, col2B = st.columns(2)
    with col1B:
        st.subheader("📆 Filtro por fecha")
        fecha_ini = st.date_input(
            "Fecha inicial:",
            value=pd.to_datetime(dataFrame["fecha"]).min(),
            key=f"fecha_ini_{clave_key}"
        )
        fecha_fin = st.date_input(
            "Fecha final:",
            value=pd.to_datetime(dataFrame["fecha"]).max(),
            key=f"fecha_fin_{clave_key}"
        )
    with col2B:
        st.subheader("⚙️ Otro espacio opcional")
    
    return negocios_sel, fecha_ini, fecha_fin

def show_data():
    st.header("📊 Análisis de Datos Financieros")
    #filtros

    #menu
    
    df_mov, df_sal = cargar_datos()
    if df_mov is None or df_sal is None:
        return

    tab1, tab2 = st.tabs(["📈 Movimientos", "💰 Saldos"])

    # ============================
    # TABLA DE MOVIMIENTOS
    # ============================
    with tab1:
        st.subheader("🎯 Filtros para Movimientos")
        negocios_sel, fecha_ini, fecha_fin = filtrosXTabla(df_mov, clave_key="mov")
        
        st.subheader("📋 Tabla de Movimientos")
        df_filtrado = df_mov[
            (df_mov["negocio"].isin(negocios_sel)) &
            (df_mov["fecha"] >= fecha_ini) &
            (df_mov["fecha"] <= fecha_fin)
        ]
        st.dataframe(df_filtrado)

        if not df_filtrado.empty:
            st.subheader("📈 Gráficas de Movimientos")
            tabGraf1, tabGraf2 = st.tabs(["📉 Débitos", "📈 Créditos"])

            with tabGraf1:
                graf1, graf2 = st.columns(2)
                with graf1:
                    df_pivot1 = df_filtrado.groupby(["fecha", "negocio"])["debitos"].sum().unstack()
                    fig1, ax1 = plt.subplots(figsize=(8, 4))
                    df_pivot1.plot(ax=ax1, marker='o', title="Débitos por fecha y negocio")
                    ax1.set_xlabel("Fecha")
                    ax1.set_ylabel("Débitos")
                    ax1.grid(True)
                    ax1.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.xticks(rotation=45)
                    st.pyplot(fig1)
                with graf2:
                    st.info("Puedes agregar otra visualización aquí")

            with tabGraf2:
                df_pivot2 = df_filtrado.groupby(["fecha", "negocio"])["creditos"].sum().unstack()
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                df_pivot2.plot(ax=ax2, marker='o', title="Créditos por fecha y negocio")
                ax2.set_xlabel("Fecha")
                ax2.set_ylabel("Créditos")
                ax2.grid(True)
                ax2.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig2)

    # ============================
    # TABLA DE SALDOS
    # ============================
    with tab2:
        st.subheader("🎯 Filtros para Saldos")
        negocios_sel, fecha_ini, fecha_fin = filtrosXTabla(df_sal, clave_key="sal")

        st.subheader("📋 Tabla de Saldos")
        df_filtrado = df_sal[
            (df_sal["negocio"].isin(negocios_sel)) &
            (df_sal["fecha"] >= fecha_ini) &
            (df_sal["fecha"] <= fecha_fin)
        ]
        st.dataframe(df_filtrado)

        if not df_filtrado.empty:
            st.subheader("📈 Gráfica de Saldos")
            df_pivot = df_filtrado.groupby(["fecha", "negocio"])["saldo"].sum().unstack()
            fig, ax = plt.subplots(figsize=(10, 5))
            df_pivot.plot(ax=ax, marker='o', title="Saldo por fecha y negocio")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Saldo")
            ax.grid(True)
            ax.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks(rotation=45)
            st.pyplot(fig)
