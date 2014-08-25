
from config.config import Config

class Check:

  def __init__(self):
    config = Config()

    print "\n==== Global ===="
    print "  CI server url    : ", config.ci_url
    print "  Polling interval : ", config.polling_interval_secs, "seconds"

    print "\n==== Builds ===="
    index = 0
    job_leds = dict()
    for job in Config.jobs:
      print job.name.ljust(16), "leds", job.led_coordinates(index)
      for i in job.led_addresses(index):
        job_leds[i] = job.name
      index = job.next_index(index)

    print "\n==== LEDs ===="
    for i in range(Config.total_number_leds):
      print " [", str(i).rjust(2), "]", job_leds.get(i, "  *")

if __name__ == '__main__':
    Check()