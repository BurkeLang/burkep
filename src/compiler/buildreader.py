import xmltodict
import io

class BuildReader:
    def __init__(self,BuildFile: str):
        self.BuildFile = BuildFile
    def ReadFile(self):
        with io.open(self.BuildFile,"r") as BuildFileReader:
            self.FileContents = BuildFileReader.read()
            BuildFileReader.close()
    def ToDict(self):
        return xmltodict.parse(self.FileContents)
    