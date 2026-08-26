import streamlit as st
from fpdf import FPDF
import datetime

# Configuración de la página
st.set_page_config(page_title="Comisiones USAER 02-E", page_icon="📄", layout="centered")

# Base de datos unificada de escuelas, directores y prefijo de género
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

def generar_pdf(nombre, datos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(25, 25, 25)

    # Fecha de emisión automática
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = datetime.date.today()
    fecha_texto = f"Mérida, Yucatán a {hoy.day:02d} de {meses[hoy.month - 1]} de {hoy.year}"

    # Encabezado
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, fecha_texto, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Número de oficio: SE/DEE- USAER No. 02-E/001/26-27", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Asunto
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: COMISIÓN", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Destinatario
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, datos["director"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Director(a) de la Esc. Primaria", new_x="LMARGIN", new_y="NEXT")
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

    # Firma de la Dirección
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

    return pdf.output()

# Interfaz web
st.title("Generador de Oficios de Comisión")
st.subheader("USAER 02-E")
st.write("Selecciona tu nombre de la lista para generar y descargar tu oficio de comisión en formato PDF para la junta del viernes 28 de agosto.")

docente_seleccionado = st.selectbox("Nombre del personal:", [""] + list(personal.keys()))

if docente_seleccionado:
    datos = personal[docente_seleccionado]
    st.info(f"**Escuela asignada:** {datos['escuela']}\n\n**A la atención de:** {datos['director']}")
    
    pdf_bytes = generar_pdf(docente_seleccionado, datos)
    
    st.download_button(
        label="📄 Descargar Oficio de Comisión",
        data=pdf_bytes,
        file_name=f"Comision_28_Ago_{docente_seleccionado.replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary"
    )