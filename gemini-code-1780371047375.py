import streamlit as st
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Dashboard Suelos Bolivia", layout="wide")

st.title("Dashboard de Fertilidad de Suelos - Bolivia")
st.write("Basado en parametros de Chilon y UMSA")

# 1. ENTRADA DE DATOS (SIDEBAR)
st.sidebar.header("Datos de Laboratorio")
cultivo = st.sidebar.selectbox("Seleccione Cultivo", ["Papa", "Quinua", "Cebada", "Haba"])
profundidad = st.sidebar.slider("Profundidad (cm)", 10, 40, 20)
da = st.sidebar.number_input("Densidad Aparente (g/cm3)", 1.0, 1.6, 1.4)
mo = st.sidebar.number_input("Materia Organica (%)", 0.0, 10.0, 2.5)
ph = st.sidebar.number_input("pH del Suelo", 3.0, 9.0, 7.0)

# 2. CALCULOS INTERNOS
# Peso de la Capa Arable (t/ha)
pca = 100 * profundidad * da 

# Nitrogeno Disponible (Estimacion simple)
nt_kg = (mo * 0.05 * 1000) * (pca / 2000)
n_disponible = nt_kg * 0.02 # 2% de mineralizacion

# 3. INTERFAZ PRINCIPAL
col1, col2 = st.columns(2)

with col1:
    st.subheader("Diagnostico Fisico-Quimico")
    st.metric("Peso Capa Arable", f"{pca:.1f} t/ha")
    st.metric("N Disponible Estimado", f"{n_disponible:.2f} kg/ha")
    
    if ph < 5.5:
        st.error("Alerta: Suelo Acido (Riesgo de Aluminio)")
    elif ph > 7.5:
        st.warning("Alerta: Suelo Alcalino (Riesgo de sales)")
    else:
        st.success("pH Optimo para la mayoria de cultivos")

with col2:
    st.subheader("Recomendacion Preliminar")
    st.write(f"Para el cultivo de **{cultivo}**:")
    if n_disponible < 40:
        st.info("Se recomienda aplicar refuerzo de Nitrogeno (Urea o Estiercol)")
    else:
        st.success("Nivel de Nitrogeno aceptable")

# 4. TABLA DE DATOS
st.subheader("Resumen de Variables")
df = pd.DataFrame({
    "Parametro": ["Cultivo", "Profundidad", "pH", "Materia Organica"],
    "Valor": [cultivo, f"{profundidad} cm", ph, f"{mo} %"]
})
st.table(df)