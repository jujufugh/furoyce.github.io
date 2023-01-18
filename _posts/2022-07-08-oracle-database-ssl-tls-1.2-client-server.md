---
title: "Configure TLS 1.2 network encryption for your Oracle database"
date: 2022-12-07
last_modified_at: 2023-01-09T16:20:02-05:00
categories:
  - Blog
tags:
  - Oracle
  - TLS 1.2
  - OCI
---

The page is working-in-progress.

# Configure TLS 1.2 network encryption for Oracle database

## Synoposis
Secure Socket Layer and Transport Layer Security are transport protocols which rely on Public Key Infrastructure to create an encrypted link and transmit the packets over the network. In order to have the SSL/TLS negotiation we need a private key and a public key. The private key is created when the certificate request is generated in the wallet and the public key is provided with the signed certificate.  The encryption is performed with the public key and the decryption is performed with the private key. Currently the Oracle SSL layer is using third party PKI libraries. It is using the SSL certificates stored in a wallet(certificate keystore) and encryption algorithms to create a secure channel between the client  and the server(databases, webservices, mail servers,etc.). With SSL encryption sensitive information can be transmitted securely.
 
The SSL certificates used by an Oracle client/database can be self signed with orapki or they can be provided by a 3rd party certification authority.  Depending on the database version the following protocols are available: SSL 1.0/2.0/3.0 and TLS1.0 for 11g, TLS 1.0/1.1/1,2 for 12c. The protocols TLS 1.1/1.2 are implemented in 11.2.0.4 by the usage of MES bundle patches.

## How doe SSL/TLS works? 
The following steps take place during a standard SSL handshake when RSA key exchange algorithm is used:
 
1. Client Hello
2. Information that the server needs to communicate with the client using SSL
3. Including SSL version number, cipher settings, session-specific data.
4. Server Hello                                                                                                                                                
5.  Information that the client needs to communicate with the server using SSL.
6.  Including SSL version number, cipher settings, session-specific data.
7.  Including Server’s Certificate (Public Key)
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

## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/furoyce/furoyce.github.io/edit/main/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/furoyce/furoyce.github.io/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
