
class TravisMonitor:

  def __init__(self, job_queues):
    self.job_queues = job_queues
    self.job_statuses = dict.fromkeys(self.job_queues.keys())

  def process_build(self, build):
    print "not processing travis build yet..."

  def error(self):
    print "ERROR in TravisMonitor"
    #self.queue.put_nowait(UNKNOWN)
