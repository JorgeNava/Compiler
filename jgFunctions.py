from jgStore import *  

def getJgFileAsCleanedLines(filePath):
    f = open(filePath, "r")
    lines = f.readlines()
    return lines

def getLexemData(lexeme, line):
  return {
      "value": lexeme,
      "type": getLexemeType(lexeme),
      "line": line,
    }  

def getLexemesAndIdentifiers(filePath):
    actLineNum = 0
    formingLexem = ""
    insideString = False
    lexemes = []
    for line in getJgFileAsCleanedLines(filePath): 
      actLineNum += 1
      lineIndex = 0
      for symbol in line:
          lineIndex += 1
          formingLexem = formingLexem.strip()
          if insideString == False: #TO-DO: Implement functionality   
            if formingLexem not in compilerLexemes["PR"] and formingLexem not in compilerLexemes["op"]:
              if symbol in compilerLexemes["op"]:
                lexemes.append(getLexemData(formingLexem, actLineNum))    # ADD IDENTIFIERS
                lexemes.append(getLexemData(symbol, actLineNum))    # ADD OPERATORS
                formingLexem = ""
              elif symbol.isspace():
                lexemes.append(getLexemData(formingLexem, actLineNum))
                formingLexem = ""
              elif actLineNum == len(getJgFileAsCleanedLines(filePath)) and lineIndex == len(line):
                lexemes.append(getLexemData(formingLexem + symbol, actLineNum))
              else:
                formingLexem += symbol
            else:
              lexemes.append(getLexemData(formingLexem, actLineNum)) # ADD RESERVE WORDS
              formingLexem = ""
    return [lexeme for lexeme in lexemes if not (lexeme['value'] == "")]

def getLexemeType(lexeme):
  if lexeme in compilerLexemes["PR"]:
    return "rw"
  elif lexeme in compilerLexemes["op"]:
    return "op"
  elif lexeme.isnumeric():
    return "num"
  elif lexeme == "true" or lexeme == "false":
    return lexeme
  elif lexeme and lexeme[0].isalpha() and lexeme.isalnum() :
    return "id"
  else:
    return "error"
    
def analyzeSyntax(filePath):
  correctStatements = 0
  incorrectStatements = 0
  actLineNum = 0
  formingLexem = ""
  insideString = False
  lexemes = []
  for line in getJgFileAsCleanedLines(filePath): 
    lexemesInLine = []
    actLineNum += 1
    lineIndex = 0
    for symbol in line:
      lineIndex += 1
      statement = ""
      formingLexem = formingLexem.strip()
      if insideString == False: #TO-DO: Implement functionality   
        if formingLexem not in compilerLexemes["PR"] and formingLexem not in compilerLexemes["op"]:
          if symbol in compilerLexemes["op"]:
            lexemes.append(getLexemData(formingLexem, actLineNum))    # ADD IDENTIFIERS
            lexemesInLine.append(getLexemData(formingLexem, actLineNum))
            lexemes.append(getLexemData(symbol, actLineNum))    # ADD OPERATORS
            lexemesInLine.append(getLexemData(symbol, actLineNum))
            formingLexem = ""
          elif symbol.isspace():
            lexemes.append(getLexemData(formingLexem, actLineNum))
            lexemesInLine.append(getLexemData(formingLexem, actLineNum))
            formingLexem = ""
          elif actLineNum == len(getJgFileAsCleanedLines(filePath)) and lineIndex == len(line):
            lexemes.append(getLexemData(formingLexem + symbol, actLineNum))
            lexemesInLine.append(getLexemData(formingLexem, actLineNum))
          else:
            formingLexem += symbol
        else:
          lexemes.append(getLexemData(formingLexem, actLineNum)) # ADD RESERVE WORDS
          lexemesInLine.append(getLexemData(formingLexem, actLineNum))
          formingLexem = ""  
    analyzeResult = analyzeStatementSyntax(lexemesInLine)
    if (analyzeResult == "correct"):
      correctStatements += 1
    if (analyzeResult == "incorrect"):
      incorrectStatements += 1
  print("correctStatements: ",correctStatements)
  print("incorrectStatements: ",incorrectStatements)
  return [lexeme for lexeme in lexemes if not (lexeme['value'] == "")]

def analyzeStatementSyntax(lexemesInLine):
  statement = ""
  analyzeResult = ""
  # get line statement
  for lexeme in lexemesInLine:
    statement += " "+lexeme["type"]

  #check if statement is in statement list  
  if statement in statementsList:
    print("=== MATCHED STATEMENT ===")
    analysisResult = "correct"
  else:
    """
      Definir lista de palabras que pueden ser constantes, si no esta en la
      lista de statements, buscamos el primer tipo de lexema que encontremos en el statement
      con el del primero del statement. si no pasamos al siguiente grupo de lexemas-
      Pasamos de lexema en lexema del statement y descartamos primero viendo si es una constante o no,
      si no es un tipo de constante (osea un tipo de lexema) entonces buscamosa que tipo de lexema
      pertenece si existe en alguno entonces es correcto y se procede con el siguiente elemento de la lista de
      lexemas en el statement.
    """
    
    print("=== ERROR STATEMENT ===")
    analysisResult = "incorrect"
  return analysisResult


# ==========================================================