from functools import lru_cache

@lru_cache(maxsize=16)
def fib(n):
    return n if n<2 else fib(n-1)+fib(n-2)

if __name__ == "__main__":
    print("fib(10)=", fib(10))
