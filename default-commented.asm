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
	
	addi $16, $0, 0
loopy:
	sll $13, $16, 2 	#address offset
	lw $14, 0x2020($13)	#value
	#if $14 contains 5 consecutive 1's, increment $19 ($19 should be stored in 0x2008 at the end)
	addi $11, $0, 0
	addi $12, $0, 4
	addi $21, $0, 0x1F
lo_op:
	srlv $15, $14, $11
	andi $15, $15, 0x1F
	bne $15, $21, skip2
	addi $19, $19, 1
	bne $19, $0, exitlo_op
skip2:
	addi $11, $11, 1
	bne $11, $12, lo_op
	#end lo_op
exitlo_op:
	
	addi $16, $16, 1
	bne $16, $17, loopy
	#end loopy
	
	sw $19, 0x2008($0)