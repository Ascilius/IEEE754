from math import log2
from random import random
import struct

debug = True;

# ---------------------------------------------------------------------------
# decimal to float

def print_binary(binary_struct):
	binary = binary_struct[0];
	exponent = binary_struct[1];

	# regular
	if exponent > (len(binary) - 1): # binary point is far right of manitssa
		print(binary + ('0' * (exponent - (len(binary) - 1))) + ".0");
	elif exponent < 0: # binary point is far left of mantissa
		print("0." + ('0' * abs(exponent + 1)) + binary);
	else: # binary point is within mantissa
		print(binary[:1+exponent] + '.' + binary[1+exponent:]);

	# scientific notation
	print(binary[0] + '.' + binary[1:] + " x 2^" + str(exponent));

def get_binary_exponent(num):
	exp = int(log2(num));
	if 0 < num and num < 1:
		exp -= 1;
	if debug:
		print("Debug: exp =", exp);
		print("Debug: 2^exp =", 2**exp);
	return exp;

# TOFIX
def round_binary(binary):
	"""
	if binary[i] == '0':
		binary = binary[:-1]
	elif binary[i] == '1':
	"""
	i = -1;
	while True:
		i -= 1;
		if binary[i] == '0':
			binary = binary[:i] + '1' + binary[i+1:];
			break;
		elif binary[i] == '1':
			binary = binary[:i] + '0' + binary[i+1:];
	return binary[:-1];

def decimal_to_binary(num, LIM):
	LIM += 2; # +1 for removing first 1, +1 for rounding
	print(f"Converting {num} to binary...");

	exp = get_binary_exponent(num);
	i = exp + 1;
	rem = num;
	bits = 0;
	binary = ''
	while rem != 0 and bits < LIM:
		i -= 1;

		sub = 2**i;
		if sub > rem:
			binary += '0'
		else:
			rem -= sub;
			binary += '1'
		bits += 1;

		if debug:
			print(f"Debug: i = {i}; binary = {binary} ({bits})");
	# adding remaining 0s
	while i > 0:
		i -= 1;
		binary += '0';

	# roundin
	if len(binary) == LIM:
		binary = round_binary(binary);

	return [binary, exp];

def decimal_to_float(num, pre):
	print(f"Converting {num} to {pre}-precision float...");

	# determining precision
	if pre == "single":
		EXP = 8
		MAN = 23
		BIA = 127
	elif pre == "double":
		EXP = 11
		MAN = 52
		BIA = 1023
	if debug:
		print("Debug: EXP =", EXP);
		print("Debug: MAN =", MAN);
		print("Debug: BIA =", BIA);

	# special value (0)
	if num == 0:
		binary = '0' * 32;
		return binary;

	# determining sign
	if num >= 0.0:
		sign = '0'; # positive
	else:
		sign = '1'; # negative
	if debug:
		print("\nDebug: sign = " + sign);

	# converting num to binary
	print();
	binary_struct = decimal_to_binary(abs(num), MAN);
	if debug:
		print("Debug: binary:");
		print_binary(binary_struct);

	# adding bias and converting to binary
	exponent = binary_struct[1] + BIA;
	if debug:
		print("\nDebug: exponent + bias =", exponent);
	exponent_binary = decimal_to_binary(exponent, EXP)[0];
	if debug:
		print("Debug: exponent binary:", exponent_binary);

	# adding 0s to front of exponent
	while len(exponent_binary) < EXP:
		exponent_binary = '0' + exponent_binary;
	# removing first 1 and adding 0s to back of mantissa
	mantissa_binary = binary_struct[0][1:];
	while len(mantissa_binary) < MAN:
		mantissa_binary += '0'
	if debug:
		print(f"\nDebug: exponent_binary: {exponent_binary} ({len(exponent_binary)})");
		print(f"Debug: mantissa_binary: {mantissa_binary} ({len(mantissa_binary)})");

	# assembling float structure
	result = sign + exponent_binary + mantissa_binary;
	return result;

# ---------------------------------------------------------------------------
# float to decimal

def float_to_decimal(binary):
	print(f"Converting {binary} to decimal...");

	# determining precision
	length = len(binary)
	if length == 32:
		PRE = "single"
		EXP = 8
		MAN = 23
		BIA = 127
	elif length == 64:
		PRE = "double"
		EXP = 11
		MAN = 52
		BIA = 1023
	if debug:
		print("Debug: PRE:", PRE)

	# splitting binary
	sig = binary[0]
	exp = binary[1:1+EXP]
	man = binary[1+EXP:]
	if debug:
		print("Debug: sig:", sig)
		print("Debug: exp:", exp)
		print("Debug: man:", man)

	# special values
	if exp == '0' * EXP:		# exponent is all 0s
		if man == '0' * MAN:	# mantissa is all 0s
			return 0.0
		else:					# arbitary mantissa
			return "Denormalized"
	elif exp == '1' * EXP:		# exponent is all 1s
		if man == '0' * MAN:	# mantissa is all 0s
			result = "Inf"
			if sig == '1':
				result = '-' + result
			return result
		else:					# arbitary mantissa
			return "NaN"

# ---------------------------------------------------------------------------
if __name__ == "__main__":
	print("IEEE 754 Decimal <-> Float Converter\nPrototype v2");

	# testing decimal to float
	
	"""
	test_numbers = [-42.625, 69.420, 0.0, 1.0, 0.999, 0.000123, 1000000];
	solutions = ["11000010001010101000000000000000", "01000010100010101101011100001010", "00000000000000000000000000000000", "00111111100000000000000000000000", "00111111011111111011111001110111", "00111001000000001111100110010000", "01001001011101000010010000000000"]
	n = len(test_numbers);
	for i in range(n):
		print("\n---------------------------------------------------------------------------\n");
		result = decimal_to_float(test_numbers[i], 'single');
		print(f"\nResult: {result} ({len(result)})");
		print(f"Answer: {solutions[i]}");
		if result == solutions[i]:
			print("Correct!");
		else:
			print("Incorrect!");
	"""

	"""
	i = 0;
	score = 0.0;
	while True:
		print("\n---------------------------------------------------------------------------\n");
		i += 1
		print(f"{i} ({round(score / i * 100)}%);")

		# https://www.slingacademy.com/article/python-how-to-convert-a-float-to-binary/
		scale = 1000000
		number = random() * scale - (scale / 2)
		
		result = decimal_to_float(number, "single")
		print("\nResult: " + result)

		s = struct.pack('!f', number)
		b = ''.join(format(c, '08b') for c in s)
		print("Answer: " + b)
		
		if result == b:
			print('\033[92m' + "Correct!" + '\033[0m')
			score += 1;
		else:
			print('\033[91m' + "Incorrect!" + '\033[0m')
			input()
	"""

	# testing float to decimal
	test_numbers = ["00000000000000000000000000000000", "10000000001010101010101000111100", "01111111100000000000000000000000", "11111111100000000000000000000000", "01111111101010101010101000111100"]
	solutions = [0.0, "Denormalized", "Inf", "-Inf", "NaN"];
	n = len(test_numbers);
	for i in range(n):
		print("\n---------------------------------------------------------------------------\n");
		result = float_to_decimal(test_numbers[i]);
		print(f"\nResult: {result}");
		print(f"Answer: {solutions[i]}");
		if result == solutions[i]:
			print("Correct!");
		else:
			print("Incorrect!");
	