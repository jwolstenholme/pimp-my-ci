
from lib.build_job import BuildJob

class Config:

  ci_url = 'http://192.168.0.93:8080/jenkins/api/json'

  num_leds = 7
  jobs=[
    BuildJob(name='test1', num_leds=num_leds),
    BuildJob(name='test2', num_leds=num_leds),
    BuildJob(name='test3', num_leds=num_leds),
    BuildJob(name='test4', num_leds=num_leds)
  ]
