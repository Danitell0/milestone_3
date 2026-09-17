Tests:

./codexion 1 800 200 200 100 3 0 fifo	dongle at 0, burnout at 800	(burnout + stops at 800)
./codexion 4 800 200 200 100 3 0 fifo	no burnout, stops at 3 compiles (success)	
./codexion 4 800 200 200 100 3 0 edf	same (success)


./codexion 4 800 200 200 100 3 1 fifo	behaves like cooldown 0	(success)
./codexion 4 800 200 200 100 3 50 fifo	no burnout (success)
./codexion 4 800 200 200 100 3 50 edf	no burnout (success)

./codexion 5 1000 200 100 100 5 50 edf	no burnout (success)
./codexion 5 800 200 100 100 5 50 edf	no burnout (success)
./codexion 5 700 200 100 100 5 50 edf	burnout	infeasible, correct (burnout at 700, runs until 901)
./codexion 5 610 200 100 100 5 50 edf	burnout	infeasible, correct (burnout at 610, runs until 901)
./codexion 7 900 200 100 100 5 50 fifo	no burnout (success)
./codexion 7 900 200 100 100 5 50 edf	no burnout (sucess)
./codexion 7 700 200 100 100 5 50 fifo	burnout	probably infeasible (burnout at 702, runs until 902)
./codexion 7 700 200 100 100 5 50 edf	burnout	probably infeasible (burnout at 702, runs until 903)

./codexion 4 100 200 200 100 3 0 fifo	compile alone exceeds burnout (burnout at 100, runs until 500)
./codexion 4 300 100 100 100 3 500 fifo	cooldown outlasts the deadline (burnout + stops at 300)

./codexion 2 400 200 100 100 3 0 fifo	only one compiles at a time	not run (burnout at 800, runs until 1000)
./codexion 200 800 200 200 100 3 0 fifo (finishes at 1713, runs until 2216)

