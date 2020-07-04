from typing import Dict
from functools import lru_cache


def fib1(num: int) -> int:
    if num < 2:
        return num

    return fib1(num - 2) + fib1(num - 1)


# cache implementação propria
cache: Dict[int, int] = {0: 0, 1: 1}

def fib2(num: int) -> int:
    if num not in cache:
        cache[num] = fib2(num - 1) + fib2(num - 2)
    
    return cache[num]


# cache do propria da linguagem
@lru_cache(maxsize=None)
def fib3(num: int) -> int:
	if num < 2:
		return num

	return cache[num]


def fib4(num: int) -> int:
	last_num: int = 0
	next_num: int = 1

	for _ in range(1, num):
		last_num, next_num = next_num, last_num + next_num

	return next_num


def fib5(num: int) -> int:
	yield 0
	if (num > 0): yield 1

	last_num: int = 0
	next_num: int = 1

	for _ in range(1, num):
		last_num, next_num = next_num, last_num + next_num
		yield next_num


if __name__ == "__main__":
	fib_num = 12
	print(fib1(fib_num))
	print(fib2(fib_num))
	print(fib3(fib_num))
	print(fib4(fib_num))
	print([n for n in fib5(fib_num)][-1])
