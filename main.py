#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import sys
import os
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# -- IMPORTAR POPUPS. FECHAR APLICAÇÃO SE NÃO CONSEGUIR IMPORTAR
try:
    from popup_erro import Popup_Erro_Class
    if "popup_erro" not in sys.modules:
        print("File 'popup_erro' missing! Place this in the same folder as main.py")
except Exception as e:
    print("File 'popup_erro' is missing or not loaded properly!")
    print(e)
    exit(1)

try:
    from popup_resultado import Popup_Resultado_Class
    if "popup_resultado" not in sys.modules:
        print("File 'popup_resultado' missing! Place this in the same folder as main.py")
except Exception as e:
    print("File 'popup_resultado' is missing or not loaded properly!")
    print(e)
    exit(1)




sftp_montado = True


modulos_necessarios = ["subprocess", "os", "sys", "gi"]

for modulo in modulos_necessarios:
    if modulo not in sys.modules:
        print("Required module '" + modulo + "' missing!")
    else:
        print("Required Module Found: " + modulo)


# -- verificar se existe uma instalação do openssl no sistema
try:
    result = subprocess.Popen(["openssl", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = result.communicate()

    if(result.returncode != 0):
        Popup_Erro_Class("Warning", "OpenSSL not found in the system! This application will only work if you connect, via ssh, to a system with openssl installed!", "OpenSSL not found in the system!")

except FileNotFoundError as erro:
    Popup_Erro_Class("Warning", "OpenSSL not found in the system! This application will only work if you connect, via ssh, to a system with openssl installed!", "OpenSSL not found in the system!")



# -- QUANDO FIZER PARTE SSH, VERIFICAR SE OPEN SSL E SSH ESTÂO INSTALADOS
# -- VERIFICAR OPENSSL NO SYSTEMA ONDE FAZ LOGIN

# -- verifica sshfs, para montar sftp para os filechoosers
try:
    result = subprocess.Popen(["sshfs", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = result.communicate()

    if(result.returncode != 0):
        Popup_Erro_Class("Warning", "SSHFS not found in the system! You won't be able to use the filechoosers to select files in remote systems", "SSHFS not found in the system!")

except FileNotFoundError as erro:
    Popup_Erro_Class("Warning", "SSHFS not found in the system! You won't be able to use the filechoosers to select files in remote systems", "SSHFS not found in the system!")



# -- INICIALIZAR GUI
builder = Gtk.Builder()
builder.add_from_file("GUI/main.glade")

# -- Importar e Iniciar classes relacionadas com as abas da stack. Se em falta, desativar abas onde são necessárias
# -- -- aba_checksum.py
try:
    from aba_digest import Aba_Digest
    if "aba_digest" not in sys.modules:
        print("File 'aba_digest' missing! Place this in the same folder as main.py")
        print("Digest options have been disabled!")
        builder.get_object("aba_digest").set_sensitive(False)
    else:
        Aba_Digest(builder)
except Exception as e:
    print("File 'aba_digest' is missing or not loaded properly!")
    print("Digest options have been disabled!")
    builder.get_object("aba_digest").set_sensitive(False)
    print(e)


# -- -- aba_testes.py
try:
    from aba_testes import Aba_Testes
    if "aba_testes" not in sys.modules:
        print("File 'aba_testes' missing! Place this in the same folder as main.py")
        print("Testes options have been disabled!")
        builder.get_object("aba_testes").set_sensitive(False)
    else:
        Aba_Testes(builder)
except Exception as e:
    print("File 'aba_testes' is missing or not loaded properly!")
    print("Testes options have been disabled!")
    builder.get_object("aba_testes").set_sensitive(False)
    print(e)




#ournewbutton = builder.get_object("btn")
#ournewbutton.set_label("Hello, World!")

window = builder.get_object("base")


def terminar_programa(*args):
    local_mount = os.path.expanduser('~/mount_gui_openssl_sftp')
    global sftp_montado
    if 'sftp_montado' not in globals():
        sftp_montado = False
    if sftp_montado:
        desmontar = subprocess.Popen(["fusermount", "-u", local_mount],stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = desmontar.communicate()

        print("Unmounting the sftp mounted filesystem")

        if(desmontar.returncode != 0):
            print("Unable to unmount the system")
            Popup_Erro_Class("Warning", "Unable to unmount the sftp of the remote system", "A problem ocurred trying to unmount the sftp filesystem created for the ssh user provided!\nMount location: " + local_mount + "\n" + stderr, True)
        else:
            Gtk.main_quit
            exit(0)
    else:
        Gtk.main_quit
        exit(0)

window.connect("delete-event", terminar_programa)
window.show_all()
Gtk.main()