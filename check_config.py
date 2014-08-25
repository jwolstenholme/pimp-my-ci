
from config.config import Config

import urllib2
import yaml

class Check:

  def __init__(self):

    print "\n==== Global ===="
    print "  CI server url    : ", Config.ci_url
    print "  Polling interval : ", Config.polling_interval_secs, "seconds"

    print "\n==== Builds ===="
    index = 0
    job_leds = dict()
    for job in Config.jobs:
      print " ", job.name.ljust(16), "leds", job.led_coordinates(index)
      for i in job.led_addresses(index):
        job_leds[i] = job.name
      index = job.next_index(index)

    print "\n==== LEDs ===="
    for i in range(Config.total_number_leds):
      print "  [", str(i).rjust(2), "]", job_leds.get(i, "  *")

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
