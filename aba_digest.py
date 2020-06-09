import subprocess
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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

class Aba_Digest:

    aba_ssh = None

    # -- elementos e variáveis
    digest_lbl_erro_config = None
    digest_comando = "openssl dgst"
    digest_algoritmo = ""

    # input
    digest_area_input_ficheiro = None
    digest_area_input_txt = None
    digest_filechooser_input = None
    digest_tipo_input = "ficheiro" # ficheiro, texto

    # output
    digest_filechooser_output = None
    digest_filechooser_pasta_output = None
    digest_area_ficheiro_output = None
    digest_area_pasta_output = None
    digest_output_format = "-hex" # opção do radiobutton default para o output format
    digest_local_output = "texto" # texto (mostra no popup resultado), ficheiro (coloca no ficheiro indicado), pasta (cria um ficheiro na pasta selecionada)
    digest_output_pasta_nome_ficheiro = "gui_openssl_dgst_output"

    # sign/verify
    digest_area_sign = None
    digest_area_verify = None
    digest_area_prverify = None
    digest_area_signature = None
    digest_cb_sign = None
    digest_cb_verify = None
    digest_cb_prverify = None
    digest_cb_signature = None
    digest_filechooser_sign = None
    digest_filechooser_verify = None
    digest_filechooser_prverify = None
    digest_filechooser_signature = None

    # outras opções
    digest_outras_c = None
    digest_outras_d = None
    digest_outras_cb_hmac = None
    digest_outras_non_fips_allow = None
    digest_outras_fips_fingerprint = None
    digest_outras_rand = None
    digest_outras_hmac_key = None
    digest_filechooser_rand = None


    def __init__(self, builder, aba_ssh):
        self.builder = builder
        self.aba_ssh = aba_ssh

        # -- carregar lista de algoritmos e preencher lista
        pedido_lista_algortimos_checksum = subprocess.Popen(["openssl", "list", "-digest-commands"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pedido_lista_algortimos_checksum.communicate()

        cb_checksums_algoritmos = builder.get_object("digest_cb_lista_algoritmos")
        if not stderr:
            for algoritmo in stdout.split():
                cb_checksums_algoritmos.append_text(algoritmo)
        else:
            print("An error as occurred loading digest algorithms")
            Popup_Erro_Class("Error", "An error as occurred loading digest algorithms", stderr)
            cb_checksums_algoritmos.append_text("An error as occurred loading digest algorithms")
            builder.get_object("aba_digest").set_sensitive(False)

        # -- "ouvir" alteração do algoritmo selecionado
        cb_checksums_algoritmos.connect("changed", self.__cb_checksums_algoritmos_changed)

        # -- tipo input pre-definido
        self.digest_tipo_input = "ficheiro"
        self.digest_area_input_ficheiro = self.builder.get_object("digest_area_input_ficheiro")
        self.digest_area_input_ficheiro.set_visible(True)
        
        self.digest_area_input_txt = self.builder.get_object("digest_area_input_txt")
        self.digest_area_input_txt.set_visible(False)
        self.digest_area_input_txt.set_no_show_all(True)

        self.digest_lbl_erro_config = self.builder.get_object("digest_lbl_erro_config")
        self.digest_lbl_erro_config.set_no_show_all(True)

        # -- colocar os radio buttons formato output a "ouvir" quando são trocados 
        self.builder.get_object("digest_rd_output_format_1").connect("toggled", self.__rd_output_on_toggled)
        self.builder.get_object("digest_rd_output_format_2").connect("toggled", self.__rd_output_on_toggled)
        self.builder.get_object("digest_rd_output_format_3").connect("toggled", self.__rd_output_on_toggled)

        # -- associar btn on click ao método criado para isso
        self.builder.get_object("digest_btn_executar").connect("clicked", self.__btn_executar_click)

        # -- colocar os radio buttons tipo input a "ouvir" quando são trocados 
        self.builder.get_object("digest_rd_input_type_1").connect("toggled", self.__rd_input_type_on_toggled)
        self.builder.get_object("digest_rd_input_type_2").connect("toggled", self.__rd_input_type_on_toggled)

        # -- filechooser
        self.digest_filechooser_input = builder.get_object("digest_filechooser_input")
        #self.digest_filechooser_input.connect("file-set", self.__file_set)


        # -- colocar os radio buttons tipo output a "ouvir" quando são trocados 
        self.builder.get_object("digest_rd_output_type_1").connect("toggled", self.__rd_output_type_on_toggled)
        self.builder.get_object("digest_rd_output_type_2").connect("toggled", self.__rd_output_type_on_toggled)
        self.builder.get_object("digest_rd_output_type_3").connect("toggled", self.__rd_output_type_on_toggled)

        # -- esconder input ficheiro para output
        self.digest_filechooser_output = builder.get_object("digest_filechooser_output")
        self.digest_area_ficheiro_output = self.builder.get_object("digest_area_output_ficheiro")
        self.digest_area_ficheiro_output.set_visible(False)
        self.digest_area_ficheiro_output.set_no_show_all(True)

        # -- esconder input pasta para output
        self.digest_filechooser_pasta_output = builder.get_object("digest_filechooser_output_pasta")
        self.digest_area_pasta_output = self.builder.get_object("digest_area_output_pasta")
        self.digest_area_pasta_output.set_visible(False)
        self.digest_area_pasta_output.set_no_show_all(True)
        self.builder.get_object("digest_txt_output_pasta_extra").set_text("A file named '"+ self.digest_output_pasta_nome_ficheiro +"' will be created at the choosen location")

        # -- obter checkboxs sign e verify
        self.digest_cb_sign = builder.get_object("digest_cb_sign")
        self.digest_cb_verify = builder.get_object("digest_cb_verify")
        self.digest_cb_prverify = builder.get_object("digest_cb_prverify")
        self.digest_cb_signature = builder.get_object("digest_cb_signature")
        self.digest_cb_sign.connect("toggled", self.__cb_sign_verify_on_toogled)
        self.digest_cb_verify.connect("toggled", self.__cb_sign_verify_on_toogled)
        self.digest_cb_prverify.connect("toggled", self.__cb_sign_verify_on_toogled)
        self.digest_cb_signature.connect("toggled", self.__cb_sign_verify_on_toogled)

        # -- obter filechoosers sing e verify
        self.digest_filechooser_sign = builder.get_object("digest_filechooser_sign")
        self.digest_filechooser_verify = builder.get_object("digest_filechooser_verify")
        self.digest_filechooser_prverify = builder.get_object("digest_filechooser_prverify")
        self.digest_filechooser_signature = builder.get_object("digest_filechooser_signature")

        # -- obter areas sign e verify e set_no_show_all()
        self.digest_area_sign = builder.get_object("digest_area_sign")
        self.digest_area_sign.set_no_show_all(True)
        self.digest_area_verify = builder.get_object("digest_area_verify")
        self.digest_area_verify.set_no_show_all(True)
        self.digest_area_prverify = builder.get_object("digest_area_prverify")
        self.digest_area_prverify.set_no_show_all(True)
        self.digest_area_signature = builder.get_object("digest_area_signature")
        self.digest_area_signature.set_no_show_all(True)

        # -- obter checkboxs outras opções
        self.digest_outras_c = builder.get_object("digest_outras_c")
        self.digest_outras_d = builder.get_object("digest_outras_d")
        self.digest_outras_cb_hmac = builder.get_object("digest_outras_cb_hmac")
        self.digest_outras_non_fips_allow = builder.get_object("digest_outras_non_fips_allow")
        self.digest_outras_fips_fingerprint = builder.get_object("digest_outras_fips_fingerprint")
        self.digest_outras_rand = builder.get_object("digest_outras_rand")
        self.digest_outras_hmac_key = builder.get_object("digest_outras_hmac_key")
        self.digest_filechooser_rand = builder.get_object("digest_filechooser_rand")
    

    def __file_set(self, fs):
        print(fs.get_filename())
    

    def __cb_checksums_algoritmos_changed(self, cb):
        self.digest_algoritmo = "-" + cb.get_active_text()
    

    def __rd_output_on_toggled(self, rd):
        if "-hex" in rd.get_label() and rd.get_active():
            self.digest_output_format = "-hex"
        elif "-binary" in rd.get_label() and rd.get_active():
            self.digest_output_format = "-binary"
        elif "-r" in rd.get_label() and rd.get_active():
            self.digest_output_format = "-r"
        else:
            self.digest_output_format = "-hex"


    def __rd_input_type_on_toggled(self, rd):
        if "File" in rd.get_label() and rd.get_active():
            self.digest_tipo_input = "ficheiro"
            self.digest_area_input_ficheiro.set_visible(True)
            self.digest_area_input_txt.set_visible(False)
        elif "Text" in rd.get_label() and rd.get_active():
            self.digest_tipo_input = "texto"
            self.digest_area_input_ficheiro.set_visible(False)
            self.digest_area_input_txt.set_visible(True)
        else:
            self.digest_tipo_input = "ficheiro"
            self.digest_area_input_ficheiro.set_visible(True)
            self.digest_area_input_txt.set_visible(False)

    
    def __rd_output_type_on_toggled(self, rd):
        if "File" in rd.get_label() and rd.get_active():
            self.digest_local_output = "ficheiro"
            self.digest_area_ficheiro_output.set_visible(True)
            self.digest_area_pasta_output.set_visible(False)
        elif "Output" in rd.get_label() and rd.get_active():
            self.digest_local_output = "texto"
            self.digest_area_ficheiro_output.set_visible(False)
            self.digest_area_pasta_output.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.digest_local_output = "pasta"
            self.digest_area_ficheiro_output.set_visible(False)
            self.digest_area_pasta_output.set_visible(True)
        else:
            self.digest_local_output = "texto"
            self.digest_area_ficheiro_output.set_visible(False)
            self.digest_area_pasta_output.set_visible(False)

    
    def __cb_sign_verify_on_toogled(self, cb):
        if "Sign File" in cb.get_label() and cb.get_active():
            self.digest_area_sign.set_visible(True)
        elif "Sign File" in cb.get_label() and not cb.get_active():
            self.digest_area_sign.set_visible(False)
        elif "Verify (public key)" == cb.get_label() and cb.get_active():
            self.digest_area_verify.set_visible(True)
        elif "Verify (public key)" == cb.get_label() and not cb.get_active():
            self.digest_area_verify.set_visible(False)
        elif "Private Key" in cb.get_label() and cb.get_active():
            self.digest_area_prverify.set_visible(True)
        elif "Private Key" in cb.get_label() and not cb.get_active():
            self.digest_area_prverify.set_visible(False)
        elif "Signature" in cb.get_label() and cb.get_active():
            self.digest_area_signature.set_visible(True)
        elif "Signature" in cb.get_label() and not cb.get_active():
            self.digest_area_signature.set_visible(False)


    def __btn_executar_click(self, btn):
        self.digest_lbl_erro_config.set_visible(False)

        comando = ""
        nome_ficheiro_input = ""
        comando_pipe = ""
        nome_ficheiro_output = ""

        # -- verificar tipo de input
        if self.digest_tipo_input == "texto":
            buffer = self.builder.get_object("digest_input_text").get_buffer()
            inicioTxt, fimTxt = buffer.get_bounds()
            if buffer.get_text(inicioTxt, fimTxt, False):
                comando_pipe = "echo '" + buffer.get_text(inicioTxt, fimTxt, False) + "'"
            else:
                txt_lbl_erro = "You must fill the input text"
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
        else:
            ficheiro = self.digest_filechooser_input.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for input"
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                nome_ficheiro_input = "\"" + ficheiro.replace(" ", "\!space!/") + "\""


        comando += self.digest_comando + " " + self.digest_algoritmo + " " + self.digest_output_format

        # -- local output é ficheiro? verificar se ficheiro selecionado
        if self.digest_local_output == "ficheiro":
            ficheiro = self.digest_filechooser_output.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the output"
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                nome_ficheiro_output = "\"" + ficheiro + "\""

        elif self.digest_local_output == "pasta":
            pasta = self.digest_filechooser_pasta_output.get_filename()
            if not pasta:
                txt_lbl_erro = "You must select a location for the output"
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                nome_ficheiro_output = "\"" + pasta + "/" + self.digest_output_pasta_nome_ficheiro + "\""

        if nome_ficheiro_output:
            comando += " -out \"" + nome_ficheiro_output.replace(" ", "\!space!/") + "\""


        # -- verificar opções sign e verify e verificar se possui ficheiros selecionados
        sign_verify_adicionar_comando = ""
        if self.digest_cb_sign.get_active():
            ficheiro = self.digest_filechooser_sign.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked 'Sign File' option in 'Sign and Verify'. You must select a sign file."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                #if " " in ficheiro:
                #    ficheiro = "\"" + ficheiro + "\""
                sign_verify_adicionar_comando += " -sign \"" + ficheiro.replace(" ", "\!space!/") + "\""
        if self.digest_cb_verify.get_active():
            ficheiro = self.digest_filechooser_verify.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked 'Verify' option in 'Sign and Verify'. You must select a verify file."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                sign_verify_adicionar_comando += " -verify \"" + ficheiro.replace(" ", "\!space!/") + "\""
        if self.digest_cb_prverify.get_active():
            ficheiro = self.digest_filechooser_prverify.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked 'Private Key Verify' option in 'Sign and Verify'. You must select a Private Key file."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                sign_verify_adicionar_comando += " -prverify \"" + ficheiro.replace(" ", "\!space!/") + "\""
        if self.digest_cb_signature.get_active():
            ficheiro = self.digest_filechooser_signature.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked 'Signature' option in 'Sign and Verify'. You must select a Signature file."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                sign_verify_adicionar_comando += " -signature \"" + ficheiro.replace(" ", "\!space!/") + "\""

        comando += sign_verify_adicionar_comando

        
        # -- verificar opções da área "outras opções"
        outras_opcoes_adicionar_comando = ""
        if self.digest_outras_c.get_active():
            outras_opcoes_adicionar_comando += " -c "
        if self.digest_outras_d.get_active():
            outras_opcoes_adicionar_comando += " -d "
        if self.digest_outras_cb_hmac.get_active():
            hmac_key = self.digest_outras_hmac_key.get_text()
            if not hmac_key:
                txt_lbl_erro = "You checked '-hmac' option in 'Other options'. You must insert a hmac key."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                outras_opcoes_adicionar_comando += " -hmac " + hmac_key
        if self.digest_outras_non_fips_allow.get_active():
            outras_opcoes_adicionar_comando += " -non-fips-allow "
        if self.digest_outras_fips_fingerprint.get_active():
            outras_opcoes_adicionar_comando += " -fips-fingerprint "
        if self.digest_outras_rand.get_active():
            ficheiro = self.digest_filechooser_rand.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked '-rand' option in 'Other options'. You must select a Rand file."
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                outras_opcoes_adicionar_comando += " -rand \"" + ficheiro.replace(" ", "\!space!/") + "\""

        comando += " " + outras_opcoes_adicionar_comando


        # -- adicionar ficherio input ao comando (se exitir)
        comando += " " + nome_ficheiro_input.replace(" ", "\!space!/")

        lista = comando.split()
        comando_final = []
        for p in lista:
            comando_final.append(p.replace("\!space!/", " ").replace("\"", ""))

        # -- tentar executar
        try:
            if not self.aba_ssh or not self.aba_ssh.obter_ssh_client():
                if comando_pipe:
                    exec_comando_pip_digest = subprocess.Popen(comando_pipe.split(), stdout=subprocess.PIPE)
                    exec_comando_digest = subprocess.Popen(comando_final, stdin=exec_comando_pip_digest.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                else:
                    exec_comando_digest = subprocess.Popen(comando_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                if "binary" in self.digest_output_format:
                    # necessário passar pelo xxd se o output for binário, noutro caso o python tenta intrepertar cada byte
                    xxd = subprocess.Popen(["xxd", "-b"], stdin=exec_comando_digest.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    stdout, stderr = xxd.communicate()
                else:
                    stdout, stderr = exec_comando_digest.communicate()
            else:
                if comando_pipe:
                    stdin,stdout,stderr= self.aba_ssh.obter_ssh_client().exec_command("echo " + comando_pipe + " | " + comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor()), timeout=15)
                else:
                    stdin,stdout,stderr= self.aba_ssh.obter_ssh_client().exec_command(comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor()), timeout=15)
                stdout = stdout.readlines()
                if stdout: stdout = stdout[0]
                else: stdout = ""
                stderr = stderr.readlines()
                if stderr: stderr = stderr[0]
                else: stderr = ""

            # -- verificar qual o local para o output
            if self.digest_local_output == "texto":
                if not stderr:
                    Popup_Resultado_Class(stdout)
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", str(stderr))
            elif self.digest_local_output == "ficheiro" or self.digest_local_output == "pasta" :
                if not stderr:
                    Popup_Resultado_Class("Command executed successfully! Check the output file")
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", str(stderr))

        
        except Exception as e:
            Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", str(e))

