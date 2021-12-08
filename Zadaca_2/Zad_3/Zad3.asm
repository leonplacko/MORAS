@R0
D = M

@R5
M = D

(POCETAK)

@R1
D = M

@temp
M = D

@R5
D = D - M

@ZAMIJENI
D; JGT

@R2
D = M

@temp
M = D

@R5
D = D - M

@ZAMIJENI
D; JGT

@R3
D = M

@temp
M = D

@R5
D = D - M

@ZAMIJENI
D; JGT

@R4
D = M

@temp
M = D

@R5
D = D - M

@ZAMIJENI
D; JGT

@KRAJ
0; JMP



(ZAMIJENI)
@temp
D = M

@R5
M = D

@POCETAK
0; JMP

(KRAJ)

(KRAJ1)
@KRAJ1
0; JMP


