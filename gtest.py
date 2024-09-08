import sys

import gfight

total_tests = 0

def asrt(cond, num, result):
	global total_tests
	total_tests = total_tests + 1
	if not cond:
		sys.exit("Test " + str(num) + " failed. Result: " + str(result))

# 1. Basic damage calc
dam = gfight.calc_damage(3, 3, 10, 10, 10)
asrt(dam == 30, 1, dam)

# 2. Attack bigger than def
dam = gfight.calc_damage(2, 2, 10, 5, -5)
asrt(dam == 30, 2, dam)

# 3. Def bigger than att
dam = gfight.calc_damage(2, 2, 10, -10, 10)
asrt(dam == 10, 3, dam)

# 4. Min/Max dam variance
res = [0, 0]
for i in range(0, 20):
	dam = gfight.calc_damage(1, 2, 1, 0, 0)
	res[dam - 1] = res[dam - 1] + 1
asrt(res[0] >= 5 and res[1] >= 5, 4, res)

# 5.
killed = gfight.calc_killed(30, 20, 10)
remain = gfight.calc_health(30, 20, 10)
asrt(killed == 2 and remain == 20, 5, (killed, remain))

# 6.
killed = gfight.calc_killed(24, 20, 5)
remain = gfight.calc_health(24, 20, 5)
asrt(killed == 1 and remain == 1, 6, (killed, remain))

# 7.
killed = gfight.calc_killed(26, 20, 5)
remain = gfight.calc_health(26, 20, 5)
asrt(killed == 2 and remain == 19, 7, (killed, remain))

# 8.
killed = gfight.calc_killed(5, 20, 5)
remain = gfight.calc_health(5, 20, 5)
asrt(killed == 1 and remain == 20, 8, (killed, remain))

# 9.
killed = gfight.calc_killed(2, 20, 5)
remain = gfight.calc_health(2, 20, 5)
asrt(killed == 0 and remain == 3, 9, (killed, remain))

print("All " + str(total_tests) + " tests ok!")
