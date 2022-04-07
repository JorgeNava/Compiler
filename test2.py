from difflib import SequenceMatcher, ndiff
from jgStore import *
from helpers import *

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
        if s[-1] == " ": 
          message = "Expected statement: " + correctStatement
        elif s[0]=='-':
          message = "Delete " + s[-1] + " from position " + str(i)
        elif s[0]=='+':
          message = "Add " + s[-1] + " to position " + str(i)
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