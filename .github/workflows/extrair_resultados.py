import requests
from bs4 import BeautifulSoup
import json
import datetime

def extrair_resultados():
    url = "https://www.portalbrasil.com.br/jogo-do-bicho/"  # Link correto do site
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        resultados = {}
        data_atual = datetime.datetime.now().strftime("%A, %d/%m/%Y")
        
        for tabela in soup.find_all("table"):  # Supondo que os resultados estejam em tabelas
            titulo = tabela.find_previous_sibling("h2").text.strip() if tabela.find_previous_sibling("h2") else "Banca Desconhecida"
            resultados[titulo] = []
            
            for linha in tabela.find_all("tr")[1:]:  # Ignora cabeçalhos
                colunas = linha.find_all("td")
                if len(colunas) > 1:
                    horario = colunas[0].text.strip()
                    resultado = colunas[1].text.strip()
                    resultados[titulo].append({"horário": horario, "resultado": resultado})
        
        with open("resultados.json", "w", encoding="utf-8") as f:
            json.dump({"data": data_atual, "bancas": resultados}, f, ensure_ascii=False, indent=4)
        
        print("Resultados extraídos com sucesso!")
    else:
        print("Erro ao acessar o site.")

if __name__ == "__main__":
    extrair_resultados()
