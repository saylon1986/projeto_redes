import re
import pandas as pd
import nltk
import chardet


abreviacoes = pd.read_csv('abreviacoes-direito.csv', sep=',',header=None, index_col=False) 
# print(abreviacoes)
# print("-------------")

tokenizador_sents = nltk.data.load('tokenizers/punkt/portuguese.pickle')


def corrige_erros_abreviacoes(texto):

	texto = re.sub('\r', '', texto)
	texto = re.sub('\n+\-', '-', texto)
	texto = re.sub('[”““”]+', '"', texto)
	texto = re.sub('[‘’`´]+', "'", texto)
	texto = re.sub('[.]+(?=[A-Za-z]{2,})','. ', texto)
	for abrev, palavra in zip(abreviacoes[0], abreviacoes[1]):
		texto = re.sub(r'(?<=[\s(])%s\.'%abrev, '%s'%palavra, texto, flags=re.IGNORECASE)
	return texto




def limpa_pagina(linha):
    linha = linha.strip()
    if re.fullmatch(r'(_)+', linha):
        return False
    if re.fullmatch(r'(^[A-Z][\w\s]+: [/0-9\.\-]+\.)*$', linha):
        return False
    if re.fullmatch(r'(^[A-Z][\w\s()]+: ([A-Z]\.[ ]*)+ (D(O|A|E)(S)* ([A-Z]\.[ ]*)+)*)$', linha):
        return False
    if re.fullmatch(r'(^[A-Z][\w\s()]+: [\w\s-]+)\.*$', linha):
        return False
    if re.fullmatch(r'(^[A-Z][\w\s]+(\(a\)|\(s\))*[ ]*: [\w\s-]+ \(.+\))\.*$', linha):
        return False
    
    return True    


def correspondencia_linhas(paginas, index_pagina, valor):
    i = 0
    while len(paginas[index_pagina][i]) == len(paginas[index_pagina+valor][i]):
        i += 1
        if i >= len(paginas[index_pagina+valor])-1 or i >= len(paginas[index_pagina])-1:
            break        
    return i



def corrige_erros_abreviacoes(texto):
    texto = re.sub('\r', '', texto)
    texto = re.sub('\n+\-', '-', texto)
    texto = re.sub('[”““”]+', '"', texto)
    texto = re.sub('[‘’`´]+', "'", texto)
    texto = re.sub('[.]+(?=[A-Za-z]{2,})','. ', texto)
    for abrev, palavra in zip(abreviacoes[0], abreviacoes[1]):
        texto = re.sub(r'(?<=[\s(])%s\.'%abrev, '%s'%palavra, texto,flags=re.IGNORECASE)
    return texto
    


def acha_cabecalho(paginas):
    lista = []
    for j in range(len(paginas)-1):
        i = correspondencia_linhas(paginas, j, 1)
        if i == 0:
            i = correspondencia_linhas(paginas, j, -1)
        lista.append(i)
        
    if not lista:
        return [0]
    
    return lista + [lista[-1]]


def limpa_texto(texto):
    texto = corrige_erros_abreviacoes(texto)
    
    paginas = [pagina.split('\n') for pagina in re.split('\n{3,}', texto) \
              if pagina != '']
    
    cabecalho = acha_cabecalho(paginas)
    texto_limpo = []
    
    for i, pagina in enumerate(paginas):
        for linha in pagina[cabecalho[i]:]:
            linha_correta = limpa_pagina(linha)
            if linha_correta:
                texto_limpo.append(linha)
               
    # print("função limpar")
    # z = input("veja")
    return ' '.join(texto_limpo)

    # return texto_limpo


def tokeniza_sentenca(texto, n=3):
	sentencas = []
	sentencas_sujas = tokenizador_sents.tokenize(texto)
	for item in sentencas_sujas:
		# print(item)
		# print("--------------------")
		for parte in item.split(';'):
			if len(parte.split()) > n:
				sentencas.append(parte)	
	# print(sentencas)
	# z = input("veja")
	return sentencas


# cmn_arq = "ADC 1_documento_0.txt"

# with open(cmn_arq, "rb") as arquivo:
# 	texto = arquivo.read()
# 	codificacao = chardet.detect(texto).get('encoding')
# 	texto = texto.decode(codificacao, errors='ignore')
# 	texto = limpa_texto(texto)
# 	sentencas = tokeniza_sentenca(texto)
# 	for item in sentencas:
# 		print(item)
# 		print("--------------")