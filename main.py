#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import sys
import os
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import paramiko


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


sftp_montado = False

modulos_necessarios = ["subprocess", "os", "sys", "gi", "paramiko"]

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


# ------- SSH ---------
ssh_client = None

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

# -- -- aba_ssh.py
try:
    from aba_ssh import Aba_SSH
    if "aba_ssh" not in sys.modules:
        print("File 'aba_ssh' missing! Place this in the same folder as main.py")
        print("Rand options have been disabled!")
        #builder.get_object("aba_ssh").set_sensitive(False)
    else:
        aba_ssh = Aba_SSH(builder, ssh_client)
except Exception as e:
    print("File 'aba_ssh' is missing or not loaded properly!")
    print("Rand options have been disabled!")
    #builder.get_object("aba_ssh").set_sensitive(False)
    print(e)

# -- -- aba_checksum.py
try:
    from aba_digest import Aba_Digest
    if "aba_digest" not in sys.modules:
        print("File 'aba_digest' missing! Place this in the same folder as main.py")
        print("Digest options have been disabled!")
        builder.get_object("aba_digest").set_sensitive(False)
    else:
        Aba_Digest(builder, aba_ssh)
except Exception as e:
    print("File 'aba_digest' is missing or not loaded properly!")
    print("Digest options have been disabled!")
    builder.get_object("aba_digest").set_sensitive(False)
    print(e)

# -- aba testes removed from main.glade !!
# -- -- aba_testes.py
#try:
#    from aba_testes import Aba_Testes
#    if "aba_testes" not in sys.modules:
#        print("File 'aba_testes' missing! Place this in the same folder as main.py")
#        print("Testes options have been disabled!")
#        builder.get_object("aba_testes").set_sensitive(False)
#    else:
#        Aba_Testes(builder)
#except Exception as e:
#    print("File 'aba_testes' is missing or not loaded properly!")
#    print("Testes options have been disabled!")
#    builder.get_object("aba_testes").set_sensitive(False)
#    print(e)

# -- -- aba_rand.py
try:
    from aba_rand import Aba_Rand
    if "aba_rand" not in sys.modules:
        print("File 'aba_rand' missing! Place this in the same folder as main.py")
        print("Rand options have been disabled!")
        builder.get_object("aba_rand").set_sensitive(False)
    else:
        Aba_Rand(builder, aba_ssh)
except Exception as e:
    print("File 'aba_rand' is missing or not loaded properly!")
    print("Rand options have been disabled!")
    builder.get_object("aba_rand").set_sensitive(False)
    print(e)

# -- -- aba_req.py
try:
    from aba_req import Aba_Req
    if "aba_req" not in sys.modules:
        print("File 'aba_req' missing! Place this in the same folder as main.py")
        print("Rand options have been disabled!")
        builder.get_object("aba_req").set_sensitive(False)
    else:
        Aba_Req(builder, aba_ssh)
except Exception as e:
    print("File 'aba_req' is missing or not loaded properly!")
    print("Rand options have been disabled!")
    builder.get_object("aba_req").set_sensitive(False)
    print(e)



window = builder.get_object("base")

def terminar_programa(*args):

    #print(aba_ssh.obter_ssh_client())

    Aba_SSH.desconecta(ssh_client)

    try:
        desmontar = subprocess.Popen(["fusermount", "-u", aba_ssh.obter_local_mount()],stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = desmontar.communicate()

        if(desmontar.returncode != 0):
            print("Unable to unmount the system")
            #Popup_Erro_Class("Warning", "Unable to unmount the sftp of the remote system", "A problem ocurred trying to unmount the sftp filesystem created for the ssh user provided!\nMount location: " + local_mount + "\n" + stderr, True)
        else:
            Gtk.main_quit
            exit(0)
    except:
        print("")
    finally:
        Gtk.main_quit
        exit(0)

window.connect("delete-event", terminar_programa)
window.show_all()
Gtk.main()




