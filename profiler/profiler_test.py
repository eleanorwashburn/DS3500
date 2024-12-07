from profiler import Profiler, profile
import time

@profile
def mult(x,y):
    time.sleep(0.01)
    return x * y


def main():
   result = mult(2342,23422)
   rslt2 = mult(23423, 564)
   print(Profiler.calls)
   print(Profiler.time)

if __name__ == '__main__':
    main()