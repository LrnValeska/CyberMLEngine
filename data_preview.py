import pandas as pd

# Lista oficial de colunas do dataset NSL-KDD
col_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes",
    "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty_level"
]


def preview_data(file_path):
    try:
        # Lendo o arquivo (ajustamos 'names' para carregar os cabeçalhos)
        df = pd.read_csv(file_path, names=col_names, header=None)

        print(f"\nArquivo '{file_path}' carregado com sucesso!")
        print("-" * 30)
        print(f"Total de linhas: {df.shape[0]}")
        print(f"Total de colunas: {df.shape[1]}")
        print("-" * 30)

        # Exibindo o cabeçalho (primeiras 5 linhas)
        print("\n--- Visualização do Cabeçalho (Header) ---")
        print(df.head())

    except FileNotFoundError:
        print(
            f"Erro: O arquivo '{file_path}' não foi encontrado na pasta atual.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    # Certifique-se que o nome do arquivo abaixo é o mesmo que você extraiu
    preview_data('KDDTrain+.txt')
