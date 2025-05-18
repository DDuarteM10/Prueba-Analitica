from librerias.lib import *

def mostrar_filtros():
    st.sidebar.header("Filtros")

    # Filtro dummy de 1 a 10
    if 'filtro_num' not in st.session_state:
        st.session_state.filtro_num = 1

    filtro_num = st.sidebar.selectbox(
        "Selecciona un número",
        list(range(1, 11)),
        index=st.session_state.filtro_num - 1,
        key="filtro_num"
    )

    return filtro_num

@st.cache_data(ttl=600)  # Cachea por 10 minutos, por ejemplo
def cargar_Archivos():
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
