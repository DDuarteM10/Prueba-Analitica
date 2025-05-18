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
       with col1A:
            negocios = dataFrame['negocio'].dropna().unique().tolist()
            opciones_negocios = ["Todas"] + negocios

            # Estado inicial del multiselect
            negocios_sel = st.multiselect(
                "Selecciona uno o más negocios:",
                options=opciones_negocios,
                default=opciones_negocios[1], #cambiar por Todas
                key=f"neg_{clave_key}"
            )

            # Reemplazar "Todas" por todos los negocios
            if "Todas" in negocios_sel:
                negocios_filtradas = negocios
            else:
                negocios_filtradas = negocios_sel
    with col2A:
        # Filtrar el DataFrame según los negocios seleccionados
        df_filtrado_negocios = dataFrame[dataFrame['negocio'].isin(negocios_filtradas)]

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
    # with col3A: #documento no se puede porque no se puede garantizar un cruce unico
    #     # Filtrar el DataFrame según los negocios seleccionados
    #     df_filtrado_negocios = dataFrame[dataFrame['negocio'].isin(negocios_sel)]
    #     # Extraer las cuentas únicas solo para esos negocios
    #     documentos = sorted(df_filtrado_negocios['documento'].dropna().unique())
    #     opciones_documentos = ["Todas"] + documentos  # Agrega opción "Todas"
    #      # Selector múltiple para elegir cuentas
    #     documentos_sel = st.multiselect(
    #         "Selecciona una o más documentos:",
    #         options=opciones_documentos,
    #         default=["Todas"],
    #         key=f"doc_{clave_key}"
    #     )

    #     # Lógica para determinar las cuentas filtradas
    #     if "Todas" in documentos_sel or not documentos_sel:
    #         documentos_filtradas = documentos
    #     else:
    #         documentos_filtradas = documentos_sel

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
    
    return negocios_filtradas, fecha_ini, fecha_fin,cuentas_filtradas

def show_data():
    st.header("📊 Análisis de Datos Financieros")
    
    # Cargar los datos
    df_mov, df_sal = cargar_datos()
    if df_mov is None or df_sal is None:
        return

    # Filtros globales (para ambas tablas)
    st.subheader("🎯 Filtros generales")
    df_union = pd.concat([df_mov[['negocio', 'cuenta', 'fecha', 'documento']], df_sal[['negocio', 'cuenta', 'fecha']]], sort=False)
    negocios_sel, fecha_ini, fecha_fin, cuentas_sel = filtrosXTabla(df_union, clave_key="global")

    # Aplicar filtros a ambos DataFrames
    df_mov_filtrado = df_mov[
        (df_mov["negocio"].isin(negocios_sel)) &
        (df_mov["fecha"] >= fecha_ini) &
        (df_mov["fecha"] <= fecha_fin) &
        (df_mov["cuenta"].isin(cuentas_sel)) 
        
    ]

    df_sal_filtrado = df_sal[
        (df_sal["negocio"].isin(negocios_sel)) &
        (df_sal["fecha"] >= fecha_ini) &
        (df_sal["fecha"] <= fecha_fin) &
        (df_sal["cuenta"].isin(cuentas_sel)) 
        
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
        st.header("🚨Alertas y Gráficas de Análisis 📊")
        Alertas,tabGraf1, tabGraf2,ResumencitoSemalal = st.tabs(["🚨 Alertas","📉 Débitos/Créditos", "📈 Saldos","Resumen semanal"])

        with tabGraf1:
            col1, col2 = st.columns(2)

            with col1:
                df_pivot1 = df_mov_filtrado.groupby(["fecha", "negocio"])["debitos"].sum().unstack()
                fig1, ax1 = plt.subplots(figsize=(8, 4))
                df_pivot1.plot(ax=ax1, marker='o', title="Tendencia de Débitos por fecha y negocio")
                ax1.set_xlabel("Fecha")
                ax1.set_ylabel("Débitos")
                ax1.grid(True)
                ax1.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig1)

            with col2:
                df_pivot2 = df_mov_filtrado.groupby(["fecha", "negocio"])["creditos"].sum().unstack()
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                df_pivot2.plot(ax=ax2, marker='o', title="Tendencias de Créditos por fecha y negocio")
                ax2.set_xlabel("Fecha")
                ax2.set_ylabel("Créditos")
                ax2.grid(True)
                ax2.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig2)

        with tabGraf2:
            col1, col2 = st.columns(2)
            with col1:
                df_pivot = df_sal_filtrado.groupby(["fecha", "negocio"])["saldo"].sum().unstack()
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                df_pivot.plot(ax=ax3, marker='o', title="Saldo por fecha y negocio")
                ax3.set_xlabel("Fecha")
                ax3.set_ylabel("Saldo")
                ax3.grid(True)
                ax3.legend(title="Negocio", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                st.pyplot(fig3)
            # with col2:
            #     fig, ax = plt.subplots(figsize=(10, 5))

            #     # Graficar cada negocio
            #     for negocio in negocios_sel:
            #         df_mov_nego = df_mov_filtrado[df_mov_filtrado["negocio"] == negocio].copy()
            #         if df_mov_nego.empty:
            #             continue

            #         # Ordenar por fecha
            #         df_mov_nego = df_mov_nego.sort_values(by="fecha")

            #         # Calcular saldo estimado acumulado
            #         df_mov_nego["saldo_estimado"] = df_mov_nego["creditos"].cumsum() - df_mov_nego["debitos"].cumsum()

            #         # Graficar en el mismo eje con etiqueta
            #         ax.plot(df_mov_nego["fecha"], df_mov_nego["saldo_estimado"], marker='o', label=negocio)

            #     # Personalizar la gráfica después del bucle
            #     ax.set_title("Saldo estimado acumulado por negocio")
            #     ax.set_xlabel("Fecha")
            #     ax.set_ylabel("Saldo estimado")
            #     ax.grid(True)
            #     ax.legend()
            #     plt.xticks(rotation=45)

            #     # Mostrar en Streamlit
            #     st.pyplot(fig)
            with Alertas:
                st.subheader("🚨 Alertas y estadisticas basicas")
                alertas1, alertas2, alertas3 = st.columns(3)
                with alertas1:
                    st.metric(label="Negocios seleccionados", value=len(negocios_sel))
                    promedio_debito = round(df_mov_filtrado["debitos"].mean(), 2)
                    color = "green" if promedio_debito > 0 else "red" if promedio_debito < 0 else "black"
                    
                    st.markdown(
                        f"""
                        <div style='text-align: left'>
                            <span style='font-size: 1em;'>Promedio en débito</span><br>
                            <span style='font-size: 1.5em; color: {color}; font-weight: bold;'>{promedio_debito}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with alertas2:
                    st.metric(label="Cant. de datos en movimientos", value=len(df_mov_filtrado))
                    promedio_credito = round(df_mov_filtrado["creditos"].mean(), 2)
                    color = "green" if promedio_credito > 0 else "red" if promedio_credito < 0 else "black"
                    st.markdown(
                        f"""
                        <div style='text-align: left'>
                            <span style='font-size: 1em;'>Promedio en créditos</span><br>
                            <span style='font-size: 1.5em; color: {color}; font-weight: bold;'>{promedio_credito}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with alertas3:
                    st.metric(label="Cant. de datos en  saldos", value=len(df_sal_filtrado))
                    promedio_saldo = round(df_sal_filtrado["saldo"].mean(), 2)
                    color = "green" if promedio_saldo > 0 else "red" if promedio_saldo < 0 else "black"
                    st.markdown(
                        f"""
                        <div style='text-align: left'>
                            <span style='font-size: 1em;'>Promedio de saldos</span><br>
                            <span style='font-size: 1.5em; color: {color}; font-weight: bold;'>{promedio_saldo}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                anomalias,df_anomalias = datos_inusuales(negocios_sel,df_sal_filtrado)
                if not df_anomalias.empty:
                    st.subheader("🔍 Anomalías detectadas")
                    st.metric(label="Cant. anomalías con un umbral del $500.000.000", value=len(df_anomalias))
                    st.dataframe(df_anomalias[["fecha", "negocio", "saldo", "variacion_saldo"]].style.applymap(color_saldo, subset=["saldo"]))
                else:
                    st.info("✅ No se detectaron anomalías con los parámetros actuales.")
                with ResumencitoSemalal:
                    colSaldos,colMov=st.columns(2)
                    with colSaldos:
                        st.subheader("📋 Resumen de Saldos")
                        # Agregar columna de semana
                        df_sal_filtrado["fecha"] = pd.to_datetime(df_sal_filtrado["fecha"], format="%Y/%m/%d", errors="coerce")
                        df_sal_filtrado["semana"] = df_sal_filtrado["fecha"].dt.isocalendar().week

                        # Agrupar por semana y negocio
                        resumen_semanal = df_sal_filtrado.groupby(["semana", "negocio"])["saldo"].agg(["mean", "sum"]).reset_index()

                        st.dataframe(resumen_semanal)

                        # Opcional: graficar promedio semanal por negocio
                        for negocio in resumen_semanal["negocio"].unique():
                            df_nego = resumen_semanal[resumen_semanal["negocio"] == negocio]
                            figsemanal, axSemanal = plt.subplots(figsize=(10, 5))
                            axSemanal.plot(df_nego["semana"], df_nego["mean"], marker="o", label=f"{negocio}")
                            axSemanal.set_title(f"Saldo promedio semanal - {negocio}")
                            axSemanal.set_xlabel("Semana")
                            axSemanal.set_ylabel("Saldo promedio")
                            axSemanal.grid(True)
                            axSemanal.legend()
                            st.pyplot(figsemanal)   
                    with colMov:
                        st.subheader("📋 Resumen de Movimientos Semanales")
                        # Asegura formato de fecha y columna semana
                        df_mov_filtrado["fecha"] = pd.to_datetime(df_mov_filtrado["fecha"], format="%Y/%m/%d", errors="coerce")
                        df_mov_filtrado["semana"] = df_mov_filtrado["fecha"].dt.isocalendar().week

                        # Agrupa por semana y negocio
                        resumen_semanal = df_mov_filtrado.groupby(["semana", "negocio"])[["debitos", "creditos"]].agg(["mean", "sum"]).reset_index()

                        st.dataframe(resumen_semanal)

                        # Graficar débitos y créditos promedio semanal por negocio
                        for negocio in resumen_semanal["negocio"].unique():
                            df_nego = resumen_semanal[resumen_semanal["negocio"] == negocio]
                            figsemanal, axSemanal = plt.subplots(figsize=(10, 5))
                            # Graficar débitos promedio
                            axSemanal.plot(df_nego["semana"], df_nego[("debitos", "mean")], marker="o", label="Débitos promedio")
                            # Graficar créditos promedio
                            axSemanal.plot(df_nego["semana"], df_nego[("creditos", "mean")], marker="o", label="Créditos promedio")
                            axSemanal.set_title(f"Débitos y Créditos promedio semanal - {negocio}")
                            axSemanal.set_xlabel("Semana")
                            axSemanal.set_ylabel("Monto promedio")
                            axSemanal.grid(True)
                            axSemanal.legend()
                            st.pyplot(figsemanal)   
                       
def color_saldo(val):
    color = "green" if val > 0 else "red" if val < 0 else "black"
    return f"color: {color}"


def datos_inusuales(negocios_sel,df_sal_filtrado):
    Umbral_Caida=500_000_000  
    anomalias=[]
    for negocio in negocios_sel:
        df_nego = df_sal_filtrado[df_sal_filtrado["negocio"] == negocio].copy()
        
        if df_nego.empty:
            continue
        df_nego = df_nego.sort_values("fecha")  # Asegura el orden cronológico
        df_nego["variacion_saldo"] = df_nego["saldo"].diff()
        df_anomalias = df_nego[
            (df_nego["saldo"] < 0) |
            (df_nego["variacion_saldo"] < -Umbral_Caida)
        ].copy()
        df_anomalias["negocio"] = negocio
        anomalias.append(df_anomalias)
    return anomalias,df_anomalias
# Aplica el estilo y muéstralo


