#!/usr/bin/env python3
import csv
import logging
from pprint import pprint
from qrcodegen import QrCode, QrSegment
import shutil
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

address_file = 'btc_addresses.csv'
temp_file = 'btc_addresses_temp.csv'

if __name__ == '__main__':
    try:
        # Copy csv file
        logger.debug('Copying csv file with BTC addresses to temp file.')
        shutil.copy(address_file, temp_file)
        
        # Read temp csv file
        address_list = []
        logger.debug('Reading csv file.')
        with open(temp_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            try:
                for row in csv_reader:
                    #logger.debug(row)
                    
                    num = row[0]
                    pub = row[1].strip('"')
                    priv = row[2].strip('"')

                    address_row = [num, pub, priv]
                    #logger.debug(address_row)

                    address_list.append(address_row)
            
            except Exception as e:
                logger.exception('Exception occurred while reading csv file.')
                logger.exception(e)
                raise

        # Debug print
        pprint(address_list)

        # Write modified values to temp csv files
        with open(temp_file, 'w', newline='') as csv_file:
            try:
                for row in address_list:
                    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(row)
            
            except Exception as e:
                logger.exception('Exception occurred while writing to temp file.')
                logger.exception(e)
                raise

        # Debug read of csv file written with modified values
        with open(temp_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            try:
                for row in csv_reader:
                    logger.debug(row)

            except Exception as e:
                logger.exception('Exception occurred while reading temp file.')
                logger.exception(e)
                raise
        
        # For each line, create qr code and save to individual directories
        print('Things')

        # Do something with temp file
        print('Junk')

    except Exception as e:
        logger.exception(e)
        sys.exit(1)
