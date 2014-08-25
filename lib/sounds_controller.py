
from lib.const import *
from sounds.player import Player

class SoundsController:

  def __init__(self, job_queues):
    self.sound_player = Player()
    self.play_sounds = dict.fromkeys(job_queues.keys(), False)

  def update_build_status(self, job, status):
    if (self.play_sounds[job]):
      if (status == SUCCESS):
        self.sound_player.play_random_success_sound()
      elif (status == FAILURE):
        self.sound_player.play_random_failure_sound()
    else:
      self.play_sounds[job] = True