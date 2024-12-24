import subprocess
import os

# Configurações
input_file = "httpx_results.txt"  # Arquivo com subdomínios
wordlist = "/path/to/wordlist.txt"  # Caminho para a wordlist

# Função para executar comandos no terminal
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Processar cada domínio na lista
with open(input_file, "r") as file:
    for domain in file:
        domain = domain.strip()
        print(f"Testando WAF para {domain}...")

        # Executar WafW00f
        waf_command = f"wafw00f -a https://{domain}"
        waf_output = run_command(waf_command)

        # Verificar resultado do WafW00f
        if "Cloudflare" in waf_output:
            print(f"WAF detectado: Cloudflare. Ajustando parâmetros do ffuf...")
            ffuf_command = f"""
            ffuf -u https://{domain}/FUZZ \
            -w {wordlist} \
            -t 1 \
            -rate 0.5 \
            --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
            -o {domain}_ffuf_results.txt
            """
        else:
            print(f"Sem WAF ou WAF genérico detectado. Rodando ffuf padrão...")
            ffuf_command = f"""
            ffuf -u https://{domain}/FUZZ \
            -w {wordlist} \
            -t 1 \
            -rate 0.2 \
            --timeout 30 \
            -o {domain}_ffuf_results.txt
            """

        # Executar FFUF
        print(f"Rodando FFUF para {domain}...")
        os.system(ffuf_command)

print("Processamento completo!")
