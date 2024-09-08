import gdatabase
import gutils
import gcommand

# Global variables
state = {
	"player": {
		"name": "Unnamed",
		"sex": "m",
		"level": 1,
		"exp": 0,

		"gold": 100,
		"land": 100,

		"m_servants": 2,
		"f_servants": 2
	},
	"monsters": [],
	"army": [],
	"fight": {
		"enemy": [],
		"round": 0,
		"reward": 0
	}
}

# Initialize database
gdatabase.init(state["monsters"])

# Welcome message
gutils.cprint("@gWelcome to Gauntlet!")
print()
state["player"]["name"] = gutils.ask_name()

# Try to load the player from database
if gdatabase.load_player(state):
	# Handle existing player
	gutils.cprint("Loading existing character @r{0}@n.".format(state["player"]["name"]))
else:
	# Handle new player
	gutils.cprint("Creating new character @r{0}@n.".format(state["player"]["name"]))
	state["player"]["sex"] = gutils.ask_sex()
	gdatabase.save_player(state, True)
	# Show the background story
	print()
	gutils.show_file("story")

# Enter main loop
while True:
	print()
	# Different prompt depending on whether a fight is going on or not
	if gutils.fighting(state["fight"]):
		args = input("(fighting) > ")
	else:
		args = input("> ")
	gcommand.handle_command(args.lower().split(), state)
