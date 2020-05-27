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

    digest_comando = "openssl dgst"
    digest_algoritmo = ""
    digest_output_format = "-hex" # opção do radiobutton default para o output format
    digest_tipo_input = "ficheiro" # ficheiro, texto
    digest_local_output = "texto" # texto (mostra no popup resultado), ficheiro (coloca no ficheiro indicado), pasta (cria um ficheiro na pasta selecionada)
    digest_output_pasta_nome_ficheiro = "gui_openssl_dgst_output"

    digest_lbl_erro_config = None
    digest_area_input_ficheiro = None
    digest_area_input_txt = None
    digest_filechooser_input = None
    digest_filechooser_output = None
    digest_filechooser_pasta_output = None
    digest_area_ficheiro_output = None
    digest_area_pasta_output = None

    def __init__(self, builder):
        self.builder = builder

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
                nome_ficheiro_input = ficheiro


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
                nome_ficheiro_output = ficheiro

        elif self.digest_local_output == "pasta":
            pasta = self.digest_filechooser_pasta_output.get_filename()
            if not pasta:
                txt_lbl_erro = "You must select a location for the output"
                self.digest_lbl_erro_config.set_text(txt_lbl_erro)
                self.digest_lbl_erro_config.set_visible(True)
                return
            else:
                nome_ficheiro_output = pasta + "/" + self.digest_output_pasta_nome_ficheiro


        if nome_ficheiro_output:
            comando += " -out " + nome_ficheiro_output

        comando += " " + nome_ficheiro_input

        # tentar executar
        try:
            if comando_pipe:
                exec_comando_pip_digest = subprocess.Popen(comando_pipe.split(), stdout=subprocess.PIPE)
                exec_comando_digest = subprocess.Popen(comando.split(), stdin=exec_comando_pip_digest.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            else:
                exec_comando_digest = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            if "binary" in self.digest_output_format:
                # necessário passar pelo xxd se o output for binário, noutro caso o python tenta intrepertar cada byte
                xxd = subprocess.Popen(["xxd", "-b"], stdin=exec_comando_digest.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = xxd.communicate()
            else:
                stdout, stderr = exec_comando_digest.communicate()

            # -- verificar qual o local para o output
            if self.digest_local_output == "texto":
                if not stderr:
                    Popup_Resultado_Class(stdout)
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", stderr)
            elif self.digest_local_output == "ficheiro" or self.digest_local_output == "pasta" :
                if not stderr:
                    Popup_Resultado_Class("Command executed successfully! Check the output file")
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", stderr)

        
        except Exception as e:
            Popup_Erro_Class("Error", "An error as occurred trying to execute the digest command! See details...", e)

