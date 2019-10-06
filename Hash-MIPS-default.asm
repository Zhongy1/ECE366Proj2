	lui $8, 0xFA19
	ori $8, $8, 0xE366

	addi $16, $0, 0
	addi $17, $0, 100
loopdi:
	addi $9, $16, 1
# C = H(A, B)
#inputs A = $9, B = $8
#output C = $10
hashion:
	addi $11, $0, 0
	addi $12, $0, 5
	addi $13, $9, 0
looper:
	multu $13, $8
	mfhi $14
	mflo $15
	xor $13, $14, $15
	addi $11, $11, 1
	bne $11, $12, looper
	#end looper
	srl $14, $13, 16
	andi $15, $13, 0xFFFF
	xor $13, $14, $15
	srl $14, $13, 8
	andi $15, $13, 0xFF
	xor $10, $14, $15
	#end hashion
	
	sll $13, $16, 2
	sw $10, 0x2020($13)
	addi $16, $16, 1
	bne $16, $17, loopdi
	#end loopdi
	sw $22, 0x2010($0)
	sw $23, 0x2014($0)