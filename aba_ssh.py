import subprocess
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import paramiko

try:
    from popup_erro import Popup_Erro_Class
    if "popup_erro" not in sys.modules:
        print("File 'popup_erro' missing in 'aba_digest.py'! Place this in the same folder as main.py")
except Exception as e:
    print("File 'popup_erro' is missing or not loaded properly in 'aba_digest.py'! Place it in the same folder as main.py")
    print(e)
    exit(1)

try:
    from popup_resultado import Popup_Resultado_Class
    if "popup_resultado" not in sys.modules:
        print("File 'popup_resultado' missing in 'aba_digest.py'! Place this in the same folder as main.py")
except Exception as e:
    print("File 'popup_resultado' is missing or not loaded properly in 'aba_digest.py'! Place it in the same folder as main.py")
    print(e)
    exit(1)

class Aba_SSH:

    builder = None

    def __init__(self, builder, ssh_client):
        self.builder = builder
        self.ssh_client = ssh_client

        servidor='192.168.1.20'
        porta=5022
        utilizador='utilizador'
        password='utilizador'
        ficheiro_chave = None

        cmd='ifconfig' 

        print("A correr...")

        try:
            ssh = self.__conecta_ssh(servidor, porta, utilizador, password, ficheiro_chave)
        except paramiko.BadHostKeyException as e:
            Popup_Erro_Class("Error", "Unable to verify host key", str(e))
            ssh = None
        except paramiko.AuthenticationException as e: 
            Popup_Erro_Class("Error", "SSH Login failed!", str(e))
            ssh = None
        except paramiko.SSHException as e: 
            Popup_Erro_Class("Error", "As unknown SSH error has occurred!", str(e))
            ssh = None
        except TimeoutError as e: 
            Popup_Erro_Class("Error", "Timed Out!", str(e))
            ssh = None
        except Exception as e: 
            Popup_Erro_Class("Error", "As unknown SSH error has occurred!", str(e))
            ssh = None

        if ssh:
            stdin,stdout,stderr=ssh.exec_command(cmd, timeout=5)
            outlines=stdout.readlines()
            resp=''.join(outlines)

            #print(resp)

            # verificar openssl instalado no servidor
            stdin,stdout,stderr=ssh.exec_command("openssl version", timeout=5)
            #outlines=stdout.readlines()
            #resp=''.join(outlines)

            resposta = stdout.readlines()
            erro = stderr.readlines()
            if erro:
                Popup_Erro_Class("Error", "The server doesn't have OpenSSL installed or doesn't have a compatible version of OpenSSL!", "Message from the server:\n" + str(erro[0]))



    # exceptions devem ser verificadas onde se chama esta função
    def __conecta_ssh(self, servidor, porta=22, utilizador=None, password=None, ficheiro_chave=None):
        ssh = None
        if not servidor:
            Popup_Erro_Class("Error", "Server address is required to connect to a remote machine!", "Server Address missing!")
            return None

        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(servidor, porta, utilizador, password, ficheiro_chave, timeout=15)
        
        return ssh


    # documentação aconselha a terminar sempre a ligação quando deixa de ser necessária
    # documentação não diz se lança algo, talvez convenha colocar dentro de um try except
    def __desconecta_ssh(self, cliente_ssh = None):
        if cliente_ssh:
            cliente_ssh.close()



