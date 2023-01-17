import requests
import pandas as pd
from collections import namedtuple

# Filter criteria
REGISTRATION_PREFIX = 'LV'
COMPETITION_IDS = ["41","ACP","GL","ZT","ZC","QM","WR","T2","MB","CPC","ZM","TL",
                   "CR","VN","DI","KC","JG","CQ","TI","AC","ZB","W","IT","NA","N1",
                   "ZG","MM","FU","EG","M1","Z3","DK","RI","DP","RR","X","ZZ","WL",
                   "EY","PB","SH","AM","V8","10","LG","1R"]
#


OgnDevice = namedtuple('OgnDevice',
                       ['device_type',
                        'device_id',
                        'aircraft_model',
                        'registration',
                        'cn',
                        'tracked',
                        'identified'])


# download all registered devices from OGN DB
ognDbRequest = requests.get('https://ddb.glidernet.org/download/')
assert ognDbRequest.status_code == 200

ognDbRecords = ognDbRequest.content.decode().splitlines()[1:]
ognDevices = [ OgnDevice( *record.replace("'","").split(',') ) for record in ognDbRecords ]


# filter devices by Competition ID and registration country prefix
# note that XCSoar supports up to 200 device IDs
devsToTrack = []
for device in ognDevices:
    if REGISTRATION_PREFIX in device.registration and device.cn in COMPETITION_IDS:
        devsToTrack.append( device )
assert len(devsToTrack) <= 200

# export to XCSoar format
with open( 'xcsoar-flarm.txt','w' ) as f:
    f.writelines( '{}={}\n'.format(dev.device_id, dev.cn) for dev in devsToTrack )

print("Succesfully wrote {} IDs (out of {}) into xcsoar-flarm.txt".format(len(devsToTrack), len(COMPETITION_IDS)))
