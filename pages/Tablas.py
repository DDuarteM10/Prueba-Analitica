# pages/Tablas.py
import streamlit as st
from Utils import mostrar_filtros
def show_Tablas():
    
    st.title("Página de Tablas")

    numero_seleccionado = mostrar_filtros()

    st.write(f"Has seleccionado el número: {numero_seleccionado}")