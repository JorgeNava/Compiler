from difflib import SequenceMatcher, ndiff
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
  RET_VAL = "> Error "
  RET_VAL +=  dictToFormattedString(error) + "\n"
  return str(RET_VAL)

def getLexemeType(lexeme):
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
      if insideString == False and skipNext == False: 
        if formingLexem not in compilerLexemesStore["PR"] and formingLexem not in compilerLexemesStore["op"]:
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

def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()

def identifyError(statment):
  MINIMUM_SIMILARITY_RATIO = 0.80
  similarStatements = []
  topSimilarStatmentIndex = 0
  for correctStatement in pythonStatementsTranslationStore:
    similarityRatio = similar(statment, correctStatement)
    if similarityRatio >= MINIMUM_SIMILARITY_RATIO:
      for i,s in enumerate(ndiff(statment, correctStatement)):
        if s[0]==' ': continue
        if s[-1] == " " or abs(len(correctStatement) - len(statment)) >= 4: 
          message = "Expected statement: '" + correctStatement + "'"
        elif s[0]=='-':
          message = "Delete '" + s[-1] + "' from position " + str(i)
        elif s[0]=='+':
          message = "Add '" + s[-1] + "' to position " + str(i)
      for idx, possibleStatments in enumerate(similarStatements):
        if similarityRatio > possibleStatments["similarityRatio"]:
          topSimilarStatmentIndex = len(similarStatements)
        else:
          topSimilarStatmentIndex = idx
      similarStatements.append({
        "statement": correctStatement,
        "similarityRatio": similarityRatio,
        "message": message
      })
  return {
    "len": len(similarStatements),
    "possibleStatments": similarStatements,
    "topSimilarStatmentIndex": topSimilarStatmentIndex
  }


# ==========================================================
# ==========================================================
# ====================== MAIN ==============================
# ==========================================================
# ==========================================================

if __name__=="__main__":
  testStatements = [
    "rw id = num",
    "rw logicalValue",
    "break",
    "builtInFunction id",
    "id = id num ;"
  ]
  for statement in testStatements:
    rslt = identifyError(statement)
    if rslt["len"] >= 1:
      print("=====")
      print("FOR:", statement)
      print(rslt["possibleStatments"][rslt["topSimilarStatmentIndex"]])
      print("=====")
    else:
      print(">Error: No similar statement founded")