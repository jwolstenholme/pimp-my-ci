
from time import sleep
import logging
import sys
import threading
import urllib2
import yaml

from lib.config import Config

log = logging.getLogger()

class TravisPoller(threading.Thread):

  def __init__(self, build_jobs, build_monitor):
    threading.Thread.__init__(self)
    self.daemon = True
    self.build_monitor = build_monitor
    self.jobs = build_jobs

  def run(self):
    poll = True
    while poll:
      sleep(Config.polling_interval_secs)

      for job in self.jobs:
        try:
          req = urllib2.Request(job.url, headers={"Accept" : "application/vnd.travis-ci.2+json"})
          response_body = urllib2.urlopen(req).read()
          self.build_monitor.process_build_for_job( yaml.load(response_body), job )
        except:
          self.build_monitor.error()
          log.error( "TravisPoller error: %s", sys.exc_info()[0] )
