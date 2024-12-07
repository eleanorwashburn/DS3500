"""
profiler.py
a profiler class that demonstrates the use of decorators for code profiling
"""
from collections import defaultdict
import time

# Good for determining if a certain function is a bottleneck
def profile(f):
    return Profiler.profile(f)

class Profiler:
    calls = defaultdict(int) # function name --> int (# of calls / invocations)
    time = defaultdict(float) # function name --> float (total runtime for each function)

    @staticmethod
    def profile(f):
        """ Profiling decorator"""
        def wrapper(*args, **kwargs):
            function_name = str(f).split()[1]
            start = time.time_ns()
            rslt = f(*args, **kwargs)
            end = time.time_ns()
            elapsed = end - start / 10**9
            Profiler.calls[function_name] += 1
            Profiler.time[function_name] += elapsed
            return rslt
        return wrapper
