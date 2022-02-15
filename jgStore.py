compilerLexemes = {
  "PR":["const", "int", "float", "char", "string", "bool", "func", "for", "if", "else", "else if", "break"], 
  "op": ["+","-", "*", "/", "%", ">", "<", ">=","<=", "==", "!=", "++", "--", ":", "//", "[","]","{", "}", "(", ")"],
  ";":[";"],
  "=":["="],
  "logicalValue":["true","false"],
  "break":["break"]
  }


statementsList = [
  "rw id ;",
  "break ;",
  "id = false ;",
  "rw id = num ;",
  "rw id = id ;",
  "rw id = id op id ;"
]

