
import logging

log = logging.getLogger()

class JenkinsMonitor:

  def __init__(self, jobs, lights_controller):

    self.jobs = dict.fromkeys(jobs)
    self.lights_controller = lights_controller

    self.status_dict = {
      'aborted'         : 'UNKNOWN',
      'aborted_anime'   : 'BUILDING_FROM_UNKNOWN',
      'blue'            : 'SUCCESS',
      'blue_anime'      : 'BUILDING_FROM_SUCCESS',
      'disabled'        : 'UNKNOWN',
      'disabled_anime'  : 'BUILDING_FROM_UNKNOWN',
      'grey'            : 'UNKNOWN',
      'grey_anime'      : 'BUILDING_FROM_UNKNOWN',
      'notbuilt'        : 'UNKNOWN',
      'notbuilt_anime'  : 'BUILDING_FROM_UNKNOWN',
      'red'             : 'FAILURE',
      'red_anime'       : 'BUILDING_FROM_FAILURE',
      'yellow'          : 'UNKNOWN',
      'yellow_anime'    : 'BUILDING_FROM_UNKNOWN'
    }

  def process_build(self, build):
    job_statuses = self.__parse_build(build)
    # TODO compare to previous build status and update if needed
    # differences = filter( self.filter_differences, job_statuses )
    # replace current builds with new builds
    self.jobs = job_statuses
    log.info("self.jobs: %s", self.jobs)
    # iterate through each job and update light controller...
    for build, status in self.jobs.iteritems():
      if (status == 'SUCCESS'):
        self.lights_controller.success(build)
      elif (status == 'FAILURE'):
        self.lights_controller.failure(build)
      elif (status == 'BUILDING_FROM_SUCCESS'):
        self.lights_controller.building_from_success(build)
      elif (status == 'BUILDING_FROM_FAILURE'):
        self.lights_controller.building_from_failure(build)
      elif (status == 'BUILDING_FROM_UNKNOWN'):
        self.lights_controller.building_from_unknown(build)
      else:
        self.lights_controller.unknown(build)

# private

  # def filter_differences(self, build_status):
  #   print 'filter_differences: ', build_status
  #   return True

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
