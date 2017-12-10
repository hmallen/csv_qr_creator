#!/usr/bin/env python3
import csv
import logging
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
        shutil.copy(address_file, temp_file)
        
        # Read temp csv file
        # For each line, create qr code and save to individual directories

    except Exception as e:
        logger.exception(e)
        sys.exit(1)
