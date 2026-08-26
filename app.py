import streamlit as st
from fpdf import FPDF
import datetime
import os

st.set_page_config(page_title="Comisiones USAER 02-E", page_icon="🏫", layout="centered")

# Base de datos del personal
personal = {
    "Cindy Mayanín Burgos González": {"escuela": "Damián Carmona", "director": "Mtra. Maribel Vargas Arana", "prefijo": "la maestra"},
    "Marycruz Caamal Coral": {"escuela": "Ichcaanziho", "director": "Mtra. Rennaty Maribel Puga Jimenez", "prefijo": "la maestra"},
    "María Cecilia Solís Vázquez": {"escuela": "Ichcaanziho", "director": "Mtra. Rennaty Maribel Puga Jimenez", "prefijo": "la maestra"},
    "Dolores Eugenia Cortázar Navarrete": {"escuela": "Gregorio Torres Quintero", "director": "Mtro. Elmer Ariel Ontiveros Requena", "prefijo": "la maestra"},
    "Dianely de Sugeidy Caamal Tamay": {"escuela": "Remigio Aguilar Sosa", "director": "Mtro. Carlos Esteban Heredia GCantón", "prefijo": "la maestra"},
    "Luis Jorge García Herrera": {"escuela": "Elvira Parra Ávila", "director": "Mtro. Manuel Jesús Alcocer Vázquez", "prefijo": "el maestro"},
    "María del Rosario Pérez Vitorin": {"escuela": "Manuel Sarrado", "director": "Mtro. José Alberto Reyna Martínez", "prefijo": "la maestra"},
    "Zuemmy del Carmen Pérez Basto": {"escuela": "Domingo Solís Rodríguez", "director": "Mtra. Erika Basto Ek", "prefijo": "la maestra"},
    "Pamela Betancourt Piña": {"escuela": "Quintana Roo", "director": "Mtro. Jorge Adrián Cetina Cach", "prefijo": "la maestra"}
}

# Creación de plantilla PDF con Encabezado y Pie de Página automáticos
class PDFInstitucional(FPDF):
    def header(self):
        if os.path.exists("encabezado.png"):
            # Coloca la imagen abarcando el ancho de la hoja
            self.image("encabezado.png", x=10, y=10, w=190)
        # ESTA ES LA SOLUCIÓN: Forzar el cursor 45mm hacia abajo para librar la imagen
        self.set_y(45)

    def footer(self):
        # Posición a 3.5 cm desde el final de la página
        self.set_y(-35)
        if os.path.exists("pie_pagina.png"):
            self.image("pie_pagina.png", x=10, y=self.get_y(), w=190)

def generar_pdf(nombre, datos):
    pdf = PDFInstitucional()
    pdf.add_page()
    pdf.set_margins(25, 20, 25)

    # Fecha estática requerida
    fecha_texto = "Mérida, Yucatán a 26 de Agosto de 2026"
    
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, fecha_texto, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Número de oficio: SE/DEE- USAER No. 02-E/132/25-26", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Asunto
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: COMISIÓN", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Destinatario con asignación dinámica de género
    cargo_directivo = "Directora" if "Mtra." in datos["director"] else "Director"

    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, datos["director"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"{cargo_directivo} de la Esc. Primaria", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f'"{datos["escuela"]}"', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "PRESENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Cuerpo del oficio
    pdf.set_font("helvetica", size=11)
    texto_cuerpo = (
        f"Por este medio le comunico que {datos['prefijo']} de apoyo {nombre.upper()}, "
        "asistirá a una Junta Académica convocada por la Dirección de la USAER 02-E, "
        "con clave de C.T. 31FUA0002Y, para tratar asuntos relacionados con el servicio de "
        "apoyo que se brinda a la escuela primaria que tiene a su cargo; el día 28 de Agosto "
        "de 2026 en su horario laboral.\n\n"
        "Agradeciendo la atención a la presente, aprovecho la ocasión para enviarle un cordial saludo."
    )
    pdf.multi_cell(0, 6, texto_cuerpo, align="J")
    pdf.ln(20)

    # Firma
    pdf.cell(0, 5, "ATTE.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.cell(0, 5, "________________________________________", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Mtro. Edgar Adrian Yam Briceño", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, "Director de la USAER No. 02-E", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    # Copia a archivo
    pdf.set_font("helvetica", size=8)
    pdf.cell(0, 5, "C.c.p. Archivo de la USAER No. 02-E", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

# Interfaz Visual Amigable
st.title("📄 Oficios de Comisión")
st.markdown("### ¡Hola! 👋 Bienvenida/o al portal de la USAER 02-E.")
st.write("Genera tu oficio de comisión en un par de clics y sin fricciones burocráticas. Solo selecciona tu nombre, verifica tus datos y descarga tu documento listo para imprimir para nuestra junta del viernes.")

st.divider()

docente_seleccionado = st.selectbox(
    "🔍 Busca tu nombre en la lista:", 
    [""] + list(personal.keys()),
    help="Puedes escribir tu nombre o buscarlo desplegando la lista."
)

if docente_seleccionado:
    datos = personal[docente_seleccionado]
    primer_nombre = docente_seleccionado.split()[0]
    
    st.success(f"¡Hola, {primer_nombre}! Hemos preparado tu formato. Por favor confirma tus datos:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🏫 **Escuela asignada:**\n\n{datos['escuela']}")
    with col2:
        cargo_display = "Directora" if "Mtra." in datos["director"] else "Director"
        st.info(f"👤 **{cargo_display}:**\n\n{datos['director']}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    pdf_bytes = generar_pdf(docente_seleccionado, datos)
    
    st.markdown("<h4 style='text-align: center;'>Tu archivo está listo 👇</h4>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
    with col_btn2:
        if st.download_button(
            label="📥 Descargar Documento PDF",
            data=pdf_bytes,
            file_name=f"Comision_USAER_{docente_seleccionado.replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        ):
            st.balloons()
