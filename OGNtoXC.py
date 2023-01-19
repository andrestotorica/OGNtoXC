import argparse
from collections import namedtuple
import pandas as pd
import requests


OgnDevice = namedtuple('OgnDevice',
                       ['device_type',
                        'device_id',
                        'aircraft_model',
                        'registration',
                        'cn',
                        'tracked',
                        'identified'])


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('registration_prefix', help='Registration prefix (country code) to filter with')
    parser.add_argument('competition_ids', help='Comma separated list of competition ids to filter')
    parser = parser.parse_args()
    return parser.registration_prefix, parser.competition_ids.split(',')

if __name__=='__main__':
    registration_prefix, competition_ids = read_args()
    
    # download all registered devices from OGN DB
    ognDbRequest = requests.get('https://ddb.glidernet.org/download/')
    assert ognDbRequest.status_code == 200

    ognDbRecords = ognDbRequest.content.decode().splitlines()[1:]
    ognDevices = [ OgnDevice( *record.replace("'","").split(',') ) for record in ognDbRecords ]

    # filter devices by Competition ID and registration country prefix
    # note that XCSoar supports up to 200 device IDs
    devsToTrack = []
    for device in ognDevices:
        if registration_prefix in device.registration and device.cn in competition_ids:
            devsToTrack.append( device )
    assert len(devsToTrack) <= 200

    # export to XCSoar format
    with open( 'xcsoar-flarm.txt','w' ) as f:
        f.writelines( '{}={}\n'.format(dev.device_id, dev.cn) for dev in devsToTrack )

    print("requirements.txt {} IDs (out of {}) into xcsoar-flarm.txt".format(len(devsToTrack), len(competition_ids)))
