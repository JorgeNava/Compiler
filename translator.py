from jgStore import *
from helpers import *

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