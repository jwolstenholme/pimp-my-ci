
class Config:

  total_number_leds = 32

  polling_interval_secs = 3

  platform = 'circleci'
  job_defaults = dict( num_leds = 32 )

  # The build jobs to monitor - defaults are overridden
  jobs = [
    dict( name = 'vix',
          url = 'https://circleci.com/api/v1/project/DiUS/vix?circle-token=8dd04ea68b5caf87a3be4ed050a97ae9d91ae4e9&limit=1&offset=0',
          success = 'Burns_Excellent',
          failure = 'Sheeeeeiiiit' ),
  ]
