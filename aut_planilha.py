import pandas as pd  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options   
from webdriver_manager.chrome import ChromeDriverManager   
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
import time  
import json  

# Carregar os dados da planilha Excel  
df = pd.read_csv('dados_contato.csv')  

# Configurações do Chrome  
options = Options()  
options.add_argument('--disable-extensions')  
options.add_argument('--disable-gpu')  
options.add_argument('--no-sandbox')  

# Iniciar o WebDriver  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  

# Lista para armazenar os contatos  
contatos = []  

# Iterar sobre as linhas da planilha  
for index, row in df.iterrows():  
    nome = row['Nome']  
    telefone = row['Telefone']  
    
    # Abrir o formulário  
    driver.get("http://localhost:5500")  # Certifique-se de usar este caminho correto  
    
    # Aguardar a página carregar  
    WebDriverWait(driver, 10).until(  
        EC.presence_of_element_located((By.ID, "nome"))  
    )  
    
    # Preencher o campo "Nome"  
    nome_input = driver.find_element(By.ID, "nome")  
    nome_input.clear()  
    nome_input.send_keys(nome)  
    
    # Preencher o campo "Telefone"  
    telefone_input = driver.find_element(By.ID, "telefone")  
    telefone_input.clear()  
    telefone_input.send_keys(telefone)  
    
    # Enviar o formulário  
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  
    submit_button.click()  
    
    # Esperar que o novo conteúdo seja carregado (se necessário)  
    time.sleep(2)  # Ajuste o tempo conforme necessário  

    # Salvar os dados em uma lista  
    contato = {'nome': nome, 'telefone': telefone}  
    contatos.append(contato)  

    # Salvar no LocalStorage com tratamento de exceção  
    try:  
        driver.execute_script(f"localStorage.setItem('contato_{index}', JSON.stringify({{'nome': '{nome}', 'telefone': '{telefone}'}}));")  
        print(f"Salvo: Contato {index} - Nome: {nome}, Telefone: {telefone}")  
    except Exception as e:  
        print(f"Erro ao salvar no LocalStorage: {e}")  

# Fechar o navegador  
driver.quit()  

# Salvar a lista de contatos em um arquivo JSON  
with open("contatos.json", "w") as json_file:  
    json.dump(contatos, json_file, indent=4)  

print("Dados salvos em contatos.json com sucesso.")