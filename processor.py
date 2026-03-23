import pandas as pd
import numpy as np
import json
from datetime import datetime

def carregar_e_mapear_fluxos(caminho_log):
    try:
        # Leitura de logs JSON (formato padrão Zeek/Suricata)
        df = pd.read_json(caminho_log, lines=True)
        
        colunas_essenciais = {
            'id.orig_h': 'ip_origem',
            'id.resp_h': 'ip_destino',
            'duration': 'duracao',
            'orig_bytes': 'bytes_enviados',
            'resp_bytes': 'bytes_recebidos',
            'orig_pkts': 'pacotes_enviados',
            'resp_pkts': 'pacotes_recebidos'
        }
        
        # Filtra apenas as colunas que existem no arquivo de log atual
        colunas_presentes = [c for c in colunas_essenciais.keys() if c in df.columns]
        df_analise = df[colunas_presentes].rename(columns=colunas_essenciais)
        
        df_analise.fillna(0, inplace=True)

        # Engenharia de Features: Ratio de Bytes para tráfego criptografado
        if 'bytes_enviados' in df_analise.columns and 'bytes_recebidos' in df_analise.columns:
            df_analise['ratio_bytes'] = df_analise['bytes_enviados'] / (df_analise['bytes_recebidos'] + 1)
        
        return df_analise

    except Exception as e:
        print(f"Erro ao processar arquivo de log: {e}")
        return None

def analisar_com_baseline(valor_atual, ip, historico_global):
    """
    Compara o fluxo atual com o passado do host usando Z-Score.
    """
    if ip not in historico_global:
        historico_global[ip] = [valor_atual]
        return False, 0.0, "Aprendendo baseline..."

    dados_passados = historico_global[ip]
    
    if len(dados_passados) < 3:
        dados_passados.append(valor_atual)
        return False, 0.0, "Coletando amostras..."

    media = np.mean(dados_passados)
    desvio = np.std(dados_passados)
    
    if desvio == 0: 
        desvio = 0.0001 

    z_score = (valor_atual - media) / desvio
    
    # Atualiza historico com limite para lidar com Concept Drift
    dados_passados.append(valor_atual)
    if len(dados_passados) > 50: 
        dados_passados.pop(0)

    # Threshold: Z > 3.0 indica anomalia estatística forte
    is_anomalia = z_score > 3.0
    status = "ANOMALIA" if is_anomalia else "NORMAL"
    
    return is_anomalia, z_score, status

def gerar_alerta_siem(ip, valor, z_score, metrica="ratio_bytes"):
    """
    Gera log estruturado em JSON para integração com SIEM/SOAR.
    """
    alerta = {
        "timestamp": datetime.now().isoformat(),
        "sensor": "CyberMLEngine-Node-01",
        "evento": "ANOMALIA_DE_FLUXO",
        "severidade": "ALTA" if z_score > 3 else "MEDIA",
        "origem_ip": ip,
        "analise": {
            "metrica_focada": metrica,
            "valor_observado": round(valor, 2),
            "z_score": round(z_score, 2),
            "explicabilidade": f"O {metrica} deste host esta {round(z_score, 1)} desvios padroes acima da media historica."
        },
        "modelo_deploy": "SENSOR-PIPELINE-ALERTA-SIEM"
    }
    
    # Escrita em arquivo de log persistente
    try:
        with open("alerts_siem.log", "a") as f:
            f.write(json.dumps(alerta) + "\n")
    except Exception as e:
        print(f"Erro ao gravar alerta: {e}")
        
    return alerta

if __name__ == "__main__":
    print("Mapeador CyberMLEngine e Motor de Baseline inicializados.")