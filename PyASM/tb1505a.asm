;-----DATA SEGMENT
; register file
;; PAGE0
.**local INDF     0x00
.local TMR0     0x01
.local PCL      0x02 
.local STATUS   0x03 ; WKPF|GPA1|GPA0|TO|PD|Z|DC|C
.local FSR      0x04
.local PORTB    0x05 ; -|-|GP[5:0]
;.local INDF    0x06
.local DC1LR    0x06
;.local INDF    0x07
.local PORTC    0x07
.local PR1L     0x08
.local PR1H     0x09
;.local PCHBUF  0x0a ; PCH[9:8]
;.local DC1LR    0x0a
.local INTCON   0x0b ; GIE|PEIE|T0IE|INTIE|GPIE|T0IF|INTF|GPIF
.local PIR1     0x0c ; -|-|-|-|CMIF|-|-|TMR1IF
.local DC1HR    0x0d
.local TMR1L    0x0e 
.local TMR1H    0x0f
.local T1CON    0x10 ; T1GNV|TMR1GE|T1CKPS1|T1CKPS0|T1OSCEN|T1SYNC|TMR1CS|TMR1ON
.local TMR2     0x11
.local T2CON    0x12
.local CCPRL    0x13
.local CCPRH    0x14
.local CCPCON   0x15
.local PWMCON   0x16
.local ECCPAS   0x17
.local WDTCON   0x18
;.local VRCON   0x19 ; CMVREN|-|VRR|FVREN|VR3|VR2|VR1|VR0
.local CMCON0   0x19 ; CMON|COUT|CMOE|CMPOL|-CMR|-CMCH
.local CMCON1   0x1a ; -|-|-|T1ACS|CMHYS|-|T1GSS|CMSYNC
.local CMCON2   0x1b
;.local INDF    0x1b
.local APCON    0x1c
.local TCCR     0x1d
.local ADRESH   0x1e
.local ADCON0   0x1f

;; PAGE1: ->PAGE0+0x80
.local OPTION   0x01 ; GDPU|INTEDG|TOCS|TOSE|PSA|PS2|PS1|PS0
;.local PCL     0x02 
;.local STATUS  0x03 ; WKPF|GPA1|GPA0|TO|PD|Z|DC|C
;.local FSR     0x04
.local TRISB    0x05 ; no tris3
.local TRISC    0x07 ; no tris3
.local COGCR0   0x08
.local COGCR1   0x09
.local PCHBUF   0x0a ; PCH[9:8]
;.local INTCON  0x0b ; GIE|PEIE|TOIE|INTIE|GPIE|TOIF|INTF|GPIF
.local PIE1     0x0c ; -|-|-|-|CMIE|-|-|TMR1IE
.local COGPHR   0x0d
.local PCON     0x0e ; WDTE|-|LVRE|DPSM1|DPSM0|SWDD|POR|LVR
.local OSCCON   0x0f
.local OSCTUNE  0x10
.local ANSEL    0x11
.local PR2      0x12
.local WPUA     0x15 ; with no PORT3 weak pullup
.local IOCA     0x16 ; IOC[5:0]
.local VRCON    0x19
.local COGAS    0x1a
.local COGDBR   0x1b
;.local EECON1  0x1c
;.local EECON2  0x1d
;.local ADRESL  0x1e
;.local ANSEL   0x1f ; 

;; USR data
.local file     1
.local wreg     0
;bank0 area
.local CTL_BYTE0        0x20
.local CTL_BYTE1        0x21
.local HOLD_BYTE        0x22

.local PR1L_REG         0x30
.local PR1H_REG         0x31
.local CCPRL_REG        0x32
.local CCPRH_REG        0x33
.local PORTC_REG        0x34
.local ECCPAS_REG       0x35
.local PWMCON_REG       0x36
.local DC1LR_REG        0x37
.local DC1HR_REG        0x38
;bank1 area
.local COGCR0_REG       0x20
.local COGCR1_REG       0x21
.local COGPHR_REG       0x22
.local COGDBR_REG       0x23
.local COGAS_REG        0x24
;cross-bank area
.local TMRBOARD         0x70
.local TMR0VAL          0x71
.local TMR0SET_OPTION   0x72
.local TMR1L_REG        0x73
.local TMR1H_REG        0x74
.local T1CON_REG        0x75
.local PCON_REG         0x76
.local WDTCON_REG       0x77
.local TMR2_REG         0x78
.local PR2_REG          0x79
.local T2CON_REG        0x7a
.local TCCR_REG         0x7b
.local PIE1_REG         0x7c
.local TRISC_REG        0x7d
.local CCPCON_REG       0x7e
.local INT_BYTE         0x7f
;-----DATA SEGMENT END

;-----CODE SEGMENT
.org 0x00
    goto    main
.org 0x04
    goto    isr
.org 0x10
main:
    bsf     STATUS, 5 ;set page1
    clrf    ANSEL ; clear ANSEL to use digital IO
    bcf     STATUS, 5 ;set page0
    nop
    clrf    CTL_BYTE0
    clrf    CTL_BYTE1
    nop
    ;send a high pulse on bit7
    ;as power on indicator
    bsf     CTL_BYTE1, 7
    bcf     CTL_BYTE1, 7
    nop
    bsf     INTCON, 7 ;enable global interrupt
    bsf     INTCON, 6 ;enable peripheral interrupt
    ;bcf WDTCON, 0
;control field
loop: ;the test loop
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 0
    goto    test_bit5_
    ; init tmr0
    bsf     STATUS, 5 ;set page1
    bcf     OPTION, 5 ; clear T0CS to use system clock
    movf    OPTION, 0 
    movwf   TMR0SET_OPTION ;copy OPTION value to file 0x42
    bcf     PCON, 5 ; clear PCON[5] to enable TMR0
    bcf     STATUS, 5 ;set page0
    bsf     INTCON, 5 ;enable timer0 interrupt
    nop
    clrf    TMR0
    clrf    TMRBOARD
    movlw   0x33
    movwf   TMR0
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit5_:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 5
    goto    test_bit4_
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    sleep
hold_loop:
    incf    HOLD_BYTE, file ; HOLD_BYTE++
    btfsc   CTL_BYTE1, 6
    goto    hold_loop ; if set ctl_byte[6] do the loop
test_bit4_:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 4
    goto    test_bit3_
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    clrwdt
test_bit3_:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 3
    goto    test_bit2_
    ; move reg to buf
    movf    PR1L, wreg
    movwf   PR1L_REG
    movf    PR1H, wreg
    movwf   PR1H_REG
    movf    CCPRL, wreg
    movwf   CCPRL_REG
    movf    CCPRH, wreg
    movwf   CCPRH_REG
    movf    T1CON, wreg
    movwf   T1CON_REG
    movf    T2CON, wreg
    movwf   T2CON_REG
    movf    CCPCON, wreg
    movwf   CCPCON_REG
    movf    PORTC, wreg
    movwf   PORTC_REG
    movf    DC1LR, wreg
    movwf   DC1LR_REG
    movf    DC1HR, wreg
    movwf   DC1HR_REG
    bsf     STATUS, 5 ;set page1
    movf    PR2, wreg
    movwf   PR2_REG
    movf    TRISC, wreg
    movwf   TRISC_REG
    movf    PIE1, wreg
    movwf   PIE1_REG
    movf    COGAS, wreg
    movwf   COGAS_REG
    movf    COGDBR, wreg
    movwf   COGDBR_REG
    movf    COGPHR, wreg
    movwf   COGPHR_REG
    movf    COGCR1, wreg
    movwf   COGCR1_REG
    movf    COGCR0, wreg
    movwf   COGCR0_REG
    ; move buf to reg
    ;send a high pulse on bit7
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    movf    CCPRL_REG, wreg
    movwf   CCPRL
    movf    CCPRH_REG, wreg
    movwf   CCPRH
    movf    PR1L_REG, wreg
    movwf   PR1L
    movf    PR1H_REG, wreg
    movwf   PR1H
    bsf     STATUS, 5 ;set page1
    movf    PR2_REG, wreg
    movwf   PR2
    movf    TRISC_REG, wreg
    movwf   TRISC
    movf    COGAS_REG, wreg
    movwf   COGAS
    movf    COGDBR_REG, wreg
    movwf   COGDBR
    movf    COGPHR_REG, wreg
    movwf   COGPHR
    movf    COGCR1_REG, wreg
    movwf   COGCR1
    movf    COGCR0_REG, wreg
    movwf   COGCR0
    movf    PIE1_REG, wreg
    movwf   PIE1
    bcf     STATUS, 5 ;set page0
    movf    CCPCON_REG, wreg
    movwf   CCPCON
    movf    T1CON_REG, wreg
    movwf   T1CON
    movf    T2CON_REG, wreg
    movwf   T2CON
    movf    PORTC_REG, wreg
    movwf   PORTC
    movf    DC1HR_REG, wreg
    movwf   DC1HR
    movf    DC1LR_REG, wreg
    movwf   DC1LR
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit2_:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 2
    goto    test_bit1_
    ;bsf     TCCR, 7
    movf    TCCR, wreg ; move TCCR to TCCR_reg
    movwf   TCCR_REG
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    ;movf    TCCR_REG, wreg ;move TCCR_reg to TCCR
    btfss   TCCR_REG, 2 ;test TCCR_REG[2]
    goto    clr_tccr2 ; if "0" clear TCCR[2]
    goto    set_tccr2 ; else set TCCR[2]
clr_tccr2:
    bcf     TCCR, 2 
    goto    test_tccr4
set_tccr2:
    bsf     TCCR, 2
test_tccr4:
    btfss   TCCR_REG, 4 ;test TCCR_REG[4]
    goto    clr_tccr4
    goto    set_tccr4
clr_tccr4:
    bcf     TCCR, 4 ; if "0" clear TCCR[4]
    goto    test_tccr7  
set_tccr4:
    bsf     TCCR, 4 ; else set TCCR[4]
test_tccr7:
    btfss   TCCR_REG, 7 ;test TCCR_REG[7]
    goto    clr_tccr7
    goto    set_tccr7
clr_tccr7:
    bcf     TCCR, 7 ; if "0" clear TCCR[7]
    goto    out_tccr_test
set_tccr7:
    bsf     TCCR, 7 ; else set TCCR[7]
out_tccr_test:
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit1_:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE1, 1
    goto    test_bit0
    bsf     STATUS, 5 ;set page1
    movlw   0xff
    movwf   PR2
    movwf   PR2_REG
    bsf     PIE1, 1 ;enable TMR2 interrupt
    bcf     STATUS, 5 ;set page0
    bsf     T2CON, 2 ; start tmr2
    movf    T2CON, wreg
    movwf   T2CON_REG
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit0: ;test bit0 if 1 then rewrite TMR0
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 0
    goto    test_bit1
    ; write tmr0 with current tmr0 value
    bcf     STATUS, 5 ;set page0
    movf    TMR0, file ; move TMR0 to TMR0
test_bit1: ;test bit0 if 1 then disable TMR0
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 1
    goto    test_bit2
    bsf     STATUS, 5 ;set page1
    bsf     PCON, 5 ; set PCON[5] to disable TMR0
    bcf     STATUS, 5 ;set page0
    bcf     INTCON, 5 ;disable timer0 interrupt
    ;send a high pulse on bit7
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit2: ;if 1 then start TMR1
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 2
    goto    test_bit3
    bsf     STATUS, 5 ;set page1
    bsf     PIE1, 0 ;set TMR1IE
    clrf    ANSEL ;clear ANSEL to use PB4 as TMR1 Gate
    bcf     STATUS, 5 ;set page0
    movf    TMR1L_REG, wreg
    movwf   TMR1L
    movf    TMR1H_REG, wreg
    movwf   TMR1H
    movf    PR1H_REG, wreg
    movwf   PR1H
    movf    PR1L_REG, wreg
    movwf   PR1L
    bsf     T1CON, 0 ;set TMR1ON to enable tmr1
    movf    T1CON, wreg ; copy T1CON to T1CON_REG
    movwf   T1CON_REG
    ;send a high pulse on bit7 as an ack
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit3: ;if 1 then disable TMR1
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 3
    goto    test_bit4
    bsf     STATUS, 5 ;set page1
    bcf     PIE1, 0 ;clear TMR1IE to disable TMR1 interrupt
    bcf     STATUS, 5 ;set page0
    bcf     T1CON, 0 ;clear TMR1ON to disable tmr1
    movf    T1CON, wreg ; copy T1CON to T1CON_REG
    movwf   T1CON_REG
    ;send a high pulse on bit7 as an ack
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
test_bit4: ;if 1 then sleep
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 4
    goto    test_bit5
    bcf     STATUS, 5 ;set page0
    ;send a high pulse on bit7 as an ack
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    ;before sleep
    sleep
test_bit5:
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 5
    goto    test_bit6
    ;send a high pulse on bit7 as an ack
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    movf    TMR1H_REG, wreg
    movwf   TMR1H
    movf    TMR1L_REG, wreg
    movwf   TMR1L
    movf    T1CON_REG, wreg
    movwf   T1CON
    ;send a high pulse on bit7 as an ack
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    ;before sleep
    sleep
test_bit6: ;WDT regs dealling
    bcf     STATUS, 5 ;set page0
    btfss   CTL_BYTE0, 6
    goto    test_again
    ; write regs back 
    bsf     STATUS, 5 ;set page1
    movf    OPTION, wreg
    movwf   TMR0SET_OPTION
    bcf     STATUS, 5 ;set page0
    movf    WDTCON, wreg
    movwf   WDTCON_REG
    ;send a high pulse on bit7 as an ack
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    ; write regs
    bsf     STATUS, 5 ;set page1
    movf    TMR0SET_OPTION, wreg
    movwf   OPTION
    bcf     STATUS, 5 ;set page0
    movf    WDTCON_REG, wreg
    movwf   WDTCON
    ;send a high pulse on bit7 as an ack
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    ;clear wdt counter at last
    ;clrwdt
    ;sleep
test_again:
    bcf     STATUS, 5 ;set page0
test_cfg_pwm:
    btfss   INT_BYTE, 1
    goto    back_to_main
    btfss   PIR1, 1 ; test TMR2IF
    goto    back_to_main
    bcf     PIR1, 1 ; clear TMR2IF
pwm_buf:
    bsf     STATUS, 5 ;set page1
    movf    PR2_REG, wreg
    movwf   PR2
    bcf     STATUS, 5 ;set page0
    movf    T2CON_REG, wreg
    movwf   T2CON
    movf    CCPCON_REG, wreg
    movwf   CCPCON
    movf    CCPRL_REG, wreg
    movwf   CCPRL
    movf    PWMCON_REG, wreg
    movwf   PWMCON
    movf    ECCPAS_REG, wreg
    movwf   ECCPAS
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
back_to_main:
    goto    loop
isr:
    incf    TMRBOARD, file ; TMRBOARD++
tmr0_dealing:
    bcf     STATUS, 5 ;set page0
    btfss   INTCON, 2
    goto    tmr1_dealing
    bsf     STATUS, 5 ;set page1
    movf    TMR0SET_OPTION, wreg
    movwf   OPTION ;copy TMR0SET_OPTION to OPTION
    bcf     STATUS, 5 ;set page0
    movf    TMR0VAL, wreg
    movwf   TMR0 ;copy TMR0VAL to TMR0
    bcf     INTCON, 2 ;clear T0IF
tmr1_dealing:
    bcf     STATUS, 5 ;set page0
    btfss   PIR1, 0
    goto    tmr2_dealing
    movf    T1CON_REG, wreg
    movwf   T1CON
    movf    TMR1L_REG, wreg
    movwf   TMR1L
    movf    TMR1H_REG, wreg
    movwf   TMR1H
    movf    PR1H_REG, wreg
    movwf   PR1H
    movf    PR1L_REG, wreg
    movwf   PR1L
    bcf     PIR1, 0 ;clear TMR1IF bit
tmr2_dealing:
    btfss   PIR1, 1
    goto    ccp_dealing
    bsf     STATUS, 5 ;set page1
    movf    PR2_REG, wreg
    movwf   PR2
    bcf     STATUS, 5 ;set page0
    movf    TMR2_REG, wreg
    movwf   TMR2
    movf    T2CON_REG, wreg
    movwf   T2CON
    bcf     PIR1, 1 ; clear TMR2IF 
ccp_dealing:
    btfss   PIR1, 5 ;test ccp if
    goto    cog_dealing
    btfsc   INT_BYTE, 0 
    clrf    CCPCON ; if set INT_BYTE[0], clear CCPCON
    movf    CCPRL, wreg
    movwf   CCPRL_REG
    movf    CCPRH, wreg
    movwf   CCPRH_REG
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    movf    CCPRL_REG, wreg
    movwf   CCPRL
    movf    CCPRH_REG, wreg
    movwf   CCPRH
    movf    PR1L_REG, wreg
    movwf   PR1L
    movf    PR1H_REG, wreg
    movwf   PR1H
    movf    CCPCON_REG, wreg
    movwf   CCPCON
    bsf     STATUS, 5 ;set page1
    movf    TRISC_REG, wreg
    movwf   TRISC
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    bcf     PIR1, 5 ; clear ccp interrupt flag
cog_dealing:
    btfss   PIR1, 7 ;test cog if
    goto    ret
block_int:
    btfsc   INT_BYTE, 2
    goto    block_int
    bsf     STATUS, 5 ;set page1
    movf    COGAS_REG, wreg
    movwf   COGAS
    bcf     STATUS, 5 ;set page0
    bsf     CTL_BYTE0, 7
    bcf     CTL_BYTE0, 7
    bcf     PIR1, 7 ; clear cog interrupt flag
ret:
    retfie
    goto    $
;-----CODE SEGMENT END

