#!/bin/sh

# Add some monsters to database

echo "INSERT INTO monsters VALUES ('peasant', 'peasants', 'attacker',    1, 10, 1, 1, 1, 2, 10, 1)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('goblin', 'goblins', 'attacker',      1,  8, 1, 1, 2, 2, 15, 2)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('skeleton', 'skeletons', 'attacker',  1, 16, 2, 1, 2, 2, 20, 1)" | sqlite3 gauntlet.db

echo "INSERT INTO monsters VALUES ('boar', 'boars', 'defender',          2, 30, 2, 3, 3, 4, 40, 2)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('hound', 'hounds', 'attacker',        2, 30, 3, 2, 4, 6, 30, 4)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('medusa', 'medusae', 'ranged',        2, 40, 2, 1, 3, 4, 20, 3)" | sqlite3 gauntlet.db

echo "INSERT INTO monsters VALUES ('swordsman', 'swordsmen', 'attacker', 3, 70, 5, 3, 6, 8, 60, 1)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('pikeman', 'pikemen', 'defender',     3, 60, 3, 5, 4, 6, 60, 1)" | sqlite3 gauntlet.db
echo "INSERT INTO monsters VALUES ('archer', 'archers', 'ranged',        3, 80, 3, 1, 4, 6, 40, 1)" | sqlite3 gauntlet.db
