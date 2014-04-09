#! /usr/bin/env python

import os
import signal
import argparse
import logging
import utils
from datetime import date, datetime, timedelta
from multiprocessing import Pool

# To convert binary MRT data to ASCII, download and compile libbgpdump:
# http://www.ris.ripe.net/source/bgpdump/libbgpdump-1.4.99.11.tar.gz

WGET = '/usr/bin/env wget'
BUNZIP = '/usr/bin/env bunzip2'
BGPDUMP = os.path.abspath('./libbgpdump-1.4.99.11/bgpdump')

#            'http://archive.routeviews.org/bgpdata/2009.11/UPDATES/updates.20091101.0000.bz2'
UPDATE_FMT = 'http://archive.routeviews.org/bgpdata/%s/UPDATES/updates.%s.bz2'

def process_data_url(url):
    downloaded_file = url.split('/')[-1]
    unzipped_file = os.path.splitext(downloaded_file)[0]
    ascii_file = '%s.ascii' % unzipped_file
    
    # Download file
    wget_cmd = '%s %s' % (WGET, url)
    logging.getLogger(__name__).debug(wget_cmd)
    try:
        utils.check_output(wget_cmd)
    except Exception as e:
        logging.getLogger(__name__).warn(e)
        return (url, False)

    # unzip file
    unzip_cmd = '%s %s' % (BUNZIP, downloaded_file)
    logging.getLogger(__name__).debug(unzip_cmd)
    try:
        utils.check_output(unzip_cmd)
    except Exception as e:
        logging.getLogger(__name__).error(e)
        return (url, False)

    # convert to ascii
    if args.ascii and os.path.isfile(BGPDUMP):
        ascii_cmd = '%s %s > %s' % (BGPDUMP, unzipped_file, ascii_file)
        logging.getLogger(__name__).debug(ascii_cmd)
        try:
            utils.check_output(ascii_cmd)
            os.remove(unzipped_file)
        except Exception as e:
            logging.getLogger(__name__).error(e)
            return (url, False)

    return (url, True)

def get_updates():
    global pool
    logging.getLogger(__name__).info('Getting updates from %s to %s', args.start, args.end)

    # make a list of data files to download
    urls_to_download = []
    currenttime = args.start
    while currenttime <= args.end:
        url = UPDATE_FMT % (currenttime.strftime('%Y.%m'), currenttime.strftime('%Y%m%d.%H%M'))
        urls_to_download.append(url)
        currenttime += timedelta(minutes=15)

    # download them using all cores
    pool = Pool()
    try:
        #results = pool.map(process_data_url, urls_to_download)
        results = pool.map_async(process_data_url, urls_to_download).get(0xFFFF)
    except KeyboardInterrupt:
        sys.exit()

    # print stats about data downloaded
    successes = [x for x in results if x[1]]
    failures = [x for x in results if not x[1]]
    print 'Downloaded %d of %d files.' % (len(successes), len(results))
    if len(failures) > 0:
        print 'The following files could not be downloaded or processed:'
        for f in failures:
            print '\t' + f[0]




def main():
    logging.getLogger(__name__).debug('Switching to %s' % args.outdir)
    if not os.path.isdir(args.outdir):
        try:
            os.makedirs(args.outdir)
        except Exception as e:
            logging.getLogger(__name__).error('Error making output directory: %s' % args.outdir)
            exit(-1)
    os.chdir(args.outdir)

    if args.type == 'updates':
        get_updates()
    else:
        logging.getLogger(__name__).warn('Downloading RIBs not supported yet')


if __name__ == '__main__':

    # build string for today
    today = date.today().strftime('%Y%m%d')

    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                        description='Download Route Views data files.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Print extra information for debugging.')
    parser.add_argument('-o', '--outdir', default='.', help='Destination directory.')
    parser.add_argument('-t', '--type', default='updates', help='Data type: RIBs or UPDATEs')
    parser.add_argument('-s', '--start', default='20090501', help='Start date (YYYYMMDD)')
    parser.add_argument('-e', '--end', default=today, help='End date (YYYYMMDD). Defaults to midnight today.')
    parser.add_argument('-a', '--ascii', action='store_true', default=False, help='Convert downloaded data files to ASCII.')

    args = parser.parse_args()
    args.type = args.type.lower()
    args.start = datetime.strptime(args.start, '%Y%m%d')
    args.end = datetime.strptime(args.end, '%Y%m%d')

    if args.ascii and not os.path.isfile(BGPDUMP):
        logging.getLogger(__name__).warning('libbgpdump not found; will not convert data to ASCII')

    # set up logging
    logging.basicConfig(
        #filename = fileName,
        format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName) -26s %(message)s",
        level = logging.DEBUG if args.verbose else logging.WARNING
    )

    main()
