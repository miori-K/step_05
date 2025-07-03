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

# 2opt法
def opt_2(tour,dist):
    N = len(tour)  #　N=都市の数
    count = 0

    while count < 5000: # 5000回繰り返す

        for i in range(1,N-4): # 0番目は0なので変えない
            for j in range(i+2,N-1): # N番目は0なので変えない

                before = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]
                after = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]

                if before > after: # 変更後の距離が変更前より短かったら組み替える

                    x = tour[i+1] 
                    tour[i+1] = tour[j]
                    tour[j] = x

        count += 1

    tour.append(0)
    return tour

# 焼きなまし法
def yaki(tour,dist):
    count = 0
    while count < 100000: #100000回繰り返す
        d = calc(tour,dist)

        # ランダムに2点を選ぶ
        i = random.randrange(1,len(tour)-1)
        j = random.randrange(1,len(tour)-1)

        # 選んだ点が同じだったらやり直し
        if i == j:
            continue

        # 選んだ点を交換する
        else: 
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

        count += 1
    print(d)
    
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