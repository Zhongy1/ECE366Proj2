	lui $8, 0xFA19
	ori $8, $8, 0xE366

	addi $16, $0, 4
	addi $17, $0, 404
loopdi:
	srl $9, $16, 2
hashion:
	multu $9, $8
	mfhi $14
	mflo $15
	xor $9, $14, $15
	multu $9, $8
	mfhi $14
	mflo $15
	xor $9, $14, $15
	multu $9, $8
	mfhi $14
	mflo $15
	xor $9, $14, $15
	multu $9, $8
	mfhi $14
	mflo $15
	xor $9, $14, $15
	multu $9, $8
	mfhi $14
	mflo $15
	xor $9, $14, $15
	
	srl $14, $9, 16
	andi $15, $9, 0xFFFF
	xor $9, $14, $15
	srl $14, $9, 8
	andi $15, $9, 0xFF
	xor $10, $14, $15
	
	sw $10, 0x201C($16)
	addi $16, $16, 4
	bne $16, $17, loopdi


	addi $16, $0, 0
	addi $17, $0, 400
	addi $12, $0, 4
	addi $21, $0, 0x1F
loopy:
	lw $14, 0x2020($16)
	andi $15, $14, 0x1F
	bne $15, $21, skip1
	addi $19, $19, 1
	bne $19, $0, finish
skip1:
	srl $15, $14, 1
	bne $15, $21, skip2
	addi $19, $19, 1
	bne $19, $0, finish
skip2:
	srl $15, $14, 2
	bne $15, $21, skip3
	addi $19, $19, 1
	bne $19, $0, finish
skip3:
	srl $15, $14, 3
	bne $15, $21, finish
	addi $19, $19, 1
	bne $19, $0, finish
finish:
	addi $16, $16, 4
	bne $16, $17, loopy
	
	
	sw $19, 0x2008($0)