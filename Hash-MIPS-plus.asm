	lui $8, 0xFA19
	ori $8, $8, 0xE366

	addi $16, $0, 0
	addi $17, $0, 100
loopdi:
	addi $9, $16, 1
	hash $10, $9, $8
	sll $13, $16, 2
	sw $10, 0x2020($13)
	addi $16, $16, 1
	bne $16, $17, loopdi
	
	sw $22, 0x2010($0)
	sw $23, 0x2014($0)
	
	addi $16, $0, 0
loopy:
	sll $13, $16, 2
	lw $14, 0x2020($13)
	
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
	
exitlo_op:
	
	addi $16, $16, 1
	bne $16, $17, loopy
	
	
	sw $19, 0x2008($0)