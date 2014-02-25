from xtermcolor import colorize
import time
import sys

toolbar_width = 32

# setup toolbar
sys.stdout.write("[%s]" % (" - " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width * 3 + 1)) # return to start of line, after '['

for i in xrange(toolbar_width):
    time.sleep(0.05) # do real work here
    # update the bar
    sys.stdout.write(colorize( ' * ', ansi=i))
    sys.stdout.flush()

sys.stdout.write("\n")
