
from lib.build_job import BuildJob

class Config:

  # The total number of LEDs available on the strip
  total_number_leds = 32

  # The URL of the CI server
  ci_url = 'http://192.168.0.69:8080/jenkins/api/json'

  # The number of seconds to wait between polling the CI server
  polling_interval_secs = 3

  # The build jobs to monitor
  leds_per_job = 7
  jobs=[
    BuildJob(total_leds=total_number_leds, name='test1', num_leds=leds_per_job),
    BuildJob(total_leds=total_number_leds, name='test2', num_leds=leds_per_job),
    BuildJob(total_leds=total_number_leds, name='test3', num_leds=leds_per_job),
    BuildJob(total_leds=total_number_leds, name='test4', num_leds=leds_per_job)
  ]
