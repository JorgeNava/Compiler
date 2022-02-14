# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:09:10 2022

@author: Jorge Nava y Gustavo Garcia

las	3
manzanas	1
son	1
frutas 1
preferidas	1
de	1
maestras
"""

def printLexemasCount(file_path, divider):
  f = open(file_path, "r")
  text = f.read()
  splitted_text = text.split(divider)
  
  lexemes_count = {}
  
  for word in splitted_text:
    if word in lexemes_count:
      lexemes_count[word] += 1 
    else:
      lexemes_count[word] = 1
  print(lexemes_count)
  
printLexemasCount("./archivos/practica1Lexemas.txt", "s")