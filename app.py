import streamlit as st
import pandas as pd
import joblib
import time
import os
import warnings
from datetime import datetime

# Ignorar avisos de nomes de features e versões do sklearn para limpar o log do Render
warnings.filterwarnings("ignore", category=UserWarning)

# 1. Configuração da Página
st.set_page_config(page_title="CyberMLEngine - IDS", layout="wide")

# Inicialização do estado de monitoramento
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

# 2. CSS - Estilização Visual
st.markdown("""
    <style>
    .main { text-align: center; }
    div[data-testid="stColumn"]:nth-of-type(2) button {
        color: #00FF41 !important;
        border: 2px solid #00FF41 !important;
        background-color: transparent !important;
        width: 100%;
    }
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

st.divider()

# 4. Carregamento do Modelo, Scaler e Dados de Exemplo
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('isolation_forest_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except Exception as e:
        return None, None

@st.cache_data
def load_sample_data():
    # ALTERADO: Agora lê o arquivo leve (sample_data.csv) para o deploy no Render
    try:
        if os.path.exists('sample_data.csv'):
            return pd.read_csv('sample_data.csv')
        else:
            # Caso o arquivo não exista, tenta ler apenas as primeiras linhas do original (se presente)
            return pd.read_csv('nsl_kdd_ready.csv', nrows=100)
    except:
        return None

model, scaler = load_assets()
df_sample = load_sample_data()

if model is None or df_sample is None:
    st.error("Erro: Arquivos 'isolation_forest_model.pkl', 'scaler.pkl' ou 'sample_data.csv' não encontrados.")
    st.info("Certifique-se de que eles estão na raiz do seu repositório no GitHub.")
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

# 6. Lógica de Execução (Simulação de IDS)
if st.session_state.monitoring:
    try:
        # Prepara os dados removendo a coluna alvo se ela existir
        X_test = df_sample.drop('target', axis=1, errors='ignore')
        
        res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
        
        with res_col2:
            placeholder = st.empty()
            
            for index, row in X_test.iterrows():
                if not st.session_state.monitoring:
                    break
                
                # Criar DataFrame com nomes de colunas para evitar o Warning do Sklearn
                data_packet = pd.DataFrame([row], columns=X_test.columns)
                
                # Normalização e Predição
                data_packet_scaled = scaler.transform(data_packet)
                # Passamos novamente as colunas para o DataFrame escalonado
                data_for_pred = pd.DataFrame(data_packet_scaled, columns=X_test.columns)
                score = model.decision_function(data_for_pred)[0]
                
                # Definição de Status baseada no Score de Anomalia
                if score < -0.12:
                    status, color = "CRÍTICO", "red"
                elif score < 0:
                    status, color = "Suspeito", "orange"
                else:
                    status, color = "Normal", "green"
                
                with placeholder.container(border=True):
                    st.metric("Score de Anomalia", f"{score:.4f}", delta=status, 
                              delta_color="inverse" if status != "Normal" else "normal")
                    st.markdown(f"### Status: :{color}[{status}]")
                    st.caption(f"Analisando Pacote ID: {index} | {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Barra de progresso visual de risco
                    risk_val = min(max((abs(score) * 100), 0), 100) / 100
                    st.progress(risk_val, text=f"Nível de Risco: {int(risk_val*100)}%")
                    
                time.sleep(0.5)
            
            st.session_state.monitoring = False
            st.success("Análise de tráfego concluída.")
            
    except Exception as e:
        st.error(f"Erro na simulação: {e}")
        st.session_state.monitoring = False