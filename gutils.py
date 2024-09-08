import os
import random

###################
# Login functions #
###################

def valid_name(name):
	return len(name) >= 3 and len(name) <= 20 and name.isalpha()

def valid_sex(sex):
	return len(sex) > 0 and sex[0] in ["m", "f"]

def ask_name():
	player_name = input("What is your name? ")
	while not valid_name(player_name):
		player_name = input("Invalid name. What is your name? ")
	return player_name.capitalize()

def ask_sex():
	player_sex = input("What is your sex? ").lower()
	while not valid_sex(player_sex):
		player_sex = input("Invalid sex. What is your sex? ").lower()
	return player_sex[0]

##############
# Misc utils #
##############

def fighting(fight):
	return len(fight["enemy"]) > 0

def show_file(name):
	with open(os.getcwd() + "/txt/" + name) as f:
		for line in f:
			print(line, end="")

# Return single or plural name, depending on quantity
def name(qty, monster):
	if qty == 1:
		return monster["name"]
	else:
		return monster["plural"]

def randint(a, b):
	return random.randint(a, b)

def randfloat(a, b):
	return random.uniform(a, b)

#################
# Monster utils #
#################

def monster_flags(monster):
	retval = " (none)"
	return retval

def counterattacks(monster):
	return 1

###################
# Army management #
###################

def print_army(army):
	print("   #  Name                Qty  Lvl  Health")
	print("--------------------------------------------")
	for i in range(0, len(army)):
		troop = army[i]
		if troop["health"] < troop["monster"]["health"]:
			hstring = "@r{:.1f}@n ({})".format(troop["health"], troop["monster"]["health"])
		else:
			hstring = "@g{:.1f}@n".format(troop["health"])
		cprint("  {0:>2}  @y{1:<16}@n  {2:>5}   {3}   {4}".format(i + 1, troop["monster"]["name"], troop["qty"], troop["monster"]["level"], hstring))

def add_to_army(monster, army, qty):
	# We only have 8 slots in the army
	maxSlots = 8

	# New troop to add
	newTroop = { "monster": monster, "qty": qty, "health": monster["health"] }

	# Try to add in the middle
	for i in range(0, len(army)):
		troop = army[i]
		if monster["name"] == troop["monster"]["name"]:
			troop["qty"] = troop["qty"] + qty
			return True
		elif monster["name"] < troop["monster"]["name"] and len(army) < maxSlots:
			army.insert(i, newTroop)
			return True

	# Try to add to end
	if len(army) < maxSlots:
		army.append(newTroop)
		return True
	else:
		return False

def remove_from_army(monster, army):
	for i in range(0, len(army)):
		if monster["name"] == army[i]["monster"]["name"]:
			army.pop(i)
			return

def army_cost(army):
	return sum(troop["monster"]["cost"] * troop["qty"] for troop in army)

def new_enemy(army, enemy, monsters):
	player_army_cost = army_cost(army)
	target_cost = randfloat(player_army_cost * 0.5, player_army_cost)

	while army_cost(enemy) < target_cost:
		index = randint(0, len(monsters) - 1)
		qty = 1
		add_to_army(monsters[index], enemy, qty)

def has_melee_troops(army):
	for troop in army:
		if troop["monster"]["type"] == "attacker" or troop["monster"]["type"] == "defender":
			return True
	return False

def has_ranged_troops(army):
	for troop in army:
		if troop["monster"]["type"] == "ranged":
			return True
	return False

##################
# Colored output #
##################

ansi_colors = {
	"@h": "\033[0;30m",
	"@r": "\033[0;31m",
	"@g": "\033[0;32m",
	"@y": "\033[0;33m",
	"@b": "\033[0;34m",
	"@m": "\033[0;35m",
	"@c": "\033[0;36m",
	"@w": "\033[0;37m",

	"@H": "\033[1;30m",
	"@R": "\033[1;31m",
	"@G": "\033[1;32m",
	"@Y": "\033[1;33m",
	"@B": "\033[1;34m",
	"@M": "\033[1;35m",
	"@C": "\033[1;36m",
	"@W": "\033[1;37m",

	"@n": "\033[0m",
	"@@": "@"
}

def parse_color_codes(txt):
	if txt.find("@") >= 0:
		for key, val in ansi_colors.items():
			txt = txt.replace(key, val)
		return txt + ansi_colors["@n"]
	else:
		return txt

def cprint(txt, e="\n"):
	print(parse_color_codes(txt), end=e)

def cinput(txt):
	return input(parse_color_codes(txt))
