
class Config:

  # The total number of LEDs available on the strip
  total_number_leds = 32

  # The number of seconds to wait between polling the CI server
  polling_interval_secs = 3

  # The CI platform we're hitting up
  platform = 'jenkins'

  # Default settings across all jobs
  job_defaults = dict(  num_leds = 7, url = 'http://192.168.0.40:8080/jenkins/api/json' )

  #platform = 'travis'
  #job_defaults = dict(  num_leds = 7, url = 'https://api.travis-ci.org/repos/jwolstenholme/pimp-my-ci' )

  # The build jobs to monitor - defaults are overridden
  jobs = [
    dict( name = 'test1',
          success = 'Burns_Excellent',
          failure = 'Sheeeeeiiiit',
          platform = 'travis'),

    dict( name = 'test2',
          success = None,
          failure = 'Sheeeeeiiiit'),

    dict( name = 'test3',
          success = 'Burns_Excellent',
          failure = None),

    dict( name = 'test4')
  ]
