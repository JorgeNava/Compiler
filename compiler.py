import json
from jgStore import *
from helpers import *
from analyzer import *

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
  RET_VAL = "> Error "
  RET_VAL +=  dictToFormattedString(error) + "\n"
  return str(RET_VAL)

def getLexemeType(lexeme):
  """
  if lexeme == "break":
    return "break"
  elif lexeme in compilerLexemesStore[";"]:
    return ";"
  elif lexeme in compilerLexemesStore["="]:
    return "="
  """
  if lexeme in compilerLexemesStore["PR"]:
    return "rw"
  elif lexeme in compilerLexemesStore["op"]:
    return "op"
  elif lexeme.isnumeric():
    return "num"
  elif lexeme == "true" or lexeme == "false":
    return "logicalValue"
  elif lexeme in compilerLexemesStore["exceptions"]:
    return lexeme
  elif lexeme in compilerLexemesStore["builtInFunction"]:
    return "builtInFunction"
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
    skipNext = False
    for idx, symbol in enumerate(line):
      lineIndex += 1
      formingLexem = formingLexem.strip()
      if insideString == False and skipNext == False: #TO-DO: Implement functionality   
        if formingLexem not in compilerLexemesStore["PR"] and formingLexem not in compilerLexemesStore["op"]:
          #if symbol in compilerLexemesStore["op"] or symbol == ";" or symbol == "=":
          if symbol in compilerLexemesStore["op"] or symbol in compilerLexemesStore["exceptions"]:
            lexemes.append(getLexemData(formingLexem, actLineNum))    # ADD IDENTIFIERS
            lexemesInLine.append(getLexemData(formingLexem, actLineNum))
            if (symbol == ">" or symbol == "<") and line[idx+1] == "=":
              lexemes.append(getLexemData(symbol + "=", actLineNum))    # ADD OPERATORS
              lexemesInLine.append(getLexemData(symbol + "=", actLineNum))
              skipNext = True
            else:  
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
      else:
        skipNext = False

    lexemesInLine = [lexeme for lexeme in lexemesInLine if not (lexeme['value'] == "")]
    lexemesInLines.append(lexemesInLine)
    analyzeResult = analyzeStatementSyntax(lexemesInLine)
    #print(lexemesInLine)
    if (analyzeResult["state"] == "correct"):
      correctStatements += 1
    if (analyzeResult["state"] == "error"):
      errorStatements += 1
      errorLogs.append(analyzeResult)
    if (analyzeResult["state"] == "unidentified"):
      incorrectStatements += 1

  # Create error logs file
  f = open("errorLogs.txt","w+")
  for error in errorLogs:
    f.write(formatErrorLog(error))
  f.write("~ Happy debugging :D ~")
  f.close()
  return ([lexeme for lexeme in lexemes if not (lexeme['value'] == "")], lexemesInLines, errorStatements, incorrectStatements)

def analyzeStatementSyntax(lexemesInLine):
  statement = ""
  rawStatement = ""
  LEXEME_LINE = lexemesInLine[0]["line"]
  for lexeme in lexemesInLine:
    statement += " "+lexeme["type"]
    rawStatement += " "+lexeme["value"]

  if statement.strip() in pythonStatementsTranslationStore:
    analysisResult = {
        "state": "correct"
    }
  else:
    analysisResult = {
      "state": "error",
      "line": LEXEME_LINE,
      "detectedStatement": statement,
      "rawStatement": rawStatement
    }

    identifiedErrors = identifyError(statement.strip())
    if identifiedErrors["len"] >= 1:
      topSimilarStatment = identifiedErrors["possibleStatments"][identifiedErrors["topSimilarStatmentIndex"]]
      analysisResult["message"] = topSimilarStatment["message"] + " in line " + str(LEXEME_LINE)
      analysisResult["condifence"] = topSimilarStatment["similarityRatio"]
      analysisResult["expectedStatement"] = topSimilarStatment["statement"]
    else:
      analysisResult = {
        "state": "unidentified",
        "line": LEXEME_LINE,
        "detectedStatement": statement,
        "rawStatement": rawStatement
      }

  return analysisResult


def translateJGFile(lexemesInLines):
  tabsCounter = 0
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

  tabsInFile = []
  for statement in lexemesInLines:
    tabsCounter = updateTabsCounter(statement, tabsCounter)
    tabsInFile.append(tabsCounter)
    (rawStatement, typesStatement) = getLexemesTokensInLine(statement)
    translatedLexemesInLine = getTranslatedLexemesInLine(statement)
    (rawTranslatedStatement, typesTranslatedStatement) = getLexemesTokensInLine(translatedLexemesInLine)
    pythonStatements.append(rawTranslatedStatement)
  
  return (pythonStatements, tabsInFile)

def getTranslatedLexemesInLine(statement):
  translatedLexemesInLine = []
  (rawStatement, typesStatement) = getLexemesTokensInLine(statement)
  if typesStatement in pythonStatementsTranslationStore and pythonStatementsTranslationStore[typesStatement] is not None: 
    for lexeme in statement:
      lexemeCounterPart = {"type": lexeme["type"]}
      if lexeme["type"] in ["id", "num", "builtInFunction"]:
        lexemeCounterPart["value"] = lexeme["value"]
      elif lexeme["value"] in pythonLexmesTranslationStore:
        lexemeCounterPart["value"] = pythonLexmesTranslationStore[lexeme["value"]]
      else:
        lexemeCounterPart = None
        error(lexeme["value"] + " not founded in pythonLexmesTranslationStore. Line: " + str(lexeme["line"]))

      if lexemeCounterPart is not None:
        translatedLexemesInLine.append(lexemeCounterPart)
  else:
    warning(typesStatement + " not founded in pythonStatementsTranslationStore or its translation is None")
  return translatedLexemesInLine

def getLexemesTokensInLine(statement):    
  rawStatement =  ""
  typeStatement =  ""
  for lexeme in statement:
    if lexeme["value"] is not None:
      rawStatement += lexeme["value"] + " "
      typeStatement += lexeme["type"] + " "
  return (rawStatement.strip(), typeStatement.strip())

def updateTabsCounter(statement, tabsCounter):
  for lexeme in statement:
    if lexeme["value"] == "{": 
      tabsCounter += 1
    elif lexeme["value"] == "}":
      tabsCounter -= 1
  return tabsCounter

def createFile(filename, fileContentList, tabsInFile):
  f = open(filename,"w+")
  tabsInNextLine = 0
  for idx, lineContent in enumerate(fileContentList):
    if lineContent:
      if lineContent.startswith("else"):
        content = ''.join(["\t"*(tabsInFile[idx-1]-1)]) + lineContent + "\n"
      else:
        content = ''.join(["\t"*(tabsInFile[idx-1])]) + lineContent + "\n"
      f.write(content)
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