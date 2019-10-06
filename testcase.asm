	addi $8, $0, 0
	addi $9, $0, 255
loop1:
	addi $8, $8, 1
	sb $8, 0x1FFF($8)
	bne $8, $9, loop1
	addi $8, $8, 1
	sb $9, 0x1FFF($8)
	
	addi $8, $0, 0
	addi $9, $0, 256
	addi $15, $0, 4
	addi $16, $0, 0
loop2:
	addi $8, $8, 1
	
	lb $10, 0x1FFF($8)
	addi $13, $0, 0
	addi $11, $0, 0
	addi $12, $0, 8
loop3:
	andi $14, $10, 1
	beq $14, $0, skip1
	addi $13, $13, 1
skip1:
	srl $10, $10, 1
	addi $11, $11, 1
	bne $11, $12, loop3
	bne $13, $15, skip2
	addi $16, $16, 1
skip2:
	bne $8, $9, loop2
	