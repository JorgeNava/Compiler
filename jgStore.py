compilerLexemes = {
  "PR":["const", "int", "float", "char", "string", "bool", "func", "for", "if", "else", "else if"], 
  "op": ["+","-", "*", "/", "%", ">", "<", ">=","<=", "==", "!=", "//","{", "}", "(", ")"],
  ";":[";"],
  "=":["="],
  "logicalValue":["true","false"],
  "break":["break"]
  }

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

pythonStatementsTranslationDict = {  
  "rw id ;": None,
  "break ;": "break",
  "id = false ;": "id = False",
  "rw id = num ;": "id = num",
  "rw id = id ;": "id = id",
  "rw id = id op id ;": "id = id op id"
}


statementsList = [
  "rw id ;",
  "break ;",
  "id = false ;",
  "rw id = num ;",
  "rw id = id ;",
  "rw id = id op id ;"
]