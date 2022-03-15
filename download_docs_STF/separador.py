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
import time



##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

# função de separação dos primeiros documentos de cada ação - não tem utilidade nesse processo - 
# está aqui para guardar em caso de necessidade de processos adicionais de manuseio das pastas das ações de controle concentrado


def Separar_primeiros_documentos():
   
   # lista as pastas
   
   path = input("digite o path: ")
   pastas = os.listdir(path)

   # lista os arquivos dentro das pastas
   
   for pasta in pastas:
      path_arquivos = os.path.join(path, pasta)
      arquivos = os.listdir(path_arquivos)

      # Separa o primeiro documento de cada pasta
      
      for arquivo in arquivos:
         if "documento_0" in str(arquivo):

            #faz uma cópia dos primeiros artigos de cada pasta

            path_arquivo = os.path.join(path_arquivos,arquivo)
            diret_semifinal = r'C:\Users\saylo\Desktop\prov'
            shutil.copy(path_arquivo, diret_semifinal)
            diret_final = r'C:\Users\saylo\Desktop\separados_teste'
            diret = os.listdir(diret_semifinal)

            # move os primeiros arquivos de cada pasta das ações para uma outra pasta
            for item in diret:
               nome_final = str(pasta)+"_"+str(arquivo)
               os.rename(os.path.join(diret_semifinal,item),nome_final)
               shutil.move(nome_final,diret_final)


#######################################################  !!! ####################################################################

Separar_primeiros_documentos()