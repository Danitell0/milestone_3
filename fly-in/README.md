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
