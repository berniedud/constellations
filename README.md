# constellations

Solving a (graph) problem from [Reddit](https://www.reddit.com/r/CodingHelp/comments/od2aew/python_starmapping_question/)

```
I have used a couple for loops to randomly assign x and y
coordinates for stars on a generated star map. stars work 
100 percent I wrote an algorithm that draws a line from 
each star to it's closest neighbor in an attempt to 
simulate trade routes, or roads, but it is giving 
disjointed constellations with gaps between them. 
Does anyone know a way to ensure that all the stars 
will be connected by roads, but by the minimum number of 
roads needed to accomplish the task?
```

You can run the code like this (your results will be different because stars are random):
```python
from pprint import pprint
from stars.main import create_and_connect_stars, find_all_constellations, connect_constellations

stars = create_and_connect_stars(20)    # try another number!
constellations = find_all_constellations(stars)
pprint(constellations)
"""
[{0, 16, 1, 6, 12, 14},
 {2, 11, 13},
 {18, 3, 4, 5, 8},
 {19, 7},
 {17, 9},
 {10, 15}
 """

stars = connect_constellations(stars, constellations)
pprint(find_all_constellations(stars))
"""
[{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}]
"""
```