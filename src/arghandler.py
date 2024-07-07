import xml.etree.ElementTree as ET
import io
import logging
import argparse

Logger = logging.getLogger(__name__)
class ArgBuilder:
    def __init__(self,ArgDir: str):
        self.ArgDir = ArgDir
        self.Parser = argparse.ArgumentParser(
            prog="Burke Python Compiler",
            description="Compiles .brk files",
            epilog="Work in Progress"
        )
    def ReadFile(self):
        Logger.info(f"Reading {self.ArgDir}")
        try:
            with io.open(self.ArgDir,"r") as ArgFile:
                self.FileContents = ArgFile.read()
                ArgFile.close()
        except Exception as Error:
            Logger.error(f"{Error}")
    def ParseFile(self):
        Logger.info(f"Parsing ArgFile")
        if self.FileContents:
            self.Root = ET.fromstring(self.FileContents)
        else:
            Logger.warn("Missing ArgFile")
    def GenerateArg(self):
        self.ArgVersion = self.Root.attrib["Version"]
        Logger.info(f"ArgFile Version: {self.ArgVersion}")
        for XMLArg in self.Root:
            Positional = False
            Name = XMLArg[1].text
            try:
                Attributes = XMLArg[2].attrib
                PositionalString = Attributes["Pos"]
                if PositionalString == "true":
                    Positional = True
            except Exception as Error:
                Logger.warn(f"Arg: {Name} does not have a positional tag, consider adding one")
            Required = XMLArg[0].text
            Type = XMLArg[2].text
            Description = XMLArg[3].text
            Logger.info(f"Reading Arg: {Name}")
            RequiredBool = False
            if Required == "true":
                RequiredBool = True
            Arg = f"--{Name}"
            Args = {
                "required": RequiredBool
            }
            if Positional:
                Arg = f"{Name}"
                Required = False
                Args = {}
            if Type == "string":
                self.Parser.add_argument(Arg,help=Description,type=str,**Args)
            elif Type == "bool":
                self.Parser.add_argument(Arg,help=Description,type=bool,**Args)