import json

def log(message, id = ""):
  print("[INFO]",str(id),message)

def error(message, id = ""):
  print("[ERROR]",str(id),message)

def warning(message, id = ""):
  print("[Warning]",str(id),message)

def printDict(dict, id = ""):
  print(str(id), json.dumps(dict, indent=4, sort_keys=True))

def dictToFormattedString(dict):
  return json.dumps(dict, indent=4, sort_keys=True)