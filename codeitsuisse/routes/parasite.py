import logging
import json
from collections import deque 
import copy

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

VACANT = 0
HEALTHY = 1
VACCINATED = 2
INFECTED = 3

@app.route('/parasite', methods=['POST'])
def evaluate_parasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    room_num = len(data)
    ans = []
    for i in range(room_num):
        room_ans = {}
        room_data = data[i]
        room_index = room_data["room"]
        grid = room_data["grid"]
        interestedIndividuals = room_data["interestedIndividuals"]
        
        a, b = part_1(grid, interestedIndividuals)
        room_ans["room"] = room_index
        room_ans["p1"] = a
        room_ans["p2"] = b
        room_ans["p3"] = part_3(grid, interestedIndividuals)
        room_ans["p4"] = 1
        ans.append(room_ans) 
    
    logging.info("My result :{}".format(ans))
    return jsonify(ans)


def check_infectable(grid, row, col):
    return grid[row][col] == HEALTHY

def check_infectable_part4(grid, row, col):
    return grid[row][col] == HEALTHY or grid[row][col] == VACCINATED or grid[row][col] == VACANT

def need_energy(grid, row, col):
    return grid[row][col] == VACCINATED or grid[row][col] == VACANT

def part_1(grid, interestedIndividuals):
    infected_time = dict.fromkeys(interestedIndividuals, -1)
    grid = [x[:] for x in grid]
    nRows = len(grid)
    nCols = len(grid[0])

    round = 0
    infected_q = deque()
   
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == INFECTED:
                infected_q.append([row, col])
                key = str(row) + "," + str(col)
                if key in infected_time:
                    infected_time[key] = round

    while True:
        frontier = deque()
        print("part 1 round ", round)
        print("queue", infected_q)
        while infected_q:
            [row, col] = infected_q.popleft()
            
            key = str(row) + "," + str(col)
            if key in infected_time:
                infected_time[key] = round

            if row - 1 >= 0 and check_infectable(grid, row - 1, col):
                grid[row - 1][col] = INFECTED
                frontier.append([row - 1, col])
            if row + 1 < nRows and check_infectable(grid, row + 1, col):
                grid[row + 1][col] = INFECTED
                frontier.append([row + 1, col])
            if col - 1 >= 0 and check_infectable(grid, row, col - 1):
                grid[row][col - 1] = INFECTED
                frontier.append([row, col - 1])
            if col + 1 < nCols and check_infectable(grid, row, col + 1):
                grid[row][col + 1] = INFECTED
                frontier.append([row, col + 1])
        
        if frontier:
            infected_q = frontier
            round += 1
        else:
            break

    energy = 0
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == HEALTHY:
                round = -1
    
    return infected_time, round

def part_3(grid, interestedIndividuals):
    grid = [x[:] for x in grid]
    nRows = len(grid)
    nCols = len(grid[0])

    round = 0
    infected_q = deque()
   
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == INFECTED:
                infected_q.append([row, col])

    while True:
        frontier = deque()
        print("part 3 round ", round)
        print("queue", infected_q)
   
        while infected_q:
            [row, col] = infected_q.popleft()
            grid[row][col] = INFECTED


            
            if row - 1 >= 0 and check_infectable(grid, row - 1, col):
                grid[row - 1][col] = INFECTED
                frontier.append([row - 1, col])
            
            if row + 1 < nRows and check_infectable(grid, row + 1, col):
                grid[row + 1][col] = INFECTED
                frontier.append([row + 1, col])
            
            if col - 1 >= 0 and check_infectable(grid, row, col - 1):
                grid[row][col - 1] = INFECTED
                frontier.append([row, col - 1])
            
            if col + 1 < nCols and check_infectable(grid, row, col + 1):
                grid[row][col + 1] = INFECTED
                frontier.append([row, col + 1])
            
            if row - 1 >= 0 and col - 1 >= 0 and check_infectable(grid, row - 1, col - 1):
                grid[row - 1][col - 1] = INFECTED
                frontier.append([row - 1, col - 1])
            
            if row - 1 >= 0 and col + 1 < nCols and check_infectable(grid, row - 1, col + 1):
                grid[row - 1][col + 1] = INFECTED
                frontier.append([row - 1 , col + 1])

            if row + 1 < nRows and col - 1 >= 0 and check_infectable(grid, row + 1, col - 1):
                grid[row + 1][col - 1] = INFECTED
                frontier.append([row + 1, col - 1])
            
            if row + 1 < nRows and col + 1 < nCols and check_infectable(grid, row + 1, col + 1):
                grid[row + 1][col + 1] = INFECTED
                frontier.append([row + 1, col + 1])
        
        if frontier:
            infected_q = frontier
            round += 1
            
        else:
            break
        
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == HEALTHY:
                round = -1
                break
    
    return round

        
    # for row in range(nRows):
    #     for col in range(nCols):
    #         if grid[row][col] == HEALTHY:
    #             round = -1
    #             break
    
    return energy


[
  {
    "room": 1,
    "grid": [
      [0, 3],
      [0, 1]
    ],
    "interestedIndividuals": [
      "0,0"
    ]
  },
  {
    "room": 2,
    "grid": [
      [0, 3, 2],
      [0, 1, 1],
      [1, 0, 0]
    ],
    "interestedIndividuals": [
      "0,2", "2,0", "1,2"
    ]
  }
]

[
  {
    "room": 1,
    "p1": { "0,0": -1},
    "p2": 1,
    "p3": 1,
    "p4": 0
  },
  {
    "room": 2,
    "p1": { "0,2":  -1, "2,0":  -1, "1,2":  2},
    "p2": -1,
    "p3": 2,
    "p4": 1
  }
]