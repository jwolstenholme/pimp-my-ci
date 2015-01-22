
from lib.const import *

status_dict = {
  'fixed'                   : SUCCESS,
  'success'                 : SUCCESS,
  'failed'                  : FAILURE,
  'building_from_success'   : BUILDING_FROM_SUCCESS,
  'building_from_failed'    : BUILDING_FROM_FAILURE,
  'building_from_unknown'   : BUILDING_FROM_UNKNOWN,
}

class CircleciMonitor:

  def __init__(self, job_queues):
    self.job_queues = job_queues
    self.job_statuses = dict.fromkeys(self.job_queues.keys())

  def process_build_for_job(self, build, job):
    current_status = self.get_status(build)

    if (self.job_statuses[job.name] != current_status):
      self.job_queues[job.name].put_nowait(current_status)

    self.job_statuses[job.name] = current_status

  def get_status(self, build):
    raw_status = build[0]['status']
    if (raw_status == 'running'):
      previous_status = build[0]['previous']['status']
      return status_dict.get('building_from_' + previous_status, BUILDING_FROM_UNKNOWN)
    else:
      return status_dict.get(raw_status, UNKNOWN)

  def error(self):
    print "ERROR in CircleciMonitor"
