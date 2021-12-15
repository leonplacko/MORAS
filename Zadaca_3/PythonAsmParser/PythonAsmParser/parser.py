# IDEJA
# 1. Iz asemblerske datoteke izbaciti sve razmake i komentare. Sjetite
#    se kako komentari u hack asembleru mogu biti jednolinijski i
#    viselinijski.
# 2. Sve simbole i varijable pretvoriti u numericke adrese (brojevi
#    linija ili adrese u memoriji).
# 3. Parsirati naredbe (A i C-instrukcije).



class Parser:

    def __init__(self, filename):
        try:
            self._file = open(filename + ".asm", "r")
        except:
            Parser._error("File", -1, "Cannot open file.")
            return

        #varijable vezanih greške
        self._flag = True
        self._line1= -1
        self._errm = ""
        
        self._labels = {}
        self._variables = {}

        #lista linija kodova u originalnom fileu
        self._lines = []
        self._read_lines()

        self._parse_lines()
        if (self._flag == False):
            Parser._error("S&C", self._line1, self._errm)
            return
        
        self._parse_symbols()
        if(self._flag == False):
            Parser._error("SYM", self._line1, self._errm)
        
        
        self._parse_commands()
        if (self._flag == False):
            Parser._error("COM", self._line1, self._errm)
        
        try:
            self.outfile = open(filename + ".hack", "w")
        except:
            Parser._error("File", -1, "cannot open output file.")
            return
        
        try:
            self._write_file()
        except:
            Parser._error("File", -1, "cannot write to output file.")
            return
        
        for line in self._lines:
            print(line)

        print("")
        print(self._labels)
        print(self._variables)
            
    
    
    def _write_file(self):
        for(line, p, o) in self._lines:
            self.outfile.write(line)
            if line[-1] != "\n":
                self.outfile.write("\n")


    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)


    from parse_line import _parse_lines, _parse_line
    from parseSymbols import _parse_symbols, _parse_symbol, _init_labels, _parse_variable
    from parseComms import _parse_commands, _parse_command, _init_comms
    from parseMakro import checkMakro, parseMakro, _init_makros

    def _read_lines(self):
        n = 0
        for line in self._file:
            if line[0] == '$':
                komands = parseMakro(self, line)
                for komand in komands:
                    self._lines.append((komand, n, n))
                    n += 1
            else:
                self._lines.append((line, n, n))
                n += 1
            
    def _iter_lines(self, func):
        i = 0
        newlines = []
        for (line, p, o) in self._lines:
            newline = func(line, p, o)
            if (len(newline) > 0):
                newlines.append((newline, i, o))
                i += 1
                
        self._lines = newlines
        
        
    

def parseMakro(self, line):
    _init_makros(self)
    Komande = checkMakro(self, line)
    return Komande


def checkMakro(self, line1):

    
    komande = []

    line = razmakremover(line1)

    x = line[1:].split("(")[0]

    if x == "MV":
        prvaAdresa = (line[4:].split(")"))[0].split(",")[0]
        drugaAdresa = (line[4:].split(")"))[0].split(",")[1]


        komande.append("@" + prvaAdresa + " ")
        komande.append(self.MV[0])
        komande.append("@" + drugaAdresa + " ")
        komande.append(self.MV[1])


    elif x == "SWP":
        prvaAdresa = (line[5:].split(")"))[0].split(",")[0]
        drugaAdresa = (line[5:].split(")"))[0].split(",")[1]

        komande.append("@" + prvaAdresa + " ")
        komande.append(self.SWP[0])
        komande.append(self.SWP[1])
        komande.append(self.SWP[2])
        komande.append("@" + drugaAdresa + " ")
        komande.append(self.SWP[3])
        komande.append("@" + prvaAdresa + " ")
        komande.append(self.SWP[4])
        komande.append(self.SWP[5])
        komande.append(self.SWP[6])
        komande.append("@" + drugaAdresa + " ")
        komande.append(self.SWP[7])

        
        
        

    elif x == "SUM":
        prvaAdresa = (line[5:].split(")"))[0].split(",")[0]
        drugaAdresa = (line[5:].split(")"))[0].split(",")[1]
        trecaAdresa = (line[5:].split(")"))[0].split(",")[2]

        

        komande.append("@" + prvaAdresa + " ")
        komande.append(self.SUM[0])
        komande.append("@" + trecaAdresa + " ")
        komande.append(self.SUM[1])
        komande.append("@" + drugaAdresa + " ")
        komande.append(self.SUM[2])
        komande.append("@" + trecaAdresa + " ")
        komande.append(self.SUM[3])

        

    ##elif x == "WHILE":
        #TODO
 
    return komande

def _init_makros(self):
    self.MV = ["D=M ", "M=D "]
    self.SWP = ["D=M " , "@THESWAPINATOR ", "M=D ", "D=M ", "M=D ", "@THESWAPINATOR ", "D=M ", "M=D "]
    self.SUM = ["D=M ", "M=D ", "D=M ", "M=M+D "]
    self.WHILE = []

def razmakremover(line1):
    line = ""
    for chr in line1:
        if chr != ' ':
            line += chr

    return line





if __name__ == "__main__":
    Parser("test1")
    print("Parsing done")
