# CyberMLEngine: Aegis-IDS

O CyberMLEngine é um Sistema de Detecção de Intrusão (IDS) em tempo real que utiliza Inteligência Artificial para identificar anomalias em fluxos de tráfego de rede. Esta versão apresenta o motor Aegis, focado em análise de severidade e baixo índice de falsos positivos.

## Funcionalidades Atuais
* Monitoramento em Tempo Real: Interface interativa via Streamlit com controles de Iniciar/Parar.
* Motor Aegis-IDS: Utiliza o algoritmo Isolation Forest para detecção de anomalias.
* Escaneamento Inteligente: Implementação de StandardScaler para garantir a integridade dos dados antes da predição.
* Níveis de Severidade: Classificação automática entre tráfego Normal, Suspeito e Crítico.
* Logging de Segurança: Geração automática de alerts.log para auditoria e resposta a incidentes.

## Tecnologias Utilizadas
* Linguagem: Python 3.10+
* IA/ML: Scikit-Learn (Isolation Forest), Joblib
* Data Science: Pandas, Numpy
* Interface: Streamlit (UI Customizada com Neon Design)
* Dataset: NSL-KDD (Versão pré-processada)

## Estrutura do Projeto
* app.py: Interface principal do usuário (Streamlit).
* data_preprocessing.py: Script de limpeza e normalização dos dados.
* isolation_forest_model.pkl: Modelo de IA treinado.
* scaler.pkl: Objeto de normalização das features.
* alerts.log: Registro de alertas detectados pelo sistema.

## Como Executar
1. Instale as dependências:
   ```bash
   pip install streamlit pandas scikit-learn joblib
2 . Inicie a aplicação
   '''bash
   streamlit run app.py

Desenvolvido por Lorena Valeska | Pesquisadora e Desenvolvedora de Software.
---

**Para atualizar no seu terminal:**
```powershell
git add README.md
git commit -m "Docs: README limpo e atualizado"
git push origin main
