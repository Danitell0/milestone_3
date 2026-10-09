Resources:

Maximum flow problem - https://en.wikipedia.org/wiki/Maximum_flow_problem

Design
Class

MapParser           - read the file, raise errors with line numbers, build Map
Map                 - zones and connections
Zone / Connections  - capacity, cost, current occupancy and reservations
Drone               - id, position or in_flight state, turns remaining
PathFinder          - reverse Dijkstra, distance per zone
Simulation          - turn loop, active drones, distances, turn counter


Map	Target	You
easy 1 / 2 / 3	≤ 6 / 8 / 6	         4 / 4 / 4
medium 1 / 2 / 3	≤ 12 / 15 / 12	 6 / 15 / 8
hard 1 / 2 / 3	≤ 30 / 35 / 45	     13 / 16 / 26
challenger	45 (optional)	         45
