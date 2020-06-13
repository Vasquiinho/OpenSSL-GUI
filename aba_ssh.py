import subprocess
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import paramiko
import os

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
    ssh_local_monta_no_servidor = ""

    ssh_lbl_disconnected = None
    ssh_lbl_connected = None
    ssh_area_server = None
    ssh_input_server = None
    ssh_area_porta = None
    ssh_input_porta = None
    ssh_area_user = None
    ssh_input_username = None
    ssh_area_pass = None
    ssh_input_password = None
    ssh_btn_conetar = None
    ssh_btn_desconetar = None
    ssh_lbl_erro = None


    def __init__(self, builder, ssh_client):
        self.builder = builder
        self.ssh_client = ssh_client

        self.ssh_lbl_disconnected = self.builder.get_object("ssh_lbl_disconnected")
        self.ssh_lbl_connected = self.builder.get_object("ssh_lbl_connected")
        self.ssh_lbl_connected.set_no_show_all(True)
        self.ssh_area_server = self.builder.get_object("ssh_area_server")
        self.ssh_input_server = self.builder.get_object("ssh_input_server")
        self.ssh_area_porta = self.builder.get_object("ssh_area_porta")
        self.ssh_input_porta = self.builder.get_object("ssh_input_porta")
        self.ssh_area_user = self.builder.get_object("ssh_area_user")
        self.ssh_input_username = self.builder.get_object("ssh_input_username")
        self.ssh_area_pass = self.builder.get_object("ssh_area_pass")
        self.ssh_input_password = self.builder.get_object("ssh_input_password")

        self.ssh_btn_conetar = self.builder.get_object("ssh_btn_conetar")
        self.ssh_btn_conetar.connect("released", self.__btn_conetar_released)
        self.ssh_btn_desconetar = self.builder.get_object("ssh_btn_desconetar")
        self.ssh_btn_desconetar.connect("released", self.__btn_desconetar_released)

        self.ssh_lbl_erro = self.builder.get_object("ssh_lbl_erro")
        self.ssh_lbl_erro.set_no_show_all(True)

        self.local_sftp_mount = os.path.expanduser('~/mount_gui_openssl_sftp')


    def obter_ssh_client(self):
        return self.ssh_client

    def obter_local_mount(self):
        return self.local_sftp_mount

    def obter_local_monta_no_servidor(self):
        return self.ssh_local_monta_no_servidor

    def __btn_conetar_released(self, btn):
        self.ssh_lbl_erro.set_visible(False)
        self.ssh_btn_conetar.set_sensitive(False)

        servidor = self.ssh_input_server.get_text()
        porta = str(int(self.ssh_input_porta.get_value()))
        utilizador = self.ssh_input_username.get_text()
        password = self.ssh_input_password.get_text()

        if not servidor or not porta or not utilizador or not password:
            self.ssh_lbl_erro.set_text("Connection information missing...")
            self.ssh_lbl_erro.set_visible(True)
            self.ssh_btn_conetar.set_sensitive(True)
            return
        
        try:
            self.ssh_client = self.__conecta_ssh(servidor, porta, utilizador, password)
        except paramiko.BadHostKeyException as e:
            Popup_Erro_Class("Error", "Unable to verify host key", str(e))
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_client = None
            return
        except paramiko.AuthenticationException as e: 
            Popup_Erro_Class("Error", "SSH Login failed!", str(e))
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_client = None
            return
        except paramiko.SSHException as e: 
            Popup_Erro_Class("Error", "As unknown SSH error has occurred!", str(e))
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_client = None
            return
        except TimeoutError as e: 
            Popup_Erro_Class("Error", "Timed Out!", str(e))
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_client = None
            return
        except Exception as e: 
            print(e)
            Popup_Erro_Class("Error", "As unknown error has occurred!", str(e))
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_client = None
            return
        
        # verificar openssl instalado no servidor
        stdin,stdout,stderr= self.ssh_client.exec_command("openssl version", timeout=5)
        resposta = stdout.readlines()
        erro = stderr.readlines()
        if erro:
            Popup_Erro_Class("Error", "The server doesn't have OpenSSL installed or doesn't have a compatible version of OpenSSL!", "Message from the server:\n" + str(erro[0]))
            self.__desconecta_ssh(self.ssh_client)
            self.ssh_btn_conetar.set_sensitive(True)
            return

        if self.ssh_client:
            
            # tenta montar sistema de ficheiros do servidor para poder fazer navegação nos filechoosers
            try:
            	os.mkdir(self.local_sftp_mount)
            except:
            	print("Dir for mount point already exists. Continuing...")
            
            password_subp = subprocess.Popen(["echo", password], stdout=subprocess.PIPE)
            self.ssh_local_monta_no_servidor = "/home/" + utilizador
            montar = subprocess.Popen(["sshfs", "-o", "password_stdin", "-p " + porta, utilizador + "@" + servidor + ":" + self.ssh_local_monta_no_servidor, self.local_sftp_mount], stdin=password_subp.stdout ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = montar.communicate()

            if stderr:
                Popup_Erro_Class("Error", "Unable to mount the remote server filesystem. SSH Login failed. Is sshfs installed on this system?", str(stderr))
                self.__desconecta_ssh(self.ssh_client)
                self.ssh_btn_conetar.set_sensitive(True)
                return
            else:
                global sftp_montado
                sftp_montado = True
                self.ssh_lbl_connected.set_visible(True)
                self.ssh_lbl_disconnected.set_visible(False)

                self.ssh_area_server.set_sensitive(False)
                self.ssh_area_porta.set_sensitive(False)
                self.ssh_area_user.set_sensitive(False)
                self.ssh_area_pass.set_sensitive(False)
                self.ssh_btn_conetar.set_sensitive(False)
                self.ssh_btn_desconetar.set_sensitive(True)
            
    
    def __btn_desconetar_released(self, btn):
        try:
            self.__desconecta_ssh(self.ssh_client)
        except Exception as e: 
            Popup_Erro_Class("Error", "As unknown error has occurred!", str(e))
            self.ssh_client = None
        finally:
            try:
                self.__desmontar_sftp(self.local_sftp_mount)
                global sftp_montado
                sftp_montado = False
            except Exception as e:
                Popup_Erro_Class("Warning", "Unable to unmount the sftp of the remote system", "A problem ocurred trying to unmount the sftp filesystem created for the ssh user provided!\nMount location: " + self.local_sftp_mount + "\n" + str(e))

        if not self.ssh_client:
            self.ssh_area_server.set_sensitive(True)
            self.ssh_area_porta.set_sensitive(True)
            self.ssh_area_user.set_sensitive(True)
            self.ssh_area_pass.set_sensitive(True)
            self.ssh_btn_conetar.set_sensitive(True)
            self.ssh_btn_desconetar.set_sensitive(False)

            self.ssh_lbl_connected.set_visible(False)
            self.ssh_lbl_disconnected.set_visible(True)


    # exceptions devem ser verificadas onde se chama esta função | não usar ficheiro, fusermount não funcionará por alguma razão
    def __conecta_ssh(self, servidor, porta=22, utilizador=None, password=None, ficheiro_chave=None):
        ssh = None
        if not servidor:
            Popup_Erro_Class("Error", "Server address is required to connect to a remote machine!", "Server Address missing!")
            return None

        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(servidor, port=porta, username=utilizador, password=password, key_filename=ficheiro_chave, timeout=15)
        
        return ssh


    # documentação aconselha a terminar sempre a ligação quando deixa de ser necessária
    # documentação não diz se lança algo, talvez convenha colocar dentro de um try except
    def __desconecta_ssh(self, cliente_ssh = None):
        if cliente_ssh:
            cliente_ssh.close()
            self.ssh_client = None

    def desconecta(self, ssh_client=None):
        if ssh_client:
            ssh_client.close()
            ssh_client = None
    

    def __desmontar_sftp(self, local_sftp_mount):
        global sftp_montado
        desmontar = subprocess.Popen(["fusermount", "-u", local_sftp_mount],stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = desmontar.communicate()

        if(desmontar.returncode != 0):
            print("Unable to unmount the system")
            Popup_Erro_Class("Warning", "Unable to unmount the sftp of the remote system", "A problem ocurred trying to unmount the sftp filesystem created for the ssh user provided!\nMount location: " + local_sftp_mount + "\n" + str(stderr), True)
        else:
            sftp_montado = False


