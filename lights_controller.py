
import logging
import random

from lib.const import *
from threading import Thread
from time import sleep

log = logging.getLogger()

class LightsController:

  def __init__(self, jobs, strand):
    self.jobs = dict.fromkeys(jobs)
    self.strand = strand

    jobLength = self.strand.leds / len(self.jobs)
    index = 0
    for build in self.jobs:
      self.jobs[build] = [index, index + jobLength, None]
      index+=jobLength

  def update_build_status(self, build, status):
    # update local dictionary of build status
    self.jobs[build][2] = status

    # perhaps stick this on a queue?

    # update lights
    start = self.__start(build)
    end = self.__end(build)
    if (status == SUCCESS):
      self.__success(start, end)
    elif (status == FAILURE):
      self.__failure(start, end)
    elif (status == BUILDING_FROM_SUCCESS):
      self.__building_from_success(build, start, end)
    elif (status == BUILDING_FROM_FAILURE):
      self.__building_from_failure(build, start, end)
    elif (status == BUILDING_FROM_UNKNOWN):
      self.__building_from_unknown(build, start, end)
    else:
      self.__unknown(build)

  def off(self):
    self.strand.off()

  def random(self):
    for build in self.jobs:
      rgb = self.__randomRgb()
      self.strand.fill(rgb[0], rgb[1], rgb[2], self.__start(build), self.__end(build))

  def error(self):
    self.strand.fill(0, 0, 255)

  def check_status(self, build, status):
    return self.jobs[build][2] == status

  def __success(self, start, end):
    # stick new status on queue, wait until empty
    #  Queue.put(SUCCESS)
    self.strand.fill(0, 255, 0, start, end) # green

  def __failure(self, start, end):
    self.strand.fill(255, 0, 0, start, end) # red

  def __building_from_success(self, build, start, end):
    self.__pulsate(build, BUILDING_FROM_SUCCESS, 0, 255, 0, start, end) # green

  def __building_from_failure(self, build, start, end):
    # self.__pulsate(self.strand, 255, 0, 0, start, end) # red
    self.__pulsate(build, BUILDING_FROM_SUCCESS, 0, 255, 0, start, end) # green

  def __building_from_unknown(self, build, start, end):
    # self.__pulsate(self.strand, 255, 255, 0, start, end) # yellow
    self.__pulsate(build, BUILDING_FROM_SUCCESS, 0, 255, 0, start, end) # green

  def __unknown(self, build):
    self.strand.wheel()

  def __start(self, build_name):
    return self.jobs[build_name][0]

  def __end(self, build_name):
    return self.jobs[build_name][1]

  def __randomRgb(self):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

  def __pulsate(self, build, status, r, g, b, start=0, end=0):
    worker = Thread(target=pulsate_strand, args=(self.strand, self.jobs[build][2], status, r, g, b, start, end, ))
    worker.setDaemon(True)
    worker.start()

def pulsate_strand(strand, build_reference, status, r, g, b, start, end):
  while build_reference == status:
    for x in range(0, 40):
      brightness = 1 - x*.02
      strand.fill(r * brightness, g * brightness, b * brightness, start, end)
      sleep(0.02)
    for x in range(40, 0, -1):
      brightness = 1 - x*.02
      strand.fill(r * brightness, g * brightness, b * brightness, start, end)
      sleep(0.02)
