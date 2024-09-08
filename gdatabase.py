import sqlite3

# sqlite3 database connection
conn = None

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def init(monsters):
	global conn
	conn = sqlite3.connect("gauntlet.db")
	conn.row_factory = dict_factory

	# Read monsters from database
	with conn:
		sql = "SELECT * FROM monsters ORDER BY level, name"
		result = conn.execute(sql).fetchall()
		for m in result:
			monster = {}
			for k in m.keys():
				monster[k] = m[k]
			monsters.append(monster)

def load_player(state):
	player = state["player"]
	army = state["army"]
	monsters = state["monsters"]

	with conn:
		# Load player
		sql = "SELECT * FROM players WHERE name=:name"
		result = conn.execute(sql, player).fetchone()
		if not result:
			return False
		for k in result.keys():
			player[k] = result[k]

		# Load army
		sql = "SELECT monster, qty FROM armies WHERE player=:name ORDER BY monster"
		result = conn.execute(sql, player).fetchall()
		for row in result:
			m = None
			# Find the right monster
			for mon in monsters:
				if mon["name"] == row["monster"]:
					m = mon
					break
			if m:
				troop = { "monster": m, "qty": row["qty"], "health": m["health"] }
				army.append(troop)
			else:
				print("Unable to find monster '{0}' while loading army.".format(row["monster"]))
		return True

def save_player(state, insert = False):
	player = state["player"]
	army = state["army"]

	with conn:
		# Save player
		keys = list(player.keys())
		if insert:
			sql = "INSERT INTO players (" + (",".join(keys)) + ") VALUES (:" + (",:".join(keys)) + ")";
		else:
			keys.remove("name")
			keys = list(key + "=:" + key for key in keys)
			sql = "UPDATE players SET " + (",".join(keys)) + " WHERE name=:name"
		conn.execute(sql, player)

		# Save army
		sql = "DELETE FROM armies WHERE player=:name"
		conn.execute(sql, player)
		for troop in army:
			sql = "INSERT INTO armies (player, monster, qty) VALUES (?, ?, ?)"
			conn.execute(sql, (player["name"], troop["monster"]["name"], troop["qty"]))
