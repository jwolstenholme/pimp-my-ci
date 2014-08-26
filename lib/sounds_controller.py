
from lib.const import *
from sounds.player import Player

class SoundsController:

  def __init__(self, job_names):
    self.sound_player = Player()
    self.play_sounds = dict.fromkeys(job_names, False)

  def update_build_status(self, job, status):
    if (not self.play_sounds[job.name]):
      self.play_sounds[job.name] = True
      return

    if (status == SUCCESS and job.success != None):
      if (job.success == '__RANDOM'):
        self.sound_player.play_random_success_sound()
      else:
        self.sound_player.play_success(job.success)

    elif (status == FAILURE and job.failure != None):
      if (job.failure == '__RANDOM'):
        self.sound_player.play_random_failure_sound()
      else:
        self.sound_player.play_failure(job.failure)
