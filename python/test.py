from collections import Counter

arr = ["a", "b", "a", "c", "a", "b"]

print(Counter(arr))

print(arr.pop(1))
print(arr)

nums = [1, 2, 3, 4, 5]

import heapq

heap = []

heapq.heappush(heap,3)
heapq.heappush(heap,1)
heapq.heappush(heap,4)
heapq.heappush(heap,2)

print(heapq.heappop(heap))
print(heap)
print(heapq.nlargest(2, heap))

import math

def lcm(a, b,):
    return abs( a * b) // math.gcd(a, b)

print("LCM",lcm(3, 4))

import re

text = "User 123 failed at 10:30"
numbers = [int(i) for i in re.findall(r'\d+', text)]
print(numbers)

def test():
    assert lcm(3,4) == 12

test()

import sys

def solve(lines):
    a, b = map(int, lines)
    return a, b #lcm(a, b)

def main():
    lines = sys.stdin.read().strip().split()
    #inp = input()
    solution = solve(lines)
    print(solution)

def parse_args():
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument("--name", type=str, default="world")
    return args.parse_args()

if __name__ == "__main__":
    main()