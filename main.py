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

def formatErrorLog(error):
  RET_VAL = "> Error:\nError type: " + error["type"] + "\nDetected Statement: " + error["detectedStatement"] + "\nRaw Statement: " + error["rawStatement"]+ "\nLine: " + str(error["line"]) + "\n\n"  
  return str(RET_VAL)

def getLexemeType(lexeme):
  if lexeme == "break":
    return "break"
  elif lexeme in compilerLexemes["PR"]:
    return "rw"
  elif lexeme in compilerLexemes["op"]:
    return "op"
  elif lexeme.isnumeric():
    return "num"
  elif lexeme == "true" or lexeme == "false":
    return lexeme
  elif lexeme in compilerLexemes[";"]:
    return ";"
  elif lexeme in compilerLexemes["="]:
    return "="
  elif lexeme and lexeme[0].isalpha() and lexeme.isalnum() :
    return "id"
  else:
    return "error"
    
def analyzeSyntax(filePath):
  correctStatements = 0
  errorStatements = 0
  incorrectStatements = 0
  actLineNum = 0
  formingLexem = ""
  insideString = False
  errorLogs = []
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
          if symbol in compilerLexemes["op"] or symbol == ";" or symbol == "=":
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
          if symbol == ";":
            lexemes.append(getLexemData(formingLexem, actLineNum))    # ADD IDENTIFIERS
            lexemesInLine.append(getLexemData(formingLexem, actLineNum))
            lexemes.append(getLexemData(symbol, actLineNum))    # ADD OPERATORS
            lexemesInLine.append(getLexemData(symbol, actLineNum))
            formingLexem = ""
          lexemes.append(getLexemData(formingLexem, actLineNum)) # ADD RESERVE WORDS
          lexemesInLine.append(getLexemData(formingLexem, actLineNum))
          formingLexem = ""  
    lexemesInLine = [lexeme for lexeme in lexemesInLine if not (lexeme['value'] == "")]
    analyzeResult = analyzeStatementSyntax(lexemesInLine)
    #print(lexemesInLine)
    if (analyzeResult["state"] == "correct"):
      correctStatements += 1
    if (analyzeResult["state"] == "error"):
      errorStatements += 1
      errorLogs.append(analyzeResult)
    if (analyzeResult["state"] == "unidentified"):
      incorrectStatements += 1
  print("correctStatements: ",correctStatements)
  print("errorStatements: ",errorStatements)
  print("unidentifiedStatements: ",incorrectStatements)

  # Create error logs file
  f = open("errorLogs.txt","w+")
  for error in errorLogs:
    f.write(formatErrorLog(error))
  f.write("~ Happy debugging :D ~")
  f.close()
  
  return [lexeme for lexeme in lexemes if not (lexeme['value'] == "")]

def analyzeStatementSyntax(lexemesInLine):
  statement = ""
  rawStatement = ""
  # get line statement
  # STATEMENT EXAMPLE: rw id;
  LEXEME_LINE = lexemesInLine[0]["line"]
  for lexeme in lexemesInLine:
    statement += " "+lexeme["type"]
    rawStatement += " "+lexeme["value"]

  print("statement: ",statement)

  #check if statement is in statement list  
  if statement.strip() in statementsList:
    print("=== MATCHED STATEMENT ===")
    analysisResult = {
        "state": "correct"
    }
  else:
    #TBD: Pasamos de lexema en lexema del statement y descartamos primero viendo si es una constante o no,
    """
      Definir lista de palabras que pueden ser constantes, si no esta en la
      lista de statements, buscamos el primer tipo de lexema que encontremos en el statement
      con el del primero del statement. si no pasamos al siguiente grupo de lexemas-
      
      Pasamos de lexema en lexema del statement y descartamos primero viendo si es una constante o no,
      si no es un tipo de constante (osea un tipo de lexema) entonces buscamosa que tipo de lexema
      pertenece si existe en alguno entonces es correcto y se procede con el siguiente elemento de la lista de
      lexemas en el statement.
    """


    # ERRORS DETECTION ZONE
    if (statement.strip().startswith('break') or statement.strip().startswith("id = false") or statement.strip().startswith("rw id")) and not lexemesInLine[-1]["value"].endswith("{"):
      print("=== ERROR STATEMENT ===")
      analysisResult = {
        "state": "error",
        "type": "Missing ';' in statement",
        "line": LEXEME_LINE,
        "detectedStatement": statement,
        "rawStatement": rawStatement
      }
    # HERE WE SHOULD SET THE REST OF ERRORS TO RECOGNIZE
    else:
      print("=== UNIDETIFIED STATEMENT ===")
      analysisResult = {
        "state": "unidentified"
      }
  return analysisResult


# ==========================================================
# ==========================================================
# ====================== MAIN ==============================
# ==========================================================
# ==========================================================

def printLexemesDetailsList(lexemes):
  for lexeme in lexemes:
    for lexemeKey in lexeme:    
      print(lexemeKey,": ",lexeme[lexemeKey])
    print("==========================")


if __name__=="__main__":
  #lexemesInFile = getLexemesAndIdentifiers("codigo.jg") [DEPRECATED]
  lexemesInFile = analyzeSyntax("codigoConErrores.jg")
  #printLexemesDetailsList(lexemesInFile)
