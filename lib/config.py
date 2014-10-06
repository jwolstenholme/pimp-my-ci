
class Config:

  # The total number of LEDs available on the strip
  total_number_leds = 32

  # The URL of the CI server
  ci_url = 'http://192.168.0.40:8080/jenkins/api/json'

  # The number of seconds to wait between polling the CI server
  polling_interval_secs = 3

  # The build jobs to monitor
  jobs=[
    dict(name='test1', num_leds=7, success='Burns_Excellent', failure='Sheeeeeiiiit'),
    dict(name='test2', num_leds=7, success=None, failure='Sheeeeeiiiit'),
    dict(name='test3', num_leds=7, success='Burns_Excellent', failure=None),
    dict(name='test4', num_leds=7)
  ]
