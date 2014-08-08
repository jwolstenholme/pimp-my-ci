
from lib.build_job import BuildJob

class Config:

  ci_url = 'http://jenkins.metest.local/api/json'

  num_leds = 4
  jobs=[
    BuildJob(name='Monitor DEV G Channel Arrangement',  num_leds=num_leds),
    BuildJob(name='Truman-ios',                         num_leds=num_leds),
    BuildJob(name='MonkeyTalk',                         num_leds=2, offset=0),
    BuildJob(name='Android_Monkey_Matrix',              num_leds=2),
    BuildJob(name='Android_Commit',                     num_leds=2, offset=0),
    BuildJob(name='Android_Functional',                 num_leds=2, offset=0),
    BuildJob(name='Android_Hockey_Deploy',              num_leds=1),
    BuildJob(name='ChannelApi',                         num_leds=num_leds),
    BuildJob(name='DAM',                                num_leds=num_leds)
  ]
