import streamlit as st
from fpdf import FPDF
import datetime
import os
import json

# --- 1. CONFIGURACIÓN DEL PORTAL ---
st.set_page_config(page_title="Portal USAER 02-E", page_icon="🏫", layout="centered")

hoy = datetime.date.today()
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
fecha_actual_texto = f"Mérida, Yucatán a {hoy.day:02d} de {meses[hoy.month - 1]} de {hoy.year}"

# --- 2. BASES DE DATOS ---
# Personal para Comisiones
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

# Escuelas para Asignaciones
escuelas = {
    "DAMIÁN CARMONA": {
        "cct": "31DPR0414P", "director": "Mtra. Maribel Vargas Arana", "direccion": "C.41 S/N X 4 Y 6 COL. MANUEL ÁVILA CAMACHO",
        "personal": [("Cindy Mayanín Burgos González", "Maestra de apoyo"), ("Psic. María José Cupul Realpozo", "Psicóloga"), ("Com. Elmy Lucelly Puerto Gone", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "ICHCAANZIHO": {
        "cct": "31DPR0232G", "director": "Mtra. Rennaty Maribel Puga Jimenez", "direccion": "C.44 S/N X 17 Y 25 JARDINES DE MERIDA",
        "personal": [("Marycruz Caamal Coral", "Maestra de apoyo"), ("María Cecilia Solís Vázquez", "Maestra de apoyo"), ("Psic. María José Cupul Realpozo", "Psicóloga"), ("Com. Elmy Lucelly Puerto Gone", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "GREGORIO TORRES QUINTERO": {
        "cct": "31DPR0466V", "director": "Mtro. Elmer Ariel Ontiveros Requena", "direccion": "C.35 Nº.353 X 22 COL. LÓPEZ MATEOS",
        "personal": [("Dolores Eugenia Cortázar Navarrete", "Maestra de apoyo"), ("Psic. Abril de María Chable Ríos", "Psicóloga"), ("Com. Marilyn Pérez Lizama", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "REMIGIO AGUILAR SOSA": {
        "cct": "31DPR0711P", "director": "Mtro. Carlos Esteban Heredia GCantón", "direccion": "C.145 S/N X 48 Y 50 SUR CINCO COLONIAS",
        "personal": [("Dianely de Sugeidy Caamal Tamay", "Maestra de apoyo"), ("Psic. Abril de María Chable Ríos", "Psicóloga"), ("Com. Marilyn Pérez Lizama", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "ELVIRA PARRA ÁVILA": {
        "cct": "31EPR0039A", "director": "Mtro. Manuel Jesús Alcocer Vázquez", "direccion": "C.20 S/N X 37 Y 39 COL. EMILIANO ZAPATA OTE.",
        "personal": [("Luis Jorge García Herrera", "Maestro de apoyo"), ("Psic. María José Cupul Realpozo", "Psicóloga"), ("Com. Elmy Lucelly Puerto Gone", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "MANUEL SARRADO": {
        "cct": "31EPR0040Q", "director": "Mtro. José Alberto Reyna Martínez", "direccion": "C.63 Nº532 X 64 Y 66 CENTRO",
        "personal": [("María del Rosario Pérez Vitorin", "Maestra de apoyo"), ("Psic. Abril de María Chable Ríos", "Psicóloga"), ("Com. Marilyn Pérez Lizama", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "DOMINGO SOLÍS RODRÍGUEZ": {
        "cct": "31EPR0075F", "director": "Mtra. Erika Basto Ek", "direccion": "C.52 Nº.555 X 73 Y 73 A CENTRO",
        "personal": [("Zuemmy del Carmen Pérez Basto", "Maestra de apoyo"), ("Psic. Abril de María Chable Ríos", "Psicóloga"), ("Com. Marilyn Pérez Lizama", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    },
    "QUINTANA ROO": {
        "cct": "31EPR0092W", "director": "Mtro. Jorge Adrián Cetina Cach", "direccion": "C. 158 No. 683 por 123 y 125 FRACC. LOS HÉROES",
        "personal": [("Pedro Manuel Torres May", "Maestro de apoyo"), ("Psic. María José Cupul Realpozo", "Psicóloga"), ("Com. Elmy Lucelly Puerto Gone", "Comunicación"), ("Mtro. Diego Peralta Torres", "Trabajo Social")]
    }
}

docentes = {
    "Cindy Mayanín Burgos González": {"escuela": "DAMIÁN CARMONA", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Marycruz Caamal Coral": {"escuela": "ICHCAANZIHO", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "María Cecilia Solís Vázquez": {"escuela": "ICHCAANZIHO", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Dolores Eugenia Cortázar Navarrete": {"escuela": "GREGORIO TORRES QUINTERO", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Dianely de Sugeidy Caamal Tamay": {"escuela": "REMIGIO AGUILAR SOSA", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Luis Jorge García Herrera": {"escuela": "ELVIRA PARRA ÁVILA", "titulo": "MAESTRO ESPECIALISTA", "rol_texto": "Maestro de Apoyo"},
    "María del Rosario Pérez Vitorin": {"escuela": "MANUEL SARRADO", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Zuemmy del Carmen Pérez Basto": {"escuela": "DOMINGO SOLÍS RODRÍGUEZ", "titulo": "MAESTRA ESPECIALISTA", "rol_texto": "Maestra de Apoyo"},
    "Pedro Manuel Torres May": {"escuela": "QUINTANA ROO", "titulo": "MAESTRO ESPECIALISTA", "rol_texto": "Maestro de Apoyo"}
}

# --- 3. MOTORES LÓGICOS ---
def obtener_folio(entidad, archivo_folios):
    if os.path.exists(archivo_folios):
        with open(archivo_folios, "r", encoding="utf-8") as f:
            try:
                folios = json.load(f)
            except json.JSONDecodeError:
                folios = {}
    else:
        folios = {}
    if entidad in folios:
        return folios[entidad]
    nuevo_folio = len(folios) + 1
    folios[entidad] = nuevo_folio
    with open(archivo_folios, "w", encoding="utf-8") as f:
        json.dump(folios, f, ensure_ascii=False, indent=4)
    return nuevo_folio

# Seguridad Comisiones
fechas_juntas = [datetime.date(2026, 8, 28)]
junta_activa = None
for fecha in fechas_juntas:
    if 0 <= (fecha - hoy).days <= 2:
        junta_activa = fecha
        break

# --- 4. PLANTILLA PDF ---
class PDFInstitucional(FPDF):
    def header(self):
        if os.path.exists("encabezado.png"):
            self.image("encabezado.png", x=10, y=10, w=190)
        self.set_y(45)

    def footer(self):
        self.set_y(-35)
        if os.path.exists("pie_pagina.png"):
            self.image("pie_pagina.png", x=10, y=self.get_y(), w=190)
            
    def insertar_firmas(self):
        self.cell(0, 5, "ATTE.", align="C", new_x="LMARGIN", new_y="NEXT")
        y_actual = self.get_y()
        if os.path.exists("firma.png"):
            self.image("firma.png", x=85, y=y_actual, w=40)
        if os.path.exists("sello.png"):
            self.image("sello.png", x=135, y=y_actual - 5, w=35)
        self.ln(25) 
        self.cell(0, 5, "________________________________________", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", style="B", size=11)
        self.cell(0, 5, "Psic. Edgar Adrián Yam Briceño MD", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", size=11)
        self.cell(0, 5, "Director de la USAER No. 02-E", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(15)
        self.set_font("helvetica", size=8)
        self.cell(0, 5, "C.c.p. Archivo de la USAER No. 02-E", new_x="LMARGIN", new_y="NEXT")

# --- 5. GENERADORES PDF ---
def generar_pdf_comision(nombre, datos, fecha_junta, folio_num):
    pdf = PDFInstitucional()
    pdf.add_page()
    pdf.set_margins(25, 20, 25)
    pdf.set_font("helvetica", size=11)
    fecha_emision = f"Mérida, Yucatán a {hoy.day:02d} de {meses[hoy.month - 1]} de {hoy.year}"
    fecha_reunion = f"{fecha_junta.day:02d} de {meses[fecha_junta.month - 1]} de {fecha_junta.year}"
    
    pdf.cell(0, 5, fecha_emision, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Número de oficio: SE/DEE- USAER No. 02-E/{folio_num:03d}/26-27", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: COMISIÓN", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    cargo = "Directora" if "Mtra." in datos["director"] else "Director"
    pdf.cell(0, 5, datos["director"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"{cargo} de la Esc. Primaria", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f'"{datos["escuela"]}"', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "PRESENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", size=11)
    texto = (
        f"Por este medio le comunico que {datos['prefijo']} de apoyo {nombre.upper()}, "
        f"asistirá a una Junta Académica convocada por la Dirección de la USAER 02-E, "
        f"con clave de C.T. 31FUA0002Y, para tratar asuntos relacionados con el servicio de "
        f"apoyo que se brinda a la escuela primaria que tiene a su cargo; el día {fecha_reunion} "
        f"en su horario laboral.\n\n"
        f"Agradeciendo la atención a la presente, aprovecho la ocasión para enviarle un cordial saludo."
    )
    pdf.multi_cell(0, 6, texto, align="J")
    pdf.ln(15)
    pdf.insertar_firmas()
    return bytes(pdf.output())

def pdf_asignacion_docente(nombre, info_docente, info_escuela):
    pdf = PDFInstitucional()
    pdf.add_page()
    pdf.set_margins(25, 20, 25)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, fecha_actual_texto, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: ASIGNACIÓN DE ESCUELA", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    prefijo = "MTRO." if "MAESTRO" in info_docente["titulo"] else "MTRA."
    pdf.cell(0, 5, f"{prefijo} {nombre.upper()}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"{info_docente['titulo']} DE LA USAER 02-E", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "PRESENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", size=11)
    texto = (
        f"Por medio de la presente me permito notificarle que ha sido asignada para prestar sus "
        f"servicios en el curso escolar 2026-2027 como {info_docente['rol_texto']} en la escuela primaria "
        f'"{info_docente["escuela"]}" con CCT {info_escuela["cct"]}, que se encuentra ubicado en la '
        f"{info_escuela['direccion'].lower()} con un horario de 7:00 a 12:00 hrs.\n\n"
        f"Sin más por el momento y esperando tenga usted un excelente desempeño en su labor "
        f"educativa agradezco la atención a la presente no sin antes enviarle un cordial saludo."
    )
    pdf.multi_cell(0, 6, texto, align="J")
    pdf.ln(15)
    pdf.insertar_firmas()
    return bytes(pdf.output())

def pdf_asignacion_director(nombre_escuela, info_escuela, folio_num):
    pdf = PDFInstitucional()
    pdf.add_page()
    pdf.set_margins(25, 20, 25)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 5, fecha_actual_texto, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Oficio No: SE/DEE- USAER No. 02-E/{folio_num:03d}/26-27", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 5, "Asunto: Se Informan Asignaciones", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    cargo = "Directora" if "Mtra." in info_escuela["director"] else "Director"
    pdf.cell(0, 5, info_escuela["director"].upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"{cargo} de la Esc. Primaria", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f'"{nombre_escuela}"', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "PRESENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 6, f"Por medio de la presente me permito informarle que durante el presente curso escolar 2026-2027, el personal que estará encargado de brindar el servicio de apoyo de la USAER 02-E en la escuela a su cargo es el que a continuación se nombra:\n", align="J")
    pdf.ln(5)
    
    pdf.set_font("helvetica", style="B", size=10)
    pdf.set_x(25)
    pdf.cell(100, 7, "PERSONAL DE LA USAER 02-E", border=1, align="C")
    pdf.cell(60, 7, "FUNCIÓN", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    for persona, funcion in info_escuela["personal"]:
        pdf.set_x(25)
        pdf.cell(100, 7, f"  {persona}", border=1)
        pdf.cell(60, 7, f"  {funcion}", border=1, new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(10)
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 6, "Sin más por el momento me despido de usted y agradezco el apoyo que siempre ha brindado al equipo de la USAER, reciba mis saludos cordiales.", align="J")
    pdf.ln(15)
    pdf.insertar_firmas()
    return bytes(pdf.output())

# --- 6. INTERFAZ GRÁFICA Y MENÚ LATERAL ---
st.sidebar.title("Menú USAER 02-E")
modulo = st.sidebar.radio("Selecciona una opción:", ["Asignaciones de Ciclo", "Comisiones a Juntas"])
st.sidebar.divider()
st.sidebar.info("Dirección USAER 02-E\n\nCiclo Escolar 2026-2027")

st.title("📄 Portal Operativo USAER 02-E")

if modulo == "Asignaciones de Ciclo":
    st.write("Genera tus documentos de inicio de ciclo escolar 2026-2027.")
    tab_docentes, tab_directores = st.tabs(["👩‍🏫 Asignaciones Docentes", "🏫 Oficios para Directores"])

    with tab_docentes:
        st.info("Este documento es tu notificación oficial de asignación de centro de trabajo.")
        seleccion_docente = st.selectbox("🔍 Selecciona tu nombre:", [""] + list(docentes.keys()), key="sb_docentes")
        if seleccion_docente:
            info_doc, info_esc = docentes[seleccion_docente], escuelas[docentes[seleccion_docente]["escuela"]]
            st.success(f"🏫 **Escuela:** {info_doc['escuela']} | 📍 **CCT:** {info_esc['cct']}")
            pdf_bytes = pdf_asignacion_docente(seleccion_docente, info_doc, info_esc)
            st.download_button("📥 Descargar Oficio de Asignación", data=pdf_bytes, file_name=f"Asignacion_{seleccion_docente.replace(' ', '_')}.pdf", mime="application/pdf", type="primary", use_container_width=True)

    with tab_directores:
        st.info("Detalla a los directores de primaria la plantilla de la USAER 02-E asignada.")
        seleccion_escuela = st.selectbox("🔍 Selecciona la escuela primaria:", [""] + list(escuelas.keys()), key="sb_escuelas")
        if seleccion_escuela:
            folio_escuela = obtener_folio(seleccion_escuela, "folios_directores.json")
            info_esc = escuelas[seleccion_escuela]
            st.success(f"A la atención de: **{info_esc['director']}**")
            pdf_bytes = pdf_asignacion_director(seleccion_escuela, info_esc, folio_escuela)
            st.download_button(f"📥 Descargar Oficio (Folio {folio_escuela:03d})", data=pdf_bytes, file_name=f"Oficio_Director_{seleccion_escuela.replace(' ', '_')}.pdf", mime="application/pdf", type="primary", use_container_width=True)

elif modulo == "Comisiones a Juntas":
    if junta_activa:
        fecha_format = f"{junta_activa.day:02d} de {meses[junta_activa.month - 1]}"
        st.info(f"🔓 **Sistema Habilitado:** Junta académica del {fecha_format}.")
        docente_seleccionado = st.selectbox("🔍 Busca tu nombre:", [""] + list(personal.keys()), key="sb_comisiones")
        if docente_seleccionado:
            folio_asignado = obtener_folio(docente_seleccionado, "folios_comisiones.json")
            datos = personal[docente_seleccionado]
            st.success(f"🏫 **Escuela:** {datos['escuela']} | 👤 **Atención a:** {datos['director']}")
            pdf_bytes = generar_pdf_comision(docente_seleccionado, datos, junta_activa, folio_asignado)
            st.download_button(f"📥 Descargar Oficio (Folio {folio_asignado:03d})", data=pdf_bytes, file_name=f"Comision_{docente_seleccionado.replace(' ', '_')}.pdf", mime="application/pdf", type="primary", use_container_width=True)
    else:
        st.error("🔒 **Generador Bloqueado**")
        st.write("El sistema de comisiones actualmente se encuentra inactivo. Los oficios únicamente pueden generarse 48 horas antes de una junta académica oficial.")
