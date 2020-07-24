#!/usr/bin/env python3
##########################################################################
# OCI Details to ADWC:
#
# Required OCI user part of UsageDownloadGroup with below permission:
#
# config file should contain:
#     [IDCS][username][password]
##########################################################################
import datetime
import json
import base64
import http.client
import mimetypes
import urllib.parse
import cx_Oracle
import sys
import argparse
from configparser import ConfigParser

version = "1.0"
empty_json_datatable = "{\"items\":[]}"
error_json_datatable = "{\"items\":[]}"
dateFormat = '%Y-%m-%dT%H:%M:%S.%fZ'

def parse_subscription_details(id,jsondata,startTime,endTime):
    xbalance=0
    xrunningBalance = 0
    xpurchase=0
    xstartDate=""
    xendDate=""
    xcommitmentModel=""
    xcurrentdate=False
    xdaysleft = 0

    for item in jsondata["items"]:
        for purchase in item["purchase"]:
            try:
                if (id == purchase["id"]):
                    for purchasedResource in purchase["purchasedResources"]:
                        if "startDate" in purchasedResource and "endDate" in purchasedResource:
                            xpurchase = round(xpurchase + purchasedResource["value"],2)
                            #if "startDate" in purchasedResource:
                            xstartDate = purchasedResource["startDate"]
                            #if "endDate" in purchasedResource:
                            xendDate = purchasedResource["endDate"]
                            #print(xstartDate)
                            xstartTime = datetime.datetime.strptime(xstartDate,dateFormat)

                            #print(xendDate)
                            xendTime = datetime.datetime.strptime(xendDate,dateFormat)

                            if (xstartTime <= startTime <= xendTime) and (xstartTime <= endTime <= xendTime):
                                #xcurrentpurchase = xcurrentpurchase + purchasedResource["value"]
                                xcurrentdate=True
                                #print("current date")
                                xdaysleft = xendTime - endTime
                                #print(xdaysleft)
                            else:
                                xcurrentdate=False

                            if "commitmentModel" in purchasedResource:
                                xcommitmentModel = purchasedResource["commitmentModel"]
                            #print(xcommitmentModel)
                            break
            except Exception as e:
                print(traceback.format_exc())
                print("first exception",e)

        for balance in item["balance"]:
            try:
                if (id == balance["id"]):
                    for purchasedResource in balance["purchasedResources"]:
                        xbalance = round((xbalance + purchasedResource["value"]),2)
                    break
            except Exception as e:
                print(traceback.format_exc())
                print("second exception ",e)

        for balance in item["runningBalance"]:
            try:
                if (id == balance["id"]):
                    for purchasedResource in balance["purchasedResources"]:
                        xrunningBalance = round((xrunningBalance + purchasedResource["value"]),2)
                    break
            except Exception as e:
                print(traceback.format_exc())
                print("third exception",e)

    compile_data = {'id':id,'purchaseStartDate':xstartDate,'purchaseEndDate':xendDate,'purchase':xpurchase,'runningBalance':xrunningBalance,'balance':xbalance,'commitmentModel':xcommitmentModel,'xcurrentdate':xcurrentdate,'xdaysleft':xdaysleft}
    #compile_data = {'id':id,'purchaseStartDate':xstartTimeStr,'purchaseEndDate':xendTimeStr,'purchase':xpurchase,'runningBalance':xrunningBalance,'balance':xbalance,'commitmentModel':xcommitmentModel,'xcurrentdate':xcurrentdate,'xdaysleft':xdaysleft}

    return compile_data


def get_subscription_dtls(parsed_json):
    json_output=empty_json_datatable
    compile_data = list()
    curr_compile_data = list()
    curr_balance = 0
    curr_purchase = 0
    curr_runningbalance = 0
    curr_daysleft = 0
    curr_commitment_model = ""
    subscriptionType = ""
    payg = ""
    billingType = ""
    entitlementId = ""
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    purchaseStartDate = startTime
    purchaseEndDate = endTime
    try:
        jsondata = json.loads(parsed_json)
        for item in jsondata["items"]:
            subscriptionType = item["subscriptionType"]
            payg = item["payg"]
            billingType = item["billingType"]
            entitlementId = item["entitlementId"]

            for purchase in item["purchase"]:
                id_compile_data = parse_subscription_details(purchase["id"],jsondata,startTime,endTime)
                #compile_data.append(id_compile_data)
                if id_compile_data["xcurrentdate"]:
                    curr_balance = curr_balance + id_compile_data["balance"]
                    curr_purchase = curr_purchase + id_compile_data["purchase"]
                    curr_runningbalance = curr_runningbalance + id_compile_data["runningBalance"]
                    curr_daysleft = id_compile_data["xdaysleft"]
                    purchaseStartDate = id_compile_data["purchaseStartDate"]
                    purchaseEndDate = id_compile_data["purchaseEndDate"]
                    if "commitmentModel" in id_compile_data:
                        if id_compile_data["commitmentModel"] != "":
                            curr_commitment_model = id_compile_data["commitmentModel"]
        #print(curr_runningbalance)
        #print(curr_balance)
        #print(curr_purchase)
    except Exception as e:
        print(traceback.format_exc())
        print("error",e)

    #detail_items = {'items':compile_data}
    full_dtls = {'curr_balance':round(curr_balance,2),'curr_purchase':round(curr_purchase,2),\
                 'curr_runningbalance':round(curr_runningbalance,2),'curr_daysleft':curr_daysleft,\
                 'curr_commitment_model':curr_commitment_model,'subscriptionType':subscriptionType,\
                 'payg':payg,'billingType':billingType,'entitlementId':entitlementId,\
                 'purchaseStartDate':purchaseStartDate,'purchaseEndDate':purchaseEndDate}
    #print(full_dtls)
    return full_dtls

def get_entitlement_details(parsed_json):
    cloudAccount = None
    cloudAccountName = None
    subscriptionId = None
    try:
        jsondata = json.loads(parsed_json)
        if "items" in jsondata:
            for item in jsondata["items"]:
                cloudAccount = item['cloudAccount']['id']
                cloudAccountName = item['cloudAccount']['name']
                subscriptionId = item["purchaseEntitlement"]["subscriptionId"]
                break
    except Exception as e:
        print(traceback.format_exc())
        print("error",e)

    details = {'cloudAccount':cloudAccount,'cloudAccountName':cloudAccountName,'subscriptionId':subscriptionId}
    return details

def call_api_parse(requestType,cloudTenant,cloudAccount,username,password):
    unpwddata = username + ":" + password
    encodedBytes = base64.b64encode(unpwddata.encode("utf-8"))
    credentialsEncodedStr = str(encodedBytes, "utf-8")
    headers = {
        'user-agent':'mozilla/4.0',
        'X-ID-TENANT-NAME': cloudTenant,
        'Authorization' : "Basic " + credentialsEncodedStr,
        'cache-control': "no-cache"
        }

    requestURL = ""
    cloudParams = {}
    if requestType == "ENTITLEMENTS":
        requestURL = "/itas/" + cloudTenant + "/myservices/api/v1/serviceEntitlements"
    elif requestType=="SUBSCRIPTION_DETAILS":
        requestURL = "/metering/api/v1/cloudbucks/" + cloudAccount

    response = None
    try:
        conn = http.client.HTTPSConnection("itra.oraclecloud.com")
        payload = ''
        params = ''
        if cloudParams:
          params = urllib.parse.urlencode(cloudParams)
          requestURL = requestURL + "?" + params

        print(requestURL)
        conn.request("GET", requestURL,payload, headers)

        res = conn.getresponse()
        data = res.read()
        if data:
           response = data.decode("utf-8")
    except:
        print("request error")
    finally:
        conn.close()

    if response:
        if requestType=="SUBSCRIPTION_DETAILS":
            return get_subscription_dtls(response)
        elif requestType == "ENTITLEMENTS":
            return get_entitlement_details(response)
    else:
        return None

def upsert_subscription_details(connection,idcsDomain,entitlementDetails,subscriptionDetails):
    try:
        # open cursor
        cursor = connection.cursor()
        print("\nMerging statistics into OCI_SUBSCRIPTION_INFORMATION...")

        # run merge to oci_update_stats
        sql = "merge into OCI_SUBSCRIPTION_INFORMATION a "
        sql += "using "
        sql += "( "
        sql += "    select  "
        sql += "   '" + idcsDomain + "' IDCS_DOMAIN_NAME, "
        sql += "   '" + entitlementDetails["cloudAccount"] + "' account_id, "
        sql += "   '" + entitlementDetails["cloudAccountName"] + "' account_name, "
        sql += "   '" + subscriptionDetails["curr_commitment_model"] + "' COMMITMENT_MODEL, "
        sql += "   '" + entitlementDetails["subscriptionId"] + "' subscription_id, "
        sql += "   '" + subscriptionDetails["subscriptionType"] + "' SUBSCRIPTION_TYPE, "
        sql += "   '" + subscriptionDetails["payg"] + "' PAY_GO, "
        sql += "   '" + subscriptionDetails["billingType"] + "' BILLING_TYPE, "
        sql += "   to_date('" + datetime.datetime.strptime(subscriptionDetails["purchaseStartDate"],dateFormat).strftime("%d-%b-%Y") + "') PURCHASE_START_DATE, "
        sql += "   to_date('" + datetime.datetime.strptime(subscriptionDetails["purchaseEndDate"],dateFormat).strftime("%d-%b-%Y") + "') PURCHASE_END_DATE "
        sql += "    from  "
        sql += "        DUAL "
        sql += ") b "
        sql += "on (a.IDCS_DOMAIN_NAME=b.IDCS_DOMAIN_NAME and a.account_id = b.account_id and a.subscription_id = b.subscription_id) "
        sql += "when matched then update set a.COMMITMENT_MODEL= b.COMMITMENT_MODEL, "
        sql += "  a.SUBSCRIPTION_TYPE = b.SUBSCRIPTION_TYPE, "
        sql += "  a.PAY_GO= b.PAY_GO, "
        sql += "  a.BILLING_TYPE= b.BILLING_TYPE, "
        sql += "  a.PURCHASE_START_DATE=b.PURCHASE_START_DATE, "
        sql += "  a.PURCHASE_END_DATE= b.PURCHASE_END_DATE "
        sql += " when not matched then insert (IDCS_DOMAIN_NAME,account_id,account_name,COMMITMENT_MODEL,subscription_id,SUBSCRIPTION_TYPE,PAY_GO,BILLING_TYPE,PURCHASE_START_DATE,PURCHASE_END_DATE)  "
        sql += "   values (b.IDCS_DOMAIN_NAME,b.account_id,b.account_name,b.COMMITMENT_MODEL,b.subscription_id,b.SUBSCRIPTION_TYPE,b.PAY_GO,b.BILLING_TYPE,b.PURCHASE_START_DATE,b.PURCHASE_END_DATE) "

        #print(sql)
        cursor.execute(sql)
        connection.commit()
        print("   Merge Completed, " + str(cursor.rowcount) + " rows merged")

        # close cursor
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print("\nError manipulating database at update_subscription_details() - " + str(e) + "\n")
        raise SystemExit

    except Exception as e:
        raise Exception("\nError manipulating database at update_subscription_details() - " + str(e))


##########################################################################
# Check Table Structure for usage
##########################################################################
def check_database_subscriptiondetails(connection):
    try:
        # open cursor
        cursor = connection.cursor()

        # check if OCI_SUBSCRIPTION_INFORMATION table exist, if not create
        sql = "select count(*) from user_tables where table_name = 'OCI_SUBSCRIPTION_INFORMATION'"
        cursor.execute(sql)
        val, = cursor.fetchone()

        # if table not exist, create it
        if val == 0:
            print("   Table OCI_SUBSCRIPTION_INFORMATION was not exist, creating")
            sql = "create table OCI_SUBSCRIPTION_INFORMATION ("
            sql += "    IDCS_DOMAIN_NAME        VARCHAR2(100),"
            sql += "    ACCOUNT_NAME            VARCHAR2(100),"
            sql += "    ACCOUNT_ID              VARCHAR2(200),"
            sql += "    SUBSCRIPTION_ID         NUMBER,"
            sql += "    COMMITMENT_MODEL        VARCHAR2(100),"
            sql += "    SUBSCRIPTION_TYPE       VARCHAR2(100),"
            sql += "    PAY_GO                  VARCHAR2(10),"
            sql += "    BILLING_TYPE            VARCHAR2(100),"
            sql += "    PURCHASE_START_DATE     DATE,"
            sql += "    PURCHASE_END_DATE       DATE"
            sql += ") COMPRESS"
            cursor.execute(sql)
            print("   Table OCI_SUBSCRIPTION_INFORMATION created")
        else:
            print("   Table OCI_SUBSCRIPTION_INFORMATION exist")

        # close cursor
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print("\nError manipulating database at check_database_table_structure_usage() - " + str(e) + "\n")
        raise SystemExit

    except Exception as e:
        raise Exception("\nError manipulating database at check_database_table_structure_usage() - " + str(e))


def get_details(connection,cfg):
    print(cfg.sections())
    for x in cfg.sections():
        try:
            print(x)
            print(cfg.get(x,"idcs"))

            cloudTenant = cfg.get(x,"idcs")
            username = cfg.get(x,"username")
            password = cfg.get(x,"password")

            requestType = "ENTITLEMENTS"
            entitlementDetails = call_api_parse(requestType,cloudTenant,None,username,password)
            if "cloudAccount" in entitlementDetails:
                requestType = "SUBSCRIPTION_DETAILS"
                subscriptionDetails = call_api_parse(requestType,cloudTenant,entitlementDetails["cloudAccount"],username,password)

            #print(entitlementDetails)
            #print(subscriptionDetails)
            #print(datetime.datetime.strptime(subscriptionDetails["purchaseStartDate"],dateFormat).strftime("%d-%b-%Y"))
            #print(datetime.datetime.strptime(subscriptionDetails["purchaseEndDate"],dateFormat).strftime("%d-%b-%Y"))
            upsert_subscription_details(connection,cloudTenant,entitlementDetails,subscriptionDetails)

        except Exception as e:
            raise Exception("\nError getting and updating details - " + str(e))

##########################################################################
# Print header centered
##########################################################################
def print_header(name, category):
    options = {0: 90, 1: 60, 2: 30}
    chars = int(options[category])
    print("")
    print('#' * chars)
    print("#" + name.center(chars - 2, " ") + "#")
    print('#' * chars)

##########################################################################
# set parser
##########################################################################
def set_parser_arguments():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-c', type=argparse.FileType('r'), dest='config', help="Config File")
    parser.add_argument('-du', default="", dest='duser', help='ADB User')
    parser.add_argument('-dp', default="", dest='dpass', help='ADB Password')
    parser.add_argument('-dn', default="", dest='dname', help='ADB Name')
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)

    result = parser.parse_args()

    if not (result.duser and result.dpass and result.dname):
        parser.print_help()
        print_header("You must specify database credentials!!", 0)
        return None

    return result

def main_process():
    cmd = set_parser_arguments()
    if cmd is None:
        exit()

    #print(cmd.config)
    cfg = ConfigParser()
    cfg.read("customers.ini")

    try:
        connection = None
        print("\nConnecting to database " + cmd.dname)
        connection = cx_Oracle.connect(user=cmd.duser, password=cmd.dpass, dsn=cmd.dname, encoding="UTF-8", nencoding="UTF-8")
        cursor = connection.cursor()
        print("   Connected")
        cursor.close()
        check_database_subscriptiondetails(connection)
        get_details(connection,cfg)
        connection.close()
    except cx_Oracle.DatabaseError as e:
        print("\nError manipulating database at check_database_table_structure_usage() - " + str(e) + "\n")
        raise SystemExit

    except Exception as e:
        raise Exception("\nError manipulating database at check_database_table_structure_usage() - " + str(e))


##########################################################################
# Execute Main Process
##########################################################################
main_process()

