#!/bin/bash
cd /home/oracle
. ./setenv.env
python3 refresh_subscriptions_details.py -du "USAGE" -dp "PaSsw0rd2" -dn "reportingdb.subnet.vcn.oraclevcn.com:1521/orclpdb1" 
