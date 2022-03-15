# Imports de bibliotecas
import os
import pandas as pd
from requests.models import get_auth_from_url
from tqdm import tqdm
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
import urllib.request


ua = UserAgent()

# Current Path 
dir_path = str(os.path.dirname(os.path.realpath(__file__)))


def acoes():
    df = pd.read_excel('numeros_acoes.xlsx')
    return list(df.titulo), list(df.processo)


def get_document_links(numeracao):
    url = f'https://redir.stf.jus.br/estfvisualizadorpub/jsp/consultarprocessoeletronico/ConsultarProcessoEletronico.jsf?seqobjetoincidente={numeracao}'
    #driver.get(url)

    session = requests.Session()
    page = session.get(url, headers={"User-Agent": str(ua.chrome)})
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))
    

    links = []
    elements = dom.xpath("//a[contains(@style, '')]")
    for element in elements:
        items = element.items()

        if items[0][0] == 'href' and len(items[0][1]) > 0:
            href = element.items()[0][1]
            if href[-8:-1] == str(numeracao) or href[-13:] == str(numeracao)+'&ad=s#':
                links.append(href)
    
    return links
    

if __name__ == '__main__':
    tipo_acao, numeracao = acoes()

    for i in tqdm(range(len(numeracao))):
        # Cria a pasta para armazenar o arquivo
        path = dir_path + f'\{tipo_acao[i].split(" ")[0]}\{tipo_acao[i]}'
        Path(path).mkdir(parents=True, exist_ok=True)

        links = get_document_links(numeracao[i])

        for j in range(len(links)):
            file = path+f'\documento_{j}.pdf'
            URL = links[j]
            response = urllib.request.urlopen(URL)    
            file = open(file, 'wb')
            file.write(response.read())
            file.close()


