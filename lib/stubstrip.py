
import logging
import sys
from ledstrip import Strand
from xtermcolor import colorize

log = logging.getLogger()

_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def triplet_int(rgb, lettercase=LOWERCASE):
  return int(format((rgb[0]<<16 | rgb[1]<<8 | rgb[2]), '06'+lettercase), 16)

class CliStrand(Strand):

  def __init__(self):
    Strand.__init__(self, 32, '/dev/null')

  def update(self):
    for x in range(self.leds):
      g = self.buffer[x][0]
      r = self.buffer[x][1]
      b = self.buffer[x][2]

      rgb = triplet_int([r, g, b])
      sys.stdout.write(colorize( ' * ', rgb=rgb))
      sys.stdout.flush()

    sys.stdout.write("\b" * (self.leds * 3)) # return to start of line
