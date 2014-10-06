
from lib.build_jobs import BuildJobs
from lib.config import Config

import urllib2
import json

class Check:

  def __init__(self):
    self.build_jobs = BuildJobs.from_dictionaries(Config.platform, Config.job_defaults, Config.jobs)
    self.printGlobal()
    self.printJobs()
    self.printLedLayout()
    self.printTestResponse()


  def printGlobal(self):
    print "\n==== Global ===="
    print "  Toal number of LEDs  : ", Config.total_number_leds
    print "  Polling interval     : ", Config.polling_interval_secs, "seconds"
    print "  Platform             : ", Config.platform
    if (Config.platform == 'jenkins'):
      print "  URL                  : ", Config.job_defaults['url']

  def printJobs(self):
    print "\n==== Builds ===="
    index = 0
    self.job_leds = dict()

    for job in self.build_jobs:
      print " ", job.name
      print "\tleds:".ljust(14), str(job.led_coordinates(index))
      if (Config.platform == 'travis'):
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
      if (Config.platform == 'jenkins'):
        self.printJenkinsResponse()
      if (Config.platform == 'travis'):
        self.printTravisResponses()
    except Exception as e:
      print "Error:", type(e), e.args, e

  def printJenkinsResponse(self):
    req = urllib2.Request(Config.job_defaults['url'])
    req.add_header('Content-Type', 'application/json')
    response_body = urllib2.urlopen(req).read()
    print json.dumps(json.loads(response_body), indent=4, separators=(',', ': '))

  def printTravisResponses(self):
    for job in self.build_jobs:
      req = urllib2.Request(job.url)
      req.add_header('Content-Type', 'application/vnd.travis-ci.2+json')
      response_body = urllib2.urlopen(req).read()
      print json.dumps(json.loads(response_body), indent=4, separators=(',', ': '))

if __name__ == '__main__':
  Check()
