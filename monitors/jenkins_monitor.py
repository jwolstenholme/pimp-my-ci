
import logging

from lib.const import *

log = logging.getLogger()

class JenkinsMonitor:

  def __init__(self, jobs, lights_controller):

    self.jobs = dict.fromkeys(jobs)
    self.lights_controller = lights_controller

    self.status_dict = {
      'aborted_anime'   : BUILDING_FROM_UNKNOWN,
      'blue'            : SUCCESS,
      'blue_anime'      : BUILDING_FROM_SUCCESS,
      'disabled_anime'  : BUILDING_FROM_UNKNOWN,
      'grey_anime'      : BUILDING_FROM_UNKNOWN,
      'notbuilt_anime'  : BUILDING_FROM_UNKNOWN,
      'red'             : FAILURE,
      'red_anime'       : BUILDING_FROM_FAILURE,
      'yellow_anime'    : BUILDING_FROM_UNKNOWN
    }

  def process_build(self, build):
    job_statuses = self.__parse_build(build)
    differences = self.__filter_differences(self.jobs, job_statuses)
    # print "differences: %s", differences
    for build, status in differences.iteritems():
      self.lights_controller.update_build_status(build, status)

    # replace current builds with new builds
    self.jobs = job_statuses

# private

  def __filter_differences(self, old_builds, new_builds):
    return dict(new_builds.viewitems() - old_builds.viewitems())

  # return true for only the jobs we're interested in
  def __filter_build(self, build):
    return build['name'] in self.jobs

  # map jenkins job entries to our jobs
  def __jenkins_to_rpi(self, job):
    return { job['name'] : self.status_dict[job['color']] }

  # returns dictionary of build_name to current status
  def __parse_build(self, build):
    jobs = filter( self.__filter_build, build['jobs'] )
    updated_statuses = map( self.__jenkins_to_rpi, jobs )
    return dict(map(dict.popitem, updated_statuses))
