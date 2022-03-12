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




def Main():
   
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
      os.mkdir("./convertidos_TXT")      
   except:
      pass


   path = "./ações"   

   msg = input("Coloque os arquivos na pasta 'ações' e clique enter para continuar")

   Separar_OAB(0,path)

   print()
   print("Processos finalizados")



#########################################################################################

def ler_arquivo(caminho):

   # Verifica as extensões dos arquivos antes da leitura
   
   try:
       extensao = caminho[-3:]
      
      # se a extensão é txt
       print(extensao)
       if extensao == 'txt':
           with open(caminho, "rb") as arquivo:
               texto = arquivo.read()
               codificacao = chardet.detect(texto).get('encoding')
               texto = texto.decode(codificacao, errors='ignore')
               # print(texto)
               partes = texto.split("\n")
               txt_limpos =[]
               for item in partes:
                  item = item.strip()
                  txt_limpos.append(item)



       # se a extensão é pdf

       elif extensao == 'pdf':
           with fitz.open(caminho) as arquivo:
               for pagina in arquivo:
                  texto = []
                  texto.append(pagina.get_text())
               
               texto = '\n'.join(texto)
               partes = texto.split("\n")
               txt_limpos =[]
               for item in partes:
                  item = item.strip()
                  txt_limpos.append(item)

               # texto = ' '.join(texto)
       
       # caso não seja retorna a lista com as frases vazia            
       else:
         txt_limpos = []
   
   
       # retorna a lista com as frases ou vazia depois da leitura do artigo   
       return txt_limpos   
   

   # em caso de algum erro ou problema retorna a lista vazia    
   except:
      txt_limpos = []
      return txt_limpos



####################################################################################

def Separar_OAB(cont, path):


   path_ini = path
   arquivos = os.listdir(path_ini)

   # listas onde serão armazenados os dados
   documento = []
   nome = []
   OAB = []
   estado = []


   # iteração de cada arquivo

   for k in range(len(arquivos)):
       print()
       print("------------")
       print('Iteração nº %s'%(k+1))
       filer = os.path.join(path_ini, arquivos[k])

       

       # regex com todas as siglas dos Estados
       rgx_estad = "AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO"
       

       # função de ler o arquivo que retorna uma lista com os textos em frases
       text_prov = ler_arquivo(filer)

       # controle do tamanho para saber se não é imagem
       if len(text_prov) > 2:

         # itera cada linha do texto
          for n in range(len(text_prov)):

            # controle do texto de cada linha para saber se não é espaço em branco ou outros resíduso
            if len(text_prov[n]) > 3:

               # regex para achar os casos que tem número de OAB

               if re.search('OAB(/|-|\s)', text_prov[n], re.IGNORECASE):


                  # limpar o texto do ponto para separar melhor o número da OAB

                  text_ajust = text_prov[n].replace(".","")

                  # separa o número da OAB e o Estado da linha
                  
                  num_oab = re.findall('[0-9]+',text_ajust)
                  estado_oab = re.findall(rgx_estad, text_prov[n])
                  
                  # colocar uma regra do numero da oab ser diferente de vazio
                  ## fazer a regra do excelentíssimo para ver se eh peticao inicial


                  # acrescenta os elementos separados nas listas
                  estado.append(estado_oab)
                  nome.append(text_prov[n])
                  OAB.append(num_oab)
                  documento.append(arquivos[k])


   # Caso não consiga ler, ele move para o diretorio das imagens
       else:
         diret_sepfinal = r'./imagens'
         shutil.move(filer,diret_sepfinal)


   ## acabando os arquivos ele transforma em um DF       

   h = pd.Series(documento)
   i = pd.Series(nome)
   g = pd.Series(OAB)
   p = pd.Series(estado)
   df_coletados = pd.concat([i,g,p,h], axis=1,keys=["Frase","Nº OAB","Estado","Documento"])


   # corta para separar o nome da ação em uma variável própria
   cortados = df_coletados["Documento"].str.split("_", n =1, expand = True)
   df_coletados ["Ação"] = cortados [0]

   # print(df_coletados)


   # transforma num excel verificando se já tinha um arquivo antes e juntando os novos, caso tenha.
   try:
      antigos = pd.read_excel("Pesquisa_redes.xlsx", engine ='openpyxl')
      anterior_certos = pd.concat([antigos,df_coletados])
      # print(df_certos)
      anterior_certos.to_excel("Pesquisa_redes.xlsx", index = False)
   except:
      df_coletados.to_excel("Pesquisa_redes.xlsx", index = False)

   if cont == 1:
      return   
   else:   
      Conversor_OCR()


################################################################################################################

def Conversor_OCR():

   # caminho do tesseract no computador
   pytesseract.tesseract_cmd ='C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


   # Path onde estão as imagens a serem convertidas
   path = r'./imagens'
   files = os.listdir(path)


   # path para onde vão as imagens convertidas de PDF para PNG
   trl = r'./convertidos_PNG'


   # convert as imagens de pdf imagem para um PNG
   for f in range(len(files)):
     if files[f].endswith('.pdf'):
          # print("estamos no",f)
          # print(files[f])
          # print()
          print("------------------")

          nome_pasta = str(files[f][:-4])
          # print(nome_pasta)
          
          # cria uma pasta com o nome do arquivo para depositar as imagens de cada página
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
   path_2 = r'./convertidos_TXT'

   for item in files:
        arqs = os.path.join(path,item)
        pages = os.listdir(arqs)
        textos = []
        for m in range(len(pages)):
             im = os.path.join(arqs,pages[m])
             text = pytesseract.image_to_string(im, lang = 'por')
             textos.append(text)

        texto_final = " ".join(textos)     
        x = open(path_2+'/{}.txt'.format(str(item)), "w+")
        x.write(texto_final)
        x.close()

   Separar_OAB(1, path_2)


Main()