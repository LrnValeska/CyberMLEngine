import time
import processor
import json

historico_geral = {}


def iniciar_monitoramento(caminho_log):
    print("Iniciando monitoramento de fluxo (Sensor-Pipeline-Alerta)...")

    # Abrimos o arquivo em modo de leitura
    with open(caminho_log, "r") as f:
        # PULA PARA O FINAL: O monitor ignora tudo o que já estava escrito
        f.seek(0, 2)
        print("Aguardando novos fluxos no log... (Pressione Ctrl+C para parar)")

        while True:
            # Tenta ler a próxima linha
            linha = f.readline()

            if not linha:
                # Se não tem linha nova, espera um pouco e tenta de novo
                time.sleep(0.1)
                continue

            try:
                # Processa apenas a linha que acabou de chegar
                dados = json.loads(linha.strip())

                # Mapeamos os dados usando a lógica do seu processor
                # (Simulando o mapeamento que o carregar_e_mapear_fluxos faria para uma linha)
                ip = dados.get('id.orig_h')
                orig_bytes = dados.get('orig_bytes', 0)
                # Evita divisão por zero
                resp_bytes = dados.get('resp_bytes', 1)
                ratio = orig_bytes / resp_bytes

                # Analisa contra o Baseline usando sua função existente
                is_anomalia, z, status = processor.analisar_com_baseline(
                    ratio, ip, historico_geral)

                # Se for anomalia, gera o log de SIEM
                if is_anomalia:
                    processor.gerar_alerta_siem(ip, ratio, z)
                    print(
                        f"\aALERTA GERADO: IP {ip} | Z-Score: {z:.2f} | Verifique alerts_siem.log")
                else:
                    print(
                        f"Novo fluxo: IP {ip} | Ratio: {ratio:.2f} | Status: {status}")

            except Exception as e:
                print(f"Erro ao processar linha: {e}")
                continue


if __name__ == "__main__":
    # Certifique-se de que o arquivo existe antes de iniciar
    open("test_log.json", "a").close()
    iniciar_monitoramento("test_log.json")
