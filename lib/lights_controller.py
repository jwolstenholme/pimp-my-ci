
import logging
import random
import Queue
import threading

from lib.const import *
from threading import Thread
from time import sleep

log = logging.getLogger()

def worker(controller, job, queue):
  status = OFF
  while True:
    try:
      status = queue.get_nowait()
      controller.update_build_status(job, status)
      queue.task_done()
    except Queue.Empty:
      if (status % 2 == 1): # check to see if we're an animation
        controller.update_build_status(job, status)
      else:
        sleep(1)

class LightsController:

  def __init__(self, led_strip, job_queues, build_jobs):
    self.job_leds = dict()
    self.jobs = list()
    self.led_strip = led_strip

    index = 0
    for job in build_jobs:
        self.jobs.append(job.name)
        self.job_leds[job.name] = job.led_coordinates(index)
        index = job.next_index(index)

    for job, queue in job_queues.iteritems():
      t = Thread(target=worker, args=(self, job, queue, ))
      t.daemon = True
      t.start()

  def update_build_status(self, build, status):
    start = self.__start(build)
    end = self.__end(build)
    # print 'update_build_status: ', build, status, start, end
    if (status == OFF):
      self.__off(start, end)
    elif (status == SUCCESS):
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
      self.__unknown(build, start, end)

  def off(self):
    self.led_strip.fillOff()

  def random(self):
    for build in self.jobs:
      rgb = self.__randomRgb()
      self.led_strip.fillRGB(rgb[0], rgb[1], rgb[2], self.__start(build), self.__end(build))

  def error(self):
    self.__fill_strand(BLUE, 0, 0)

  def __off(self, start, end):
    self.__fill_strand(NONE, start, end)

  def __success(self, start, end):
    self.__fill_strand(GREEN, start, end)

  def __failure(self, start, end):
    self.__fill_strand(RED, start, end)

  def __building_from_success(self, build, start, end):
    self.__building(GREEN, start, end)

  def __building_from_failure(self, build, start, end):
    self.__building(RED, start, end)

  def __building_from_unknown(self, build, start, end):
    self.__building(YELLOW, start, end)

  def __unknown(self, build, start, end):
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

  def __building(self, color, start=0, end=0):
    for x in range(0, 40):
      b = 1 - x*.02
      self.led_strip.fillRGB(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)
    for x in range(40, 0, -1):
      b = 1 - x*.02
      self.led_strip.fillRGB(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)


