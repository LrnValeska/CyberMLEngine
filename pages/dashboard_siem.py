import streamlit as st
import pandas as pd
import json
import os
import time

st.set_page_config(page_title="CyberMLEngine Dashboard", layout="wide", page_icon="🛡️")

st.title("CyberMLEngine - SIEM em Tempo Real")
st.markdown("---")

def carregar_dados():
    alertas = []
    if os.path.exists("alerts_siem.log"):
        with open("alerts_siem.log", "r") as f:
            for linha in f:
                try:
                    d = json.loads(linha.strip())
                    alertas.append({
                        "Horário": d['timestamp'],
                        "IP": d['origem_ip'],
                        "Severidade": d['severidade'],
                        "Z-Score": float(d['analise']['z_score']),
                        "Valor Observado": d['analise']['valor_observado']
                    })
                except:
                    continue
    return pd.DataFrame(alertas)

# --- REATIVIDADE DO STREAMLIT ---
# Em vez de while True, o Streamlit gerencia a atualização
df = carregar_dados()

if not df.empty:
    # Métricas em destaque
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Alertas", len(df))
    col2.metric("Maior Z-Score", f"{df['Z-Score'].max():.1e}")
    col3.metric("Último IP Alvo", df['IP'].iloc[-1])

    # Gráfico e Tabela
    st.write("### Evolução das Anomalias")
    st.line_chart(df.set_index("Horário")["Z-Score"])

    st.write("### Detalhes dos Incidentes")
    st.dataframe(df.sort_values(by="Horário", ascending=False), use_container_width=True)
    
    # Botão de Ação
    if st.button("🚨 Bloquear IP da Última Anomalia"):
        ultimo_ip = df['IP'].iloc[-1]
        st.error(f"Comando enviado para o Firewall: Bloquear {ultimo_ip}")
        # Opcional: Salvar em arquivo para o monitor.py ler
        with open("blacklist.txt", "a") as bl:
            bl.write(f"{ultimo_ip}\n")
else:
    st.info("Aguardando novas detecções do monitor.py...")

# Faz o dashboard recarregar sozinho a cada 5 segundos
time.sleep(5)
st.rerun()