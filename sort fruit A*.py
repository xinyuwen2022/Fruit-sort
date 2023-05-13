#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 09:47:14 2023

@author: wenxinyu
"""
import heapq
import numpy as np

def normalize_and_sort(data, min_val, max_val):


     # Extract sizes from the given data
    sizes = [d[1] for d in data]
    
    # Normalize sizes within the specified range
    normalized_sizes = np.interp(sizes, (min(sizes), max(sizes)), (min_val, max_val))
    
    # Convert normalized sizes to integers
    normalized_sizes = [int(x) for x in normalized_sizes]
    
    return normalized_sizes

def group_and_normalize(data,fruit_order):

    # Flatten the data into a single list
    flat_data = [item for sublist in data for item in sublist]
    
    # Group fruits by their types
    fruits = {}
    for d in flat_data:
        if d[0] in fruits:
            fruits[d[0]].append(d)
        else:
            fruits[d[0]] = [d]

    # Normalize sizes for each fruit type
    for fruit, sizes in fruits.items():
        if fruit == fruit_order[0]:
            min_val, max_val = 1, 10
        elif fruit == fruit_order[1]:
            min_val, max_val = 11, 20
        else:  # orange
            min_val, max_val = 21, 30
        fruits[fruit] = normalize_and_sort(sizes, min_val, max_val)
    
    # Replace original sizes with normalized sizes in the original data structure
    output = []
    for sublist in data:
        normalized_sublist = []
        for item in sublist:
            fruit, size = item
            normalized_size = fruits[fruit].pop(0)
            normalized_sublist.append(normalized_size)
        output.append(normalized_sublist)
    
    return output

def map_to_original(input_data, data,fruit_order):

    # Flatten the data into a single list
    flat_data = [item for sublist in data for item in sublist]
    
    # Group fruits by their types and sort the sizes
    fruits = {}
    for d in flat_data:
        if d[0] in fruits:
            fruits[d[0]].append(d[1])
        else:
            fruits[d[0]] = [d[1]]
    for fruit in fruits:
        fruits[fruit].sort()
    
    # Map the input_data to original sizes
    output = []
    for sublist in input_data:
        original_sublist = []
        for item in sublist:
            if 1 <= item <= 10:
                fruit = fruit_order[0]
            elif 11 <= item <= 20:
                fruit = fruit_order[1]
            else:  # 21 <= item <= 30
                fruit = fruit_order[2]
            original_size = fruits[fruit].pop(0)
            original_sublist.append((fruit, original_size))
        output.append(original_sublist)
    
    return output

# Heuristic function to estimate the number of moves required to reach the goal state
def heuristic(state):

    joined_list = []
    for sublist in state:
        joined_list.extend(sublist)
    sorted_list = sorted(joined_list)
    return np.sum(np.abs(np.array(joined_list) - np.array(sorted_list)))

def possible_moves(state):

    moves = []
    for i in range(3):
        for j in range(10):
            # Horizontal swap: exchange two fruits in the same column
            if j < 9:
                new_state = [list(column) for column in state]
                new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
                moves.append(new_state)
            # Vertical swap: exchange two fruits in different columns
            if i < 2:
                new_state = [list(column) for column in state]
                new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                moves.append(new_state)
    return moves

# A* algorithm to find the minimum number of moves required to reach the goal state
def a_star(initial_state, data,fruit_order):

    queue = [(heuristic(initial_state), 0, initial_state)]  # Initialize the priority queue with the initial state
    
   
    visited = []  # Set to store the visited states
    while queue:

        c, steps, state = heapq.heappop(queue)  # Pop the state with the lowest estimated cost

        if np.array_equal(state, (np.arange(1, 31)).reshape((3, 10))):
            # Goal state reached

            # print("Normalized end state:",state)
            
            for sublist in map_to_original(state, data,fruit_order):
                print(sublist)
            print("\n")

            return steps  # Return the number of steps if the goal state is reached

        for new_state in possible_moves(state):  # Generate all possible next states
            

            if  new_state not in visited:
                visited.append( new_state)  # Add the new state to the visited set
                cost = heuristic(new_state) + steps + 1  # Calculate the cost of the new state
                # print("available possible state and cost",new_state, cost)
                heapq.heappush(queue, (cost, steps + 1, new_state))  # Add the new state to the priority queue

    return -1 # No solution

def main():

    # Specify the order of fruit types
    fruit_order=["banana", "apple", "orange"]

    # Define the initial state of the baskets
    data = [
    [('apple', 4), ('apple', 2), ('apple', 8), ('apple', 3), ('apple', 7), ('banana', 10), ('banana', 5), ('banana', 1), ('banana', 8), ('banana', 3)], 
    [('orange', 5), ('banana', 7), ('banana', 2), ('banana', 9), ('banana', 6), ('orange', 3), ('orange', 4), ('orange', 7), ('orange', 2), ('orange', 9)], 
    [('orange', 6), ('orange', 10), ('banana', 4), ('orange', 1), ('orange', 8), ('apple', 1), ('apple', 9), ('apple', 6), ('apple', 10), ('apple', 5)]]
    # print("Original Initial State", data)
   
    
    initial_state = group_and_normalize(data, fruit_order) 
    
    # Find the minimum number of moves required to reach the goal state using A* algorithm
    moves = a_star(initial_state, data, fruit_order)
    print(f"Minimum number of moves: {moves}")

if __name__ == "__main__":
    main()
