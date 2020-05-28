# GUI_OpenSSL
Repository for the Miniproject of Systems And Network Security


This is a simple GUI for OpenSSL developed in Python for Ubuntu
Developed in Ubuntu 20.04 and Python 3.8.

Still in development.

Do not run main.py with sudo if you want to use ssh. sshfs will not work properly. You can run with sudo, but all filepickers will be replaced with textinputs, and you'll need to write the paths by hand. SSHFS is used to mount the remote system filesystem so that the user can use the filechoosers inputs to select the files in the remote system via gui.

### Functionality soo far
- Dgst Operations
  - Input from file or text
  - Output formats (hex, binary and coreutils format)
  - Output to file, to directory or to a popup with a textarea showing the result
  - Some sign and verify options (-sign, -verify, -prverify, -signature)
  - Other Options (-c, -d, -hmac, -non-fips-allow, -fips-fingerprint, -rand (only one file))
- Rand
  - Insert a number in a input box
  - Output formats (default - binary?, hex and base64)
  - Output do file, to directory or to a popup with a textarea showing the result
  - Use and select a rand file (-rand)
  - Write a rand file (-writerand) to a file or to directory

***Important note regarding functionality implemented:** Some of the options of the different OpenSSL commands may require other options. This applications will not check most of them, because i don't know what command options require other options. If the application fails to execute with the configuration the user inserts, a popup will appear with the error message returned by openssl*

***Also:** I'm new to OpenSSL, expect some missing validations (like specific file types needed for some commands, ...) or hints how to use the application*



(reminder to complete readme sometime in the future)

Feel free to use and edit this project for your own needs.
