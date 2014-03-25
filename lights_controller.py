
import logging
import random

log = logging.getLogger()

class LightsController:

  def __init__(self, jobs, strand):
    self.jobs = dict.fromkeys(jobs)
    self.strand = strand

    jobLength = self.strand.leds / len(self.jobs)
    index = 0
    for build in self.jobs:
      self.jobs[build] = (index, index + jobLength)
      index+=jobLength

  def off(self):
    self.strand.off()

  def random(self):
    for build in self.jobs:
      rgb = self.randomRgb()
      self.strand.fill(rgb[0], rgb[1], rgb[2], self.start(build), self.end(build))

  def error(self):
    self.strand.fill(0, 0, 255)

  def success(self, build):
    self.strand.fill(0, 255, 0, start(build), end(build)) # green

  def failure(self, build):
    self.strand.fill(255, 0, 0, start(build), end(build)) # red

  def building_from_success(self, build):
    self.strand.pulsate(0, 255, 0, start(build), end(build)) # green

  def building_from_failure(self, build):
    self.strand.pulsate(255, 0, 0, start(build), end(build)) # red

  def building_from_unknown(self, build):
    self.strand.pulsate(255, 255, 0, start(build), end(build)) # yellow

  def unknown(self, build):
    self.strand.wheel()

  def start(self, build_name):
    return self.jobs[build_name][0]

  def end(self, build_name):
    return self.jobs[build_name][1]

  def randomRgb(self):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

