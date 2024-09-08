# Gauntlet

Gauntlet is a single player text game written in Python. It is loosely based on the popular *Heroes of Might & Magic* games. You hire an army and fight against other armies for gold and experience.

I wrote this game in 2013 as an exercise to learn Python. The code reflects that; it is not beautiful. But it is a fun little game.

## How to play

Run the game:

    $ python gmain.py

The game will create a SQLite database file `gauntlet.db` on first start and exit.

Next you need to add some monsters into the database. You can do so by executing this shell script:

    $ ./add-monsters.sh

You can edit the script before running it to add your own monsters.

After there are monsters in the database run the game again and you can start playing normally:

    $ python gmain.py

While playing type `commands` to see available commands.

The game is not easy! When you encounter an enemy, you need to carefully consider should you fight them or attempt to flee. You should only fight if the enemy army is clearly weaker than yours. Also it matters which troops you choose to buy. Some are better than others.
