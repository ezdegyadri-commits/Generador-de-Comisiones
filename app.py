import streamlit as st
from fpdf import FPDF
import datetime
import os
import json

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

# 1. MOTOR DE SEGURIDAD: Calendario de Juntas
fechas_juntas = [
    datetime.date(2026, 8, 28)
]

hoy = datetime.date.today()
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

junta_activa = None
for fecha in fechas_juntas:
    diferencia = (fecha - hoy).days
    if 0 <= diferencia <= 2:
        junta_activa = fecha
        break

# 2. MOTOR DE FOLIOS CORRELATIVOS
def obtener_folio(nombre):
    archivo_folios = "folios.json"
    
    if os.path.exists(archivo_folios):
        with open(archivo_folios, "r", encoding="utf-8") as f:
            try:
                folios_historial = json.load(f)
            except json.JSONDecodeError:
                folios_historial = {}
    else:
        folios_historial = {}

    if nombre in folios_historial:
        return folios_historial[nombre]
    
    nuevo_folio = len(folios_historial) + 1
    folios_historial[nombre] = nuevo_folio
    
    with open(archivo_folios, "w", encoding="utf-8") as f:
        json.dump(folios_historial, f, ensure_ascii=False, indent=4)
        
    return nuevo_folio

# 3. PLANTILLA INSTITUCIONAL PDF
class PDFInstitucional(FPDF):
    def header(self):
        if os.path.exists("encabezado.png"):
            self.image("encabezado.png", x=10, y=10, w=190)
        self.set_y(45)

    def footer(self):
        self.set_y(-35)
        if os.path.exists("pie_pagina.png"):
            self.image("pie_pagina.png", x=10, y=self.get_y(), w=190)

def generar_pdf(nombre, datos, fecha_junta, folio_num):
    pdf = PDFInstitucional()
    pdf.add_page()
    pdf.set_margins(25, 20, 25)

    folio_str = f"{folio_num:03d}"
    
    fecha_emision_texto = f"Mérida, Yucatán a {hoy.day:02d} de {meses[hoy.month - 1]} de {hoy.year}"
    fecha_reunion_texto = f"{fecha_junta.day:02d} de {meses[fecha_junta.month - 1]} de {fecha_junta.year}"
    
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, fecha_emision_texto, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Número de oficio: SE/DEE- USAER No. 02-E/{folio_str}/26-27", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: COMISIÓN", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    cargo_directivo = "Directora" if "Mtra." in datos["director"] else "Director"

    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, datos["director"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"{cargo_directivo} de la Esc. Primaria", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f'"{datos["escuela"]}"', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "PRESENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # LA SOLUCIÓN: Agregué la "f" al inicio de todas las líneas del párrafo para que procese correctamente la fecha
    pdf.set_font("helvetica", size=11)
    texto_cuerpo = (
        f"Por este medio le comunico que {datos['prefijo']} de apoyo {nombre.upper()}, "
        f"asistirá a una Junta Académica convocada por la Dirección de la USAER 02-E, "
        f"con clave de C.T. 31FUA0002Y, para tratar asuntos relacionados con el servicio de "
        f"apoyo que se brinda a la escuela primaria que tiene a su cargo; el día {fecha_reunion_texto} "
        f"en su horario laboral.\n\n"
        f"Agradeciendo la atención a la presente, aprovecho la ocasión para enviarle un cordial saludo."
    )
    pdf.multi_cell(0, 6, texto_cuerpo, align="J")
    pdf.ln(15)

    # Bloque de Firma y Sello
    pdf.cell(0, 5, "ATTE.", align="C", new_x="LMARGIN", new_y="NEXT")
    
    y_actual = pdf.get_y()
    
    if os.path.exists("firma.png"):
        pdf.image("firma.png", x=85, y=y_actual, w=40)
        
    if os.path.exists("sello.png"):
        pdf.image("sello.png", x=135, y=y_actual - 5, w=35)
        
    pdf.ln(25) 
    
    pdf.cell(0, 5, "________________________________________", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", style="B", size=11)
    
    pdf.cell(0, 5, "Psic. Edgar Adrián Yam Briceño MD", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, "Director de la USAER No. 02-E", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    pdf.set_font("helvetica", size=8)
    pdf.cell(0, 5, "C.c.p. Archivo de la USAER No. 02-E", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

# 4. INTERFAZ GRÁFICA
st.title("📄 Oficios de Comisión")
st.markdown("### ¡Hola! 👋 Bienvenida/o al portal de la USAER 02-E.")

st.divider()

if junta_activa:
    fecha_format = f"{junta_activa.day:02d} de {meses[junta_activa.month - 1]}"
    st.info(f"🔓 **Sistema Habilitado:** Junta académica del {fecha_format}.")
    
    docente_seleccionado = st.selectbox(
        "🔍 Busca tu nombre en la lista para generar tu oficio:", 
        [""] + list(personal.keys()),
        help="Puedes escribir tu nombre o buscarlo desplegando la lista."
    )

    if docente_seleccionado:
        folio_asignado = obtener_folio(docente_seleccionado)
        
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
        
        pdf_bytes = generar_pdf(docente_seleccionado, datos, junta_activa, folio_asignado)
        
        st.markdown("<h4 style='text-align: center;'>Tu archivo está listo 👇</h4>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
        with col_btn2:
            if st.download_button(
                label=f"📥 Descargar Oficio (Folio {folio_asignado:03d})",
                data=pdf_bytes,
                file_name=f"Comision_USAER_{docente_seleccionado.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            ):
                st.balloons()
else:
    st.error("🔒 **Generador Bloqueado**")
    st.write("El sistema de comisiones actualmente se encuentra inactivo. Los oficios únicamente pueden generarse 48 horas antes de una junta académica oficial autorizada por la Dirección.")
