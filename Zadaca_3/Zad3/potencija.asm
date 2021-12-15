@R0
D = M

@temp
M = D

@j
M = 1

(POT_LOOP)

    @R1
    D = M

    @j
    D = M - D

    @END_POT_LOOP
    D; JGE

    @MNOZENJE
    0; JMP





(MNOZENJE)

@i
M = 0

    (LOOP_START_MNOZ)

        @R0
        D = M

        @i
        D = M - D

        @MNOZEND
        D; JGE


        @temp 
        D = M

        @rez
        M = M + D

        @i
        M = M + 1

        @LOOP_START_MNOZ
        0; JMP

    (MNOZEND)

    @rez
    D = M

    @temp
    M = D

    @rez
    M = 0

    @j
    M = M + 1

    @POT_LOOP
    0; JMP

(END_POT_LOOP)


@temp
D = M

@R2
M = D


(END)
@END
0; JMP