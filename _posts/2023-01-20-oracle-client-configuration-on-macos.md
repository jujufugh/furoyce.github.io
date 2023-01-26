---
title: "Configure orapki in Oracle Client on macOS"
date: 2022-07-08
last_modified_at: 2023-01-26T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle Client
  - MacOS
  - orapki
  - mkstore
---

## Background

I recently got a use case to configure SSL/TLS 1.2 network encryption for Oracle Database server, check out the blog post here. During the testing environment configuration, I noticed that Oracle Instant Client for macOS(intel x86) was missing the executable binary for orapki and mkstore. Therefore it posed challenges of creating Oracle Wallet and importing SSL/TLS related certificates. 

### Download Oracle instance client and sqlcl for macOS 
[Download Oracle Client](https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html)
[Download SQLcl](https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/download/)

### Create orapki and mkstore based on SQLcl java library

After researching, I came across [Ottmar Gobrecht](https://ogobrecht.com/posts/2020-07-29-how-to-use-mkstore-and-orapki-with-oracle-instant-client/) and [Andriy Dmytrenko](https://andriydmytrenko.wordpress.com/2013/07/01/using-the-secure-external-password-store-with-instant-client/) blog about creating orapki and mkstore manually.

Inspired by their approach, I created the following executables to use the sqlcl java library oraclepki.jar, osdt_core.jar, osdt_cert.jar. 

- **orapki** 

```bash
#!/bin/bash
# set classpath for orapki - align this to your local SQLcl installation
SQLCL=$(dirname $(which sql))/../lib
CLASSPATH=${SQLCL}/oraclepki.jar:${SQLCL}/osdt_core.jar:${SQLCL}/osdt_cert.jar
# simulate orapki command
java -classpath ${CLASSPATH} oracle.security.pki.textui.OraclePKITextUI "$@"
```

- **mkstore**

```
#!/bin/bash
# set classpath for mkstore - align this to your local SQLcl installation
SQLCL=$(dirname $(which sql))/../lib
CLASSPATH=${SQLCL}/oraclepki.jar:${SQLCL}/osdt_core.jar:${SQLCL}/osdt_cert.jar
# simulate mkstore command
java -classpath ${CLASSPATH} oracle.security.pki.OracleSecretStoreTextUI  "$@"

```

### Testing the utilities

```
# ./orapki
Oracle PKI Tool Release 21.0.0.0.0 - Production
Version 21.0.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

orapki [crl|wallet|cert|help] <-nologo> <-jsafe> <-use_jce> <-use_jce_only> <-fips140_mode>
```

```
# ./mkstore
Oracle Secret Store Tool Release 21.0.0.0.0 - Production
Version 21.0.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

mkstore [-wrl wrl] [-create] [-createSSO] [-createLSSO] [-createALO] [-delete] [-deleteSSO] [-list] [-createEntry alias secret] [-viewEntry alias] [-modifyEntry alias secret] [-deleteEntry alias] [-createCredential connect_string username password] [-listCredential] [-modifyCredential connect_string username password] [-deleteCredential connect_string]  [-createUserCredential map key  <username> password]  [-modifyUserCredential map key username password]  [-deleteUserCredential map key] [-help] [-nologo]
```

### Create Wallet on macOS client

```
# orapki wallet create -wallet "/Users/macos/Downloads/instantclient_19_8/wallet" -pwd xxxxxxxxxxx -auto_login
Oracle PKI Tool Release 21.0.0.0.0 - Production
Version 21.0.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.

#
```

### Import self-signed certificates as trusted_cert

```
# orapki wallet add -wallet "/Users/macos/Downloads/instantclient_19_8/wallet" -pwd xxxxxxxxxxxxx -trusted_cert -cert /Users/macos/instance-20220726-0920-cert.crt
Oracle PKI Tool Release 21.0.0.0.0 - Production
Version 21.0.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Operation is successfully completed.
macos # orapki wallet display -wallet "/Users/macos/Downloads/instantclient_19_8/wallet" -pwd xxxxxxxxxxxxx
Oracle PKI Tool Release 21.0.0.0.0 - Production
Version 21.0.0.0.0
Copyright (c) 2004, 2021, Oracle and/or its affiliates. All rights reserved.

Requested Certificates:
User Certificates:
Subject:        CN=macos-mac
Trusted Certificates:
Subject:        CN=instance-20220726-0920
Subject:        CN=macos-mac
macos #
```

### Configure TNS_ADMIN

```
# env | grep TNS
TNS_ADMIN=/Users/macos/Downloads/instantclient_19_8/network/admin
# cat sqlnet.ora

NAMES.DIRECTORY_PATH= (TNSNAMES, EZCONNECT)

SSL_CLIENT_AUTHENTICATION = FALSE
SSL_VERSION = 1.2

WALLET_LOCATION =
  (SOURCE =
    (METHOD = FILE)
    (METHOD_DATA =
      (DIRECTORY = /Users/macos/Downloads/instantclient_19_8/wallet)
    )
  )

```

### Test the SSL/TLS 1.2 connection between client and database server

```
# sqlplus XX/XXXXXXX@orclpdb_tls

SQL*Plus: Release 19.0.0.0.0 - Production on Thu Aug 4 16:30:05 2022
Version 19.8.0.0.0

Copyright (c) 1982, 2020, Oracle.  All rights reserved.

Last Successful login time: Thu Aug 04 2022 16:28:39 -04:00

Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.14.0.0.0

SQL> select sys_context('userenv','network_protocol') from dual;

SYS_CONTEXT('USERENV','NETWORK_PROTOCOL')
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tcps

SQL> 
```

### (Optional) Configure SQLDeveloper to use Oracle Instant Client and TNS_ADMIN

In order to have Oracle SQLDeveloper can connect to the database using Oracle wallet, we need to configure thick option so it will use the Oracle Instant Client and TNS_ADMIN configuration. 

**thin client** means using SQLDeveloper own jar library to connect to the database
**thick client** means using external Oracle client 

Jeff Smith has a great [blog post](https://www.thatjeffsmith.com/archive/2019/04/sql-developer-19-1-connections-thick-or-thin/) explaining different options in SQLDeveloper to connect to the database via thick or thin client. 

After switching to thick client and point the Oracle Client to our instant client, we are seeing following error

```
Testing the Instant Client located at /Users/macos/Downloads/instantclient_19_8
Testing client directory ... OK
Testing loading Oracle JDBC driver ... OK
Testing checking Oracle JDBC driver version ... OK
  Driver version: 19.8.0.0.0
Testing testing native OCI library load ... Failed:
  Error loading the native OCI library
  The native OCI driver could not be loaded. The system propertyjava.library.path contains the entries from the environment variable DYLD_LIBRARY_PATH. Check it to verify that
  the expected native library directory /Users/macos/Downloads/instantclient_19_8 is present and precedes any other client installations.
  java.library.path = /Users/macos/Library/Java/Extensions:/Library/Java/Extensions:/Network/Library/Java/Extensions:/System/Library/Java/Extensions:/usr/lib/java:.

```

Following Cendy Sint Jago's [post](https://sites.google.com/site/cendysplace/oracle/sql-developer-using-the-thick-client), you need to modify the SQLDeveloper ~/.sqldeveloper/21.4.3/product.conf to fix the **java.library.path** issue within **product.conf**

**Steps:**
- Run SQL Developer:
  * goto Help -> About -> Properties,
  * use the filter box to look for "java.library.path",
  * verify that the path is the same as you entered in product.conf file.
- Open the Preferences dialog and go to Database -> Advanced.
  * Enable "Use Oracle Client",
  * Enable "Use OCI/Thick Client",
  * Click "Configure"
  * Choose "Instant Client" for Client Type,
  * "Browse.." to client location ("/Library/Oracle/InstantClient_12_2"),
  * Click "Test.."


```
# pwd
/Users/macos/.sqldeveloper/21.4.3
# tail product.conf
  #
  # AddVMOption -Xmx800m
  # Add32VMOption -Xmx800m
  # Add64VMOption -Xmx2g

  # ======================
  # Custom Settings
  # ======================
  # OCI Thick Driver
  AddVMOption -Djava.library.path=/Users/macos/Downloads/instantclient_19_8:/Library/Java/Extensions:/Network/Library/Java/Extensions:/System/Library/Java/Extensions:/usr/lib/java:.

```

Run testing again
```

  Testing the Instant Client located at /Users/macos/Downloads/instantclient_19_8
  Testing client directory ... OK
  Testing loading Oracle JDBC driver ... OK
  Testing checking Oracle JDBC driver version ... OK
    Driver version: 19.8.0.0.0
  Testing testing native OCI library load ... OK
  Success!

```

**Additional Read:** [Oracle Database SSL/TLS 1.2 network encryption configuration]({% post_url 2022-07-08-oracle-database-ssl-tls-1.2-client-server %})