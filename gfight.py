import gutils

def calc_damage(min_dam, max_dam, qty, attack, defense):
	dam = gutils.randint(min_dam, max_dam) * qty

	if attack > defense:
		dam = dam * (1 + (0.05 * (attack - defense)))
	elif defense > attack:
		dam = dam / (1 + (0.05 * (defense - attack)))

	# Damage must be at least 1
	return max(1.0, dam)

def calc_killed(dam, total_health, remaining_health):
	# Calculate how many full ones were killed
	killed = dam // total_health
	# First one with low health was also possibly killed
	if dam % total_health >= remaining_health:
		killed = killed + 1
	return int(killed)

def calc_health(dam, total_health, remaining_health):
	return total_health - ((dam - remaining_health) % total_health)

# Return True if some defending troops survived
def do_attack(attacker, defender, att_side, is_counter):
	# Calculate damage
	dam = calc_damage(attacker["monster"]["min_dam"], attacker["monster"]["max_dam"], attacker["qty"],
		attacker["monster"]["attack"], defender["monster"]["defense"])

	# Calculate how many were killed
	killed = min(calc_killed(dam, defender["monster"]["health"], defender["health"]), defender["qty"])

	# Print a message to player
	if att_side == 0:
		att_side_str = "Your"
		def_side_str = "Enemy"
		att_col = "@g"
	else:
		att_side_str = "Enemy"
		def_side_str = "Your"
		att_col = "@r"

	# att_qty_str = "" if attacker["qty"] == 1 else " (" + str(attacker["qty"]) + ")"
	# def_qty_str = "" if defender["qty"] == 1 else " (" + str(defender["qty"]) + ")"

	gutils.cprint("{} @y{}@n {}attack{} {} @y{}@n for {:.1f} damage".format(
		att_side_str, gutils.name(attacker["qty"], attacker["monster"]),
		"counter" if is_counter else "", "s" if attacker["qty"] == 1 else "",
		def_side_str.lower(), gutils.name(defender["qty"], defender["monster"]),
		dam), e="")
	if killed > 0:
		gutils.cprint(", killing {0}{1}@n.".format(att_col, killed))
	else:
		print(".")

	# Reduce the killed amount
	defender["qty"] = defender["qty"] - killed

	# If any remain alive, calculate their remaining health
	if defender["qty"] > 0:
		defender["health"] = calc_health(dam, defender["monster"]["health"], defender["health"])
		return True
	else:
		return False

def can_attack(attacker, defender, att_army, def_army, is_counter):
	# Melee units can never attack ranged units if defender has
	# melee troops present
	if attacker["monster"]["type"] != "ranged" and defender["monster"]["type"] == "ranged" and gutils.has_melee_troops(def_army):
		return False

	# Ranged troops can never counterattack
	# Ranged troops can never be countered
	if is_counter and (attacker["monster"]["type"] == "ranged" or defender["monster"]["type"] == "ranged"):
		return False

	# Other attacks are ok
	return True

def find_target(attacker, att_army, def_army):
	# Find all possible targets
	targets = []
	for i in range(0, len(def_army)):
		if can_attack(attacker, def_army[i], att_army, def_army, False):
			targets.append(i)

	if len(targets) == 0:
		return None
	else:
		# Select random target for now
		return def_army[targets[gutils.randint(0, len(targets) - 1)]]

def next_round(state):
	player = state["player"]
	army = state["army"]
	fight = state["fight"]
	enemy = fight["enemy"]

	fight["round"] = fight["round"] + 1
	print("Round {0} starts...".format(fight["round"]))

	# Check for ranged troops (no melee attack in 1st round if present)
	ranged_troops = gutils.has_ranged_troops(army) or gutils.has_ranged_troops(enemy)

	# Add all troops to a common list
	unacted_fighters = []
	for troop in army:
		troop["countered"] = 0
		if fight["round"] > 1 or troop["monster"]["type"] == "ranged" or not ranged_troops:
			ftroop = {
				"side": 0,
				"speed": troop["monster"]["speed"] + gutils.randfloat(-0.5, 0.5),
				"troop": troop
			}
			unacted_fighters.append(ftroop)
	for troop in enemy:
		troop["countered"] = 0
		if fight["round"] > 1 or troop["monster"]["type"] == "ranged" or not ranged_troops:
			ftroop = {
				"side": 1,
				"speed": troop["monster"]["speed"] + gutils.randfloat(-0.5, 0.5),
				"troop": troop
			}
			unacted_fighters.append(ftroop)

	# Sort the fighters by their speed
	unacted_fighters = sorted(unacted_fighters, key=lambda troop: troop["speed"], reverse=True)

	while len(unacted_fighters) > 0:
		# Select attacking and defending troops
		att_side = unacted_fighters[0]["side"]
		def_side = 1 if att_side == 0 else 0
		att_army = army if att_side == 0 else enemy
		def_army = army if def_side == 0 else enemy
		attacker = unacted_fighters[0]["troop"]
		defender = find_target(attacker, att_army, def_army)

		# Perform the attack if we have a target
		if defender:
			if do_attack(attacker, defender, att_side, False):
				# Some defenders survived, try to perform a counterattack
				if defender["countered"] < gutils.counterattacks(defender["monster"]) and can_attack(defender, attacker, def_army, att_army, True):
					defender["countered"] = defender["countered"] + 1
					if not do_attack(defender, attacker, def_side, True):
						gutils.remove_from_army(attacker["monster"], att_army)
			else:
				# All defenders died, remove defender from army
				gutils.remove_from_army(defender["monster"], def_army)
				# Also remove defender from unacted list (start at index 1, because 0 is attacker)
				for i in range(1, len(unacted_fighters)):
					if unacted_fighters[i]["side"] == def_side and unacted_fighters[i]["troop"]["monster"]["name"] == defender["monster"]["name"]:
						unacted_fighters.pop(i)
						break

		# Remove attacker from unacted list
		unacted_fighters.pop(0)

		# Check for end conditions
		if len(enemy) == 0:
			reward_gold = fight["reward"] // 4
			reward_exp = fight["reward"] // 2
			player["gold"] = player["gold"] + reward_gold
			player["exp"] = player["exp"] + reward_exp
			print("You are victorious!")
			gutils.cprint("Your reward is @Y{0}@n gold and @m{1}@n experience.".format(reward_gold, reward_exp))
			# Restore the health of all your troops to full
			for troop in army:
				troop["health"] = troop["monster"]["health"]
			return
		elif len(army) == 0:
			print("You have been defeated!")
			print("The enemy has taken all your gold and servants.")
			player["gold"] = 0
			player["m_servants"] = 0
			player["f_servants"] = 0
			del enemy[:]
			return
