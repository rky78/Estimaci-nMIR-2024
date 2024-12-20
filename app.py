import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  # Replaced matplotlib with Plotly
from scipy.interpolate import interp1d

# --- TITLE AND INSTRUCTIONS ---
st.title('🧮 APROXIMACIÓN SEGÚN MIR2024')
st.write('Este programa te permite calcular una **estimación de tus resultados en el MIR2024**. Basándonos en tu **Nota de Expediente**, estimamos cuántas **Netas y Aciertos** necesitas para lograr un puesto o percentil objetivo. Para obtener una estimación más precisa, se eliminan las notas más bajas para evitar sesgos.')

# --- USER INPUTS ---
st.header('🔍 Configuración inicial')
with st.form("user_input_form", clear_on_submit=False):
    nota_expediente = st.number_input('Introduce tu Nota de Expediente (Obligatorio)', min_value=0.0, max_value=10.0, value=7.88, step=0.01)
    percentil_input = st.number_input('Introduce el Percentil que deseas alcanzar (Opcional)', min_value=1, max_value=100, value=50, step=1)
    puesto_input = st.number_input('Introduce el Puesto que deseas alcanzar (Opcional)', min_value=1, max_value=15000, value=3000, step=1)
    submitted = st.form_submit_button("Calcular")

if not submitted:
    st.warning('⚠️ Debes completar la Nota de Expediente y hacer clic en "Calcular".')
    st.stop()

# --- FUNCTIONS ---
def calculate_pqr(nota_expediente, netas):
    """Calculate the PQR score based on the given formula."""
    return (nota_expediente * 10 / 8.8) + (netas * 90 / 461.3)

def calculate_netas_and_aciertos(nota_expediente, percentil):
    """Calculate the Netas and Aciertos for a given percentil and Nota de Expediente."""
    pqr_values = np.linspace(20, 80, 100)  # Simulated range of PQR for percentiles 1 to 100
    pqr_for_percentil = np.percentile(pqr_values, percentil)
    netas = ((pqr_for_percentil - (nota_expediente * 10 / 8.8)) * 461.3 / 90)
    aciertos = (netas * 4 / 5) + 40
    return round(netas), round(aciertos)

def calculate_full_table(nota_expediente):
    """Generate a table of percentiles, Netas, Aciertos, and Puesto."""
    percentiles = np.arange(5, 105, 5)
    pqr_values = np.linspace(20, 80, 100)  # Simulated range of PQR for percentiles 1 to 100
    pqr_for_percentiles = np.percentile(pqr_values, percentiles)
    netas = ((pqr_for_percentiles - (nota_expediente * 10 / 8.8)) * 461.3 / 90)
    aciertos = (netas * 4 / 5) + 40
    df = pd.DataFrame({
        'Percentil': percentiles,
        'Netas': np.round(netas).astype(int),
        'Aciertos': np.round(aciertos).astype(int),
        'Puesto Aproximado': np.linspace(100, 15000, len(percentiles)).astype(int)
    })
    return df

# --- CALCULATIONS ---
netas, aciertos = calculate_netas_and_aciertos(nota_expediente, percentil_input)
table_df = calculate_full_table(nota_expediente)

# --- OUTPUT RESULTS ---
st.header('📊 Cálculos de tu objetivo personalizado')
st.write(f'**Nota de Expediente:** {nota_expediente}')
st.write(f'**Percentil Objetivo:** {percentil_input}')
st.write(f'**Puesto Objetivo:** {puesto_input}')
st.write(f'**Netas Necesarias:** {netas}')
st.write(f'**Aciertos si se responde todo:** {aciertos}')

st.subheader('📋 Tabla de Percentiles de 5 en 5')
st.write(table_df)

# --- PLOT DISTRIBUTION ---
st.subheader('📈 Gráfica de la Distribución')
pqr_values = np.linspace(20, 80, 100)  # Simulated PQR for demonstration
df_pqr = pd.DataFrame({'PQR': pqr_values})

# Create the histogram using Plotly
fig = px.histogram(df_pqr, x='PQR', nbins=30, title='Distribución de la PQR', 
                   labels={'PQR': 'PQR'}, opacity=0.7, color_discrete_sequence=['lightblue'])
fig.add_vline(x=pqr_values[int(percentil_input) - 1], line_dash='dash', line_color='red', annotation_text='Percentil Objetivo')

# Display the plot
st.plotly_chart(fig)
