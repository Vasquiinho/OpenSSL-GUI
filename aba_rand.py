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

class Aba_Rand:

    # -- elementos e variáveis
    rand_lbl_erro_config = None
    rand_comando = "openssl rand"
    rand_input = None
    aba_ssh = None

    # output
    rand_formato_output = "default" # default, base64, hex
    rand_tipo_output = "output" #output, ficheiro, pasta
    rand_output_pasta_nome_ficheiro = "gui_openssl_rand_output"
    rand_area_output_ficheiro = None
    rand_filechooser_output = None
    rand_area_output_pasta = None
    rand_filechooser_output_pasta = None
    
    # outras opções
    rand_outras_rand = None # usa -rand
    rand_area_ficheiro_rand = None
    rand_filechooser_rand = None
    rand_outras_writerand = None # cria ficheiro rand -writerand
    rand_area_writerand = None
    rand_writerand_tipo_output = "ficheiro" # ficheiro, pasta
    rand_writerand_pasta_nome_ficheiro = "gui_openssl_writerand_output"
    rand_area_writerand_ficheiro = None
    rand_area_writerand_pasta = None
    rand_filechooser_ficheiro_writerand = None
    rand_filechooser_local_writerand = None
    rand_txt_writerand_pasta_extra = None


    def __init__(self, builder, aba_ssh):
        self.builder = builder
        self.aba_ssh = aba_ssh

        # -- obter label erro config
        self.rand_lbl_erro_config = self.builder.get_object("rand_lbl_erro_config")
        self.rand_lbl_erro_config.set_no_show_all(True)

        # -- obter input numero
        self.rand_input = self.builder.get_object("rand_input_num")

        # -- colocar os radio buttons formato output a "ouvir" quando são trocados 
        self.builder.get_object("rand_rd_output_format_1").connect("toggled", self.__rd_formato_output_on_toggled)
        self.builder.get_object("rand_rd_output_format_2").connect("toggled", self.__rd_formato_output_on_toggled)
        self.builder.get_object("rand_rd_output_format_3").connect("toggled", self.__rd_formato_output_on_toggled)

        # -- colocar os radio buttons tipo output a "ouvir" quando são trocados 
        self.builder.get_object("rand_rd_output_type_1").connect("toggled", self.__rd_tipo_output_on_toggled)
        self.builder.get_object("rand_rd_output_type_2").connect("toggled", self.__rd_tipo_output_on_toggled)
        self.builder.get_object("rand_rd_output_type_3").connect("toggled", self.__rd_tipo_output_on_toggled)

        # -- esconder area output - output file
        self.rand_filechooser_output = builder.get_object("rand_filechooser_output")
        self.rand_area_output_ficheiro = self.builder.get_object("rand_area_output_ficheiro")
        self.rand_area_output_ficheiro.set_visible(False)
        self.rand_area_output_ficheiro.set_no_show_all(True)

        # -- esconder area output - pasta output
        self.rand_area_output_pasta = self.builder.get_object("rand_area_output_pasta")
        self.rand_filechooser_output_pasta = builder.get_object("rand_filechooser_output_pasta")
        self.rand_area_output_pasta.set_visible(False)
        self.rand_area_output_pasta.set_no_show_all(True)
        self.builder.get_object("rand_txt_output_pasta_extra").set_text("A file named '"+ self.rand_output_pasta_nome_ficheiro +"' will be created at the choosen location")

        # -- ligar checkboxs outras opções ao evento toogled
        self.rand_outras_rand = self.builder.get_object("rand_outras_rand")
        self.rand_outras_writerand = self.builder.get_object("rand_outras_writerand")
        self.rand_outras_rand.connect("toggled", self.__bd_outras_opcoes_on_toggled)
        self.rand_outras_writerand.connect("toggled", self.__bd_outras_opcoes_on_toggled)

        # -- esconder area outras opcoes ficheiro rand
        self.rand_area_ficheiro_rand = self.builder.get_object("rand_area_ficheiro_rand")
        self.rand_area_ficheiro_rand.set_no_show_all(True)
        self.rand_area_ficheiro_rand.set_visible(False)

        # -- esconder area outras opcoes writerand
        self.rand_area_writerand = self.builder.get_object("rand_area_writerand")
        self.rand_area_writerand.set_no_show_all(True)
        self.rand_area_writerand.set_visible(False)

        # -- obter area writerand ficheiro
        self.rand_area_writerand_ficheiro = self.builder.get_object("rand_area_writerand_ficheiro")

        # -- esconder area writerand output location e alterar txt extra
        self.rand_area_writerand_pasta = self.builder.get_object("rand_area_writerand_pasta")
        self.rand_area_writerand_pasta.set_no_show_all(True)
        self.rand_area_writerand_pasta.set_visible(False)
        self.rand_txt_writerand_pasta_extra = self.builder.get_object("rand_txt_writerand_pasta_extra")
        self.rand_txt_writerand_pasta_extra.set_text("A file named '"+ self.rand_writerand_pasta_nome_ficheiro +"' will be created at the choosen location")

        # -- ligar radiobuttons outras opções writerand output ao evento toogled
        self.builder.get_object("rand_rd_writerand_output_1").connect("toggled", self.__rd_writerand_output_on_toggled)
        self.builder.get_object("rand_rd_writerand_output_2").connect("toggled", self.__rd_writerand_output_on_toggled)

        # -- obter filechoosers outras opcoes
        self.rand_filechooser_rand = self.builder.get_object("rand_filechooser_rand")
        self.rand_filechooser_ficheiro_writerand = self.builder.get_object("rand_filechooser_ficheiro_writerand")
        self.rand_filechooser_local_writerand = self.builder.get_object("rand_filechooser_local_writerand")

        # -- handler btn clicked
        self.builder.get_object("rand_btn_executar").connect("clicked", self.__btn_executar_click)
    

    def __rd_writerand_output_on_toggled(self, rd):
        if "File" in rd.get_label() and rd.get_active():
            self.rand_writerand_tipo_output = "ficheiro"
            self.rand_area_writerand_ficheiro.set_visible(True)
            self.rand_area_writerand_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.rand_writerand_tipo_output = "pasta"
            self.rand_area_writerand_ficheiro.set_visible(False)
            self.rand_area_writerand_pasta.set_visible(True)
        else:
            self.rand_writerand_tipo_output = "ficheiro"
            self.rand_area_writerand_ficheiro.set_visible(True)
            self.rand_area_writerand_pasta.set_visible(False)
    

    def __rd_formato_output_on_toggled(self, rd):
        if "Default" in rd.get_label() and rd.get_active():
            self.rand_formato_output = "default"
        elif "-hex" in rd.get_label() and rd.get_active():
            self.rand_formato_output = "hex"
        elif "-base64" in rd.get_label() and rd.get_active():
            self.rand_formato_output = "base64"
        else:
            self.rand_formato_output = "default"


    def __rd_tipo_output_on_toggled(self, rd):
        if "popup" in rd.get_label() and rd.get_active():
            self.rand_tipo_output = "output"
            self.rand_area_output_ficheiro.set_visible(False)
            self.rand_area_output_pasta.set_visible(False)
        elif "File" in rd.get_label() and rd.get_active():
            self.rand_tipo_output = "ficheiro"
            self.rand_area_output_ficheiro.set_visible(True)
            self.rand_area_output_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.rand_tipo_output = "pasta"
            self.rand_area_output_ficheiro.set_visible(False)
            self.rand_area_output_pasta.set_visible(True)
        else:
            self.rand_tipo_output = "output"
            self.rand_area_output_ficheiro.set_visible(False)
            self.rand_area_output_pasta.set_visible(False)


    def __bd_outras_opcoes_on_toggled(self, rd):
        if "-rand" in rd.get_label() and rd.get_active():
            self.rand_area_ficheiro_rand.set_visible(True)
        elif "-rand" in rd.get_label() and not rd.get_active():
            self.rand_area_ficheiro_rand.set_visible(False)
        elif "-writerand" in rd.get_label() and rd.get_active():
            self.rand_area_writerand.set_visible(True)
        elif "-writerand" in rd.get_label() and not rd.get_active():
            self.rand_area_writerand.set_visible(False)


    def __btn_executar_click(self, btn):
        self.rand_lbl_erro_config.set_visible(False)

        comando = ""
        ficheiro_local_output = ""
        ficheiro_local_writerand = ""

        comando += self.rand_comando + " "

        # -- verificar e selecionar o local do output do resultado
        if self.rand_tipo_output == "ficheiro":
            ficheiro = self.rand_filechooser_output.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the output"
                self.rand_lbl_erro_config.set_text(txt_lbl_erro)
                self.rand_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = ficheiro

        elif self.rand_tipo_output == "pasta":
            pasta = self.rand_filechooser_output_pasta.get_filename()
            if not pasta:
                txt_lbl_erro = "You must select a location for the output"
                self.rand_lbl_erro_config.set_text(txt_lbl_erro)
                self.rand_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = pasta + "/" + self.rand_output_pasta_nome_ficheiro

        if ficheiro_local_output:
            comando += " -out \"" + ficheiro_local_output.replace(" ", "\!space!/") + "\""


        # -- verificar formato do output (base64, hex, default)
        if self.rand_formato_output == "base64":
            comando += " -base64"
        elif self.rand_formato_output == "hex":
            comando += " -hex"
        #else defautl = str vazia ("")


        
        # -- verificar opções da área "outras opções"
        if self.rand_outras_rand.get_active():
            ficheiro = self.rand_filechooser_rand.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked '-rand' option in 'Other options'. You must select a Rand file."
                self.rand_lbl_erro_config.set_text(txt_lbl_erro)
                self.rand_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -rand \"" + ficheiro.replace(" ", "\!space!/") + "\""

        if self.rand_outras_writerand.get_active():
            if self.rand_writerand_tipo_output == "ficheiro":
                ficheiro = self.rand_filechooser_ficheiro_writerand.get_filename()
                if not ficheiro:
                    txt_lbl_erro = "You must select a file for the writerand output"
                    self.rand_lbl_erro_config.set_text(txt_lbl_erro)
                    self.rand_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = ficheiro
            elif self.rand_writerand_tipo_output == "pasta":
                pasta = self.rand_filechooser_local_writerand.get_filename()
                if not pasta:
                    txt_lbl_erro = "You must select a location for the writerand output file"
                    self.rand_lbl_erro_config.set_text(txt_lbl_erro)
                    self.rand_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = pasta + "/" + self.rand_writerand_pasta_nome_ficheiro

        if ficheiro_local_writerand:
            comando += " -writerand \"" + ficheiro_local_writerand.replace(" ", "\!space!/") + "\""


        # -- adicionar número input ao comando
        if self.rand_input.get_value():
            comando += " " + str(int(self.rand_input.get_value()))
        else:
            comando += " 0"

        lista = comando.split()
        comando_final = []
        for p in lista:
            comando_final.append(p.replace("\!space!/", " ").replace("\"", ""))

        # -- tentar executar
        try:
            if not self.aba_ssh or not self.aba_ssh.obter_ssh_client():
                exec_comando_rand = subprocess.Popen(comando_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                if self.rand_formato_output == "default":
                    # necessário passar pelo xxd se o output for binário, noutro caso o python tenta intrepertar cada byte
                    xxd = subprocess.Popen(["xxd", "-b"], stdin=exec_comando_rand.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    stdout, stderr = xxd.communicate()
                else:
                    stdout, stderr = exec_comando_rand.communicate()
            else:
                stdin,stdout,stderr= self.aba_ssh.obter_ssh_client().exec_command(comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor()), timeout=15)
                stdout = stdout.readlines()
                stderr = stderr.readlines()
                if stderr:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(stderr))
                    return
                if self.rand_formato_output == "default":
                    a = comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor())
                    stdin,stdout,stderr = self.aba_ssh.obter_ssh_client().exec_command("echo " + a + " | xxd -b", timeout=15)
                    stdout = stdout.readlines()
                    stderr = stderr.readlines()

            # -- verificar qual o local para o output
            if self.rand_tipo_output == "output":
                if not stderr:
                    Popup_Resultado_Class(str(stdout))
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(stderr))
            elif self.rand_tipo_output == "ficheiro" or self.rand_tipo_output == "pasta" :
                if not stderr:
                    Popup_Resultado_Class("Command executed successfully! Check the output file")
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(stderr))

        except Exception as e:
            Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(e))
    
    
