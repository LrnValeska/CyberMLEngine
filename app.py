import streamlit as st
import pandas as pd
import joblib
import time
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="CyberMLEngine - IDS", layout="wide")

# Inicialização do estado de monitoramento (essencial para o botão funcionar)
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

# 2. CSS - CORES FIXAS (Verde para Iniciar, Vermelho para Parar)
st.markdown("""
    <style>
    .main { text-align: center; }
    
    /* Estilo para o botão INICIAR (Segunda Coluna) */
    div[data-testid="stColumn"]:nth-of-type(2) button {
        color: #00FF41 !important;
        border: 2px solid #00FF41 !important;
        background-color: transparent !important;
        width: 100%;
    }

    /* Estilo para o botão PARAR (Terceira Coluna) */
    div[data-testid="stColumn"]:nth-of-type(3) button {
        color: #FF3131 !important;
        border: 2px solid #FF3131 !important;
        background-color: transparent !important;
        width: 100%;
    }

    .stProgress > div > div > div > div {
        background-color: #BB00FF;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
st.markdown("<h1 style='text-align: center; color: #BB00FF;'>CyberMLEngine</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Monitoramento de Rede com Inteligência Artificial</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Detector de anomalias de Rede</p>", unsafe_allow_html=True)

st.divider()

# 4. Carregamento do Modelo e Scaler
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('isolation_forest_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except:
        return None, None

model, scaler = load_assets()

if model is None:
    st.error("Erro ao carregar arquivos de modelo.")
    st.stop()

# 5. Botões de Controle
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col2:
    if st.button('Iniciar', use_container_width=True):
        st.session_state.monitoring = True

with col3:
    if st.button('Parar', use_container_width=True):
        st.session_state.monitoring = False
        st.rerun()

# 6. Lógica de Execução (Roda enquanto o estado for True)
if st.session_state.monitoring:
    try:
        df_test = pd.read_csv('nsl_kdd_ready.csv').head(100)
        X_test = df_test.drop('target', axis=1, errors='ignore')
        
        res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
        
        with res_col2:
            placeholder = st.empty()
            
            for index, row in X_test.iterrows():
                # Se o usuário clicou em parar durante o loop
                if not st.session_state.monitoring:
                    break
                    
                data_packet = pd.DataFrame([row])
                data_packet_scaled = scaler.transform(data_packet)
                score = model.decision_function(data_packet_scaled)[0]
                
                if score < -0.12:
                    status, color = "CRÍTICO", "red"
                elif score < 0:
                    status, color = "Suspeito", "orange"
                else:
                    status, color = "Normal", "green"
                    
                with placeholder.container(border=True):
                    st.metric("Score de Anomalia", f"{score:.4f}", delta=status, delta_color="inverse" if status != "Normal" else "normal")
                    st.markdown(f"### Status: :{color}[{status}]")
                    st.caption(f"Analisando Pacote ID: {index} | {datetime.now().strftime('%H:%M:%S')}")
                    
                    risk_val = min(max((abs(score) * 100), 0), 100) / 100
                    st.progress(risk_val, text=f"Nível de Risco: {int(risk_val*100)}%")
                    
                time.sleep(0.5)
            
            # Ao final do loop, desliga o monitoramento
            st.session_state.monitoring = False
            st.success("Processamento concluído.")
            
    except Exception as e:
        st.error(f"Erro: {e}")
        st.session_state.monitoring = False