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
        
        a, b, part4 = part_1(grid, interestedIndividuals)
        room_ans["room"] = room_index
        room_ans["p1"] = a
        room_ans["p2"] = b
        room_ans["p3"] = part_3(grid, interestedIndividuals)
        room_ans["p4"] = part4
        ans.append(room_ans) 
    
    logging.info("My result :{}".format(ans))
    return jsonify(ans)


def check_infectable(grid, row, col):
    return grid[row][col] == HEALTHY

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
    part4_ans = 0
    
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == HEALTHY:
                round = -1
                part4_ans = part4(grid)
                break

    
    return infected_time, round, part4_ans

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]

    def find(self, u):
        if u != self.parent[u]:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        pu, pv = self.find(u), self.find(v)
        if pu == pv: return False
        self.parent[pu] = pv
        return True


def part4(grid):
    def manhattanDist(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) - 1 

    grid = [x[:] for x in grid]
    nRows = len(grid)
    nCols = len(grid[0])
    print(grid)
    edges = []
    n = 0
    dic = {}
    for row in range(nRows):
        for col in range(nCols):
            if grid[row][col] == VACANT or grid[row][col] == VACCINATED :
                continue
            if row*(nCols)+ col not in dic:
                dic[row*(nCols)+ col] = n
                n += 1

            infected_a =  (grid[row][col] == INFECTED)
            
            for i in range(nRows):
                for j in range(nCols):
                    if (row == i and col == j) or grid[i][j] == VACANT or grid[i][j] == VACCINATED :
                        continue
                    else:
                        if (i*(nCols)+j) not in dic:
                            dic[i*(nCols)+j] = n
                            n += 1
                        infected_b =  (grid[i][j] == INFECTED)
                        if infected_a and infected_b:
                            if dic[i*(nCols)+j] > dic[row*(nCols)+ col]:
                                edges.append([0, dic[row*(nCols)+ col], dic[i*(nCols)+j]])
                        else:
                            if dic[i*(nCols)+j] > dic[row*(nCols)+ col]:
                                edges.append(
                                    [manhattanDist([row, col], [i, j]), 
                                    dic[row*(nCols)+ col], 
                                    dic[i*(nCols)+j]])
    

    edges.sort()  # Sort increasing order by dist
    print("edges: ", edges)
    uf = UnionFind(n)
    ans = 0
    for d, u, v in edges:
        if uf.union(u, v):
            print(u,v)
            print(d)
            ans += d
            n -= 1
        if n == 1: 
            break  # a bit optimize when we found enough n-1 edges!
    print(ans)
    return ans  


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