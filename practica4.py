from jgFunctions import *  

def printLexemesDetailsList(lexemes):
  for lexeme in lexemesInFile:
    for lexemeKey in lexeme:    
      print(lexemeKey,": ",lexeme[lexemeKey])
    print("==========================")

#lexemesInFile = getLexemesAndIdentifiers("codigo.jg")
lexemesInFile = analyzeSyntax("codigo.jg")
#printLexemesDetailsList(lexemesInFile)
#statements = getStatements(lexemesInFile)
#analyzeStatementsSyntax(statements)











