#!/usr/bin/env python3

import random
import sys
import math

from common import print_tour, read_input

def distance(city1, city2): #　2つの都市間の距離を計算する関数
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 貪欲法
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

    return tour,dist

# 2opt法もどき
def opt_2(tour,dist):
    N = len(tour)  #　N=都市の数
    count = 0

    while count < 100: # 100回繰り返す

        for i in range(1,N-4): # 0,N番目はstartなので変えない

                before = dist[tour[i]][tour[i+1]] + dist[tour[i+2]][tour[i+3]]
                after = dist[tour[i]][tour[i+3]] + dist[tour[i+1]][tour[i+3]]

                if before > after: # 変更後の距離が変更前より短かったら組み替える

                    x = tour[i+1] 
                    tour[i+1] = tour[i+2]
                    tour[i+2] = x

        count += 1

    tour.append(0)
    return tour

# 焼きなまし法
def yaki(tour,dist):
    d = calc(tour,dist)
    T = 100
    while T > 0.0001: 
        prev_tour = tour.copy()

        # ランダムに点を選ぶ
        i = random.randrange(1,len(tour)-1)
        j = random.randrange(1,len(tour)-1)

        if tour[i] == 0 or tour[j] == 0:
            continue
        else:  # 選んだ点と隣の点を交換する
            x = tour[i]
            tour[i] = tour[j]
            tour[j] = x
            new = calc(tour,dist)

        # 新しいルートが古いルートよりよかったら新しいルートにする
        if new < d:
            d = new
    
        # 新しいルートが古いルートより悪かったら、20%の確率で新しいルートにし、80%の確率でそのまま
        else:
            y = random.randrange(1,11)
            if y > 2:
                continue
            else:
                d = new
                tour[:] = prev_tour

        T *= 0.995 
    
    return tour
    

def calc(tour,dist): # tourを受け取り、全距離を求める
    all_distance = 0
    for i in range(len(tour)-1):
        all_distance += dist[tour[i]][tour[i+1]]
    return all_distance

def solve(cities):
    t,dist = greedy(cities)
    tour =  opt_2(t,dist)
    return yaki(tour,dist)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    print_tour(solve(read_input(sys.argv[1])))