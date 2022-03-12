import pandas as pd
import re


anterior_certos = pd.read_excel("Pesquisa_redes.xlsx", engine ='openpyxl')

anterior_certos = anterior_certos.drop_duplicates(subset = ["Nº OAB", "Estado", "Documento"])


## Precisa eliminar os duplicados com base nas colunas OAB, Estado, Ação 

anterior_certos.to_excel("Pesquisa_redes.xlsx", index = False)

anterior_certos = pd.read_excel("Pesquisa_redes.xlsx", engine ='openpyxl')

nome_acao = pd.DataFrame(anterior_certos.groupby(["Ação"])["Ação"].count())
nome_acao.columns = ["quantidade"]

print(nome_acao)

nome_acao = nome_acao.reset_index()
nome_acao.to_excel("Quantidade_Ação_Pesquisa_redes.xlsx", index = False)


# text_limpo =[]
# conf = []

# trecho_1 = "mais de 9.000"
# aval =[]
# for d in range(len(anterior_certos["Publicação"])):
# 	texto = str(anterior_certos["Publicação"][d])
# 	# # print(texto[35:250])
# 	# # print("------------------------")
# 	# partes.append(texto[35:250])
# 	# if re.search(trecho_1, texto, re.IGNORECASE):
# 	# 	# print("o texto tinha", len(texto))
# 	# 	txt_1 = re.search(trecho_1, texto, re.IGNORECASE).group()
# 	# 	# print(txt_1)
# 	# 	numer_1 = texto.find(txt_1)
# 	# 	# print(numer_1)
# 	# 	# print(texto[numer_1-15: numer_1+150])
# 	# 	# numer_2 = texto.find(trecho_2)
# 	# 	# print(numer_2)
# 	# 	texto = texto[0:numer_1-15]+ texto[numer_1+150:]
# 	# 	# print("o texto tem", len(texto))
# 	# 	# print("-------------------")
# 	# else:
# 	# 	pass	


# 	trecho_final = texto[-400:]
# 	if re.search('defir|indefir|conced|neg|provid',trecho_final, re.IGNORECASE):
# 		trecho = re.search('defir|indefir|conced|neg|provid',trecho_final, re.IGNORECASE).group()
# 		numer_1 = trecho_final.find(trecho)
# 		pedac = trecho_final[numer_1-10:]
# 		print(trecho)
# 		print(pedac)
# 		print("-----------------")
# 		aval.append(pedac)
# 		conf.append(trecho_final)
# 	else:
# 		aval.append("")
# 		conf.append(trecho_final)	




# # anterior_certos ["possui termo famílias|pessoas"] = conf
# # anterior_certos ["Publicação (nova)"] = text_limpo
# anterior_certos ["Trecho"] = conf
# anterior_certos ["Aval"] = aval

# anterior_certos.to_excel("Planilha_anotacao.xlsx", index = False)