#!/usr/bin/env python3
import argparse
import csv
import datetime
import logging
import os
from pprint import pprint
from qrcodegen import QrCode, QrSegment
import shutil
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help='Choose alternate input csv file. [Default = \'btc_addresses.csv\']')
args = parser.parse_args()

if args.input:
    address_file = args.input
    logger.info('Set csv file to input path: \'' + address_file + '\'')
    
else:
    address_file = 'btc_addresses.csv'
    logger.info('Set csv file to default path: \'' + address_file + '\'')

if not os.path.isfile(address_file):
    logger.error('File \'' + address_file + '\' does not exist.')
    if not args.input:
        logger.error('Confirm default file \'btc_addresses.csv\' exists or define csv path manually using \'--input\'.')
    sys.exit(1)
else:
    logger.info('File \'' + address_file + '\' found.')


def create_temp_csv():
    # Copy csv file
    logger.debug('Copying csv to temp file.')
    shutil.copy(address_file, temp_file)
    
    # Read temp csv file
    address_list = []
    logger.debug('Reading csv temp file.')
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
    #pprint(address_list)

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


def create_svg():
    #errcorlvl = QrCode.Ecc.QUARTILE # Error correction level. Need to determine best setting!
    errcorlvl = QrCode.Ecc.LOW
    svg_list = []

    with open(temp_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        try:
            for row in csv_reader:
                qr_pub = QrCode.encode_text(row[1], errcorlvl)
                qr_svg_pub = qr_pub.to_svg_str(4)
                #logger.debug('PUBLIC')
                #logger.debug(qr_svg_pub)
                file_name_pub = output_path + row[0] + '_pub.svg'
                logger.debug(file_name_pub)
                with open(file_name_pub, 'w') as svg_file:
                    svg_file.write(qr_svg_pub)
                
                qr_priv = QrCode.encode_text(row[2], errcorlvl)
                qr_svg_priv = qr_priv.to_svg_str(4)
                #logger.debug('PRIVATE')
                #logger.debug(qr_svg_priv)
                file_name_priv = output_path + row[0] + '_priv.svg'
                logger.debug(file_name_priv)
                with open(file_name_priv, 'w') as svg_file:
                    svg_file.write(qr_svg_priv)

        except Exception as e:
            logger.exception('Exception while creating svg files.')
            logger.exception(e)
            raise


if __name__ == '__main__':
    if not os.path.exists('output'):
        logger.info('Output directory not found. Creating.')
        try:
            os.makedirs('output')
        except Exception as e:
            logger.exception('Failed to create output directory. Exiting.')
            logger.exception(e)
            sys.exit(1)
    else:
        logger.info('Found output directory.')

    dt_current = datetime.datetime.now().strftime('%m%d%Y-%H%M%S')

    temp_file = 'output/' + dt_current + '/btc_addresses_temp.csv'

    try:
        output_path = 'output/' + dt_current + '/'
        os.makedirs(output_path)
        
        create_temp_csv()

        """
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
        """

        # For each line, create qr code and handle svg files
        create_svg()

    except Exception as e:
        logger.exception(e)
        sys.exit(1)
