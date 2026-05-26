import streamlit as st
import pandas as pd
import unicodedata
import os

#ESTE ES EL BUENO!!!


#   1. Configuración
st.set_page_config(page_title="Inventario Médico", layout="wide")
st.markdown("""
<style>

/* Fondo general */
.main {
    background-color: #f5f7fa;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* Texto sidebar */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Tarjetas */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

/* Botones */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    border-radius: 10px;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Títulos */
h1, h2, h3 {
    color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

# 1.1 Titulo de la interfaz: 
st.markdown("""
<h1 style='text-align: center; color:#2563eb;'>
🏥 Sistema Inteligente de Inventario Médico
</h1>
<p style='text-align:center; color:gray;'>
Gestión • Mantenimiento • Trazabilidad • QR
</p>
<hr>
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

        st.title(f"📄 {equipo['nombre']}")

        st.subheader("Información del equipo")

        st.write(f"**Código:** {equipo.get('codigo', '')}")
        st.write(f"**Área:** {equipo.get('area', '')}")
        st.write(f"**Nombre:** {equipo.get('nombre', '')}")
        st.write(f"**Marca:** {equipo.get('marca', '')}")
        st.write(f"**Modelo:** {equipo.get('modelo', '')}")
        st.write(f"**No. Serie:** {equipo.get('no. serie', '')}")
        st.write(f"**Ubicación:** {equipo.get('ubicacion', '')}")
        st.write(f"**Adquisición:** {equipo.get('adquisicion', '')}")
        st.write(f"**Año:** {equipo.get('ano', '')}")
        st.write(f"**Garantía:** {equipo.get('garantia', '')}")
        st.write(f"**Estado del equipo:** {equipo.get('estado del equipo', '')}")
        st.write(f"**Batería:** {equipo.get('bateria', '')}")
        st.write(f"**Accesorios:** {equipo.get('accesorios', '')}")

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


#   4. Despliegue de interfaz: 
if opcion == "Inicio":

    st.markdown("## 👋 Bienvenido al sistema")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📋 Equipos registrados", len(df))

    with col2:
        st.metric("🏥 Áreas hospitalarias", df["area"].nunique())

    with col3:
        st.metric("🔧 Mantenimientos", 
        len(pd.read_csv("MANTENIMIENTOS.csv")) if os.path.exists("MANTENIMIENTOS.csv") else 0)

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

        # 🔥 eliminar duplicadas
        df_mant = df_mant.loc[:, ~df_mant.columns.duplicated()]

        # 🔥 eliminar basura
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
    garantia = st.text_input("Garantía:")
    estado = st.selectbox("Estado:", ["Operativo", "Mantenimiento", "Fuera de servicio"])
    bateria = st.text_input("Batería:")
    accesorios = st.text_input("Accesorios:")

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

    ruta_img = f"imagenes/{equipo_select}.jpg"

    col1, col2 = st.columns([1,2])

    with col1:

        if os.path.exists(ruta_img):
            st.image(ruta_img, use_container_width=True)
        else:
            st.warning("No hay imagen disponible")

    with col2:

        st.markdown(f"""
        <div class="card">

        <h2>{datos['nombre']}</h2>

        <b>Código:</b> {datos['codigo']} <br>
        <b>Área:</b> {datos['area']} <br>
        <b>Marca:</b> {datos['marca']} <br>
        <b>Modelo:</b> {datos['modelo']} <br>
        <b>Estado:</b> {datos['estado del equipo']}

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
        else:
            st.warning("QR no encontrado")

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


# 4.7 Opción : Salida del sistema: 
if opcion == "Salir":
    st.warning("🚪 ¡Saliendo del Sistema, vuelve pronto! ")