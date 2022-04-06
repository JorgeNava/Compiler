"""
";":[";"],
"=":["="],
"{": ["{"],
"}": ["}"],
"break":["break"]
"""
compilerLexemesStore = {
  "PR":["const", "int", "float", "char", "string", "bool", "func", "for", "while", "if", "else", "else if"], 
  "op": ["+","-", "*", "/", "%", ">", "<", ">=","<=", "==", "!=", "//", "(", ")"],
  "exceptions": [";", "=", "{", "}", "break"],
  "logicalValue": ["true","false"],
  "builtInFunction": ["print"]
  }

pythonLexmesTranslationStore = {
  # Lexemes with equivalents in Python
  "func": "def",
  "for": "for",
  "while": "while",
  "if": "if",
  "else": "else",
  "else if": "elif",
  "true": "True",
  "false": "False",
  "break": "break",
  "//": "#",
  "{": ":",
  "print": "print($$$)",
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
  "}": None,
  ";": None,
}

pythonStatementsTranslationStore = {  
  "rw id ;": None,
  "break ;": "break",
  # Declarations
  "rw id = num ;": "id = num",
  "rw id = id ;": "id = id",
  # Assignations
  "id = logicalValue ;": "id = logicalValue",
  "id = id ;": "id = id",
  "id = num ;": "id = num",
  "id = id op id ;": "id = id op id",
  "id = id op num ;": "id = id op num",
  "id = num op id ;": "id = num op id",
  "id = num op num ;": "id = num op num",
  # For
  "for int id = num ; id op = num ; id op op {": "for id in range ( id ) :",
  # Ifs
  "rw id op num {": "rw id op num :", #if myAge > 18:
  "rw id op id {": "rw id op id :",
  "rw logicalValue {": "rw logicalValue :",
  "rw num op num {": "rw num op num :",
  # Else
  "} rw {": "rw :",
  "rw {": "rw :",
  # Whiles
  "rw logicalValue {": "rw logicalValue :",
  "rw id op id {": "rw id op id :",
  "rw id op num {": "rw id op num :",
  "rw num op id {": "rw num op id :",
  "rw num op num {": "rw num op num:",
  # Built-in funcitons
  "builtInFunction op id op ;": "builtInFunction ( id )", 
  "builtInFunction op num op ;": "builtInFunction ( num )", 
  # Others
  "}": None,
}


statementsStore = [
  # declarations
  "rw id ;",
  "rw id = num ;",
  "rw id = id ;",
  "rw id = id op id ;",
  # break
  "exceptions ;",
  #"break ;",
  # assignations
  "id = logicalValue ;",
  #for
  "rw rw id = num ; id op = num ; id op op {",
  # while / if
  "rw id op num {",
  "rw op"
  # built-in functions
  "builtInFunctions id",
  "builtInFunctions num",
]