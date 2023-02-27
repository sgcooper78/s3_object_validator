import re, urllib.parse, random
from pathlib import Path

def makeFullStructureSanitize(rootdir,history,filesBool=False,dirsBool=False, verboseBool = False):

    for path in Path(rootdir).iterdir():
        if path.is_symlink():
            if verboseBool:
                print("unlinking symlink")
                print(path)
            path.unlink()
        if path.is_file() and filesBool:
            # history['before']['files'].append(path)
            if needsSanitizing(path):
                if verboseBool:
                    print("changing file")
                    print(path)
                path = sanitize(path)
                # history['after']['files'].append(path)
        elif path.is_dir() and not path.is_symlink():
            if dirsBool:
                # history['before']['dirs'].append(path)
                if needsSanitizing(path):
                    if verboseBool:
                        print("changing dir")
                        print(path)
                    path = sanitize(path)
                    # history['after']['dirs'].append(path)
            makeFullStructureSanitize(path,history,filesBool,dirsBool)


def sanitizeStructure(rootdir,filesBool=False,dirsBool=False, verboseBool = False):
    history = {"before": {"files" : [] , "dirs" : [] }, "after": {"files" : [] , "dirs" : [] }}

    makeFullStructureSanitize(rootdir,history,filesBool,dirsBool,verboseBool)

    if filesBool:
        return { "before" : history['before']['files'], "after" : history['after']['files']}
    if dirsBool:
        return { "before" : history['before']['dirs'], "after" : history['after']['dirs']}
    else:
        return history

def pathExists(pathString):
    path = Path(pathString)
    if path.exists():
        return True
    else:
        return False

def specialCharacters(string):
    # specialChars = ["&","$","@","=",";","/",":","+"," ",",","?"]
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return urllib.parse.quote(string)
    else:
        return string

def avoidCharacters(string):
    # avoidChars = ["{","\^","<","}","%","`","]",">","\[","~","<","#","\\","|"]
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        # string = re.sub(reg, "", string)
        return urllib.parse.quote(string)
    else:
        return string

def hasSpecialCharacters(string):
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return True
    else:
        return False

def hasAvoidCharacters(string):
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        string = re.sub(reg, "", string)
        return True
    else:
        return False

def needsSanitizing(path):
    actualPath = extractActualPath(path)
    if hasAvoidCharacters(actualPath) or hasSpecialCharacters(actualPath):
        return True
    else:
        return False

def extractActualPath(path):
    pathString = str(path).split('/')
    return pathString[-1]
    # actualPath = pathString[-1]
    # return actualPath

def sanitize(path):
    
    pathString = str(path).split('/')
    newActualPath = actualPath = pathString[-1]
    if hasSpecialCharacters(newActualPath):
        newActualPath = specialCharacters(newActualPath)
    if hasAvoidCharacters(newActualPath):
        newActualPath = avoidCharacters(newActualPath)

    if newActualPath == actualPath:
        return path
    pathString[-1] = newActualPath
    newPath = "/".join(pathString)
    if pathExists(newPath):
        randomNumber = str(random.randrange(1, 10000000))
        path.replace(newPath + randomNumber)
        newPathObject = Path(newPath + randomNumber)
    else:
        path.replace(newPath)
        newPathObject = Path(newPath)

    return newPathObject