from librerias.lib import *
from PIL import Image

def show_Tablas():
    st.title("Conoce al desarrollador de EUC PARCE")
    
    # Cargar imagen con alta resolución
    image = Image.open("fig/Image.jpg")
    
    # Contenedor centrado
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image(image, use_column_width=True, caption=None,width=150)

    with col2:
        
        
        st.markdown("""
            <div style='
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-top: 20px;
            '>
                <h2 style='margin-bottom: 10px;'>David Alejandro Duarte Montañez</h2>
                <p style='font-size: 18px; margin: 5px 0;'>Ingeniero en Mecatrónica</p>
                <p style='font-size: 16px; margin: 5px 0;'>📧 ing.dduartem@gmail.com</p>
                <p style='font-size: 16px; margin: 5px 0;'>🔗 <a href='https://www.linkedin.com/in/davidduartem' target='_blank'>LinkedIn</a></p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        st.write("""
            Estudiante de décimo semestre de Ingeniería en Mecatrónica en la Universidad
            Militar Nueva Granada, con una profunda pasión por la tecnología, la investigación
            y el aprendizaje. Mi entusiasmo por explorar nuevas ideas y conceptos me permite
            adaptarme rápidamente a entornos dinámicos, desafiantes y de trabajo en equipo.
            He trabajado con diversos lenguajes de programación como Python, Java, C++,
            C#, SQL y JavaScript, aplicando estos conocimientos en automatización de procesos y en la integración de bases de datos y conexiones a la nube. Además, tengo
            experiencia en el desarrollo backend utilizando Spring Boot con la arquitectura
            clean (nivel junior), y en el manejo de herramientas como Git, Azure, Power BI, y
            bases de datos relacionales como PostgreSQL y SQL Server. Utilizo entornos de
            desarrollo como Visual Studio, IntelliJ, NetBeans y DBeaver para la creación de
            soluciones robustas y escalables.
            """)