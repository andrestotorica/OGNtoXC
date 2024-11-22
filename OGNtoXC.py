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
    print(f"Downloaded {len(ognDevices)} device records from OGN DB")

    # filter devices by Competition ID and registration country prefix
    # note that XCSoar supports up to 200 device IDs
    devsToTrack = []
    for device in ognDevices:
        if device.registration.startswith(registration_prefix) and device.cn in competition_ids:
            devsToTrack.append( device )
    assert len(devsToTrack) <= 200

    # export to XCSoar format
    with open( 'xcsoar-flarm.txt','w' ) as f:
        f.writelines( f'{dev.device_id}={dev.cn}\n' for dev in devsToTrack )
    # export human-readable report
    with open( 'report.txt','w' ) as f:
        f.writelines( f'{dev.device_id}\t{dev.device_type}\t{dev.registration}\t{dev.cn}\t{dev.aircraft_model}\n' for dev in devsToTrack )

    print(f"Succesfully wrote {len(devsToTrack)} IDs into xcsoar-flarm.txt (out of {len(competition_ids)} competition IDs provided) ")
