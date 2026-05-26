import streamlit as st
import pandas as pd
import unicodedata
import os
import io

#ESTE ES EL BUENO!!!


#   1. Configuración
st.set_page_config(page_title="Inventario Médico", layout="wide")
st.markdown("""
<style>

/* ===== APP ===== */
.stApp{
    background:
    radial-gradient(circle at top left, #1e3a8a 0%, transparent 25%),
    radial-gradient(circle at bottom right, #0f172a 0%, transparent 30%),
    linear-gradient(135deg,#020617 0%,#0f172a 100%);
    color:white;
    font-family: 'Inter', sans-serif;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"]{
    background: rgba(15,23,42,0.85);
    backdrop-filter: blur(20px);
    border-right:1px solid rgba(255,255,255,0.06);
}

/* ===== SIDEBAR TEXTO ===== */
section[data-testid="stSidebar"] *{
    color:white;
}

/* ===== TITULOS ===== */
h1,h2,h3{
    color:white !important;
    font-weight:700;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input{
    background: rgba(255,255,255,0.04)!important;
    border:1px solid rgba(255,255,255,0.08)!important;
    border-radius:18px!important;
    color:white!important;
    padding:12px!important;
}

/* ===== SELECT ===== */
div[data-baseweb="select"] > div{
    background: rgba(255,255,255,0.04)!important;
    border-radius:18px!important;
    border:1px solid rgba(255,255,255,0.08)!important;
}

/* ===== BOTONES ===== */
.stButton > button{
    width:100%;
    background:linear-gradient(135deg,#2563eb,#3b82f6);
    border:none;
    color:white;
    border-radius:18px;
    padding:14px;
    font-size:16px;
    font-weight:700;
    transition:0.3s;
    box-shadow:0px 8px 30px rgba(37,99,235,0.35);
}

/* ===== HOVER ===== */
.stButton > button:hover{
    transform:translateY(-3px);
    box-shadow:0px 12px 35px rgba(37,99,235,0.55);
}

/* ===== CARDS ===== */
.card{
    background: rgba(15,23,42,0.72);
    border:1px solid rgba(255,255,255,0.06);
    backdrop-filter:blur(20px);
    border-radius:28px;
    padding:35px;
    box-shadow:0px 15px 40px rgba(0,0,0,0.35);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
}

.card h2{
    color:white!important;
    font-size:44px;
    margin-bottom:20px;
}

.card b,
.card{
    color:#cbd5e1!important;
    font-size:18px;
}

/* ===== METRICS ===== */
[data-testid="metric-container"]{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.06);
    padding:28px;
    border-radius:24px;
    backdrop-filter:blur(18px);
    box-shadow:0px 10px 35px rgba(0,0,0,0.28);
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"]{
    border-radius:24px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,0.06);
}

/* ===== ALERTS ===== */
.stAlert{
    border-radius:20px;
}

/* ===== IMAGENES ===== */
img{
    border-radius:24px;
}

/* ===== SCROLL ===== */
::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#2563eb;
    border-radius:20px;
}

::-webkit-scrollbar-track{
    background:#0f172a;
}

/* ===== ANIMACIÓN ===== */
.block-container{
    animation:fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(12px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)




col_logo1, col_logo2 = st.columns([8,1])

with col_logo2:
    st.image("logo.png", width=90)



# 1.1 Titulo de la interfaz: 
st.markdown("""
<div style="
padding:35px;
border-radius:28px;
background: linear-gradient(
135deg,
rgba(37,99,235,0.18),
rgba(15,23,42,0.85)
);
border:1px solid rgba(255,255,255,0.08);
backdrop-filter: blur(18px);
margin-bottom:30px;
box-shadow: 0px 10px 40px rgba(0,0,0,0.35);
">

<h1 style="
margin-bottom:5px;
font-size:55px;
font-weight:800;
color:white;
">
🩺 VitaCore OS
</h1>

<p style="
font-size:22px;
color:#93c5fd;
margin-bottom:18px;
">
Plataforma Inteligente de Gestión Biomédica
</p>

<div style="
display:flex;
gap:12px;
flex-wrap:wrap;
">

<div style="
background:rgba(255,255,255,0.06);
padding:10px 18px;
border-radius:14px;
color:#cbd5e1;
font-size:15px;
">
Inventario
</div>

<div style="
background:rgba(255,255,255,0.06);
padding:10px 18px;
border-radius:14px;
color:#cbd5e1;
font-size:15px;
">
Mantenimientos
</div>

<div style="
background:rgba(255,255,255,0.06);
padding:10px 18px;
border-radius:14px;
color:#cbd5e1;
font-size:15px;
">
QR Inteligente
</div>

<div style="
background:rgba(255,255,255,0.06);
padding:10px 18px;
border-radius:14px;
color:#cbd5e1;
font-size:15px;
">
Cloud Access
</div>

</div>

</div>
""", unsafe_allow_html=True)



#   2. Cargar la base de datos: 
df = pd.read_csv("INVENTARIO.csv")

query = st.query_params

query = st.query_params

codigo_qr = query.get("codigo")

if codigo_qr:

    equipo_qr = df[df["codigo"].astype(str) == str(codigo_qr)]

    if not equipo_qr.empty:

        equipo = equipo_qr.iloc[0]

        # ===== BUSCAR IMAGEN =====
        ruta_img = None

        for ext in ["jpg", "jpeg", "png"]:

            posible_ruta = f"imagenes/{codigo_qr}.{ext}"

            if os.path.exists(posible_ruta):
                ruta_img = posible_ruta
                break

        # ===== INTERFAZ QR =====
        st.markdown(f"""
        <div class="card">

        <h1> {equipo['nombre']}</h1>

        <p style="color:#94a3b8;font-size:18px;">
        Información biomédica del equipo
        </p>

        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1,2])

        with col1:

            if ruta_img:
                st.image(ruta_img, use_container_width=True)

            else:
                st.warning("Imagen no disponible")

        with col2:

            estado = equipo.get("estado del equipo", "")

            if estado == "Operativo":
                color_estado = "#22c55e"

            elif estado == "Mantenimiento":
                color_estado = "#facc15"

            else:
                color_estado = "#ef4444"

            st.markdown(f"""
            <div class="card">

            <h2>{equipo.get('nombre','')}</h2>

            <b>Código:</b> {equipo.get('codigo','')} <br>
            <b>Área:</b> {equipo.get('area','')} <br>
            <b>Marca:</b> {equipo.get('marca','')} <br>
            <b>Modelo:</b> {equipo.get('modelo','')} <br>
            <b>Serie:</b> {equipo.get('no. serie','')} <br>
            <b>Ubicación:</b> {equipo.get('ubicacion','')} <br>

            <p>
            <b>Estado:</b>
            <span style="
            color:{color_estado};
            font-weight:bold;
            ">
            ● {estado}
            </span>
            </p>

            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("Equipo no encontrado")

    st.stop()

#   2.1. Limpieza de las columnas para evitar errores ortograficos: 
def limpiar(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

df.columns = [limpiar(col) for col in df.columns]

#   2.2 Eliminar columnas duplicadas: 
df = df.loc[:, ~df.columns.duplicated()]

st.sidebar.markdown("""
<div style='
text-align:center;
padding:25px 10px;
margin-bottom:20px;
background:rgba(255,255,255,0.04);
border-radius:22px;
border:1px solid rgba(255,255,255,0.06);
'>

<h1 style='
margin-bottom:0px;
font-size:36px;
'>
🩺
</h1>

<h2 style='
margin-top:8px;
margin-bottom:5px;
font-size:24px;
'>
VitaCore
</h2>

<p style='
font-size:14px;
color:#94a3b8;
'>
Gestión Biomédica Inteligente
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

#   3. Creación de menú desplegable: 
opcion = st.sidebar.selectbox(
    "Selecciona una opción: ",
    [
        "Inicio",
        "📋 Ver Inventario Completo",
        "🔍 Buscar Equipo por Código",
        "🏥 Filtrar por Área",
        "🗂 Mantenimientos Realizados",
        "➕ Agregar Nuevo Equipo",
        "🔧 Registrar Mantenimiento",
        "📸 Identificación de Equipos",
        "📱 QR por Equipo",
        "🗑 Dar de Baja Equipo",
        "Salir"
    ]
)


# ===== ALERTAS DE MANTENIMIENTO =====
from datetime import datetime

hoy = datetime.now().date()

equipos_vencidos = 0

if os.path.exists("MANTENIMIENTOS.csv"):

    df_alertas = pd.read_csv("MANTENIMIENTOS.csv")

    df_alertas.columns = [limpiar(col) for col in df_alertas.columns]

    if "proximo mantenimiento" in df_alertas.columns:

        fechas = pd.to_datetime(
            df_alertas["proximo mantenimiento"],
            errors="coerce"
        ).dt.date

        equipos_vencidos = (fechas < hoy).sum()


#   4. Despliegue de interfaz: 
if opcion == "Inicio":

    st.markdown("""
<div class="card">

<h1 style="margin-bottom:8px;">
¡Bienvenido a VitaCore!
</h1>

<p style="
font-size:20px;
color:#94a3b8;
">
Sistema avanzado para gestión biomédica hospitalaria.
Administra inventario, mantenimientos y trazabilidad QR desde cualquier dispositivo.
</p>

</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Equipos registrados", len(df))

    with col2:
        st.metric("🏥 Áreas hospitalarias", df["area"].nunique())

    with col3:
        st.metric("🔧 Mantenimientos", 
        len(pd.read_csv("MANTENIMIENTOS.csv")) if os.path.exists("MANTENIMIENTOS.csv") else 0) 
        
        with col4: 
            st.metric(
        "⚠️ Pendientes",
        equipos_vencidos
    )
        
    st.markdown("---")

    st.info("""
Este sistema permite:
- Gestión de inventario médico.
- Registro de mantenimientos.
- Consulta rápida mediante QR.
- Acceso remoto desde dispositivos móviles.
""")
    
# 4.1 Opción 1: Ver inventario Completo: 
elif opcion == "📋 Ver Inventario Completo":
    st.subheader("📋 Inventario completo")
    st.dataframe(df, use_container_width=True)


# 4.2 Opción 2: Buscar equipo mediante código establecido en la base de datos:
elif opcion == "🔍 Buscar Equipo por Código":
    st.subheader("🔍 Buscar equipo por código")

    codigo = st.text_input("Ingresa el Código")

    if codigo:
        resultado = df[df["codigo"].astype(str).str.lower() == codigo.lower()]
        
        if not resultado.empty:
            st.success(" ¡Equipo encontrado! ")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.error(" ¡Equipo NO encontrado! ")
            
            
# 4.3 Opción 3: Visualización por área: 
elif opcion == "🏥 Filtrar por Área":
    st.markdown("## 🏥 Filtrar por Área: ")

    area = st.selectbox("Selecciona un Área", df["area"].dropna().unique())

    filtrado = df[df["area"] == area]

    st.dataframe(filtrado, use_container_width=True)
    
    
# 4.4 Ver mantenimientos
elif opcion == "🗂 Mantenimientos Realizados":
    st.subheader("🗂 Historial de Mantenimientos")

    ruta_mant = "MANTENIMIENTOS.csv"

    if os.path.exists(ruta_mant): 
        df_mant = pd.read_csv(ruta_mant)

        df_mant.columns = [limpiar(col) for col in df_mant.columns]

        df_mant = df_mant.loc[:, ~df_mant.columns.duplicated()]

       
        df_mant = df_mant.dropna(how="all")

        st.dataframe(df_mant, use_container_width=True)

    else:
        st.warning("¡No hay mantenimientos registrados aún!")
    

# 4.5 Opción 4: Añadir nuevos equipos a la lista predeterminada de 10 por área:
elif opcion == "➕ Agregar Nuevo Equipo":
    st.subheader("Agregar nuevo equipo")
    st.info("""
📌 Instrucciones:
- Completa todos los campos obligatorios (no dejes espacio vacíos). 
- Utiliza un código distinto a nuevas adiciones. 
- El registro debe empezar con una letras MAYUS (Ej: Equipo (bien), EQUIPO (incorrecto) ).
""")

    codigo = st.text_input("Código:")
    area = st.text_input("Área:")
    nombre = st.text_input("Nombre del equipo:")
    marca = st.text_input("Marca:")
    modelo = st.text_input("Modelo:")
    serie = st.text_input("Número de serie (3 letras MAYUS - 8 digitos):")
    ubicacion = st.text_input("Ubicación")
    adquisicion = st.text_input("Adquisición (Usa guiones (-) entre numeros (aaaa-mm-dd) ):")
    anio = st.number_input("Año:", min_value=2000, max_value=2100)
    garantia = st.selectbox(
    "Garantía:",
    ["Sí", "No"])
    estado = st.selectbox("Estado:", ["Operativo", "Mantenimiento", "Fuera de servicio"])
    bateria = st.selectbox(
    "Batería:",
    ["Sí", "No"])
    accesorios = st.text_input("Accesorios:") 
    imagen = st.camera_input("📸 Tomar foto del equipo")

    if st.button("Guardar equipo"):
        nuevo = pd.DataFrame([{
            "codigo": codigo,
            "area": area,
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "no. serie": serie,
            "ubicacion": ubicacion,
            "adquisicion": adquisicion,
            "ano": anio,
            "garantia": garantia,
            "estado del equipo": estado,
            "bateria": bateria, 
            "accesorios": accesorios
            
        }])

        nuevo.columns = [limpiar(col) for col in nuevo.columns]

        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("INVENTARIO.csv", index=False, encoding="utf-8-sig") 
        if imagen is not None: 
            os.makedirs("imagenes", exist_ok=True) 
            with open(f"imagenes/{codigo}.jpg", "wb") as f: 
                f.write(imagen.getbuffer())
        st.success("¡Equipo agregado correctamente!")
        

#  4.6 Opción 5: Registro de nuevos mantenimientos: 
elif opcion == "🔧 Registrar Mantenimiento":
    st.subheader("Registro de mantenimiento")

    ruta_mant = "MANTENIMIENTOS.csv"

    control = st.text_input("Control:")
    fecha = st.text_input("Fecha (aaaa/mm/dd):")
    tipo = st.selectbox("Tipo:", ["Preventivo", "Correctivo"])
    descripcion = st.text_area("Descripción:")
    actividad = st.text_area("Actividad:")
    responsable = st.text_input("Responsable:")
    estado = st.selectbox("Estado:", ["Operativo", "En mantenimiento"])
    proximo = st.text_input("Próximo mantenimiento:")

    if st.button("Guardar mantenimiento"):

        if not control.strip() or not descripcion.strip() or not actividad.strip():
            st.error("¡Completa los campos obligatorios!")

        else:
            nuevo_mant = pd.DataFrame([{
                "control": control,
                "fecha": fecha,
                "tipo de mantenimiento": tipo,
                "descripcion del problema": descripcion,
                "actividad realizada": actividad,
                "responsable": responsable,
                "estado": estado,
                "proximo mantenimiento": proximo
            }])

            columnas_correctas = [
                "control",
                "fecha",
                "tipo de mantenimiento",
                "descripcion del problema",
                "actividad realizada",
                "responsable",
                "estado",
                "proximo mantenimiento"
            ]

            if os.path.exists(ruta_mant):
                df_mant = pd.read_csv(ruta_mant)
                df_mant.columns = [limpiar(col) for col in df_mant.columns] 
                df_mant = df_mant.rename(columns={
    "proximo matenimiento": "proximo mantenimiento",
    "próximo mantenimiento": "proximo mantenimiento"
})
                df_mant.columns = [limpiar(col) for col in df_mant.columns]
                df_mant = df_mant.loc[:, ~df_mant.columns.duplicated()]
            else:
                df_mant = pd.DataFrame(columns=columnas_correctas)

            df_mant = df_mant.reindex(columns=columnas_correctas)
            nuevo_mant = nuevo_mant.reindex(columns=columnas_correctas)

            df_mant = pd.concat([df_mant, nuevo_mant], ignore_index=True)

            df_mant.to_csv(ruta_mant, index=False, encoding="utf-8-sig")

            st.success("¡Mantenimiento registrado correctamente!")

            st.rerun()



# 4.7 Identificación visual de equipos
elif opcion == "📸 Identificación de Equipos":

    st.subheader("📸 Identificación Visual de Equipos")

    equipo_select = st.selectbox(
        "Selecciona un equipo:",
        df["codigo"]
    )

    datos = df[df["codigo"] == equipo_select].iloc[0]

    ruta_img = None

    for ext in ["jpg", "jpeg", "png"]:

        posible_ruta = f"imagenes/{equipo_select}.{ext}"

        if os.path.exists(posible_ruta):
            ruta_img = posible_ruta
            break

    col1, col2 = st.columns([1,2])

    with col1:

        if ruta_img:
            st.image(ruta_img, use_container_width=True)

        else:
            st.warning("No hay imagen disponible")

    with col2:

        estado = datos['estado del equipo']

        if estado == "Operativo":
            color_estado = "#22c55e"

        elif estado == "Mantenimiento":
            color_estado = "#facc15"

        else:
            color_estado = "#ef4444"

        st.markdown(f"""
        <div class="card">

        <h2>{datos['nombre']}</h2>

        <b>Código:</b> {datos['codigo']} <br>
        <b>Área:</b> {datos['area']} <br>
        <b>Marca:</b> {datos['marca']} <br>
        <b>Modelo:</b> {datos['modelo']} <br>

        <p>
        <b>Estado:</b>
        <span style="
        color:{color_estado};
        font-weight:bold;
        ">
        ● {estado}
        </span>
        </p>

        </div>
        """, unsafe_allow_html=True)


# 4.8 QR por equipo
elif opcion == "📱 QR por Equipo":

    st.subheader("📱 QR de Equipos")

    equipo_select = st.selectbox(
        "Selecciona un equipo:",
        df["codigo"]
    )

    ruta_qr = f"qr/{equipo_select}.png"

    datos = df[df["codigo"] == equipo_select].iloc[0]

    col1, col2 = st.columns([1,2])

    with col1:

        if os.path.exists(ruta_qr):

            st.image(ruta_qr, width=300)

            with open(ruta_qr, "rb") as file:

                st.download_button(
                    label="📥 Descargar QR",
                    data=file,
                    file_name=f"{equipo_select}_QR.png",
                    mime="image/png"
                )

        else:
            st.warning("QR no encontrado")

        st.markdown("### 📤 Subir nuevo QR")

        modo_edicion = st.toggle("✏️ Editar QR")

        if modo_edicion:

            qr_manual = st.file_uploader(
                "Sube un QR manual",
                type=["png", "jpg", "jpeg"],
                key="qr_upload"
            )

            if qr_manual is not None:

                os.makedirs("qr", exist_ok=True)

                with open(ruta_qr, "wb") as f:
                    f.write(qr_manual.getbuffer())

                st.success("✅ QR actualizado correctamente")

                st.rerun()

    with col2:

        st.markdown(f"""
        <div class="card">

        <h2>{datos['nombre']}</h2>

        <b>Código:</b> {datos['codigo']} <br>
        <b>Área:</b> {datos['area']} <br>
        <b>Marca:</b> {datos['marca']} <br>
        <b>Modelo:</b> {datos['modelo']}

        </div>
        """, unsafe_allow_html=True)

# 4.9 Dar de baja equipo
elif opcion == "🗑 Dar de Baja Equipo":

    st.subheader("🗑 Dar de Baja Equipo")

    equipo_select = st.selectbox(
        "Selecciona el equipo:",
        df["codigo"]
    )

    datos = df[df["codigo"] == equipo_select].iloc[0]

    st.markdown(f"""
    <div class="card">

    <h2>{datos['nombre']}</h2>

    <b>Código:</b> {datos['codigo']} <br>
    <b>Área:</b> {datos['area']} <br>
    <b>Estado actual:</b> {datos['estado del equipo']}

    </div>
    """, unsafe_allow_html=True)

    motivo = st.text_area("Motivo de baja:")

    if st.button("Dar de baja"):

        df.loc[
            df["codigo"] == equipo_select,
            "estado del equipo"
        ] = "Baja definitiva"

        df.to_csv("INVENTARIO.csv", index=False, encoding="utf-8-sig")

        st.success("✅ Equipo dado de baja correctamente")

        st.rerun()


st.markdown("""
<hr>

<div style="
text-align:center;
padding:20px;
color:#64748b;
font-size:14px;
">

VitaCore • Plataforma Biomédica Inteligente  
Cloud Edition • 2026

</div>
""", unsafe_allow_html=True)


# 4.7 Opción : Salida del sistema: 
if opcion == "Salir":
    st.warning("🚪 ¡Saliendo del Sistema, vuelve pronto! ")