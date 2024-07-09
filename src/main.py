import argparse
import logging
import uuid
import traceback
from arghandler import ArgBuilder
from vaidatefile import ValidFile
from compiler.buildreader import BuildReader

Logger = logging.getLogger(__name__)
class BurkeP:
    def __init__(self,ArgDir,ID):
        self.ID = ID
        self.ArgDir = ArgDir
        self.ArgBuilderClass = ArgBuilder(self.ArgDir)
    def SetupArgs(self):
        try:
            self.ArgBuilderClass.ReadFile()
            self.ArgBuilderClass.ParseFile()
            self.ArgBuilderClass.GenerateArg()
            try:
                self.Args = self.ArgBuilderClass.Parser.parse_args()
            except argparse.ArgumentError as Error:
                Logger.error(Error)
                self.ArgBuilderClass.Parser.print_help()
        except Exception as Error:
            Logger.error(f"{Error}")
    def GenerateConfig(self):
        self.Config = {
            "input": self.Args.input,
            "output": self.Args.output,
            "run": self.Args.run,
            "requirements": self.Args.requirements,
            "install": self.Args.install
        }
    def Compile(self):
        try:
            InputFileExists = ValidFile(self.Config["input"])
            if InputFileExists:
                self.BuildReaderClass = BuildReader(self.Config["input"])
                self.BuildReaderClass.ReadFile()
                self.BuildFile = self.BuildReaderClass.ToDict()
                self.CompilerConfig = self.BuildFile["Build"]["CompilerConfig"]
                
            else:
                self.ArgBuilderClass.Parser.print_help()
        except Exception as Error:
            print(f"[ERROR]: {Error}")
            Logger.error(Error)
    
if __name__ == "__main__":
    print("[INIT]: Starting")
    ID = str(uuid.uuid4())
    try:
        print("[INIT]: Starting Logger")
        print(f"[INIT]: Current ID: {ID}")
        LogDir = f"logs/{ID}.log"
        print(f"[INIT]: Current Log File: {LogDir}")
        with open(LogDir,"w") as LogFile:
            LogFile.close()
        logging.basicConfig(filename=LogDir, level=logging.INFO,format='[%(asctime)s][%(filename)s][%(levelname)s]: %(message)s')
        Logger.info("Init")
        BurkePClass = BurkeP("src/config/args.xml",ID)
        BurkePClass.SetupArgs()
        BurkePClass.GenerateConfig()
        BurkePClass.Compile()
        print(BurkePClass.Config)
    except Exception as Error:
        print(f"[UNLOGGED][ERROR]: {Error}")
        print(f"{traceback.print_exc()}")
else:
    print("[INIT]: Cannot be ran as a module, use BurkeAPI.Compilers.BurkeP to interface")