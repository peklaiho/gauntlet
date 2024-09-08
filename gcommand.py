import sys
import os

import gutils
import gdatabase
import gfight

# List of all commands in the game
command_table = [
	( "army",       "(show your army)" ),
	( "buy",        "(buy troops)" ),
	( "commands",   "(list commands)" ),
	( "enemy",      "(show hostile army)" ),
	( "fight",      "(start a fight)" ),
	( "file",       "(view text files)" ),
	( "flee",       "(escape combat)" ),
	( "gold",       "(show your wealth)" ),
	( "help",       "(view help)" ),
	( "info",       "(show troop info)" ),
	( "next",       "(start next round)" ),
	( "quit",       "(quit the game)" ),
	( "save",       "(save progress)" ),
	( "sell",       "(sell troops)" ),
	( "status",     "(display status)" ),
]

def cmd_army(args, state):
	army = state["army"]
	if len(army) == 0:
		print("You do not have any troops in your army.")
	else:
		print("Your army consists of the following troops:")
		gutils.print_army(army)

def cmd_buy(args, state):
	player = state["player"]
	monsters = state["monsters"]
	army = state["army"]

	if gutils.fighting(state["fight"]):
		print("You cannot buy troops in the middle of a fight.")
		return

	# Parse quantity if given
	qty = 1
	if len(args) >= 3:
		try:
			qty = int(args[2])
		except:
			qty = 0
		if qty <= 0:
			print("Invalid quantity.")
			return

	# Display all possible creatures
	if len(args) < 2:
		print("   #  Name             Lvl   Cost")
		print("-----------------------------------")
		for i in range(0, len(monsters)):
			m = monsters[i]
			gutils.cprint("  {0:>2}  @y{1:<16}@n  {2}   @Y{3:>5}".format(i + 1, m["name"], m["level"], m["cost"]))
	# We are actually buying something
	else:
		for m in monsters:
			if m["name"].startswith(args[1]):
				# Calculate how many we can really afford
				total = m["cost"] * qty
				if total > player["gold"]:
					qty = player["gold"] // m["cost"]
					total = m["cost"] * qty
				# Handle purchase
				if qty == 0:
					gutils.cprint("You can't afford a single @y{0}@n!".format(m["name"]))
				else:
					if gutils.add_to_army(m, army, qty):
						player["gold"] = player["gold"] - total
						gutils.cprint("You buy {0} @y{1}@n for @Y{2}@n gold.".format(qty, gutils.name(qty, m), total))
						gutils.cprint("You have @Y{0}@n gold remaining.".format(player["gold"]))
					else:
						print("Your army can only contain 8 types of troops.")
				return
		print("No troop by such name.")

def cmd_commands(args, state):
	print("Available commands:")
	for i in range(0, len(command_table)):
		gutils.cprint("  @r{0:<8}@n  {1:<19}".format(command_table[i][0], command_table[i][1]), e="")
		if (i % 2) != 0:
			print()
	if (len(command_table) % 2) != 0:
		print()

def cmd_enemy(args, state):
	if not gutils.fighting(state["fight"]):
		print("You are not currently in a fight.")
	else:
		print("The hostile army consists of the following troops:")
		gutils.print_army(state["fight"]["enemy"])

def cmd_fight(args, state):
	if gutils.fighting(state["fight"]):
		print("You are already fighting!")
	elif len(state["army"]) == 0:
		print("Your army has no troops to start a fight with.")
	else:
		gutils.new_enemy(state["army"], state["fight"]["enemy"], state["monsters"])
		print("You encounter a hostile army:")
		gutils.print_army(state["fight"]["enemy"])
		state["fight"]["round"] = 0
		# Calculate reward which player receives on victory
		state["fight"]["reward"] = gutils.army_cost(state["fight"]["enemy"])

def cmd_file(args, state):
	if len(args) < 2:
		print("Available files:")
		for f in os.listdir("txt/"):
			gutils.cprint("  @r{0}".format(f))
	elif not args[1].isalpha():
		print("Invalid file name.")
	else:
		try:
			gutils.show_file(args[1])
		except:
			print("Unable to read file {0}.".format(args[1]))

def cmd_flee(args, state):
	if not gutils.fighting(state["fight"]):
		print("Flee from what?")
	else:
		if gutils.randint(0, 1) == 0:
			del state["fight"]["enemy"][:]
			# Restore the health of all your troops to full
			for troop in state["army"]:
				troop["health"] = troop["monster"]["health"]
			print("You flee from the fight like a pathetic coward.")
		else:
			print("You are unable to flee. The enemy attacks.")
			gfight.next_round(state)

def cmd_gold(args, state):
	gutils.cprint("You have @Y{}@n gold coins.".format(state["player"]["gold"]))

def cmd_help(args, state):
	gutils.show_file("help")

def cmd_info(args, state):
	monsters = state["monsters"]
	if len(args) < 2:
		print("Available troops:")
		for m in monsters:
			gutils.cprint("  @y{0}".format(m["name"]))
	else:
		for m in monsters:
			if m["name"].startswith(args[1]):
				gutils.cprint("Information about '@y{0}@n':".format(m["name"]))
				print("  Type:       {0}".format(m["type"]))
				print("  Level:      {0}".format(m["level"]))
				print("  Cost:       {0}".format(m["cost"]))
				print("  Att / Def:  {0} / {1}".format(m["attack"], m["defense"]))
				print("  Damage:     {0} - {1}".format(m["min_dam"], m["max_dam"]))
				print("  Health:     {0}".format(m["health"]))
				print("  Speed:      {0}".format(m["speed"]))
				print("  Flags:     {0}".format(gutils.monster_flags(m)))
				return
		print("No troop by such name.")

def cmd_next(args, state):
	if not gutils.fighting(state["fight"]):
		print("You can only start the next round during a fight.")
	else:
		gfight.next_round(state)

def cmd_quit(args, state):
	if gutils.fighting(state["fight"]):
		print("You cannot quit during a fight.")
	else:
		gdatabase.save_player(state)
		print("Goodbye...")
		sys.exit()

def cmd_save(args, state):
	if gutils.fighting(state["fight"]):
		print("You cannot save your progress during a fight.")
	else:
		gdatabase.save_player(state)
		print("Saved.")

def cmd_sell(args, state):
	player = state["player"]
	army = state["army"]

	if gutils.fighting(state["fight"]):
		print("You cannot sell troops in the middle of a fight.")
		return
	elif len(args) < 2:
		print("Sell which troop?")
		return

	# Parse quantity if given
	qty = 1
	if len(args) >= 3:
		try:
			qty = int(args[2])
		except:
			qty = 0
		if qty <= 0:
			print("Invalid quantity.")
			return

	# Find the right monster in player's army
	for i in range(0, len(army)):
		troop = army[i]
		if troop["monster"]["name"].startswith(args[1]):
			# Check for limit
			if qty > troop["qty"]:
				qty = troop["qty"]
			# Delete totally or lower qty
			if qty == troop["qty"]:
				army.pop(i)
			else:
				troop["qty"] = troop["qty"] - qty
			# Calculate total price and add to gold
			total = (qty * troop["monster"]["cost"]) // 2
			player["gold"] = player["gold"] + total
			# Show messages to player
			gutils.cprint("You sell {0} @y{1}@n for @Y{2}@n gold.".format(qty, gutils.name(qty, troop["monster"]), total))
			gutils.cprint("You have @Y{0}@n gold total.".format(player["gold"]))
			return
	print("No such troop in your army.")

def cmd_status(args, state):
	player = state["player"]
	army = state["army"]

	sex_titles = {
		"m": "handsome young Lord",
		"f": "beautiful young Lady"
	}

	gutils.cprint("You are a {0} named {1}.".format(sex_titles[player["sex"]], player["name"]))
	gutils.cprint("You have {0} experience and you are level {1}.".format(player["exp"], player["level"]))
	gutils.cprint("You have {0} male and {1} female servants.".format(player["m_servants"], player["f_servants"]))
	gutils.cprint("You have @Y{0}@n gold coins and {1} acres of land.".format(player["gold"], player["land"]))
	gutils.cprint("Your army contains a total of {0} troops.".format(sum(troop["qty"] for troop in army)))

def handle_command(args, state):
	if len(args) == 0:
		return

	for cmd in command_table:
		if cmd[0].startswith(args[0]):
			globals()["cmd_" + cmd[0]](args, state)
			return

	# Command was not found
	print("Unknown command.")
