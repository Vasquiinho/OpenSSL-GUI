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

class Aba_Enc:

    # -- elementos e variáveis
    enc_comando = "openssl enc"
    builder = None
    aba_ssh = None
    enc_lbl_erro_config = None
    enc_btn_executar = None

    # input
    enc_rd_input_type_file = None
    enc_rd_input_type_text = None
    enc_area_input_ficheiro = None
    enc_filechooser_input = None
    enc_area_input_txt = None
    enc_input_text = None
    enc_tipo_input = "ficheiro" # valores possiveis: ficheiro, texto
    enc_cb_input_e = None
    enc_cb_input_d = None
    enc_cb_input_a = None

    # output
    enc_rd_output_type_popup = None
    enc_rd_output_type_file = None
    enc_rd_output_type_folder = None
    enc_area_output_ficheiro = None
    enc_filechooser_output = None
    enc_area_output_pasta = None
    enc_filechooser_output_pasta = None
    enc_txt_output_pasta_extra = None
    enc_tipo_output = "popup" # valores possiveis: popup, ficheiro, pasta
    enc_output_pasta_nome_ficheiro = "Gui_openssl_enc_output"

    # key
    enc_key_cb_pass = None
    enc_key_input_pass = None
    enc_key_cb_md = None
    enc_key_combo_digest = None
    enc_key_cb_iter = None
    enc_key_input_iter = None
    enc_key_cb_pbkdf2 = None
    enc_key_rd_salt = None
    enc_key_rd_nosalt = None
    enc_key_input_salt = None
    enc_key_cb_key = None
    enc_key_input_key = None
    enc_key_cb_iv = None
    enc_key_input_iv = None
    enc_key_cb_nopad = None

    # other settings
    enc_outras_cb_A = None
    enc_outras_cb_p = None
    enc_outras_cb_P = None
    enc_outras_cb_bufsize = None
    enc_outras_input_bufsize = None
    enc_outras_cb_none = None
    enc_outras_cb_z = None
    enc_outras_rand = None
    enc_area_ficheiro_rand = None
    enc_filechooser_rand = None
    enc_outras_writerand = None
    enc_area_writerand = None
    enc_rd_writerand_output_file = None
    enc_rd_writerand_output_folder = None
    enc_area_writerand_ficheiro = None
    enc_filechooser_ficheiro_writerand = None
    enc_area_writerand_pasta = None
    enc_filechooser_local_writerand = None
    enc_txt_writerand_pasta_extra = None
    enc_writerand_tipo_output = "ficheiro" # valores possiveis: ficheiro, pasta
    enc_writerand_pasta_nome_ficheiro = "Gui_openssl_writerand_output"


    def __init__(self, builder, aba_ssh):
        self.builder = builder
        self.aba_ssh = aba_ssh

        self.enc_lbl_erro_config = self.builder.get_object("enc_lbl_erro_config")
        self.enc_lbl_erro_config.set_no_show_all(True)
        self.enc_btn_executar = self.builder.get_object("enc_btn_executar")
        self.enc_btn_executar.connect("clicked", self.__btn_executar_clicked)

        # input
        self.enc_rd_input_type_file = self.builder.get_object("enc_rd_input_type_file")
        self.enc_rd_input_type_text = self.builder.get_object("enc_rd_input_type_text")
        self.enc_rd_input_type_file.connect("toggled", self.__rd_tipo_input_on_toggled)
        self.enc_rd_input_type_text.connect("toggled", self.__rd_tipo_input_on_toggled)
        self.enc_area_input_ficheiro = self.builder.get_object("enc_area_input_ficheiro")
        self.enc_filechooser_input = self.builder.get_object("enc_filechooser_input")
        self.enc_area_input_txt = self.builder.get_object("enc_area_input_txt")
        self.enc_area_input_txt.set_visible(False)
        self.enc_area_input_txt.set_no_show_all(True)
        self.enc_input_text = self.builder.get_object("enc_input_text")
        self.enc_cb_input_d = self.builder.get_object("enc_cb_input_d")
        self.enc_cb_input_a = self.builder.get_object("enc_cb_input_a")
        self.enc_cb_input_e = self.builder.get_object("enc_cb_input_e")

        # output
        self.enc_rd_output_type_popup = self.builder.get_object("enc_rd_output_type_popup")
        self.enc_rd_output_type_file = self.builder.get_object("enc_rd_output_type_file")
        self.enc_rd_output_type_folder = self.builder.get_object("enc_rd_output_type_folder")
        self.enc_rd_output_type_popup.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.enc_rd_output_type_file.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.enc_rd_output_type_folder.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.enc_area_output_ficheiro = self.builder.get_object("enc_area_output_ficheiro")
        self.enc_area_output_ficheiro.set_visible(False)
        self.enc_area_output_ficheiro.set_no_show_all(True)
        self.enc_filechooser_output = self.builder.get_object("enc_filechooser_output")
        self.enc_area_output_pasta = self.builder.get_object("enc_area_output_pasta")
        self.enc_area_output_pasta.set_visible(False)
        self.enc_area_output_pasta.set_no_show_all(True)
        self.enc_filechooser_output_pasta = self.builder.get_object("enc_filechooser_output_pasta")
        self.enc_txt_output_pasta_extra = self.builder.get_object("enc_txt_output_pasta_extra")
        self.enc_txt_output_pasta_extra.set_text("A file named '" + self.enc_output_pasta_nome_ficheiro + "' will be created at the choosen location")

        # key
        self.enc_key_cb_pass = self.builder.get_object("enc_key_cb_pass")
        self.enc_key_cb_pass.connect("toggled", self.__cb_pass_toggled)
        self.enc_key_input_pass = self.builder.get_object("enc_key_input_pass")
        self.enc_key_cb_md = self.builder.get_object("enc_key_cb_md")
        self.enc_key_cb_md.connect("toggled", self.__cb_md_toggled)
        self.enc_key_combo_digest = self.builder.get_object("enc_key_combo_digest")
        self.enc_key_cb_iter = self.builder.get_object("enc_key_cb_iter")
        self.enc_key_cb_iter.connect("toggled", self.__cb_iter_toggled)
        self.enc_key_input_iter = self.builder.get_object("enc_key_input_iter")
        self.enc_key_cb_pbkdf2 = self.builder.get_object("enc_key_cb_pbkdf2")
        self.enc_key_rd_salt = self.builder.get_object("enc_key_rd_salt")
        self.enc_key_rd_nosalt = self.builder.get_object("enc_key_rd_nosalt")
        self.enc_key_rd_salt.connect("toggled", self.__rd_salt_nosalt_toggled)
        self.enc_key_rd_nosalt.connect("toggled", self.__rd_salt_nosalt_toggled)
        self.enc_key_input_salt = self.builder.get_object("enc_key_input_salt")
        self.enc_key_cb_key = self.builder.get_object("enc_key_cb_key")
        self.enc_key_cb_key.connect("toggled", self.__cb_key_toggled)
        self.enc_key_input_key = self.builder.get_object("enc_key_input_key")
        self.enc_key_cb_iv = self.builder.get_object("enc_key_cb_iv")
        self.enc_key_cb_iv.connect("toggled", self.__cb_iv_toggled)
        self.enc_key_input_iv = self.builder.get_object("enc_key_input_iv")
        self.enc_key_cb_nopad = self.builder.get_object("enc_key_cb_nopad")

        # outras
        self.enc_outras_cb_A = self.builder.get_object("enc_outras_cb_A")
        self.enc_outras_cb_p = self.builder.get_object("enc_outras_cb_p")
        self.enc_outras_cb_P = self.builder.get_object("enc_outras_cb_P")
        self.enc_outras_cb_bufsize = self.builder.get_object("enc_outras_cb_bufsize")
        self.enc_outras_cb_bufsize.connect("toggled", self.__cb_bufsize_toggled)
        self.enc_outras_input_bufsize = self.builder.get_object("enc_outras_input_bufsize")
        self.enc_outras_cb_none = self.builder.get_object("enc_outras_cb_none")
        self.enc_outras_cb_z = self.builder.get_object("enc_outras_cb_z")
        self.enc_outras_rand = self.builder.get_object("enc_outras_rand")
        self.enc_outras_rand.connect("toggled", self.__cb_rand_toggled)
        self.enc_area_ficheiro_rand = self.builder.get_object("enc_area_ficheiro_rand")
        self.enc_area_ficheiro_rand.set_no_show_all(True)
        self.enc_filechooser_rand = self.builder.get_object("enc_filechooser_rand")
        self.enc_outras_writerand = self.builder.get_object("enc_outras_writerand")
        self.enc_outras_writerand.connect("toggled", self.__cb_writerand_toggled)
        self.enc_area_writerand = self.builder.get_object("enc_area_writerand")
        self.enc_area_writerand.set_no_show_all(True)
        self.enc_rd_writerand_output_file = self.builder.get_object("enc_rd_writerand_output_file")
        self.enc_rd_writerand_output_folder = self.builder.get_object("enc_rd_writerand_output_folder")
        self.enc_rd_writerand_output_file.connect("toggled", self.__rd_writerand_output_on_toggled)
        self.enc_rd_writerand_output_folder.connect("toggled", self.__rd_writerand_output_on_toggled)
        self.enc_area_writerand_ficheiro = self.builder.get_object("enc_area_writerand_ficheiro")
        self.enc_filechooser_ficheiro_writerand = self.builder.get_object("enc_filechooser_ficheiro_writerand")
        self.enc_area_writerand_pasta = self.builder.get_object("enc_area_writerand_pasta")
        self.enc_area_writerand_pasta.set_no_show_all(True)
        self.enc_filechooser_local_writerand = self.builder.get_object("enc_filechooser_local_writerand")
        self.enc_txt_writerand_pasta_extra = self.builder.get_object("enc_txt_writerand_pasta_extra")
        self.enc_txt_writerand_pasta_extra.set_text("A file named '" + self.enc_writerand_pasta_nome_ficheiro + "' will be created at the choosen location")


    def __rd_writerand_output_on_toggled(self, rd):
        if "File" in rd.get_label() and rd.get_active():
            self.enc_writerand_tipo_output = "ficheiro"
            self.enc_area_writerand_ficheiro.set_visible(True)
            self.enc_area_writerand_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.enc_writerand_tipo_output = "pasta"
            self.enc_area_writerand_ficheiro.set_visible(False)
            self.enc_area_writerand_pasta.set_visible(True)
        else:
            self.enc_writerand_tipo_output = "ficheiro"
            self.enc_area_writerand_ficheiro.set_visible(True)
            self.enc_area_writerand_pasta.set_visible(False)

    def __cb_writerand_toggled(self, cb):
        self.enc_area_writerand.set_visible(cb.get_active())

    def __cb_rand_toggled(self, cb):
        self.enc_area_ficheiro_rand.set_visible(cb.get_active())

    def __cb_bufsize_toggled(self, cb):
        self.enc_outras_input_bufsize.set_sensitive(cb.get_active())

    def __cb_iv_toggled(self, cb):
        self.enc_key_input_iv.set_sensitive(cb.get_active())

    def __cb_key_toggled(self, cb):
        self.enc_key_input_key.set_sensitive(cb.get_active())

    def __rd_salt_nosalt_toggled(self, rd):
        if "no" in rd.get_label():
            self.enc_key_input_salt.set_visible(False)
        else:
            self.enc_key_input_salt.set_visible(True)

    def __cb_iter_toggled(self, cb):
        self.enc_key_input_iter.set_sensitive(cb.get_active())

    def __cb_pass_toggled(self, cb):
        self.enc_key_input_pass.set_sensitive(cb.get_active())
    
    def __cb_md_toggled(self, cb):
        self.enc_key_combo_digest.set_sensitive(cb.get_active())

    def __rd_tipo_input_on_toggled(self, rd):
        if "Text" in rd.get_label() and rd.get_active():
            self.enc_tipo_input = "texto"
            self.enc_area_input_ficheiro.set_visible(False)
            self.enc_area_input_txt.set_visible(True)
        elif "File" in rd.get_label() and rd.get_active():
            self.enc_tipo_input = "ficheiro"
            self.enc_area_input_ficheiro.set_visible(True)
            self.enc_area_input_txt.set_visible(False)
        else:
            self.enc_tipo_input = "ficheiro"
            self.enc_area_input_ficheiro.set_visible(True)
            self.enc_area_input_txt.set_visible(False)
    

    def __rd_tipo_output_on_toggled(self, rd):
        if "popup" in rd.get_label() and rd.get_active():
            self.enc_tipo_output = "popup"
            self.enc_area_output_ficheiro.set_visible(False)
            self.enc_area_output_pasta.set_visible(False)
        elif "File" in rd.get_label() and rd.get_active():
            self.enc_tipo_output = "ficheiro"
            self.enc_area_output_ficheiro.set_visible(True)
            self.enc_area_output_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.enc_tipo_output = "pasta"
            self.enc_area_output_ficheiro.set_visible(False)
            self.enc_area_output_pasta.set_visible(True)
        else:
            self.enc_tipo_output = "popup"
            self.enc_area_output_ficheiro.set_visible(False)
            self.enc_area_output_pasta.set_visible(False)

    

    def __btn_executar_clicked(self, btn):
        self.enc_lbl_erro_config.set_visible(False)
        
        comando = ""
        comando += self.enc_comando + " "
        comando_pipe = ""

        # input
        if self.enc_tipo_input == "texto":
            buffer = self.enc_input_text.get_buffer()
            inicioTxt, fimTxt = buffer.get_bounds()
            if buffer.get_text(inicioTxt, fimTxt, False):
                comando_pipe = "echo '" + buffer.get_text(inicioTxt, fimTxt, False) + "'"
            else:
                txt_lbl_erro = "You must fill the input text"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
        else:
            ficheiro = self.enc_filechooser_input.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for input"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -in \"" + ficheiro.replace(" ", "\!space!/") + "\" "
        if self.enc_cb_input_e.get_active():
            comando += " -e "
        if self.enc_cb_input_d.get_active():
            comando += " -d "
        if self.enc_cb_input_a.get_active():
            comando += " -a "
        
        # output
        # -- verificar e selecionar o local do output do resultado
        ficheiro_local_output = ""
        if self.enc_tipo_output == "ficheiro":
            ficheiro = self.enc_filechooser_output.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the output in output options"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = ficheiro

        elif self.enc_tipo_output == "pasta":
            pasta = self.enc_filechooser_output_pasta.get_filename()
            if not pasta:
                txt_lbl_erro = "You must select a location for the output in output options"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = pasta + "/" + self.enc_output_pasta_nome_ficheiro

        if ficheiro_local_output:
            comando += " -out \"" + ficheiro_local_output.replace(" ", "\!space!/") + "\" "

        


        print(comando_pipe + " | " + comando)