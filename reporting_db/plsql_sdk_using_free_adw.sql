
--Create the credentials

BEGIN
  DBMS_CLOUD.CREATE_CREDENTIAL (
    credential_name => 'cen2020',
    user_ocid              => 'ocid1.user.oc1..aaaaaaaatat3hi6z37poabcge6cyxqac7fpwsc2xbraui63flr6qqngyw7oa',
    tenancy_ocid           => 'ocid1.tenancy.oc1..aaaaaaaacr2kimui4s25ck7zeyjrqvfc3bpyjlr73hjrydgukzwcwqctbqra',
    private_key            => 'MIIEogIBAAKCAQEAt3ImIgO8caxjZPFNMRRFjfqzBKleuiQDepVagCIN4d1oMJ3d
n4k+SAqtjyzLMVNskpzAlNX0JpERd1n1XTLXOy9uE6WeaPf1StLpoVdWDc1zWeRk
srKuM1dO/oWrmYvze0VP+N7nsyqfKuVyk2UjiHs04mCFKbkqIWf726MQsRkI6QMC
5V5ni430BIMNMcYTcR+YIlMLd8y85Y6Avhp0ThAJ/w7/ACVSJp2nLn6zq784tcFX
+s1dnzlexhk9njb8UmUYpL7TlTuMntktkYOxn4EsujrxLM7E5iOA1jA9+iChI7t4
/eF3HynoBtjlVQEPm9NsY3q9qSBHaw/Y0TRCMQIDAQABAoIBAE9lo2WDcnNMpnRR
EBTW7kfGIuc4mxw7bBoJPHNKyfFhD7BDE2HyV7d8j6PxQjymG87U83E3rQVoMkQS
9mSRFaCzJZRxUT+jWlI5OQ8wqrksm+ljNcY2Gbl052a32g6KCSboV/WiHGxqXRuG
1XFADAINOVVlax0k3Dw7MkHcsOPE84LF0DDaHg19oohUjgIsutCLIVJ8S+wYziEb
WvOEI7CHY4NTz4orpH6IVnE5GhlpyOuVR+i6rOSoGLMbI8wsDyjS8pO26T6P4CUQ
7NuUPMV35plXh4c5X0+qTffj/RkuvkaZ9/mhFi5BM2Eye0evGvy0osF8cbKT6wxl
k0ZyD0ECgYEA2piwgLOShIjZO+ZZ9BwX1OfFIzXvesrNX0bApCrJk9HwJ24NW8vs
Bqi57RG+IynKztNBorNm+/f3q68mrwtQFBrzDrElE5I7mysgGQjkCQ54XUwXNMKJ
8XnwuD3Q7GnUr3eAr5NBYIPBWR9SH3LcfxRbxGiPIdWQbnYZIbpaLRkCgYEA1tW9
L9VgIrto3LTRSeeL0C7QHpwap+TiUg9RKOlssyLdUuDwknHBit18bwkbwuQGEFxD
4CYHSUhENJKMlPzp0boQ+mnIAS2wG9ytLTjbp6YMTWuAyXxf0w+xhyI0qBPnVf5t
1AG3PVu0f+aiW9Xv8QmUBKr9xlgOL4q47nxdSNkCgYBUx+ec4wiukoz+aGb3AHZV
wtZ4w5BwJXvlugE5Kscnp8Lm6A4STlLqekIyKjF+XdUkxlasjbwheZj7Y2EzfsW+
Jn2icx4YKx0nH2DBlOssgAo61Soi8lih6VNtgbwoFRvCOi0U653tmuxAbp9hRyEx
wGmfEZaB3ty3muJAbJBQ8QKBgDdICMamQXaugu1IGhLKYk/Pu/4kbTeGzjYPevLs
Hex6rDkHaOBGJWd2Vu67iUk9I9JR66ViI73XurVMgKBV9FTjbDsDvVOQTiDdSDK6
zsr1D3VclGdEeeP1xdjgFGyrsnuOXPSQ/HXtgyTmVCENjBCaRlxtI6BGSGAzciLs
HZUBAoGAH48bSR4Bu1HPLZj4L2gXOdxLJ0Nx9+H5CRgvc/1gEzOXscS9FNtxU/a8
0UKdbzHgNProdnXY+EYZRVktng1aDlEFxPekA5gUTL0wxCI6u/T3Dd3uWhe8Mp7z
Fu2779Vsa/NY6r1IN3Mn77ZBOAFNvae2qcC3r8EOfm1sAn5uomM=',
    fingerprint            => '30:54:04:ba:d5:c2:62:09:9e:bd:b1:e3:b0:03:01:4d');
END;
/

SELECT owner, credential_name FROM dba_credentials ;

begin
DBMS_CLOUD.DROP_CREDENTIAL ( 'centroid_30');
end;
/

--Test Credentials

set serveroutput on
declare
  l_type_status  PLS_INTEGER;
  response       dbms_cloud_oci_obs_object_storage_get_namespace_response_t;
  l_json_obj     json_object_t;
  l_keys         json_key_list;
begin
response := dbms_cloud_oci_obs_object_storage.get_namespace(credential_name => 'hidoci', region => 'us-ashburn-1');
dbms_output.put_line(response.status_code);
dbms_output.put_line(response.response_body);
end;
/

--List announcements
--make sure to all the types defined before hand. https://docs.oracle.com/en-us/iaas/pl-sql-sdk/doc/dbms_cloud_oci_as_announcement_t.html

set serveroutput on
declare
  l_type_status  PLS_INTEGER;
  resp_body dbms_cloud_oci_as_announcement_announcements_collection_t;
  response       dbms_cloud_oci_as_announcement_list_announcements_response_t;
  l_json_obj     json_object_t;
  l_keys         json_key_list;
begin

  response := DBMS_CLOUD_OCI_AS_ANNOUNCEMENT.list_announcements (
  compartment_id =>'ocid1.tenancy.oc1..aaaaaaaacr2kimui4s25ck7zeyjrqvfc3bpyjlr73hjrydgukzwcwqctbqra',
  credential_name => 'cen2020',
  region => 'us-ashburn-1' );
  
  resp_body := response.response_body;
  
dbms_output.put_line(response.status_code);
dbms_output.put_line(resp_body.items);
end;
/

-- DB link in reportingDB going to adwfree
CREATE  DATABASE LINK adwfree 
CONNECT TO admin IDENTIFIED BY "M33yr##6HCXu72rvj"
USING 'adwfree_high';

-- DB link in adwfree going to reportingDB
-- turned on tcps/ssl on reportingDB. Vir did that first
--https://blogs.oracle.com/datawarehousing/how-to-create-a-database-link-from-an-autonomous-data-warehouse-to-a-database-cloud-service-instance-v2

create directory wallet_dir as 'walletdir';

--using the object storage creds created above for cen2020 tenancy	
BEGIN
  DBMS_CLOUD.GET_OBJECT(
    credential_name => 'CEN2020',
    object_uri => 'https://objectstorage.us-ashburn-1.oraclecloud.com/p/spWX-02rO4FTlY0Z9fQD9iuMgbE7We9HEB2zQ7OxE4Z9vn7dIvtZTCIq6MpimMes/n/id3nodyt06el/b/testpublic/o/reportingDB_walletcwallet.sso',
    directory_name => 'WALLET_DIR'); 
END;
/    

BEGIN
  DBMS_CLOUD.CREATE_CREDENTIAL(
    credential_name => 'DBCS_LINK_CRED',
    username => 'USAGE',
    password => 'PaSsw0rd2');
END;
/    

BEGIN
  DBMS_CLOUD_ADMIN.CREATE_DATABASE_LINK(
    db_link_name => 'reportingdb', 
    hostname => '150.136.84.44', 
    port => '1521',
    service_name => 'orclpdb1',
    ssl_server_cert_dn => 'CN=dbcs',
    credential_name => 'DBCS_LINK_CRED',
    directory_name => 'WALLET_DIR');
END;
/   
/*
CREATE  DATABASE LINK reportingDB 
CONNECT TO usage IDENTIFIED BY "PaSsw0rd2"
USING '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=150.136.84.44)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orclpdb1)))';
*/

---Ability to send email from autonomous DB
https://docs.oracle.com/en/cloud/paas/autonomous-database/adbsa/smtp-send-mail.html#GUID-CBBA9AD1-2FE2-418D-B155-CAB7C61E176E
Public Endpoint: smtp.email.us-ashburn-1.oci.oraclecloud.com
SMTP Ports: 25, 587

username: ocid1.user.oc1..aaaaaaaatat3hi6z37poabcge6cyxqac7fpwsc2xbraui63flr6qqngyw7oa@ocid1.tenancy.oc1..aaaaaaaacr2kimui4s25ck7zeyjrqvfc3bpyjlr73hjrydgukzwcwqctbqra.tb.com
password: cVogMCTd}o#iSgj4F.5]

BEGIN
  -- Allow SMTP access for user ADMIN
  DBMS_NETWORK_ACL_ADMIN.APPEND_HOST_ACE(
    host => 'smtp.email.us-ashburn-1.oci.oraclecloud.com',
    lower_port => 587,
    upper_port => 587,
    ace => xs$ace_type(privilege_list => xs$name_list('SMTP'),
                       principal_name => 'ADMIN',
                       principal_type => xs_acl.ptype_db));
END;
/


CREATE OR REPLACE PROCEDURE SEND_MAIL (
  msg_to varchar2,
  msg_subject varchar2,
  msg_text varchar2 ) 
IS

  mail_conn utl_smtp.connection;
  username varchar2(1000):= 'ocid1.user.oc1..aaaaaaaatat3hi6z37poabcge6cyxqac7fpwsc2xbraui63flr6qqngyw7oa@ocid1.tenancy.oc1..aaaaaaaacr2kimui4s25ck7zeyjrqvfc3bpyjlr73hjrydgukzwcwqctbqra.tb.com';
  passwd varchar2(50):= 'cVogMCTd}o#iSgj4F.5]';
  msg_from varchar2(50) := 'cloudoptimizer@centroid.com';
  mailhost VARCHAR2(50) := 'smtp.email.us-ashburn-1.oci.oraclecloud.com';

BEGIN
  mail_conn := UTL_smtp.open_connection(mailhost, 587);
  utl_smtp.starttls(mail_conn);
  
  UTL_SMTP.AUTH(mail_conn, username, passwd, schemes => 'PLAIN');
  
  utl_smtp.mail(mail_conn, msg_from);
  utl_smtp.rcpt(mail_conn, msg_to);
  
  UTL_smtp.open_data(mail_conn);
 
  UTL_SMTP.write_data(mail_conn, 'Date: ' || TO_CHAR(SYSDATE, 'DD-MON-YYYY HH24:MI:SS') || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'To: ' || msg_to || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'From: ' || msg_from || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Subject: ' || msg_subject || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Reply-To: ' || msg_to || UTL_TCP.crlf || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, msg_text || UTL_TCP.crlf || UTL_TCP.crlf);
  
  UTL_smtp.close_data(mail_conn);
  UTL_smtp.quit(mail_conn);

EXCEPTION
  WHEN UTL_smtp.transient_error OR UTL_smtp.permanent_error THEN
    UTL_smtp.quit(mail_conn);
    dbms_output.put_line(sqlerrm);
  WHEN OTHERS THEN
    UTL_smtp.quit(mail_conn);
    dbms_output.put_line(sqlerrm);
END;
/


execute send_mail('sridhar.doki@centroid.com, navdeep.saini@centroid.com', 'Email from Oracle Autonomous Database', 'Sent using UTL_SMTP - Navdeep');

---Invoke Function from adwfree
SET SERVEROUTPUT ON
  DECLARE
    resp DBMS_CLOUD_TYPES.resp;
  BEGIN
--HTTP POST Request
    resp := DBMS_CLOUD.send_request(
               credential_name => 'CEN2020',
               uri => 'https://taabzgw4kna.us-ashburn-1.functions.oci.oraclecloud.com/20181201/functions/ocid1.fnfunc.oc1.iad.aaaaaaaaabmh5ntcbgwdzfbdwvgrk3hjqdwzrgtwvwa7a27pwi7iazgjg2qq/actions/invoke',
               method => DBMS_CLOUD.METHOD_POST,
              body => UTL_RAW.cast_to_raw('{"command":"start", "instance_ocid":"ocid1.instance.oc1.iad.anuwcljt6rfcedyc62w6k7ouegeu5utiuom7gacouiau6qk2f6zryobi33vq"}')
            );

    DBMS_OUTPUT.put_line('Body: ' || '------------' || CHR(10) ||
  DBMS_CLOUD.get_response_text(resp) || CHR(10));

-- Response Status Code
  DBMS_OUTPUT.put_line('Status Code: ' || CHR(10) || '------------' || CHR(10) ||
  DBMS_CLOUD.get_response_status_code(resp));
END;
/ 




