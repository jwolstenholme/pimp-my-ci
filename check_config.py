
from lib.build_job import BuildJob
from lib.config import Config

import urllib2
import json

class Check:

  def __init__(self):
    self.build_jobs = BuildJob.from_dictionaries(Config.platform, Config.job_defaults, Config.jobs)
    self.printGlobal()
    self.printJobs()
    self.printLedLayout()
    self.printTestResponse()


  def printGlobal(self):
    print "\n==== Global ===="
    print "  Toal number of LEDs  : ", Config.total_number_leds
    print "  Polling interval     : ", Config.polling_interval_secs, "seconds"
    print "  Platform             : ", Config.platform

  def printJobs(self):
    print "\n==== Builds ===="
    index = 0
    self.job_leds = dict()

    print "got build_jobs: ", self.build_jobs
    for job in self.build_jobs:
      print " ", job.name
      print "\tleds:".ljust(14), str(job.led_coordinates(index))
      print "\turl:".ljust(14), job.url
      print "\tsuccess:".ljust(14), str(job.success)
      print "\tfailure:".ljust(14), job.failure
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
      for job in self.build_jobs:
        req = urllib2.Request(job.url)
        if (Config.platform == 'jenkins'):
          req.add_header('Content-Type', 'application/json')
        if (Config.platform == 'travis'):
          req.add_header('Content-Type', 'application/vnd.travis-ci.2+json')
        response_body = urllib2.urlopen(req).read()
        print json.dumps(json.loads(response_body), indent=4, separators=(',', ': '))
    except Exception as e:
      print "Error:", type(e), e.args, e


if __name__ == '__main__':
  Check()
