def parseMakro(self, line):
    _init_makros(self)
    Komande = checkMakro(self, line)
    return Komande

#funkcije se nemogu importat u parser.py pa su implementirane i u parser.py da rade

def checkMakro(self, line1):

    
    komande = []

    line = razmakremover(line1)

    x = line[1:].split("(")[0]

    if x == "MV":
        prvaAdresa = (line[4:].split(")"))[0].split(",")[0]
        drugaAdresa = (line[4:].split(")"))[0].split(",")[1]


        komande.append("@" + prvaAdresa + " ")

        for lines in self.MV:
            komande.append(lines)

        komande.append("@" + drugaAdresa + " ")


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
