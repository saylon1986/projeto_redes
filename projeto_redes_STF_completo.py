import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path
import textract
from pathlib import Path
import fitz
import re
import os
import pandas as pd
import chardet
import shutil
from separador_frases import limpa_texto, tokeniza_sentenca
import time


###########################################################################

# função principal

def Main():
   

   # cria as pastas para que o programa seja autônomo ao ser rodado
   try:
      os.mkdir("./ações")
   except:
      pass

   try:
      os.mkdir("./imagens")
   except:
      pass
   try:
      os.mkdir("./convertidos_PNG")
   except:
      pass

   try:   
      os.mkdir("./iniciais")      
   except:
      pass   


   # orientação para inserir os documentos na pasta   
   msg = input("Coloque os arquivos na pasta 'ações' e clique enter para continuar")


   # inicia o processo de separar os PDF
   raiz = "./ações"
   Separar_imagens(raiz)


   # # converte as imagens
   Conversor_OCR()

   # Separa os números da OAB
   pasta_iniciais = "./iniciais"
   Separar_OAB(pasta_iniciais)

   print("-------------------")
   print()
   print("*********         Processos finalizados              **********")
   print()
   print("-------------------")


 

#########################################################################################

# Função que separa os PDF do tipo imagens dos PDF dos tipos normais

def Separar_imagens(path_pasta):


   # mensagem inicial
   print("---------------------")
   print()
   print("Separando os PDF das imagens")
   print()
   print("---------------------")
   print()

   # lista para salvar os casos a serem verificar
   para_verificar = []

   # separa os arquivos para a leitura

   arqs = os.listdir(path_pasta)
   # print(arqs)
   for arq in arqs:
      cmn_arq = os.path.join(path_pasta,arq)

   
      extensao = arq[-3:]


   # se a extensão é txt já coloca na pasta das iniciais
      # print(extensao)
      if extensao == 'txt':
         diret_sepfinal = r'./iniciais'
         shutil.move(cmn_arq,diret_sepfinal)


   # se for PDF lê e verifica se não é imagem      
      elif extensao == 'pdf':
         # print(cmn_arq)
         with fitz.open(cmn_arq) as arquivo:
            # print("arquivo", arquivo)
            print("---------------------")
            texto = []
            for pagina in arquivo:
               text = pagina.get_text()
               text = text.strip()
               texto.append(text)
            
            arquivo.close()
            texto = '\n'.join(texto)
            print(arq, len(texto))
            # print(texto.encode())
            # print(type(texto))

   # se for imagem move para a pasta das imagens
            if re.search('\w', texto, re.MULTILINE.IGNORECASE) == None:
               print(cmn_arq,"é uma imagem")
               print("------------------")
               print()   
               diret_sepfinal = r'./imagens'
               shutil.move(cmn_arq,diret_sepfinal)   
            
   # se for legível move para a pasta das iniciais            
            else:
               print(cmn_arq,"não é uma imagem")
               print("------------------")   
               diret_sepfinal = r'./iniciais'
               shutil.move(cmn_arq,diret_sepfinal)

################################################################################################################

# Função que converte os casos da pasta imagens em PNG, para depois transformar em TXT com o Tesseract


def Conversor_OCR():

   print()
   print("-------------------------------")
   print("iniciando conversão das imagens")
   print("-------------------------------")
   print()


   # caminho do tesseract no computador
   pytesseract.tesseract_cmd ='C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

   # site pra baixar o tesseract
   # https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download


   # Path onde estão as imagens a serem convertidas
   path = r'./imagens'
   files = os.listdir(path)


   # path para onde vão as imagens convertidas de PDF para PNG
   trl = r'./convertidos_PNG'


   # convert as imagens de pdf imagem para um PNG
   for f in range(len(files)):
     if files[f].endswith('.pdf'):
          print("estamos no",f) # controle de cada documento
          # print(files[f])
          print()
          print("------------------")


          # cria uma pasta com o nome do arquivo para depositar as imagens de cada página

          nome_pasta = str(files[f][:-4])
          # print(nome_pasta)
          
          try:
            os.mkdir(trl+"/"+nome_pasta)
          except:
            pass
          
          # lê o arquivo e salva todas as imagens em uma lista

          n = os.path.join(path,files[f])
          img = convert_from_path(n, dpi=200)
          # img[-1].save(trl+str(f)+'.png', 'PNG') # salvava só a última página
          
          # print(len(img))
          
          # coverte e salva todas as páginas na pasta
          for j in range(len(img)):
               img[j].save(trl+"/"+nome_pasta+"/"+str(files[f])+"_"+str(j)+'.png', 'PNG')



   # path com as imagens convertidas em PNG
   path = r'./convertidos_PNG'
   files = os.listdir(path)


   # print(files)

   # Path para onde vão os TXT
   path_2 = r'./iniciais'


   # Lê cada um das imagens geradas pelas páginas do PDF, transforma em texto e junta em um artigo TXT
   for item in files:
        arqs = os.path.join(path,item)
        print("estamos no",arqs)
        print()
        pages = os.listdir(arqs)
        textos = []
        for m in range(len(pages)):
             im = os.path.join(arqs,pages[m])
             text = pytesseract.image_to_string(im, lang = 'por') # aciona o tesseract e coloca a linguagem em português
             textos.append(text)
             print("convertida a página", m)

        # salva os textos unificados em um único TXT
             
        texto_final = " ".join(textos)     
        x = open(path_2+'/{}.txt'.format(str(item)), "w+")
        x.write(texto_final)
        x.close()
        print()
        print("                **************            ")



#########################################################################################################

# Função para ler os arquivos e separar os textos


def Ler_arquivos(cmn_arq):

   para_verificar = []

   
   extensao = cmn_arq[-3:]


# se a extensão é txt
   # print(extensao)
   if extensao == 'txt':
      with open(cmn_arq, "rb") as arquivo:
         texto = arquivo.read()
         codificacao = chardet.detect(texto).get('encoding')
         texto = texto.decode(codificacao, errors='ignore')
         # print(texto)
         partes = texto.split("\n")
         txt_limpos =[]
         for item in partes:
            item = item.strip()
            txt_limpos.append(item)

         ##################################

         # chama  a função de verificar a iniciai para apurar o critério do excelentíssimo|a

         nome = Verificar_inicial(txt_limpos,cmn_arq)
         if nome != -1:
            para_verificar.append(nome)   


      # se a extensão é pdf

   elif extensao == 'pdf':
      with fitz.open(cmn_arq) as arquivo:
         texto = []
         pg_1 = []
         for n in range(len(arquivo)):
            texto.append(arquivo[n].get_text().strip())
            if n == 0:
               pg_1.append(arquivo[n].get_text().strip())


         arquivo.close()
         texto = '\n'.join(texto)

         partes = texto.split("\n")
         txt_limpos =[]
         for item in partes:
            item = item.strip()
            txt_limpos.append(item)
         
         ###############################


         # chama  a função de verificar a iniciai para apurar o critério do excelentíssimo|a

         nome = Verificar_inicial(pg_1,cmn_arq)
         if nome != -1:
            para_verificar.append(nome)   
               
   txt_limpos = ' '.join(txt_limpos)
   return txt_limpos, para_verificar


####################################################################################

## Função que verifica potencialmente a iniciai

def Verificar_inicial(txt_limpos,cmn_arq):

   lis_aux = txt_limpos # corta as listas para pegar as 20 primeiras linhas
   # print(lis_aux)
   # print()
   inc = False
   for item in lis_aux:
      if re.search('excelent(í|i)ssim|EXM', item, re.MULTILINE.IGNORECASE): # testa o critério nas 15 primeiras linhas
         # print(item)
         # print()
         inc = True
         break # se encontrar interrompe o ciclo

   # print("o inc é", inc)      

   if inc == True: # caso tenha encontrado
      return -1


   # caso não tenha encontrado o padrão
      
   else: 
      nome = str(cmn_arq).split("/")
      nome_ac = str(nome[-1][9:])
      # print(nome_ac)
      return nome_ac    



########################################################################################################


# Função para separar os AOB das frases selecionadas

def Separar_OAB(path):

   print("iniciando a separação dos números da OAB")


   path_ini = path
   arquivos = os.listdir(path_ini)

   # listas onde serão armazenados os dados
   documento = []
   nome = []
   OAB = []
   estado = []
   trecho = []
   para_verificar = []


   # iteração de cada arquivo

   for k in range(len(arquivos)):
       print()
       print("------------")
       print('Documento nº %s'%(k+1))
       filer = os.path.join(path_ini, arquivos[k])

       

       # regex com todas as siglas dos Estados
       rgx_estad = "AC |AL |AP |AM |BA |CE |DF |ES |GO |MA |MT |MS |MG |PA |PB |PR |PE |PI |RJ |RN |RS |RO |RR |SC |SP |SE |TO "
       

       # função de ler o arquivo que retorna uma lista com os textos em frases
       text_prov, verificar = Ler_arquivos(filer)
       
       # adiciona os casos sem Excelentissim* na lista para verificar
       # print(verificar)
       if len(verificar) >= 1:
         para_verificar.append(verificar[0])
       
       ####################################################################

       text_prov = str(text_prov)
       text_prov = limpa_texto(text_prov)
       text_prov = tokeniza_sentenca(text_prov)

       # print(text_prov)
       # z = input("dê uma olhada")
       ###################################################################

      # itera cada linha do texto
       for n in range(len(text_prov)):

         # controle do texto de cada linha para saber se não é espaço em branco ou outros resíduso
         if len(text_prov[n]) > 3:


               # limpar o texto do ponto para separar melhor o número da OAB

               text_ajust = text_prov[n].replace(".","")

               #separar as OAB permitindo multiplas linhas e maiúsculo e minúsculo

               text_ajust = re.findall("(OAB.[A-Z]{2}.*?\d{3,6})", text_ajust, re.MULTILINE.IGNORECASE)

               for d in range(len(text_ajust)):
                 
                  # separa o número da OAB e o Estado da linha
                     
                  num_oab = re.findall('\d{3,6}',text_ajust[d])
                  estado_oab = re.findall(rgx_estad, text_ajust[d])
                  

                  # Numero da oab precisa ser diferente de vazio para minimizar os falsos positivos
                  
                  for item in num_oab:
                     
                     if re.search('[0-9]+',item, re.IGNORECASE):

                     # acrescenta os elementos separados nas listas
                        trecho.append(text_ajust[d])
                        try:
                           estado.append(estado_oab[0])
                        except:
                           estado.append("")
                        nome.append(text_prov[n])
                        try:
                           OAB.append(num_oab[0])
                        except:
                           OAB.append("")
                        documento.append(arquivos[k])


   ## acabando os arquivos ele transforma em um DF       

   i = pd.Series(nome)
   r = pd.Series(trecho)
   g = pd.Series(OAB)
   p = pd.Series(estado)
   h = pd.Series(documento)
   df_coletados = pd.concat([i,r,g,p,h], axis=1,keys=["Parágrafo","Trecho específico","Nº OAB","Estado","Documento"])

   if len(df_coletados) > 0:
      # corta para separar o nome da ação em uma variável própria
      cortados = df_coletados["Documento"].str.split("_", n=2, expand = True)
      df_coletados ["Ação"] = cortados [0]
      cortados = cortados[2].str.split(".", n=1, expand = True)
      df_coletados ["Tipo documento"] = cortados[1] 

   # print(df_coletados)


   # elimina os duplicados

   df_coletados = df_coletados.drop_duplicates(subset = ["Nº OAB", "Estado", "Ação"])


   # transforma num excel verificando se já tinha um arquivo antes e juntando os novos, caso tenha.
   try:
      antigos = pd.read_excel("Pesquisa_redes.xlsx", engine ='openpyxl')
      anterior_certos = pd.concat([antigos,df_coletados])
      # print(df_certos)
      anterior_certos.to_excel("Pesquisa_redes.xlsx", index = False)
   except:
      df_coletados.to_excel("Pesquisa_redes.xlsx", index = False)


   print(df_coletados)   


   ### DF do para verificar (os que não tem excelentíssimo|a)
   df = pd.DataFrame(columns = ["Para verificar"])
   df ["Para verificar"] = para_verificar


   if len(df) > 0:
      # corta para separar o nome da ação em uma variável própria
      cortados = df["Para verificar"].str.split("_", n =2, expand = True)
      # print(cortados)
      df["Ação"] = cortados [0]
      cortados = cortados[2].str.split(".", n=1, expand = True)
      # print(cortados)
      df ["Tipo documento"] = cortados[1] 

   df = df.drop_duplicates(subset = ["Ação"])

   # transforma em um excel
   df.to_excel("Inicial_nao_identificada.xlsx", index = False)

###########################################################################################################################################



# chama a função principal e realiza todos os processos
ini = time.time()
Main()
fim = time.time()
tempo_total = (fim-ini)//60 #calcula o tempo decorrido
print("o tempo decorrido foi de", tempo_total,"minutos")





##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

# função de separação dos primeiros documentos de cada ação - não tem utilidade nesse processo - 
# está aqui para guardar em caso de necessidade de processos adicionais de manuseio das pastas das ações de controle concentrado


# def Separar_primeiros_documentos():
   
#    # lista as pastas
   
#    path = input("digite o path: ")
#    pastas = os.listdir(path)

#    # lista os arquivos dentro das pastas
   
#    for pasta in pastas:
#       path_arquivos = os.path.join(path, pasta)
#       arquivos = os.listdir(path_arquivos)

#       # Separa o primeiro documento de cada pasta
      
#       for arquivo in arquivos:
#          if "documento_0" in str(arquivo):

#             #faz uma cópia dos primeiros artigos de cada pasta

#             path_arquivo = os.path.join(path_arquivos,arquivo)
#             diret_semifinal = r'C:\Users\saylo\Desktop\separados_teste\prov'
#             shutil.copy(path_arquivo, diret_semifinal)
#             diret_final = r'C:\Users\saylo\Desktop\separados_teste'
#             diret = os.listdir(diret_semifinal)

#             # move os primeiros arquivos de cada pasta das ações para uma outra pasta
#             for item in diret:
#                nome_final = str(pasta)+"_"+str(arquivo)
#                os.rename(os.path.join(diret_semifinal,item),nome_final)
#                shutil.move(nome_final,diret_final)


#######################################################  !!! ####################################################################

# Separar_primeiros_documentos()