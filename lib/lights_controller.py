
import logging
import random
import Queue

from lib.const import *
from threading import Thread
from time import sleep

log = logging.getLogger()

def worker(controller, job, queue):
    while True:
      item = queue.get()
      print 'got item: ', job, item
      controller.update_build_status(job, item)
      queue.task_done()

class LightsController:

  def __init__(self, job_queues, strand):
    self.job_leds = dict.fromkeys(job_queues.keys())
    self.job_queues = job_queues
    self.jobs = job_queues.keys()
    self.strand = strand

    jobLength = self.strand.leds / len(self.job_leds)
    index = 0
    for build in self.job_leds:
      self.job_leds[build] = [index, index + jobLength -1]
      index+=jobLength

    print 'created led segments: ', self.job_leds

    for job, queue in job_queues.iteritems():
      t = Thread(target=worker, args=(self, job, queue, ))
      t.daemon = True
      t.start()

  def update_build_status(self, build, status):
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

  def __success(self, start, end):
    self.strand.fill(0, 255, 0, start, end) # green

  def __failure(self, start, end):
    self.strand.fill(255, 0, 0, start, end) # red

  def __building_from_success(self, build, start, end):
    self.__pulsate(0, 255, 0, start, end) # green

  def __building_from_failure(self, build, start, end):
    self.__pulsate(255, 0, 0, start, end) # red

  def __building_from_unknown(self, build, start, end):
    self.__pulsate(255, 255, 0, start, end) # yellow

  def __unknown(self, build):
    self.strand.fill(255, 255, 0) # red

  def __start(self, build_name):
    return self.job_leds[build_name][0]

  def __end(self, build_name):
    return self.job_leds[build_name][1]

  def __randomRgb(self):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

  def __pulsate(self, r, g, b, start, end):
    for x in range(0, 40):
      brightness = 1 - x*.02
      self.strand.fill(r * brightness, g * brightness, b * brightness, start, end)
      sleep(0.02)
    for x in range(40, 0, -1):
      brightness = 1 - x*.02
      self.strand.fill(r * brightness, g * brightness, b * brightness, start, end)
      sleep(0.02)
