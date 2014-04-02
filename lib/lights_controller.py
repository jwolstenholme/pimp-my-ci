
import logging
import random
import Queue
import threading

from lib.const import *
from threading import Thread
from time import sleep

log = logging.getLogger()
semaphore = threading.BoundedSemaphore()

def worker(controller, job, queue):
  status = UNKNOWN
  while True:
    try:
      status = queue.get_nowait()
      controller.update_build_status(job, status)
      queue.task_done()
    except Queue.Empty:
      controller.update_build_status(job, status)
    sleep(1.0)

class LightsController:

  def __init__(self, job_queues, strand):
    self.job_leds = dict.fromkeys(job_queues.keys())
    self.job_queues = job_queues
    self.jobs = job_queues.keys()
    self.strand = strand

    jobLength = self.strand.leds / len(self.job_leds)
    index = 0
    for build in self.job_leds:
      self.job_leds[build] = [index, index + jobLength-1]
      index+=jobLength

    # print 'created led segments: ', self.job_leds

    for job, queue in job_queues.iteritems():
      t = Thread(target=worker, args=(self, job, queue, ))
      t.daemon = True
      t.start()

  def update_build_status(self, build, status):
    semaphore.acquire()
    start = self.__start(build)
    end = self.__end(build)
    # print 'update_build_status: ', build, status, start, end
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
      self.__unknown(build, start, end)
    semaphore.release()

  def off(self):
    self.strand.off()

  def random(self):
    for build in self.jobs:
      rgb = self.__randomRgb()
      self.strand.fill(rgb[0], rgb[1], rgb[2], self.__start(build), self.__end(build))

  def error(self):
    self.__fill_strand(BLUE, 0, 0)

  def __success(self, start, end):
    self.__fill_strand(GREEN, start, end)

  def __failure(self, start, end):
    self.__fill_strand(RED, start, end)

  def __building_from_success(self, build, start, end):
    self.__pulsate(GREEN, start, end)

  def __building_from_failure(self, build, start, end):
    self.__pulsate(RED, start, end)

  def __building_from_unknown(self, build, start, end):
    self.__pulsate(YELLOW, start, end)

  def __unknown(self, build, start, end):
    self.__fill_strand(YELLOW, start, end)

  def __fill_strand(self, color, start, end):
    # print '__fill_strand: ', color, start, end
    self.strand.fill(color[0], color[1], color[2], start, end)

  def __start(self, build_name):
    return self.job_leds[build_name][0]

  def __end(self, build_name):
    return self.job_leds[build_name][1]

  def __randomRgb(self):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

  def __pulsate(self, color, start=0, end=0):
    for x in range(0, 40):
      b = 1 - x*.02
      self.strand.fill(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)
    for x in range(40, 0, -1):
      b = 1 - x*.02
      self.strand.fill(color[0] * b, color[1] * b, color[2] * b, start, end)
      sleep(0.02)
