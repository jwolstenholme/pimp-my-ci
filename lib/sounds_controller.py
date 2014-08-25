
import Queue

from lib.const import *
from sounds.player import Player
from threading import Thread
from time import sleep

def worker(controller, job, queue):
  while True:
    try:
      status = queue.get_nowait()
      status.update_build_status(job, status)
      queue.task_done()
    except Queue.Empty:
      sleep(1)

class SoundsController:

  def __init__(self, job_queues):
    self.sound_player = Player()
    for job, queue in job_queues.iteritems():
      t = Thread(target=worker, args=(self, job, queue, ))
      t.daemon = True
      t.start()

  def update_build_status(self, build, status):
    elif (status == SUCCESS):
      self.sound_player.play_random_success_sound()
    elif (status == FAILURE):
      self.sound_player.play_random_failure_sound()

