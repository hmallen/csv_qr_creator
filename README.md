# CSV to QR code creator

Creates QR codes for Bitcoin addresses in csv file generated from "Bulk Wallet" mode on Bitaddress.org.

By default, the program looks for 'btc_addresses.csv' in the root directory. This file should be in the format [row number, public address, private address] to be read properly.

If desired, one can use the '-i' or '--input' options to manually define a path to the csv file to be used for QR code creation.

A copy of the input csv file is placed in a newly created directory, stripping unnecessary characters first. The csv file is read line-by-line, creating svg images of QR codes corresponding to the public and private keys. The files are named using the first column in the csv file as a prefix followed by 'pub' or 'priv' to identify the keys. Each set of keys is placed in a unique directory to prevent reuse.