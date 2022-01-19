class Parser:
    def __init__(self):
        self._lab = 0
        self._olines = []
        self._flag = True
    
    def parseFile(self, filename):
        # Otvaramo datoteku s ekstenzijom ".vm".
        try:
            self._file = open(filename + ".vm", "r")
        except:
            Parser._error("File", -1, "Cannot open source file.")
            return

        self._name = filename # Ime datoteke.
        self._ilines = [] # Linije koda.
        self._func = ""
        self._labels = []
        self._gotoLabels = []
        self._gtLineERR = []

        # Citamo linije koda iz VM datoteke.
        try:
            self._readFile()
        except:
            Parser._error("File", -1, "Cannot read source file.")
            return

        # Parsiramo VM kod liniju po liniju.
        if not self._parseLines():
            return

    def writeFile(self, filename):
        try:
            self._file = open(filename + ".asm", "w")
        except:
            Parser._error("File", -1, "Cannot open destination file.")
            return

        try:
            self._writeFile()
        except:
            Parser._error("File", -1, "Cannot write to destination file.")
            return

    def _parseLines(self):
        lines = []
        for (line, n) in self._ilines:
            l = self._parseLine(line, n)
            if not self._flag:
                return False
            if len(l) > 0:
                lines.append(l)

        i = 0
        for gtlabel in self._gotoLabels:
            if gtlabel not in self._labels:
                self._flag = False
                Parser._error("goto or if-goto", self._gtLineERR[i], "Non existing label");
                return False
            i = i + 1

        self._olines = self._olines + lines
        return True

    # IMPLEMENTIRATI!
    # Za sada parsiramo SAMO push, pop i aritmeticko/logicke naredbe...
    def _parseLine(self, line, n):
        # Ideja:
        #   1. Pobrinemo se za evantualne jednolinijske komentare i prazne
        #      linije.
        #   2. Parsiramo liniju i po prvoj kljucnoj rijeci odredjujemo koja
        #      vrsta naredbe je u njoj.
        #   3. Parsiramo naredbu i zapisujemo odgovarajuci asemblerski kod.
        l = line.split("//")[0].split()
        if len(l) == 0 or len(l[0]) == 0:
            return ""

        if l[0] == "push":
            if len(l) == 3:
                isPosInt1 = True
                try:
                    b = int(l[2])
                    if b < 0:
                        self._flag = False
                        Parser._error("Parser", n, "Negative number in push argument");
                        isPosInt1 = False
                except ValueError:
                    self._flag = False
                    Parser._error("Parser", n, "Is not an Int");
                    isPosInt1 = False

                if isPosInt1:
                    return "//" + " ".join(l) + "\n" + self._push(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined command");
                return ""

        elif l[0] == "pop":
            if len(l) == 3:
                isPosInt2 = True
                try:
                    b = int(l[2])
                    if b < 0:
                        self._flag = False
                        Parser._error("Parser", n, "Negative number in pop argument");
                        isPosInt2 = False
                except ValueError:
                    self._flag = False
                    Parser._error("Parser", n, "Is not an Int");
                    isPosInt2 = False

                if isPosInt2:
                    return "//" + " ".join(l) + "\n" + self._pop(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined command");
                return ""
            
        elif l[0] == "label" and len(l) == 2:
            return "//" + " ".join(l) + "\n" + self._label(l[1], n)
        
        elif l[0] == "goto" and len(l) == 2:
            return "//" + " ".join(l) + "\n" + self._goto(l[1], n)
        
        elif l[0] == "if-goto" and len(l) == 2:
            return "//" + " ".join(l) + "\n" + self._ifgoto(l[1], n)

        elif l[0] == "function" and len(l) == 3:
            return "//" + " ".join(l) + "\n" + self._function(l[1], l[2], n)
        
        elif l[0] == "call" and len(l) == 3:
            return "//" + " ".join(l) + "\n" + self._call(l[1], l[2], n)
        
        elif l[0] == "return" and len(l) == 1:
            return "//" + " ".join(l) + "\n" + self._return(n)

        elif len(l) == 1:
            return "//" + " ".join(l) + "\n" + self._comm(l[0], n)

        return ""

    def _label(self, name, n):
        label = "(" + self._func + "$" + name + ")"
        self._labels.append(label) 
        return label
    
    def _goto(self, name, n):
        label = "(" + self._func + "$" + name + ")"
        self._gotoLabels.append(label)
        self._gtLineERR.append(n)
        return "@" + self._func + "$" + name + "\n0;JMP"
    
    def _ifgoto(self, name, n):
        label = "(" + self._func + "$" + name + ")"
        self._gotoLabels.append(label)
        self._gtLineERR.append(n)
        return "@SP\nAM=M-1\nD=M+1\n@" + self._func + "$" + name + "\nD;JEQ"
    
    def _function(self, name, nLocals, n):
        self._func = self._name + "." + name
        s = "(" + self._func + ")" 
        for i in range(int(nLocals)):
            s += "\n@SP\nM=M+1\nA=M-1\nM=0"
        return s
    
    def _call(self, name, nArgs, n):
        retAddrLabel = name + "$ret" + str(self._lab)
        self._lab += 1
        s = "@" + retAddrLabel + "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n"
        s += "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        s += "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        s += "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        s += "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        # ARG = SP - 5 - nArgs = SP - (5 + nArgs)
        s += "@" + str(5 + int(nArgs)) + "D=A\n@SP\nD=M-D\n@ARG\nM=D\n"
        s += "@SP\nD=M\n@LCL\nM=D\n"
        s += "@" + name + "\n0;JMP\n"
        s += "(" + retAddrLabel + ")"
        return s
    
    def _return(self, n):
        s = "@LCL\nD=M\n@R15\nM=D\n"
        s += "@5\nD=A\n@R15\nA=M-D\nD=M@R14\nM=D\n"
        s += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
        s += "@ARG\nD=M+1\n@SP\nM=D\n"
        s += "@R15\nAM=M-1\nD=M\n@THAT\nM=D\n"
        s += "@R15\nAM=M-1\nD=M\n@THIS\nM=D\n"
        s += "@R15\nAM=M-1\nD=M\n@ARG\nM=D\n"
        s += "@R15\nAM=M-1\nD=M\n@LCL\nM=D\n"
        s += "@R14\nA=M\n0;JMP"
        return s

    # Funkcija zapisuje asemblerski kod push naredbe.
    # Argumenti:
    #   1. src - segment s kojeg se dogadja push (npr. constant),
    #   2. loc - lokacija push-a (npr. local 5, loc = 5),
    #   3. n - linija izvornog koda (radi vracanja greske).
    def _push(self, src, loc, n):
        if src == "constant":
            l = "@" + str(loc) + "\nD=A\n"
        elif src == "local":
            l = "@" + str(loc) + "\nD=A\n@LCL\nA=D+M\nD=M\n"
        elif src == "argument":
            l = "@" + str(loc) + "\nD=A\n@ARG\nA=D+M\nD=M\n"
        elif src == "this":
            l = "@" + str(loc) + "\nD=A\n@THIS\nA=D+M\nD=M\n"
        elif src == "that":
            l = "@" + str(loc) + "\nD=A\n@THAT\nA=D+M\nD=M\n"
        elif src == "static":
            l = "@" + self._name + "." + str(loc) + "\nD=M"
        elif src == "temp":
            l = "@" + str(5 + int(loc)) + "\nD=M"
        elif src == "pointer":
            l = "@" + str(3 + int(loc)) + "\nD=M"
        else:
            self._flag = False
            Parser._error("Push", n, "Undefined source \"" + src + "\".");
            return ""
        return l + "@SP\nM=M+1\nA=M-1\nM=D"

    # Funkcija zapisuje asemblerski kod pop naredbe.
    # Argumenti:
    #   1. dst - segment na koji se vrsi pop (npr. local),
    #   2. loc - lokacija pop-a (npr. local 5, loc = 5),
    #   3. n - linija izvornog koda (radi vracanja greske).
    def _pop(self, dst, loc, n):
        if dst == "local":
            l = "@" + str(loc) + "\nD=A\n@LCL\nD=D+M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "argument":
            l = "@" + str(loc) + "\nD=A\n@ARG\nD=D+M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "this":
            l = "@" + str(loc) + "\nD=A\n@THIS\nD=D+M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "that":
            l = "@" + str(loc) + "\nD=A\n@THAT\nD=D+M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "static":
            l = "@SP\nAM=M-1\nD=M\n@" + self._name + "." + str(loc) + "\nM=D"
        elif dst == "temp":
            l = "@SP\nAM=M-1\nD=M\n@" + str(5 + int(loc)) + "\nM=D"
        elif dst == "pointer":
            l = "@SP\nAM=M-1\nD=M\n@" + str(3 + int(loc)) + "\nM=D"
        else:
            self._flag = False
            Parser._error("Push", n, "Undefined destination \"" + dst + "\".");
            return ""
        return l

    # Funkcija zapisuje asemblerski kod a/l naredbe.
    # Argumenti:
    #   1. comm - pozvana naredba (npr. sum),
    #   2. n - linija izvornog koda (radi vracanja greske).
    def _comm(self, comm, n):
        if comm == "add":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"
        elif comm == "sub":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"
        elif comm == "neg":
            l = "@SP\nA=M-1\nM=-M"
        elif comm == "and":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D"
        elif comm == "or":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D"
        elif comm == "not":
            l = "@SP\nA=M-1\nM=!M"
        elif comm == "eq":
            l1 = "LAB" + str(self._lab)
            l2 = "LAB" + str(self._lab + 1)
            self._lab += 2
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JEQ\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n" + \
                "@SP\nA=M-1\nM=D"
        elif comm == "lt":
            l1 = "LAB" + str(self._lab)
            l2 = "LAB" + str(self._lab + 1)
            self._lab += 2
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JLT\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n" + \
                "@SP\nA=M-1\nM=D"
        elif comm == "gt":
            l1 = "LAB" + str(self._lab)
            l2 = "LAB" + str(self._lab + 1)
            self._lab += 2
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JGT\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n" + \
                "@SP\nA=M-1\nM=D"                
        elif comm == "sp":
            l = "@256\nD=A\n@SP\nM=D"
        elif comm == "ep":
            l = "($EP$)\n@$EP$\n0;JMP"
                        
        else:
            self._flag = False
            Parser._error("Push", n, "Undefined command \"" + comm + "\".");
            return ""
        return l

    def _readFile(self):
        n = 0
        for line in self._file:
            if len(line) > 0:
                self._ilines.append((line, n))
            n += 1

    def _writeFile(self):
        for line in self._olines:
            self._file.write(line + "\n")

    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line + 1) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)

def main1():
    P = Parser()
    P.parseFile("test")
    P.writeFile("test")

def main2():
    P = Parser()
    P.parseFile("test2")
    P.writeFile("test2")

if __name__ == '__main__':
    main1()
    main2()
