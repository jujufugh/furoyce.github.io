---
title: "Configure TLS 1.2 network encryption for your Oracle database"
date: 2022-12-07
last_modified_at: 2023-01-09T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle 19c
  - TLS 1.2
  - OCI
---

## Synoposis
Network encryption is an important security measure that provides encryption for data transmitted between the client and the database. It becomes even critical for companies going through cloud transformation journey. It helps protect data from being accessed by unauthorized users, and it helps keep sensitive information, such as credit card numbers, secure. Additionally, enable SSL/TLS 1.2 connection can help meet compliance requirements, such as the Health Insurance Portability and Accountability Act (HIPPA), Payment Card Industry Data Security Standard (PCI DSS), etc. 

## References
- Primary Note For SSL/TLS (Doc ID 2229775.1)
- Configuring SSL for Client Authentication and Encryption With Self Signed Certificates On Both Ends Using orapki (Doc ID 401251.1)
- Step by Step Guide To Configure SSL Authentication (Doc ID 736510.1)
- Tnsping To A TCPS Endpoint Fails With Ora-12560 (Doc ID 2198446.1)
- https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-secure-sockets-layer-authentication.html#GUID-6AD89576-526F-4D6B-A539-ADF4B840819F 

## How doe SSL/TLS works? 

Secure Socket Layer and Transport Layer Security are transport protocols which rely on Public Key Infrastructure to create an encrypted link and transmit the packets over the network. In order to have the SSL/TLS negotiation we need a private key and a public key. The private key is created when the certificate request is generated in the wallet and the public key is provided with the signed certificate.  The encryption is performed with the public key and the decryption is performed with the private key. Currently the Oracle SSL layer is using third party PKI libraries. It is using the SSL certificates stored in a wallet(certificate keystore) and encryption algorithms to create a secure channel between the client  and the server(databases, webservices, mail servers,etc.). With SSL encryption sensitive information can be transmitted securely.
 
The SSL certificates used by an Oracle client/database can be self signed with orapki or they can be provided by a 3rd party certification authority.  Depending on the database version the following protocols are available: SSL 1.0/2.0/3.0 and TLS1.0 for 11g, TLS 1.0/1.1/1,2 for 12c. The protocols TLS 1.1/1.2 are implemented in 11.2.0.4 by the usage of MES bundle patches.

The following steps take place during a standard SSL handshake when RSA key exchange algorithm is used:

```
1. Client Hello
2. Information that the server needs to communicate with the client using SSL
3. Including SSL version number, cipher settings, session-specific data.
4. Server Hello                                               
5. Information that the client needs to communicate with the server using SSL.
6. Including SSL version number, cipher settings, session-specific data.
7. Including Server’s Certificate (Public Key)
8. Authentication and Pre-Primary Secret
9. Client authenticates the server certificate. (e.g. Common Name / Date / Issuer)
10. Client (depending on the cipher) creates the pre-Primary secret for the session
11. Encrypts with the server's public key and sends the encrypted pre-Primary secret to the server.
12. Decryption and Primary Secret
13. Server uses its private key to decrypt the pre-Primary secret
14. Both Server and Client perform steps to generate the Primary secret with the agreed cipher.
15. Generate Session Keys
16.  Both the client and the server use the Primary secret to generate the session keys, which are symmetric keys used to encrypt and decrypt information exchanged during the SSL session
17. Encryption with Session Key
18.  Both client and server exchange messages to inform that future messages will be encrypted.
```
 
<img src='/images/posts/2023-01-19/e197a6469c0d6874936092c3990e5be711b54883ee1b96712bc8fa95bddb5205.png'/>


## Environment
* Oracle Database Server: 19c RU4
* Oracle Database Client: 19c RU4
* SQL Developer on MacOSX: 21.2
* Oracle Database Instant Client: 19c RU8

## Option 1: Create Server Self-signed Certificate
- Create Oracle Wallet on the server

```
$ mkdir /u01/app/oracle/wallet

$ orapki wallet create -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -auto_login
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

- Create a self-signed certificate

```
$ orapki wallet add -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -dn "CN=`hostname`" -keysize 1024 -self_signed -validity 3650
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

- Verify the wallet contains newly created self-signed certificate

```
$ orapki wallet display -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Requested Certificates:
User Certificates:
Subject:        CN=instance-20220726-0920
Trusted Certificates:
Subject:        CN=instance-20220726-0920

$ ls -ltr wallet
total 8
-rw-------. 1 oracle oinstall    0 Aug  4 14:23 ewallet.p12.lck
-rw-------. 1 oracle oinstall    0 Aug  4 14:23 cwallet.sso.lck
-rw-------. 1 oracle oinstall 2480 Aug  4 14:27 ewallet.p12
-rw-------. 1 oracle oinstall 2525 Aug  4 14:27 cwallet.sso

$
```

- Export the certificate for client wallet

```
$ orapki wallet export -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -dn "CN=`hostname`" -cert /home/oracle/`hostname`-cert.crt
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$ ls -ltr /home/oracle/instance*
-rw-------. 1 oracle oinstall 667 Aug  4 14:28 /home/oracle/instance-20220726-0920-cert.crt

$
```

## Create Client wallet and Self-Signed Ceritificate
- Create wallet folder

```
$ mkdir -p /u01/app/oracle/wallet

$ orapki wallet create -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -auto_login
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

- Create a Self-Signed certificate into the wallet

```
$ orapki wallet add -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -dn "CN=`hostname`" -keysize 1024 -self_signed -validity 3650
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

- Validate the wallet content

```
$ orapki wallet display -wallet "/u01/app/oracle/wallet"
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Requested Certificates:
User Certificates:
Subject:        CN=instance-20220804-1205
Trusted Certificates:
Subject:        CN=instance-20220804-1205

$
```

- Export the Client Wallet into a certificate file

```
$ orapki wallet export -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -dn "CN=`hostname`" -cert /home/oracle/`hostname`-cert.crt
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

[oracle@instance-20220804-1205 ~]$ ls -ltr /home/oracle/*crt
-rw-------.  1 oracle oinstall  667 Aug  4 18:28 instance-20220804-1205-cert.crt

$
```

## Exchange Server and Client Certificates
- scp the server certificate to client, and **vice versa**
- Import the client certificate into server side Oracle Wallet


```
$ orapki wallet add -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -trusted_cert -cert /home/oracle/instance-20220726-0920-cert.crt
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

- Import the server certificate into client side Oracle Wallet


```
$ orapki wallet add -wallet "/u01/app/oracle/wallet" -pwd WalletPasswd123 -trusted_cert -cert /home/oracle/instance-20220804-1205-cert.crt
Oracle PKI Tool Release 19.0.0.0.0 - Production
Version 19.4.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

$
```

## Option 2: Create Certificate Signing Request and get it signed by Certificate Authority
**How certificate chains work**
- A certificate chain is an ordered list of certificates, containing an SSL/TLS Certificate and Certificate Authority (CA) Certificates, that enable the receiver to verify that the sender and all CA's are trustworthy. 
- The chain or path begins with the SSL/TLS certificate, and each certificate in the chain is signed by the entity identified by the next certificate in the chain.
{: .notice--info}

**What is the Root CA Certificate?**
The chain terminates with a Root CA Certificate. The Root CA Certificate is always signed by the CA itself. The signatures of all certificates in the chain must be verified up to the Root CA Certificate.
{: .notice--info}

**What is an Intermediate(Sub) Certificate?**
- Any certificate that sits between the SSL/TLS Certificate and the Root Certificate is called a chain or Intermediate Certificate. 
- The Intermediate Certificate is the signer/issuer of the SSL/TLS Certificate. 
- The Root CA Certificate is the signer/issuer of the Intermediate Certificate. 
- If the Intermediate Certificate is not installed on the server (where the SSL/TLS certificate is installed) it may prevent some browsers, mobile devices, applications, etc. from trusting the SSL/TLS certificate. 
- In order to make the SSL/TLS certificate compatible with all clients, it is necessary that the Intermediate Certificate be installed.
{: .notice--info}

<img src='/images/posts/2023-01-19/Figure_CA_Chains.jpg'/>

You can use oracle orapki or keystore to secure trust certificates and private keys. Creat ethe keystore if not using already, else skip the step. 
{: .notice--primary}

- Create the Oracle Wallet

```
mkdir -p /home/oraclt/admin/wallet

orapki wallet create -wallet /home/oraclt/admin/wallet -auto_login -pwd *******
```

- Create the certificate signing request
```
orapki wallet add -dn “CN=<HOSTNAME>,OU=….,O=….” -wallet /home/oraclt/admin/wallet -pwd <PASSWORD>

orapki wallet export -wallet "/home/oraclt/admin/wallet" -dn “CN=<HOSTNAME>,OU=….,O=….” -request /home/oraclt/admin/HOSTNAME.req

```

- Submit the Certificate Signing Request

```
Once the certificate signing request has been created, you must submit it to a certificate authority for certification. You can obtain an SSL certificate from a commercial or public certificate authority or from an internal CA server if your organization uses one. 

    Comodo (www.comodo.com) 
    Digicert (www.websecurity.digicert.com/ssl-certificate)
    GeoTrust, Inc. (www.geotrust.com)
    GoDaddy SSL (https://www.godaddy.com/web-security/ssl-certificate) 
```

- Import Root and Intermediate Certificates as trusted certificates

```
orapki wallet add -wallet "/home/oraclt/admin/wallet" -trusted_cert -cert /home/oraclt/admin/root-ca.cer -pwd ******
orapki wallet add -wallet "/home/oraclt/admin/wallet" -trusted_cert -cert /home/oraclt/admin/sub.cer -pwd ******
```

- Import signed user certificate as user certificate

```
orapki wallet add -wallet "/home/oraclt/admin/wallet" -user_cert -cert /home/oraclt/admin/`hostname`.crt -pwd ******
```

## Server side Certificate Configuration

- Add wallet configuration into sqlnet.ora

```
$ cat sqlnet.ora
# sqlnet.ora Network Configuration File: /u01/app/oracle/product/19c/dbhome_1/network/admin/sqlnet.ora
# Generated by Oracle configuration tools.

NAMES.DIRECTORY_PATH= (TNSNAMES, EZCONNECT)

WALLET_LOCATION =
   (SOURCE =
     (METHOD = FILE)
     (METHOD_DATA =
       (DIRECTORY = /u01/app/oracle/wallet)
     )
   )

SSL_VERSION = 1.2
SSL_CLIENT_AUTHENTICATION = FALSE
```

- Add SSL/TLS configuration into listener.ora

```
$ cat listener.ora
# listener.ora Network Configuration File: /u01/app/oracle/product/19c/dbhome_1/network/admin/listener.ora
# Generated by Oracle configuration tools.

SSL_CLIENT_AUTHENTICATION = FALSE
SSL_VERSION = 1.2

WALLET_LOCATION =
  (SOURCE =
    (METHOD = FILE)
    (METHOD_DATA =
      (DIRECTORY = /u01/app/oracle/wallet)
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = instance-20220726-0920.xxxxxx.oraclevcn.com)(PORT = 1521))
      (ADDRESS = (PROTOCOL = TCPS)(HOST = instance-20220726-0920.xxxxxx.oraclevcn.com)(PORT = 1621))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )
```

- Restart your listener

```
lsnrctl stop
lsnrctl start
```

## Client side Certificate Configuration

- Add wallet configuration into sqlnet.ora

```
$ cat sqlnet.ora
# sqlnet.ora Network Configuration File: /u01/app/oracle/product/19c/dbhome_1/network/admin/sqlnet.ora
# Generated by Oracle configuration tools.

NAMES.DIRECTORY_PATH= (TNSNAMES, EZCONNECT)

SSL_CLIENT_AUTHENTICATION = FALSE
SSL_VERSION = 1.2

WALLET_LOCATION =
  (SOURCE =
    (METHOD = FILE)
    (METHOD_DATA =
      (DIRECTORY = /u01/app/oracle/wallet)
    )
  )

TNSPING.TRACE_DIRECTORY = /home/oracle
TNSPING.TRACE_LEVEL = support

$
```

- Add TCPs connection string into tnsnames.ora 

```
orclpdbins1_tls =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCPS)(HOST = instance-20220726-0920.xxxxxx.oraclevcn.com)(PORT = 1621))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orclpdb)
    )
  )

$
```

- Test the connection

```
[oracle@instance-20220804-1205 admin]$ tnsping orclpdbins1_tls

TNS Ping Utility for Linux: Version 19.0.0.0.0 - Production on 04-AUG-2022 18:55:59

Copyright (c) 1997, 2021, Oracle.  All rights reserved.

Used parameter files:
/u01/app/oracle/product/19c/dbhome_1/network/admin/sqlnet.ora


Used TNSNAMES adapter to resolve the alias
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCPS)(HOST = xxx.xxx.xxx.xxx)(PORT = 1621)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))
OK (40 msec)

$

$ sqlplus hr/xxxxxxxx@orclpdbins1_tls

SQL*Plus: Release 19.0.0.0.0 - Production on Thu Jan 19 19:46:47 2023
Version 19.14.0.0.0

Copyright (c) 1982, 2021, Oracle.  All rights reserved.

Last Successful login time: Fri Dec 02 2022 19:07:29 +00:00

Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.14.0.0.0

SQL> select sys_context('userenv','network_protocol') from dual;

SYS_CONTEXT('USERENV','NETWORK_PROTOCOL')
--------------------------------------------------------------------------------
tcps

$
```

**Note:** As you can see the session context here, we are connecting to the database server via TCPS through the SSL/TLS 1.2 tunnel. 

## What if you want to setup the SSL/TLS 1.2 connection from your MacOS? 
Please check out the post: [Create Oracle Wallet and configure SQL Developer to non-default TNS_ADMIN on MacOS.md](#)


