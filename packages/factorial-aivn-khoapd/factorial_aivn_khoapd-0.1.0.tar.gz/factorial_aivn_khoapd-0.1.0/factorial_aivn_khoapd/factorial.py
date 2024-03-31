def fact(n):
	"""
	3 Tính giai thừa của một số nguy ên dương n.
	4
	5 Tham số:
	6 - n: Số nguy ên dương.
	7
	8 Trả về:
	9 - Giai thừa của n.
	10 """

	if n < 0:
		raise ValueError(" Factorial is not defined for negative numbers ")
	elif n == 0 or n == 1:
		return 1
	else:
		return n * fact(n - 1)
