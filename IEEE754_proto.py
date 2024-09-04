from math import log2
from random import random

debug = True

# ---------------------------------------------------------------------------
def front_trim(binary):
	# finding first 1
	i = binary.index('1');

def to_sci_not(binary, exponent): # binary string with decimal point
	i = binary.index('.');
	front = binary[:i];
	back = binary[i+1:];
	sci_not = front[0] + '.' + front[1:] + back + " x 2^" + str(exponent);
	return sci_not;

def decimal_to_float(num, pre):
	# determining precision
	if pre == 's':
		PRE = "Single"
		LEN = 32
		EXP = 8
		MAN = 23
		BIA = 127
	elif pre == 'd':
		PRE = "Double"
		LEN = 64
		EXP = 11
		MAN = 52
		BIA = 1023
	print(PRE + ' precision selected:')
	if debug:
		print("Debug: LEN =", LEN)
		print("Debug: EXP =", EXP)
		print("Debug: MAN =", MAN)
		print("Debug: BIA =", BIA)
	print()

	# determining sign
	if num >= 0:
		sig = '0'
	else:
		sig = '1'
	print("Sign: " + sig + '\n')

	# converting to binary
	i = int(log2(abs(num)))
	rem = abs(num)
	bits = 0
	binary = ''
	binary_added = False;
	while rem != 0:
		# break when max bits reached
		if bits >= MAN + 1:
			break
		bits += 1
		
		# calculating next bit
		sub = 2**i
		if sub <= rem:
			rem -= sub
			binary += '1'
		else:
			binary += '0'
		
		# debug info
		if debug:
			print(f"Debug: i = {i}")	
			print(f"Debug: rem = {rem}")
			print(f"Debug: bits = {bits}")
			print("Debug: binary = " + binary)
			input()
		
		# adding decimal point
		if i <= 0 and not binary_added:
			binary += '.'
			binary_added = True;
		
		# next bit
		i -= 1

	print("Binary: " + binary)

	# shifting binary point (TODO)
	if binary[0] == '1':
		exp = binary.index('.') - 1
	elif binary[0] == '0': # -1.0 < num < 1.0
		exp = 1 - binary.index('1')
	print(f"Exponent: {exp}")
	print(f"Scientific Notation: {to_sci_not(binary, exp)}\n")

# ---------------------------------------------------------------------------
def float_to_decimal(): # TOFIX
	# user input
	if debug:
		precision = 'Single'
	else:
		precision = input('Precision (Single/Double): ')
	if precision == 'Single':
		LEN = 32
		EXP = 8
		MAN = 23
		BIA = 127
	elif precision == 'Double':
		LEN = 64
		EXP = 11
		MAN = 52
		BIA = 1023
	print(precision + ' precision selected:')

	# generating random number
	binary = ''
	for i in range(LEN):
		if random() < 0.5:
			binary += '0'
		else:
			binary += '1'
	print(binary)

	# separating binary
	sig_str = binary[0]
	sep = 1 + EXP
	exp_str = binary[1:sep]
	man_str = binary[sep:]
	print('\n' + sig_str + '\n ' + exp_str + '\n' + (' ' * sep) + man_str + '\n')

	# determining sign
	if sig_str == '0':
		sig_str = '+'
	elif sig_str == '1':
		sig_str = '-'
	print('Sign: ' + sig_str + '\n')

	# determining exponent
	exp_num = 0
	for i in range(EXP):
		if exp_str[i] == '1':
			bit = 2**(EXP - i - 1)
			if debug:
				print(f'Debug: exp_str[{i}] -> {bit}')
			exp_num += bit
	if debug:
		print('Debug: Exponent + Bias: ' + str(exp_num))
	exp_num -= BIA
	print('Exponent: ' + str(exp_num))

	# determining mantissa
	if debug:
		print('Debug: Adjusted mantissa: ' + man_str[0] + '.' + man_str[1:] + ' x 2^' + str(exp_num))
		if exp_num >= 0:
			rem = exp_num - MAN + 1
			print('Debug: rem =', rem)
			if rem >= 0:
				print("0b" + man_str + ('0' * rem) + '.0')
			else:
				print("0b" + man_str[:MAN+rem] + '.' + man_str[MAN+rem:])
		else:
			print("0b0." + ('0' * (abs(exp_num) - 1)) + man_str)

# ---------------------------------------------------------------------------

if __name__ == "__main__":
	decimal_to_float(-42.625, 's')
	# decimal_to_float(0.625, 's')
	# decimal_to_float(1.0, 's')
	decimal_to_float(0.0001, 's')