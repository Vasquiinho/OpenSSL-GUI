import subprocess
import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Aba_Testes:
    def __init__(self, builder):
        file_chooser_btn = builder.get_object("filechooser")
        file_chooser_btn.connect("file-set", self.__file_set)

        criar_dir_mount_point = subprocess.Popen(["mkdir", os.path.expanduser('~/mount_gui_openssl_sftp')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = criar_dir_mount_point.communicate()

        print(stdout)
        print(stderr)

        password = subprocess.Popen(["echo", "utilizador"], stdout=subprocess.PIPE)
        montar = subprocess.Popen(["sshfs", "-o", "password_stdin", "-p 5022", "utilizador@192.168.1.20:/home", os.path.expanduser('~/mount_gui_openssl_sftp')], stdin=password.stdout ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = montar.communicate()

        global sftp_montado
        sftp_montado = True

        print(stdout)
        print(stderr)

    def __file_set(self, fs):
        print(fs.get_filename())