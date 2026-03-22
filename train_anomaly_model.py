import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import joblib

print("Carregando dados para detecção de anomalias...")
df = pd.read_csv('nsl_kdd_ready.csv')

X = df.drop('target', axis=1)
y_true = df['target'] # 0 = Normal, 1 = Ataque

# --- EDIÇÃO 1: REDUÇÃO DE RUÍDO ---
# Mudamos de 0.45 para 0.1 (ou 'auto') para o modelo ser menos "assustado"
contamination_rate = 0.05 

model = IsolationForest(
    n_estimators=100, 
    contamination=contamination_rate, 
    random_state=42
)

print("Procurando anomalias no tráfego...")
model.fit(X)

# --- EDIÇÃO 2: PONTUAÇÃO DE ANOMALIA (SCORE) ---
# Além do predict, vamos gerar o score para conferir a "certeza" do modelo
scores = model.decision_function(X)

y_pred_raw = model.predict(X)
y_pred = [1 if x == -1 else 0 for x in y_pred_raw]

print("\nDesempenho do Isolation Forest (Detecção de Anomalias):")
print(classification_report(y_true, y_pred))

# --- EDIÇÃO 3: SALVAMENTO ---
joblib.dump(model, 'isolation_forest_model.pkl')
print("\nModelo de anomalias salvo como 'isolation_forest_model.pkl'!")

# DICA EXTRA: Se o seu StandardScaler estiver no arquivo de preprocessamento, 
# certifique-se de que o arquivo 'scaler.pkl' também esteja na mesma pasta 
# que o seu 'aegis_ids.py' para a próxima etapa.