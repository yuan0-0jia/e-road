# E-Road

This program finds the shortest path from one city to another. The program takes in network.txt, which contains a list of tuples indicating the connections between two cities.  
vertex_names.txt contains the names of the cities, with IDs matching those in network.txt.  
vertex_locations.txt indicates the coordinates of each city in vertex_names.txt.

## Usage

Run the program with the following command:

```
python3 e_roads.py start_location end_location
```

This returns the shortest path of cities from start_location to end_location.

```
python3 e_roads.py start_location end_location a_third_argu
```

The third argument enables the program to return a link to Google map direction.
