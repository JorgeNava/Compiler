lexemesDict = {"PR":["const", "int", "float", "char", "string", "bool", "func", "for", "if", "else", "else if", "dict", "break"], 
"op": ["=", "+","-", "*", "/", "%", ">", "<", ">=","<=", "==", "!=", "++", "--", ":", ";", "//", "[","]","{", "}", "(", ")"]}

def getJgFileAsCleanedLines(filePath):
    f = open(filePath, "r")
    lines = f.readlines()
    return lines

def getLexemData(lexeme, line):
  return {
      "value": lexeme,
      "lexemeType": getLexemeType(lexeme),
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
            if formingLexem not in lexemesDict["PR"] and formingLexem not in lexemesDict["op"]:
              if symbol in lexemesDict["op"]:
                lexemes.append(getLexemData(symbol, actLineNum))    # ADD OPERATORS
                lexemes.append(getLexemData(formingLexem, actLineNum))    # ADD IDENTIFIERS
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
  if lexeme in lexemesDict["PR"]:
    return "Reserved Word"
  elif lexeme in lexemesDict["op"]:
    return "Operator"
  elif lexeme.isnumeric():
    return "Number"
  elif lexeme and lexeme[0].isalpha() and lexeme.isalnum() :
    return "Identifier"
  else:
    return "Error"
    
def printLexemesDetailsList(lexemes):
  for lexeme in lexemesInFile:
    for lexemeKey in lexeme:    
      print(lexemeKey,": ",lexeme[lexemeKey])
    print("==========================")
      
# ==========================================================

lexemesInFile = getLexemesAndIdentifiers("D:\\UAG\\11_Cuatrimestre\\Compiladores\\Primer Parcial\\Practicas\\Practicas 3\\codigo.jg")
printLexemesDetailsList(lexemesInFile)














