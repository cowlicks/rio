import os
import optparse


def parseargs():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', type=int, default=1986,
                      help="Port on which to listen for clients")
    parser.add_option('-H', '--host', default="localhost",
                      help="Our hostname")
    (options, args) = parser.parse_args()
    return (options, args)

opts, _ = parseargs()

HOST = opts.host
PORT = opts.port

DIRECTORY = os.path.expanduser('~/{host}/public/simply'.format(host=HOST))

STREAMS = [
    'http://pub1.di.fm/di_lounge',
    'http://pub1.di.fm/di_chillout',
    'http://listen.radionomy.com/air-lounge',
    'http://listen.radionomy.com/aair-lounge-radio',
]

Radionomy_ads = [
    'Musicplus - Jingle',
    'Joyeux Noel -',
    'Air Lounge Radio - Jingle',
    'Sfx - AdArrival',
    'AddictedToRadio',
]

DIfm_ads = [
    'ADWTAG',
    'www.di.fm/jobs',
]

AD_TITLES = Radionomy_ads + DIfm_ads
