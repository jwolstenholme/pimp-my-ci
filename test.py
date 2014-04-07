import Queue

from time import sleep
from lib.ledstrip import Strand
from lib.const import *
from lib.lights_controller import LightsController

jobs = ['Truman', 'ChannelApi', 'Security-POC']
job_queues = {job: Queue.Queue() for job in jobs}

print 'job_queues: ', job_queues

strand = Strand()
strand.fill(0, 0, 0)

lights_controller = LightsController(job_queues, strand)

job_queues['Truman'].put_nowait(SUCCESS)
job_queues['ChannelApi'].put_nowait(FAILURE)
job_queues['Security-POC'].put_nowait(UNKNOWN)

sleep(2)

job_queues['Security-POC'].put_nowait(SUCCESS)
job_queues['Truman'].put_nowait(FAILURE)
job_queues['ChannelApi'].put_nowait(UNKNOWN)

sleep(2)


#lights_controller.update_build_status('Truman', SUCCESS)
#lights_controller.update_build_status('ChannelApi', FAILURE)
#lights_controller.update_build_status('Security-POC', UNKNOWN)



#for i in range(32):
#  strand.set(i, i*7, i*4, i*1)

#strand.update()

#strand.fill(0, 0, 0)
#strand.fill(255, 0, 0, 0, 10)
#strand.fill(0, 255, 0, 11, 20)
#strand.fill(0, 0, 255, 21, 32)

#sleep(1)
#strand.fill(0, 255, 0, 0, 10)
#sleep(1)
#strand.fill(0, 0, 255, 11, 20)
#sleep(1)
#strand.fill(255, 0, 0, 21, 32)

#sleep(1)
#strand.fill(0, 0, 255, 0, 10)
#sleep(1)
#strand.fill(255, 0, 0, 11, 20)
#sleep(1)
#strand.fill(0, 255, 0, 21, 32)


