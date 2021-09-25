import logging
import json
from math import gcd

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
MAX_RATING = 10**9


def contains(qn, data):
    start = qn[0]
    end = qn[1]
    return start<= data[0][0] and end >= data[-1][1]

def partition(qn, data):
    a = data
    b = []
    q_start = qn[0]
    q_end = qn[1]
    
    if q_start > data[0][0] and q_end >= data[-1][1]:
        for i in range(len(data)):
            interval = data[i]
            i_s, i_e = interval[0], interval[1]
            if i_s >= q_start:
                a = data[:i]
                b = data[i:]
                break

            if i_e >= q_start:
                a = data[:i]
                a.append([i_s, q_start-1])
                b = [[q_start, i_e]]
                b = b + data[i+1:]
                break

        return a, b
    
    if q_start <= data[0][0] and q_end < data[-1][1]:
        for i in range(len(data)):
            interval = data[i]
            i_s, i_e = interval[0], interval[1]
            
            if i_s > q_end:
                a = data[i:]
                b = data[:i]
                break

            if i_e > q_end:
                a = [[q_end+1, i_e]] + data[i + 1:]
                b =  data[:i] + [[i_s, q_end]]
                break
            
        return a, b
    
    if q_start > data[0][0] and q_end < data[-1][1]:
        for i in range(len(data)):
            interval = data[i]
            i_s, i_e = interval[0], interval[1]
            if i_s >= q_start:
                a = data[:i]
                b = data[i:]
                break

            if i_e >= q_start:
                a = data[:i]
                a.append([i_s, q_start-1])
                b = [[q_start, i_e]]
                b = b + data[i+1:]
                break

        aa, bb = partition(qn, b)

        a = a + aa
        b = bb
        return a, b
    
    return -1

def reduceFraction(x, y) :
     
    d = gcd(x, y);
 
    x = x // d;
    y = y // d;
 
    return x, y

def compare_and_update(data, qn):
    if contains(qn, data):
        return None
    return partition(qn, data)

@app.route('/stig/perry', methods=['POST'])
def evaluate_stig():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for subtask in data:
        qns = subtask["questions"]
        database = []
        database.append([[1, MAX_RATING]])
        print(qns[0])
        for qn_str in qns[0]:
            new_data = []
            for i in range(len(database)):
                data = database[i]
                qn = [qn_str["from"], qn_str["to"]]
                if compare_and_update(data, qn):
                    print("meaningful split")
                    print(data)
                    print(qn)
                    a,b = compare_and_update(data, qn)
                    print("a ", a)
                    print("b ", b)
                else:
                    continue
                
                database[i] = a
                database.append(b)
                print(database)
        database = list(filter(lambda a: a != [], database))
        length = len(database)
        p,q = reduceFraction(length, MAX_RATING)
        print(len(database))
        dic = {}
        dic["p"]= p
        dic["q"]= q
        ans.append(dic)
                

    logging.info("My result :{}".format(database))
    return jsonify(ans)
    # return json.dumps(ans)



