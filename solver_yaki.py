#!/usr/bin/env python3

import random
import sys
import math

from common import print_tour, read_input


def distance(city1, city2): #　2つの都市間の距離を計算する関数
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def search_dist(city1,city2,dist):
    return dist[city1][city2]

def greedy(cities): 
    N = len(cities) #　N=都市の数

    dist = [[0] * N for i in range(N)] #　全ての都市間の初期値をゼロに設定
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    # dist = [[AAの距離、ABの距離、ACの距離],[BAの距離、BBの距離、BCの距離],[CAの距離、CBの距離、CCの距離]]のようになる

    current_city = 0
    unvisited_cities = set(range(1, N)) #　すべての都市をunvisitedにする
    tour = [current_city] #　訪れた順番に記録

    while unvisited_cities: #　すべての都市に訪れるまで
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    tour.append(tour[0])

    return tour,dist

def yaki(tour,dist):
    pair_list = make_pair(tour)
    #T = calc(pair_list,dist)
        
    t_list = {}
    for k in range(100):
        temp = calc(pair_list,dist)
        i = random.randrange(1,len(tour)-2)
        j = random.randrange(1,len(tour)-2)
        x = tour[i]
        tour[i] = tour[j]
        tour[j] = x
        pair_list = make_pair(tour)
        t_list[k] = {'tour': tour, 'T': calc(pair_list,dist)}
        print(t_list)
    
    best = min(t_list, key=lambda k: t_list[k]['T'])
    best_tour = t_list[best]['tour']
    best_pair_list = make_pair(best_tour)

    answer = []
    for k in range(len(best_pair_list)):
        answer.append(best_pair_list[k][0])
    answer.append(answer[0])  

    return answer

def calc(pair_list,dist): # ペアリストを受け取り、全部の距離を求める
    all_distance = 0
    for i in range(len(pair_list)):
        all_distance += search_dist(pair_list[i][0],pair_list[i][1],dist)
    return all_distance

def make_pair(tour): # 2つずつ取り出したリストを作る
    pair_list = []
    for i in range(len(tour) - 1): 
        pair_list.append([tour[i], tour[i + 1]])
    return pair_list

def solve(cities):
    tour,dist = greedy(cities)
    return yaki(tour,dist)

if __name__ == '__main__':
    assert len(sys.argv) > 1
    print_tour(solve(read_input(sys.argv[1])))
