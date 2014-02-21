
import logging

from lib.ledstrip import Strand

log = logging.getLogger()

class LightsController:

  # TODO partition the led stip by the builds we're interested in....

  def __init__(self, jobs):
    self.jobs = jobs
    self.strand = Strand()

  def success(self, build_name):
    log.debug('success ', build_name)
    self.strand.fill(0, 255, 0) # green

  def failure(self, build_name):
    log.debug('failure ', build_name)
    self.strand.fill(255, 0, 0) # red

  def building_from_success(self, build_name):
    log.debug('building_from_success ', build_name)
    self.strand.pulsate(0, 255, 0) # green

  def building_from_failure(self, build_name):
    log.debug('building_from_failure ', build_name)
    self.strand.pulsate(255, 0, 0) # red

  def unknown(self, build_name):
    log.debug('unknown ', build_name)
    self.strand.wheel()


