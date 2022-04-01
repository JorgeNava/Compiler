pythonLexmesTranslationDict = {
  "PR": [{
    "jg": "const",
    "py": None
  },{
    "jg": "int",
    "py": None
  },{
    "jg": "char",
    "py": None
  },{
    "jg": "string",
    "py": None
  },{
    "jg": "bool",
    "py": None
  },{
    "jg": "func",
    "py": "def"
  },{
    "jg": "for",
    "py": "for"
  },{
    "jg": "if",
    "py": "if"
  },{
    "jg": "else",
    "py": "else"
  },{
    "jg": "else if",
    "py": "elif"
  }],
  "op": [{
    "jg": "+",
    "py": "+"
  },{
    "jg": "-",
    "py": "-"
  },{
    "jg": "*",
    "py": "*"
  },{
    "jg": "/",
    "py": "/"
  },{
    "jg": "%",
    "py": "%"
  },{
    "jg": ">",
    "py": ">"
  },{
    "jg": "<",
    "py": "<"
  },{
    "jg": ">=",
    "py": ">="
  },{
    "jg": "==",
    "py": "=="
  },{
    "jg": "!=",
    "py": "!="
  },{
    "jg": "//",
    "py": "//"
  },{
    "jg": "{",
    "py": None
  },{
    "jg": "}",
    "py": None
  },{
    "jg": "(",
    "py": "("
  },{
    "jg": "(",
    "py": "("
  }],
  ";":[{
    "jg": ";",
    "py": None
  }],
  "=":[{
    "jg": "=",
    "py": "="
  }],
  "logicalValue": [{
    "jg": "true",
    "py": "True"
  },{
    "jg": "false",
    "py": "False"
  }],
  "break": [{
    "jg": "break",
    "py": "break"
  }]
}



statement = [
  {
    "type": "rw",
    "value": "int"
  },
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
    "value": "num"
  },
]
typesStatement = "rw id = num ;"
rawStatement = "int myVar = 8;"

translatedTypesStatement = "id = num"
# OUTPUT: id = num / "myVar = 8

# ! JUST FOR ON LINE
for lexeme in statement:
  translatedLexeme = None
  if typesStatement in ["rw id = num ;"]:
    #conseguir contraparte de int, si es None entonces se salta
    # si su contraparte tiene un valor, enotnces se reemplaza por el valor
    valueCounterPart = # Get value from trasnlation dictionary
    if valueCounterPart is not None:
      translatedLexeme["value"] = valueCounterPart
    # append translatedLexeme to a nre list of translatedLexemesInLine