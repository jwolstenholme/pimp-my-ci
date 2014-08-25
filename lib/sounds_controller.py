
from lib.const import *
from sounds.player import Player

class SoundsController:

  def __init__(self, job_queues):
    self.sound_player = Player()

  def update_build_status(self, build, status):
    if (status == SUCCESS):
      self.sound_player.play_random_success_sound()
    elif (status == FAILURE):
      self.sound_player.play_random_failure_sound()

