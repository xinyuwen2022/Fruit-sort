# Fruit-sort

You are given 10 apples of different sizes, 10 bananas of different sizes and 10 oranges of different sizes, 
organized in a 3x10 array.  You want to organize them so that fruits go from top to bottom in ascending order of size.
Any fruit can be used in any column that you like.  The only move allowed is to swap two fruits horizontally or vertically. 
You want to use A* algorithm to minimize the number of moves for this.


The A* search algorithm is used in the code to solve this problem.
The A* search algorithm is a heuristic search algorithm that uses an evaluation function to determine the direction of the next search. 
The evaluation function usually consists of two parts, 
one is the length of the path that has been walked (in this case,
the number of swaps that have been made),
and the other is a heuristic function that estimates how many steps are still needed from the current state to the target state (in this case,
the difference between the fruits in the current basket and the target sorting).
