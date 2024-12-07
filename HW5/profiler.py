"""
profiler.py
A profiler class that demonstrates the use of decorators to support code profiling
DS3500: Advanced Programming with Data (Prof. Rachlin)
"""
from collections import defaultdict
import time



def profile(f):
    """ Convenience function to make decorator tags simpler:
        e.g. @profile instead of @Profiler.profile """
    return Profiler.profile(f)


class Profiler:
    """ A code profiling class.  Keeps track of function calls and running time. """
    calls = defaultdict(int)  # default = 0
    time = defaultdict(float)  # default = 0.0

    @staticmethod
    def _add(function_name, sec):
        """ Add 1 call and <sec> time to named function tracking """
        Profiler.calls[function_name] += 1
        Profiler.time[function_name] += sec

    @staticmethod
    def profile(f):
        """ The profiling decorator """

        def wrapper(*args, **kwargs):
            function_name = str(f).split()[1]
            start = time.time_ns()
            val = f(*args, **kwargs)
            sec = (time.time_ns() - start) / 10 ** 9
            Profiler._add(function_name, sec)
            return val

        return wrapper

    @staticmethod
    def report(filename=None):
        """Summarize # calls, total runtime, and time/call for each function.
           Optionally export the report to a file.
        """
        total_runtime = 0
        output = []
        output.append("Function              Calls     TotSec   Sec/Call")
        for name, num in Profiler.calls.items():
            sec = Profiler.time[name]
            total_runtime += sec  # Add each function's runtime to the total
            output.append(f'{name:20s} {num:6d} {sec:10.6f} {sec / num:10.6f}')

        # Add aggregate runtime to the report
        output.append("\nTotal Runtime: {:.6f} seconds".format(total_runtime))

        # Print the report to console
        report_text = "\n".join(output)
        print(report_text)

        # If filename is provided, write to file
        if filename:
            with open(filename, "w") as file:
                file.write(report_text)
            print(f"Profiler report has been saved to {filename}")