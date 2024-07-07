import os
def ValidFile(FileDir):
    return os.path.isdir(os.path.dirname(str(FileDir).strip()))