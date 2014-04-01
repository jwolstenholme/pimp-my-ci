from lib.const import *

class JenkinsMonitor:

  def __init__(self, job_queues):
    self.job_queues = job_queues

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
    for build, status in job_statuses.iteritems():
      self.job_queues[build].put(status)

  # return true for only the jobs we're interested in
  def __filter_build(self, build):
    return build['name'] in self.job_queues.keys()

  # map jenkins job entries to our jobs
  def __jenkins_to_rpi(self, job):
    return { job['name'] : self.status_dict.get(job['color'], UNKNOWN) }

  # returns dictionary of build_name to current status
  def __parse_build(self, build):
    jobs = filter( self.__filter_build, build['jobs'] )
    updated_statuses = map( self.__jenkins_to_rpi, jobs )
    return dict(map(dict.popitem, updated_statuses))
