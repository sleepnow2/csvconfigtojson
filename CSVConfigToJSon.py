import os
from typing import List, Dict, Tuple
import sys

"""
██████   █████  ████████  █████  ████████ ██    ██ ██████  ███████ ███████
██   ██ ██   ██    ██    ██   ██    ██     ██  ██  ██   ██ ██      ██
██   ██ ███████    ██    ███████    ██      ████   ██████  █████   ███████
██   ██ ██   ██    ██    ██   ██    ██       ██    ██      ██           ██
██████  ██   ██    ██    ██   ██    ██       ██    ██      ███████ ███████


"""
Path = str              # simply a rename to ensure I know what the strings are for.
verbosity = 1           # the verbosity of the program. see handleHelp() for more details
verbosity_term = 3      # the verbosity of printing the output to the terminal. see handleHelp() for more details

class Config:
    selected: str
    unitID: str
    regType: str
    regOffset: str
    dataType: str
    bitMap: str
    name: str
    convFact: str
    convOffset: str
    streamID: str

    def __init__(self, line: str):
        # removes all forms of whitespace to prevent weird forms of whitespace from breaking the program.
        def removeWhiteSpace(S: str)->str:
            return S.replace(" ","").replace("\t","").replace("\n","").replace("\r","")
        
        selected, UnitID, RegType, RegOffset, DataType, BitMap, _, name, ConvFact, ConvOffset, StreamID = line.split(',')

        # remove whitespace ONLY ON SELECT ITEMS
        self.selected = removeWhiteSpace(selected)
        self.unitID = removeWhiteSpace(UnitID)
        self.regType = removeWhiteSpace(RegType)
        self.regOffset = removeWhiteSpace(RegOffset)
        self.dataType = removeWhiteSpace(DataType)
        self.bitMap = removeWhiteSpace(BitMap)
        self.convFact = removeWhiteSpace(ConvFact)
        self.convOffset = removeWhiteSpace(ConvOffset)
        self.name = name
        # remove a very specific whitespace
        self.streamID=StreamID.removesuffix('\n')

        # correcting BitMap
        if self.bitMap == "":
            self.bitMap = "null"
        elif len(self.bitMap)==1:
            self.bitMap = f'0{self.bitMap}'
        else:
            self.bitMap = f'{self.bitMap}'

                #correcting selected
        if self.selected == "":
            self.selected = "false"
        else:
            self.selected = "true"

        #correcting ConvOffset
        if self.convOffset == "":
            self.convOffset = "0"

        #correcting ConvFact
        if self.convFact == "":
            self.convFact = "1"

    def addBitmap(self, bitmap):
        self.bitMap = bitmap + self.bitMap

    def __str__(self):
        return "\t{" f"""
\t\t"Name": "{self.name}",
\t\t"StreamId": "{self.streamID if self.bitMap == "null" else (self.streamID.split("_")[0]+"_OFFSET_"+self.regOffset+"_"+self.regType)}",
\t\t"Selected": {self.selected},
\t\t"UnitId": {self.unitID},
\t\t"DataTypeCode": {self.dataType},
\t\t"RegisterType": "{self.regType}",
\t\t"RegisterOffset": {self.regOffset},
\t\t"ConversionFactor": {self.convFact},
\t\t"ConversionOffset": {self.convOffset},
\t\t"BitMap": "{self.bitMap}"
\t""" "}"


"""
██    ██ ████████ ██ ██      ██ ████████ ██ ███████ ███████ 
██    ██    ██    ██ ██      ██    ██    ██ ██      ██
██    ██    ██    ██ ██      ██    ██    ██ █████   ███████
██    ██    ██    ██ ██      ██    ██    ██ ██           ██
 ██████     ██    ██ ███████ ██    ██    ██ ███████ ███████


"""
def log(verb: int, line:str) -> None:
    global verbosity
    if verb <= verbosity and verbosity != verbosity_term:
        print(line)

# reads a file into a list of strings and closes the file.
def readFile(path:Path) -> List[str]:
    with open(path, 'r') as f:
        return f.readlines()[1:]

# writes a list of strings into a file. It is
def writeFile(path:Path, lines:List[str]) -> None:
    with open(path, 'w') as f:
        f.writelines((line+'\n' for line in lines))

# gets all the CSV files in the listed path
def getAllCSVs(path:Path)-> List[Path]:
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return [path]
    else:
        files = [f.name for f in os.scandir(path) if f.is_file()]
        return [os.path.join(path,f) for f in files if f.endswith(".csv")]

def handleHelp() -> None:
    print("""
        Welcome to...
 ██████ ███████ ██    ██  ██████  ██████  ███    ██ ███████ ██  ██████  ████████  ██████       ██ ███████  ██████  ███    ██ ██
██      ██      ██    ██ ██      ██    ██ ████   ██ ██      ██ ██          ██    ██    ██      ██ ██      ██    ██ ████   ██ ██
██      ███████ ██    ██ ██      ██    ██ ██ ██  ██ █████   ██ ██   ███    ██    ██    ██      ██ ███████ ██    ██ ██ ██  ██ ██
██           ██  ██  ██  ██      ██    ██ ██  ██ ██ ██      ██ ██    ██    ██    ██    ██ ██   ██      ██ ██    ██ ██  ██ ██
 ██████ ███████   ████    ██████  ██████  ██   ████ ██      ██  ██████     ██     ██████   █████  ███████  ██████  ██   ████ ██

This program was written by Alex Olson (olsona1).
If you encounter any problems, contact him at Alex.Olson@cat.com

Usage is as follows:

    csvconfigtojson [-h/--help][-i:###/--input:###][-o:###/--output:###][-v:#/--verbosity:#][-s/--silent]

-h and --help
    Displays the help screen! (this screen)
    Ignores all other commands and does nothing

-i:### or --input:###
    Changes the input to be from the parent working directory to the directory or file listed by ###
    If it is a directory, it applies transforms all .csv files in the directory
    if it is a file, it only applies the transformation to that specific file

-o:### or --output:###
    Changes the output to be from the parent working directory to the directory or file listed by ###
    If it is a directory, it dumps all outputs to the specified directory. All files will have the same name, but will have their file types changed to json
    If it is a file, it dumps all the outputs to the specified file.
    CAUTION: if you choose a directory as input and a file as output, only the next processed file will overwrite all previous versions
    -o:NONE disables all output through files saving. This is most useful if -v:3 is set.

-io:### or --inout:###
    a shortcut for doing both -i:### and -o:### with the same thing.
    be advised, using -io on a file will overwrite the file, but it will not change it's file extension.

-v:# or --verbosity:#
    Changes the verbosity of the program.
    0 = no output whatsoever
    1 = print statements for files found
    2 = print statements for files found, lines written, and execution time.
    3 = file output to terminal. This allows you to use pipes to store or grep your converted files to your will.
    Defaults to 1

-s or --silent
    shortcut for -v:0
""")

"""
██████  ██████   ██████   ██████ ███████ ███████ ███████      ██████ ███████ ██    ██
██   ██ ██   ██ ██    ██ ██      ██      ██      ██          ██      ██      ██    ██
██████  ██████  ██    ██ ██      █████   ███████ ███████     ██      ███████ ██    ██
██      ██   ██ ██    ██ ██      ██           ██      ██     ██           ██  ██  ██
██      ██   ██  ██████   ██████ ███████ ███████ ███████      ██████ ███████   ████


"""
# MEAT AND POTATOES.
# this processes the lines of CSV into the very specific JSON they need.
def processCSV(lines: list[str]) -> list[str]:
    output: Dict[Tuple[int, str], Config] = {}

    for line in lines:
        config = Config(line)
        key = (config.regOffset, config.regType)
        if key in output.keys():
            output[key].addBitmap(config.bitMap)
        else:
            output[key] = config

    return ["\n[", ",\n".join((str(cfg) for cfg in output.values())), "\n]"]

def main():
    global verbosity
    #os.chdir("CSVtoJSON")
    input = os.getcwd()
    output = os.getcwd()

    #sys.argv = ['gogogaga', "-i:../SITE_TEM_EZGEN_CONFIG_FILE.csv"]
    
    for arg in sys.argv:
        if arg=="-h" or arg=="--help":
            handleHelp()
            exit()
        elif arg=="-s" or arg=="--silent":
            verbosity = 0

        elif arg.startswith("-i:"):
            input = arg.replace("-i:","")
        elif arg.startswith("--input:"):
            input = arg.replace("--input:","")

        elif arg.startswith("-o:"):
            output = arg.replace("-o:","")
        elif arg.startswith("--output:"):
            output = arg.replace("--output:","")

        elif arg.startswith("-io:"):
            input = arg.replace("-io:","")
            output = input
        elif arg.startswith("--inout:"):
            input = arg.replace("--inout:","")
            output = input

        elif arg.startswith("-v:"):
            verbosity = int(arg.replace("-v:","").replace(" ",""))
        elif arg.startswith("--verbosity:"):
            verbosity = int(arg.replace("--verbosity:","").replace(" ",""))

            
    csvs = getAllCSVs(input)
    log(1, f"{len(csvs)} CSVs detected")
    
    for csv in csvs:        
        log(1, f"Reading CSV file {csv}")
        lines = readFile(csv)
        log(2, f"Read {len(lines)-1} lines from {csv}")

        json = processCSV(lines)

        if output != "none":
            if os.path.isfile(output):
                outfile
            else:
                outfile = output +"\\"+ os.path.basename(csv.replace('.csv','.json'))
            writeFile(outfile, json)
            log(1, f"Wrote to file {outfile}\n")
        if verbosity == verbosity_term:
            print("\n".join(json))

    log(2, "Done. Thank You!\n")

main()
