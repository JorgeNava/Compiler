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
  # Ifs
  "rw id op num {": "rw id op num :",
  "rw id op id {": "rw id op id :",
  "rw num op num {": "rw num op num :",
  # Else
  "} rw {": "rw :",
  "rw {": "rw :",
  # Whiles
  "rw logicalValue {": "rw logicalValue :", # If or while
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