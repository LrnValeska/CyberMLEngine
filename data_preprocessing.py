import pandas as pd
import joblib # <--- ADICIONADO: Necessário para salvar o scaler
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1. Carregar os dados
col_names = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty_level"]

df = pd.read_csv('KDDTrain+.txt', names=col_names, header=None)

# 2. Remover coluna desnecessária
df = df.drop('difficulty_level', axis=1)

# 3. Label Encoding
categorical_cols = ['protocol_type', 'service', 'flag']
le = LabelEncoder()

for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

# 4. Criar o Alvo (Target)
df['target'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
df = df.drop('label', axis=1)

# 5. Normalização (Escalonamento)
scaler = StandardScaler()
features = df.drop('target', axis=1)
scaled_features = scaler.fit_transform(features)

# --- EDIÇÃO ESSENCIAL: SALVAR O SCALER ---
# Isso garante que o motor de detecção use a mesma escala do treino
joblib.dump(scaler, 'scaler.pkl')
print("Régua de normalização (scaler.pkl) salva com sucesso!")
# ----------------------------------------

# Criar um novo DataFrame com os dados prontos
df_ready = pd.DataFrame(scaled_features, columns=features.columns)
df_ready['target'] = df['target'].values

print("Pré-processamento concluído!")

# Salvar para usar no próximo passo
df_ready.to_csv('nsl_kdd_ready.csv', index=False)
print("\n💾 Arquivo 'nsl_kdd_ready.csv' salvo e pronto para a IA!")