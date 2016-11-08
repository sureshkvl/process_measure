import sys
import psutil
import argparse
from threading import Timer
from time import sleep
import time

# second commit
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def measure(pids, ):
    if not pids:
        return
    Result = []
    for pid in pids:
        res = [pid]
        try:
            p = psutil.Process(int(pid))
            localtime = time.asctime(time.localtime(time.time()))
            res.append(localtime)
            res.append(p.memory_percent())
            res.append(p.cpu_percent(interval=1.0))
        except:
            print "ERROR: while reading the process,memory", pid
        finally:
            Result.append(res)
    print Result


def main(argv):
    parser = argparse.ArgumentParser("Program for measuring the memory,cpu")
    parser.add_argument("-p", "--pid", required=True,
                        help="Input PID Number", action="append")
    args = parser.parse_args(argv[1:])
    rt = RepeatedTimer(60, measure, args.pid)
    try:
        sleep(24*60*60)
    finally:
        rt.stop()

if __name__ == '__main__':
    main(sys.argv)
