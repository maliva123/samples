import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

agg = 'e136320@nrxav0362.bcbsm.com:/opt/data/knowbe4/'

#agg1 = 'e136320@nrxav0362.bcbsm.com:/home/ent.corp.bcbsm.com/e136320/'

pp='/Users/e136320/knowbe4_proj/*'

p = subprocess.Popen(["scp", pp, agg])
p.wait()
print('process %d finished' % p.pid)










