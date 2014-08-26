
from lib.build_job import BuildJob
from lib.config import Config

import urllib2
import yaml

class Check:

  def __init__(self):
    self.printGlobal()
    self.printJobs()
    self.printLedLayout()
    self.printTestResponse()


  def printGlobal(self):
    print "\n==== Global ===="
    print "  CI server url    : ", Config.ci_url
    print "  Polling interval : ", Config.polling_interval_secs, "seconds"

  def printJobs(self):
    print "\n==== Builds ===="
    index = 0
    self.job_leds = dict()

    build_jobs = BuildJob.from_dictionaries(Config.jobs)

    for job in build_jobs:
      print " ", job.name.ljust(16), "leds:", str(job.led_coordinates(index)).ljust(10), "success:", str(job.success).ljust(20), "failure:", job.failure
      for i in job.led_addresses(index):
        self.job_leds[i] = job.name
      index = job.next_index(index)

  def printLedLayout(self):
    print "\n==== LEDs ===="
    for i in range(Config.total_number_leds):
      print "  [", str(i).rjust(2), "]", self.job_leds.get(i, "  *")

  def printTestResponse(self):
    print "\n==== Test ===="
    try:
      req = urllib2.Request(Config.ci_url)
      req.add_header('Content-Type', 'application/json')
      response_body = urllib2.urlopen(req).read()
      print yaml.load(response_body)
    except:
      print "Error:", sys.exc_info()[0]


if __name__ == '__main__':
  Check()
