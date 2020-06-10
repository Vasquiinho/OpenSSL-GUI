# GUI_OpenSSL

This is a simple GUI for OpenSSL developed in Python for Ubuntu
Developed in Ubuntu 20.04 and Python 3.8.

![](https://raw.githubusercontent.com/Vasquiinho/GUI_OpenSSL/master/Image/apresentacao.PNG | width=600)

### Functionality
- Req Options (Request Certificate or Generate Self-Signed Certificate)
  - Set Subject Information
  - Set Input Settings (-in, -inform, -passin, -config)
  - Key Settings (-keyform, -key, -keyout, -pubkey, -new, -nodes, -passout)
  - x509 options, and set x509 extensions (-x509, -days, -serialno, -addext (dynamic table for selection of extensions))
  - Output to file, to folder, or view in a popup window, and select output type (-outform)
  - Rand file usage allowed and possibility to generate a rand file (writerand) to a sepecified file or location
  - Other Options (-subject, -text, -noout, -modulus, -verify, -digest, -precert, -utf8, -batch)
- Enc Options (symmetric cipher routines)
  - Input from file or textarea
  - Output to text in a popup, file or file in folder
  - Encrypt, Decrypt, also for Base64
  - Cipher And Digest selection
  - Password, key, iv, salt and number of iterations customizable
  - Rand file usage allowed and possibility to generate a rand file (writerand) to a sepecified file or location
  - Other options: (-nopad, -pbkdf2, -A, -p, -P, -bufsize, -none, -z)
- Dgst Options (perform digest operations)
  - Input from file or text
  - Output formats (hex, binary and coreutils format)
  - Output to file, to directory or to a popup with a textarea showing the result
  - Some sign and verify options (-sign, -verify, -prverify, -signature)
  - Rand file usage allowed
  - Other Options (-c, -d, -hmac, -non-fips-allow, -fips-fingerprint)
- Rand Options (generate pseudo-random bytes)
  - Insert a number in a input box
  - Output formats (default - binary?, hex and base64)
  - Output do file, to directory or to a popup with a textarea showing the result
  - Use and select a rand file (-rand)
  - Write a rand file (-writerand) to a file or to directory
- SSH Connection to server to execute commands
  - Server filesystem is also mounted so user can easily select files on the server
  - When SSH is connected in the application, all openssl commands are executed on the server


### Requirments / Versions Used in development:
  - Python 3.8.2 64-bit
  - Ubuntu 20.04 LTS
  - Python modules: subprocess, os, sys, gi, paramiko
  - OpenSSL 1.1.1f
  - SSHFS 2.10.0
    - Fuse 2.9.9
    - fusermount 2.9.9
    - FUSE kernel interface 7.9
  
  (Other configurations may work, i didn't test other versions)

*Do not run main.py with sudo if you want to use ssh. SSHFS will not work properly, and because of that SSH connection will not be allowed. SSHFS is used to mount the remote system filesystem so that the user can use the filechoosers inputs to select the files in the remote system via gui.*


***Important note regarding functionality implemented:** Some of the options the users specifies to execute the OpenSSL commands may require other options. This applications will not check most of them, because i don't know what command options require other options (i'm new to openssl). If the application fails to execute with the configuration the user inserts, a popup will appear with the error message returned by openssl*

***Also:** I'm new to OpenSSL, expect some missing validations (like specific file types needed for some commands, ...) or hints how to use the application*

***If the application seems to "hang" for a lot of time, check the python console used to execute the program. It may be asking for some type of password or other specific setting that i didn't verify in code***


---
This application was developed for the Network and Systems Security Curricular Unit of Computer Science and Engineering. This was the first time i worked with Python GTK, Glade, Paramiko and OpenSSL, so expect some "bad practices" in Python code with gtk things, and "most used" features of openssl missing, since i don't have the experience with it to identify what those features are, the commands implemented here were just by checking the docs and some websites found on google.



Feel free to use and edit this project for your own needs.
