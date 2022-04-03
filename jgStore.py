compilerLexemesStore = {
  "PR":["const", "int", "float", "char", "string", "bool", "func", "for", "if", "else", "else if"], 
  "op": ["+","-", "*", "/", "%", ">", "<", ">=","<=", "==", "!=", "//","{", "}", "(", ")"],
  ";":[";"],
  "=":["="],
  "logicalValue":["true","false"],
  "break":["break"]
  }

pythonLexmesTranslationStore = {
  # Lexemes with equivalents in Python
  "func": "def",
  "for": "for",
  "if": "if",
  "else": "else",
  "else if": "elif",
  "true": "True",
  "false": "False",
  "break": "break",
  "//": "#",
  # Lexemes where equivalents are the same in Python
  "+": "+",
  "-": "-",
  "*": "*",
  "/": "/",
  "%": "%",
  ">": ">",
  "<": "<",
  ">=": ">=",
  "<=": "<=",
  "==": "==",
  "!=": "!=",
  "(": "(",
  ")": ")",
  "=": "=",
  # Lexemes with no equivalents in Python
  "const": None,
  "int": None,
  "char": None,
  "string": None,
  "bool": None,
  "{": None,
  "}": None,
  ";": None,
}

pythonStatementsTranslationStore = {  
  "rw id ;": None,
  "break ;": "break",
  "id = false ;": "id = False",
  "id = true ;": "id = True",
  "rw id = num ;": "id = num",
  "rw id = id ;": "id = id",
  "rw id = id op id ;": "id = id op id",
  "rw rw id = num ; id op = num ; id op op op": "rw id rw range ( id ) :", #for i in range(i):
  "rw id op num op": "rw id op num :", #if myAge > 18:
  "rw op": "rw :", #else:
}


statementsStore = [
  "rw id ;",
  "break ;",
  "id = false ;",
  "rw id = num ;",
  "rw id = id ;",
  "rw id = id op id ;",
  "rw rw id = num ; id op = num ; id op op op",
  "rw id op num op",
  "rw op"
]