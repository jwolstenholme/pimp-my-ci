
from lib.build_job import BuildJob

class Config:

  polling_interval_secs = 3

  ci_url = 'http://localhost:8080/jenkins/api/json'

  num_leds = 7
  jobs=[
    BuildJob(name='test1', num_leds=num_leds),
    BuildJob(name='test2', num_leds=num_leds),
    BuildJob(name='test3', num_leds=num_leds),
    BuildJob(name='test4', num_leds=num_leds)
  ]
