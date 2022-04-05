from jgStore import *
from helpers import *

statement = [
  {
    "type": "id",
    "value": "myVar"
  },
  {
    "type": "=",
    "value": "="
  },
  {
    "type": "num",
    "value": "8"
  },
  {
    "type": "op",
    "value": "/"
  },
  {
    "type": "num",
    "value": "8"
  },
  {
    "type": ";",
    "value": ";"
  },
]

# INPUT:  rw id op num op / if myAge > 18 {
# OUTPUT: rw id op num op / if myAge > 18 :


def getTranslatedLexemesInLine(statement):
  translatedLexemesInLine = []
  (rawStatement, typesStatement) = getLexemesTokensInLine(statement)
  if typesStatement in pythonStatementsTranslationStore: 
    for lexeme in statement:
      lexemeCounterPart = {"type": lexeme["type"]}
      if lexeme["type"] in ["id", "num"]:
        lexemeCounterPart["value"] = lexeme["value"]
      elif lexeme["value"] in pythonLexmesTranslationStore:
        lexemeCounterPart["value"] = pythonLexmesTranslationStore[lexeme["value"]]
      else:
        lexemeCounterPart = None
        error(lexeme["value"] + " not founded in pythonLexmesTranslationStore. Line: " + str(lexeme["line"]))

      if lexemeCounterPart is not None:
        translatedLexemesInLine.append(lexemeCounterPart)
  else:
    error(typesStatement + " not founded in pythonStatementsTranslationStore or its translation is None")
  return translatedLexemesInLine

def getLexemesTokensInLine(statement):    
  rawStatement =  ""
  typeStatement =  ""
  for lexeme in statement:
    if lexeme["value"] is not None:
      rawStatement += lexeme["value"] + " "
      typeStatement += lexeme["type"] + " "
  return (rawStatement.strip(), typeStatement.strip())

(rawStatement, typesStatement) = getLexemesTokensInLine(statement)

translatedLexemesInLine = getTranslatedLexemesInLine(statement)
(rawTranslatedStatement, typesTranslatedStatement) = getLexemesTokensInLine(translatedLexemesInLine)

log("rawStatement: " + rawStatement)
log("translatedRawStatement: " + rawTranslatedStatement)