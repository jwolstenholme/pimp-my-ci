
from lib.base_message_interface import BaseMessageInterface

class LightsController:

  # TODO partition the led stip by the builds we're interested in....

  def __init__(self, jobs):
    self.jobs = jobs
    self.base_message_interface = BaseMessageInterface()

  def success(self, build_name):
    print 'success ', build_name
    tokens = ['0', '1', '32', '1.0', 'green']
    self.base_message_interface.issue_update(tokens)

  def failure(self, build_name):
    print 'failure ', build_name
    #tokens? ['2', '5', '6', '1.0', 'green', 'white', 'red', 'blue', 'red']
    tokens = ['0', '1', '32', '1.0', 'red']
    self.base_message_interface.issue_update(tokens)

  def building_from_success(self, build_name):
    print 'building_from_success ', build_name
    self.base_message_interface.issue_start_build()

  def building_from_failure(self, build_name):
    print 'building_from_failure ', build_name
    self.base_message_interface.issue_start_build()

  def unknown(self, build_name):
    print 'unknown ', build_name
    # self.base_message_interface.issue_unknown()
