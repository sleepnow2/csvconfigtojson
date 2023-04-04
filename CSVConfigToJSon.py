import os
from typing import List

#simply a rename to ensure I know what the strings are for.
Path = str

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
    files = list(zip(*os.walk(path)))[2][0]
    return [os.path.join(path,f) for f in files if f.endswith(".csv")]

# removes all forms of whitespace to prevent weird forms of whitespace from breaking the program.
def removeWhiteSpace(S:str)->str:
    return S.replace(" ","").replace("\t","").replace("\n","").replace("\r","")

# MEAT AND POTATOES.
# this processes the lines of CSV into the very specific JSON they need.
def processCSV(lines:List[str])->List[str]:
    output: List[str] = ["["]

    for line in lines:
        output.append("\t{")
        
        # split the items
        selected, UnitID, RegType, RegOffset, DataType, BitMap, _, Name, ConvFact, ConvOffset, StreamID = line.split(',')

        # remove whitespace ONLY ON SELECT ITEMS
        selected = removeWhiteSpace(selected)
        UnitID = removeWhiteSpace(UnitID)
        RegType = removeWhiteSpace(RegType)
        RegOffset = removeWhiteSpace(RegOffset)
        DataType = removeWhiteSpace(DataType)
        BitMap = removeWhiteSpace(BitMap)
        ConvFact = removeWhiteSpace(ConvFact)
        ConvOffset = removeWhiteSpace(ConvOffset)
        # remove a very specific whitespace
        StreamID=StreamID.removesuffix('\n')
        
        # correcting BitMap
        if BitMap == "":
            BitMap = "null"
        elif len(BitMap)==1:
            BitMap = f'"0{BitMap}"'
        else:
            BitMap = f'"{BitMap}"'

        #correcting selected
        if selected == "":
            selected = "false"
        else:
            selected = "true"

        #correcting ConvOffset
        if ConvOffset == "":
            ConvOffset = "0"

        #correcting ConvFact
        if ConvFact == "":
            ConvFact = "1"


        output.append(f'\t\t"Name": "{Name}",')
        output.append(f'\t\t"StreamId": "{StreamID}",')
        output.append(f'\t\t"Selected": {selected},')
        output.append(f'\t\t"UnitId": {UnitID},')
        output.append(f'\t\t"DataTypeCode": {DataType},')
        output.append(f'\t\t"RegisterType": "{RegType}",')
        output.append(f'\t\t"RegisterOffset": {RegOffset},')
        output.append(f'\t\t"ConversionFactor": {ConvFact},')
        output.append(f'\t\t"ConversionOffset": {ConvOffset},')
        output.append(f'\t\t"BitMap": {BitMap}')
        output.append("\t},")
    
    output[-1]= output[-1].replace(',','')
    output.append("]")
    return output


def main():
    print("This Program was written by Alex Olson (olsona1).")
    print("If you encounter any problems, contact him at Alex.Olson@cat.com")
    print("")
    #csvs = getAllCSVs(os.path.dirname(__file__))
    csvs = getAllCSVs(os.getcwd())
    
    for csv in csvs:
        lines = readFile(csv)
        print(f"Read {len(lines)-1} lines from {csv}")
        
        json = processCSV(lines)
        print(f"Processed CSV into JSON")

        writeFile(csv.replace(".csv",".json"), json)
        print(f"Wrote to file {csv.replace('.csv','.json')}")
        print()

    print("Done. Thank You!")
    print()


main()