# GUI_OpenSSL
Repository for the Miniproject of Systems And Network Security


This is a simple GUI for OpenSSL developed in Python for Ubuntu
Developed in Ubuntu 20.04 and Python 3.8.

Still in development.

Do not run main.py with sudo if you want to use ssh. sshfs will not work properly. You can run with sudo, but all filepickers will be replaced with textinputs, and you'll need to write the paths by hand. SSHFS is used to mount the remote system filesystem so that the user can use the filechoosers inputs to select the files in the remote system via gui.

###Functionality soo far
- Dgst Operations
  - Input from file or text
  - Output formats (hex, binary and coreutils format)
  - Output to file, to directory or to a popup with a textarea
  - Some sign and verify options (-sign, -verify, -prverify, -signature)
  - Other Options (-hmac, -non-fips-allow, -fips-fingerprint, -rand (only one file))




(reminder to complete readme sometime in the future)

Feel free to use and edit this project for your own needs.
