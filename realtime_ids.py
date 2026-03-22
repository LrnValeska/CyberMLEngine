import pandas as pd
import joblib
import time
import logging
import warnings # <--- ADICIONADO: Para gerenciar avisos
from datetime import datetime

# Silenciar avisos de nomes de features para um terminal mais limpo
warnings.filterwarnings("ignore")

# Configuração de Logs
logging.basicConfig(
    filename='alerts.log',
    level=logging.WARNING,
    format='%(asctime)s - ALERT - %(message)s'
)

# Cores para o terminal
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RESET = "\033[0;0m"

# Contadores para estatísticas finais
stats = {"normal": 0, "suspeito": 0, "critico": 0}

print("Inicializando motor de detecção Aegis-IDS...")

# 1. Carregar o Modelo e o Scaler
try:
    model = joblib.load('isolation_forest_model.pkl')
    scaler = joblib.load('scaler.pkl')
    print(f"{GREEN}Modelo e Scaler carregados com sucesso!{RESET}")
except FileNotFoundError:
    print(f"{RED}Erro: Arquivos de modelo ou scaler não encontrados.{RESET}")
    exit()

# 2. Carregar dados de teste
try:
    df_test = pd.read_csv('nsl_kdd_ready.csv').head(500)
except:
    print(f"{RED}Erro: nsl_kdd_ready.csv não encontrado.{RESET}")
    exit()

X_test = df_test.drop('target', axis=1)

print(f"{GREEN}Sistema Online. Monitorando tráfego...{RESET}\n")

# 3. Simulação "Linha por Linha" com Score de Severidade (v2)
try:
    for index, row in X_test.iterrows():
        # Converte a linha para o formato que a IA espera, mantendo os nomes das colunas
        data_packet = pd.DataFrame([row]) 
        
        # Aplica a normalização
        data_packet_scaled = scaler.transform(data_packet)
        
        # Obtendo o score de anomalia
        anomaly_score = model.decision_function(data_packet_scaled)[0]
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Lógica de Alertas Baseada em Severidade
        if anomaly_score < -0.12:
            stats["critico"] += 1
            msg = f"CRÍTICO: Anomalia detectada no Pacote {index}! Score: {anomaly_score:.3f}"
            print(f"[{timestamp}] {RED}{msg}{RESET}")
            logging.warning(msg)
        
        elif anomaly_score < 0:
            stats["suspeito"] += 1
            msg = f"SUSPEITO: Atividade atípica no Pacote {index}. Score: {anomaly_score:.3f}"
            print(f"[{timestamp}] {YELLOW}{msg}{RESET}")
        
        else:
            stats["normal"] += 1
            print(f"[{timestamp}] Pacote {index}: {GREEN}Tráfego Normal (Score: {anomaly_score:.3f}){RESET}")
        
        time.sleep(0.4) # Velocidade levemente ajustada para a demo

except KeyboardInterrupt:
    print(f"\n{RED}Sistema interrompido.{RESET}")

# Resumo Final (Excelente para mostrar resultados após a demo)
print("\n" + "="*40)
print("RELATÓRIO DE MONITORAMENTO FINAL")
print("="*40)
print(f"Pacotes Normais:  {GREEN}{stats['normal']}{RESET}")
print(f"Alertas Suspeitos: {YELLOW}{stats['suspeito']}{RESET}")
print(f"Alertas Críticos:  {RED}{stats['critico']}{RESET}")
print("="*40)