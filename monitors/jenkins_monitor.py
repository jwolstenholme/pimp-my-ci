from lib.const import *

status_dict = {
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

class JenkinsMonitor:

  def __init__(self, job_queues):
    self.job_queues = job_queues
    self.job_statuses = dict.fromkeys(job_queues.keys())

  def process_build(self, build):
    job_statuses = self.__parse_build(build)
    differences = self.__filter_differences(self.job_statuses, job_statuses)

    for build, status in differences.iteritems():
      self.job_queues[build].put_nowait(status)

    self.job_statuses = job_statuses

  def __filter_differences(self, old_builds, new_builds):
    return dict(new_builds.viewitems() - old_builds.viewitems())

  # return true for only the jobs we're interested in
  def __filter_build(self, build):
    return build['name'] in self.job_queues.keys()

  # map jenkins job entries to our jobs
  def __jenkins_to_rpi(self, job):
    return { job['name'] : status_dict.get(job['color'], UNKNOWN) }

  # returns dictionary of build_name to current status
  def __parse_build(self, build):
    jobs = filter( self.__filter_build, build['jobs'] )
    updated_statuses = map( self.__jenkins_to_rpi, jobs )
    return dict(map(dict.popitem, updated_statuses))
