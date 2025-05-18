import streamlit as st
import os

def show_Tablas():
    st.title("Respondiendo algunas preguntas!!")
    st.markdown("---")    
    st.subheader("Recorre los avances del desarrollo")
    Zcol1, Zcol2, Zcol3 = st.columns([1, 2, 1])
    with Zcol2:
        img_folder = os.path.join(os.getcwd(), "Recorrido avances")
        images = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(".png")]
        images.sort()  # Asegura orden si es importante

        if "img_index" not in st.session_state:
            st.session_state.img_index = 0

        if images:
            st.image(images[st.session_state.img_index], use_column_width=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Anterior") and st.session_state.img_index > 0:
                    st.session_state.img_index -= 1
            with col3:
                if st.button("Siguiente ➡️") and st.session_state.img_index < len(images) - 1:
                    st.session_state.img_index += 1
        else:
            st.warning("No se encontraron imágenes en la carpeta 'Recorrido avances'.")
    
