from jgStore import *  
from helpers import *  

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
  elif lexeme in compilerLexemesStore["PR"]:
    return "rw"
  elif lexeme in compilerLexemesStore["op"]:
    return "op"
  elif lexeme.isnumeric():
    return "num"
  elif lexeme == "true" or lexeme == "false":
    return lexeme
  elif lexeme in compilerLexemesStore[";"]:
    return ";"
  elif lexeme in compilerLexemesStore["="]:
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
  lexemesInLines = []
  for line in getJgFileAsCleanedLines(filePath): 
    lexemesInLine = []
    actLineNum += 1
    lineIndex = 0
    for symbol in line:
      lineIndex += 1
      statement = ""
      formingLexem = formingLexem.strip()
      if insideString == False: #TO-DO: Implement functionality   
        if formingLexem not in compilerLexemesStore["PR"] and formingLexem not in compilerLexemesStore["op"]:
          if symbol in compilerLexemesStore["op"] or symbol == ";" or symbol == "=":
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
    lexemesInLines.append(lexemesInLine)
    analyzeResult = analyzeStatementSyntax(lexemesInLine)
    ##print(lexemesInLine)
    if (analyzeResult["state"] == "correct"):
      correctStatements += 1
    if (analyzeResult["state"] == "error"):
      errorStatements += 1
      errorLogs.append(analyzeResult)
    if (analyzeResult["state"] == "unidentified"):
      incorrectStatements += 1
  #print("correctStatements: ",correctStatements)
  #print("errorStatements: ",errorStatements)
  #print("unidentifiedStatements: ",incorrectStatements)

  # Create error logs file
  f = open("errorLogs.txt","w+")
  for error in errorLogs:
    f.write(formatErrorLog(error))
  f.write("~ Happy debugging :D ~")
  f.close()
  return ([lexeme for lexeme in lexemes if not (lexeme['value'] == "")], lexemesInLines)

def analyzeStatementSyntax(lexemesInLine):
  statement = ""
  rawStatement = ""
  # get line statement
  # STATEMENT EXAMPLE: rw id;
  LEXEME_LINE = lexemesInLine[0]["line"]
  for lexeme in lexemesInLine:
    statement += " "+lexeme["type"]
    rawStatement += " "+lexeme["value"]

  ##print("statement: ",statement)

  #check if statement is in statement list  
  if statement.strip() in statementsStore:
    #print("=== MATCHED STATEMENT ===")
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
      #print("=== ERROR STATEMENT ===")
      analysisResult = {
        "state": "error",
        "type": "Missing ';' in statement",
        "line": LEXEME_LINE,
        "detectedStatement": statement,
        "rawStatement": rawStatement
      }
    # HERE WE SHOULD SET THE REST OF ERRORS TO RECOGNIZE
    else:
      #print("=== UNIDETIFIED STATEMENT ===")
      analysisResult = {
        "state": "unidentified"
      }
  return analysisResult


def translateJGFile(lexemesInLines):
  pythonStatements = []
  statement = ""
  rawStatement = ""
  typeStatements = []
  rawStatements = []
  newLine = False
  for lexemeInLine in lexemesInLines:
    for lexeme in lexemeInLine:
      if newLine:
        typeStatements.append(statement.strip())
        rawStatements.append(rawStatement.strip())
        statement = ""
        rawStatement = ""
        newLine = False
      statement += " "+lexeme["type"]
      rawStatement += " "+lexeme["value"]
      if len(lexemesInLines) == lexeme["line"]:
        typeStatements.append(statement.strip())
        rawStatements.append(rawStatement.strip())
    newLine = True

  for statement in lexemesInLines:
    (rawStatement, typesStatement) = getLexemesTokensInLine(statement)
    translatedLexemesInLine = getTranslatedLexemesInLine(statement)
    (rawTranslatedStatement, typesTranslatedStatement) = getLexemesTokensInLine(translatedLexemesInLine)
    pythonStatements.append(rawTranslatedStatement)
  
  return pythonStatements

def getTranslatedLexemesInLine(statement):
  translatedLexemesInLine = []
  (rawStatement, typesStatement) = getLexemesTokensInLine(statement)
  if typesStatement in pythonStatementsTranslationStore and pythonStatementsTranslationStore[typesStatement] is not None: 
    for lexeme in statement:
      lexemeCounterPart = {"type": lexeme["type"]}
      if lexeme["type"] in ["id", "num"]:
        lexemeCounterPart["value"] = lexeme["value"]
      elif lexeme["value"] in pythonLexmesTranslationStore:
        lexemeCounterPart["value"] = pythonLexmesTranslationStore[lexeme["value"]]
      else:
        lexemeCounterPart = None
        error(lexeme["value"] + " not founded in pythonLexmesTranslationStore")

      if lexemeCounterPart is not None:
        translatedLexemesInLine.append(lexemeCounterPart)
  else:
    error(typesStatement + " not founded in pythonLexmesTranslationStore or its translation is None")
  return translatedLexemesInLine

def getLexemesTokensInLine(statement):    
  rawStatement =  ""
  typeStatement =  ""
  for lexeme in statement:
    if lexeme["value"] is not None:
      rawStatement += lexeme["value"] + " "
      typeStatement += lexeme["type"] + " "
  return (rawStatement.strip(), typeStatement.strip())

def createFile(filename, fileContentList):
  f = open(filename,"w+")
  for lineContent in fileContentList:
    if lineContent:
      f.write(lineContent + "\n")
  f.close()

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
  (lexemesInFile, lexemesInLines) = analyzeSyntax("codigo.jg") 
  trasnlatedLexemesInFile = translateJGFile(lexemesInLines)
  createFile("codigo.py",trasnlatedLexemesInFile)
  print("!!! TRANSLATION COMPLETED !!!")


"""
  TBD 
  * Agregar soporte para tabulaciones basadas en las '{' y sustituir por ':' (NAVA)
  * Agregar soporte para for, if/else
    * Hacer la gramatica y agregarla a las tiendas de diccionarios (GUS)
    * Agregar funcionalidad en traduccion de codigo de for, if/else (NAVA)
"""