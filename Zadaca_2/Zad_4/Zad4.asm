@i
M = 1

(LOOP_START)

    @4092
    D = A

    @i
    D = M - D

    @END
    D; JGE

    @SCREEN
    D = A

    @i
    D = D + M

    @address
    M = D
    
    D = 1

    @address
    A = M
    M = D

    @32
    D = A

    @i
    M = M + D

    @LOOP_START
    0; JMP

(END)



@i
M = 0

(LOOP_START1)

    @8
    D = A

    @i
    D = M - D

    @END1
    D; JGE

    @20449
    D = A

    @i
    D = D + M

    @address
    M = D

    @address
    A = M
    M = -1

    @i
    M = M + 1

    @LOOP_START1
    0; JMP

(END1)

//hipotenuza

@j
M = 1

@32
D = A

@i
M = 1
D = M 

@512
D = A

@acumulator
M = D

(LOOP_OUTER)
 
    @9
    D = A

    @j
    D = M - D

    @ENDen
    D; JGE

    @vrij
    M = 1

    (LOOP_START2)

        @acumulator
        D = M

        @i
        D = M - D

        @END2
        D; JGE

        @SCREEN
        D = A

        @i
        D = D + M

        @address
        M = D

        @vrij
        D = M

        @address
        A = M
        M = M + D   

        @vrij
        D = M
        M = M + D

        @32
        D = A

        @i
        M = M + D

        @LOOP_START2
        0; JMP


    (END2)

    @j
    M = M + 1

    @512
    D = A

    @acumulator
    M = M + D

    @i
    M = M + 1

    @LOOP_OUTER
    0; JMP

(ENDen)

@SCREEN
D = A

@33
D = D + A

@popravak
M = D

@1
D = M 

@popravak
A = M
M = 1

@SCREEN
D = A

@32
D = D + A

@popravak1
M = D

@1
D = M 

@popravak1
A = M
M = 0

@34
D = D + A

@popravak2
M = D

@1
D = M 

@popravak2
A = M
M = D + 1

(END3)
@END3
0; JMP

