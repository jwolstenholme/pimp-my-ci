
import logging
import random
import threading
from time import sleep

from lib.const import *

log = logging.getLogger()

job_statuses = dict()

def animation_worker(led_strip, job, status, color, start, end):
  while job_statuses[job] == status:
    for x in range(0, 40):
      b = 1 - x*.02
      led_strip.fillRGB(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)
    for x in range(40, 0, -1):
      b = 1 - x*.02
      led_strip.fillRGB(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)

class LightsController:

  def __init__(self, led_strip, build_jobs):
    self.job_leds = dict()
    self.jobs = list()
    self.led_strip = led_strip

    index = 0
    for job in build_jobs:
        self.jobs.append(job.name)
        self.job_leds[job.name] = job.led_coordinates(index)
        index = job.next_index(index)

  def update_build_status(self, job, status):
    start = self.__start(job.name)
    end = self.__end(job.name)
    job_statuses[job] = status
    # print 'update_build_status: ', job, status, start, end
    if (status == OFF):
      self.__off(start, end)
    elif (status == SUCCESS):
      self.__success(start, end)
    elif (status == FAILURE):
      self.__failure(start, end)
    elif (status == BUILDING_FROM_SUCCESS):
      self.__building_from_success(job, start, end)
    elif (status == BUILDING_FROM_FAILURE):
      self.__building_from_failure(job, start, end)
    elif (status == BUILDING_FROM_UNKNOWN):
      self.__building_from_unknown(job, start, end)
    else:
      self.__unknown(job, start, end)

  def off(self):
    self.led_strip.fillOff()

  def random(self):
    for job in self.jobs:
      rgb = self.__randomRgb()
      self.led_strip.fillRGB(rgb[0], rgb[1], rgb[2], self.__start(job), self.__end(job))

  def error(self):
    self.__fill_strand(BLUE, 0, 0)

  def __off(self, start, end):
    self.__fill_strand(NONE, start, end)

  def __success(self, start, end):
    self.__fill_strand(GREEN, start, end)

  def __failure(self, start, end):
    self.__fill_strand(RED, start, end)

  def __building_from_success(self, job, start, end):
    self.__building(job, BUILDING_FROM_SUCCESS, GREEN, start, end)

  def __building_from_failure(self, job, start, end):
    self.__building(job, BUILDING_FROM_FAILURE, RED, start, end)

  def __building_from_unknown(self, job, start, end):
    self.__building(job, BUILDING_FROM_UNKNOWN, YELLOW, start, end)

  def __unknown(self, job, start, end):
    self.__fill_strand(YELLOW, start, end)

  def __fill_strand(self, color, start, end):
    semaphore = threading.BoundedSemaphore()
    semaphore.acquire()
    self.led_strip.fillRGB(color[0], color[1], color[2], start, end)
    semaphore.release()

  def __start(self, build_name):
    return self.job_leds[build_name][0]

  def __end(self, build_name):
    return self.job_leds[build_name][1]

  def __randomRgb(self):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

  def __building(self, job, status, color, start, end):
    t = threading.Thread(target=animation_worker, args=(self.led_strip, job, status, color, start, end))
    t.daemon = True
    t.start()


