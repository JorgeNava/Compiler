from analyzer import *
from translator import *

def printLexemesDetailsList(lexemes):
  for lexeme in lexemes:
    for lexemeKey in lexeme:
      print(lexemeKey,": ",lexeme[lexemeKey])
    print("==========================")

# ==========================================================
# ==========================================================
# ====================== MAIN ==============================
# ==========================================================
# ==========================================================

if __name__=="__main__":
  (lexemesInFile, lexemesInLines, errors, unidentified) = analyzeSyntax("codigoConErrores.jg") 
  #printLexemesDetailsList(lexemesInFile)
  if not errors and not unidentified:
    (trasnlatedLexemesInFile, tabsInFile) = translateJGFile(lexemesInLines)
    createFile("codigo.py",trasnlatedLexemesInFile, tabsInFile)
    print("!!! TRANSLATION COMPLETED !!!")
  else:
    print("!!! ERROR WHILE ANALYZING CODE !!!")
    print("Errors in code: ", errors)
    print("Unidentified sentences: ", unidentified)
    print("Error logs file created, please check it.")