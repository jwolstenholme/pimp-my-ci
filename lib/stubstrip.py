
import logging
import sys
from ledstrip import Strand
from xtermcolor import colorize
from xtermcolor.ColorMap import XTermColorMap, VT100ColorMap

log = logging.getLogger()

class CliStrand(Strand):

  def __init__(self):
    Strand.__init__(self, 32, '/dev/null')
    self.colorMap = XTermColorMap()

  def update(self):
    for x in range(self.leds):
      g = self.buffer[x][0]
      r = self.buffer[x][1]
      b = self.buffer[x][2]

      rawRgb = format('0x%02X%02X%02X' % (r, g, b))
      rawRgb = int(rawRgb, 16)
      (ansi, rgb) = self.colorMap.convert(rawRgb)

      sys.stdout.write(colorize( ' * ', rgb=rgb))
      sys.stdout.flush()

    sys.stdout.write("\b" * (self.leds * 3)) # return to start of line
