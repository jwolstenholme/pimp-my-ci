
from lib.const import *

status_dict = {
  'passed'     : SUCCESS,
  'failed'     : FAILURE
}

class TravisMonitor:

  def __init__(self, job_queues):
    self.job_queues = job_queues
    self.job_statuses = dict.fromkeys(self.job_queues.keys())

  def process_build_for_job(self, build, job):
    raw_status = build['repo']['last_build_state']
    current_status = status_dict.get(raw_status, UNKNOWN)
    if (self.job_statuses[job.name] != current_status):
      self.job_queues[job.name].put_nowait(current_status)

    self.job_statuses[job.name] = current_status

  def error(self):
    print "ERROR in TravisMonitor"
