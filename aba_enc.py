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
    usa_base64 = False

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
    enc_key_cb_chiper = None
    enc_key_combo_cipher = None
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
        self.enc_key_cb_chiper = self.builder.get_object("enc_key_cb_chiper")
        self.enc_key_cb_chiper.connect("toggled", self.__cb_cipher_toggled)
        self.enc_key_combo_cipher = self.builder.get_object("enc_key_combo_cipher")
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

        pedido_lista_algortimos_digest = subprocess.Popen(["openssl", "list", "-digest-commands"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pedido_lista_algortimos_digest.communicate()
        if not stderr:
            for algoritmo in stdout.split():
                    self.enc_key_combo_digest.append_text(algoritmo)
        else:
            print("An error as occurred loading digest algorithms")
            self.enc_key_combo_digest.append_text("An error as occurred loading digest algorithms")

        pedido_lista_algortimos_cipher = subprocess.Popen(["openssl", "enc", "-list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pedido_lista_algortimos_cipher.communicate()
        if not stderr:
            for algoritmo in stdout.split():
                if "ciphers" not in algoritmo and "Supported" not in algoritmo:
                    self.enc_key_combo_cipher.append_text(algoritmo)
        else:
            print("An error as occurred loading digest algorithms")
            self.enc_key_combo_cipher.append_text("An error as occurred loading cipher algorithms")

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
            self.enc_key_input_salt.set_sensitive(False)
        else:
            self.enc_key_input_salt.set_visible(True)
            self.enc_key_input_salt.set_sensitive(True)

    def __cb_iter_toggled(self, cb):
        self.enc_key_input_iter.set_sensitive(cb.get_active())

    def __cb_pass_toggled(self, cb):
        self.enc_key_input_pass.set_sensitive(cb.get_active())
    
    def __cb_cipher_toggled(self, cb):
        self.enc_key_combo_cipher.set_sensitive(cb.get_active())

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
            self.usa_base64 = True
        else:
            self.usa_base64 = False
        
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

        # key
        if self.enc_key_cb_pass.get_active():
            password = self.enc_key_input_pass.get_text()
            if not password:
                txt_lbl_erro = "Password option checked! You must insert a password in key settings"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -pass pass:" + password.replace(" ", "\!space!/") + " "
        if self.enc_key_cb_chiper.get_active():
            if not self.enc_key_combo_cipher.get_active_text() == "An error as occurred loading cipher algorithms" and not self.enc_key_combo_cipher.get_active_text() == "Select chiper algorithm...": 
                comando += " " + self.enc_key_combo_cipher.get_active_text() + " "
            elif not self.enc_key_combo_cipher.get_active_text() == "An error as occurred loading cipher algorithms":
                txt_lbl_erro = "Cipher option checked in key settings. You must select cipher algorithm!"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
        if self.enc_key_cb_md.get_active():
            if not self.enc_key_combo_digest.get_active_text() == "An error as occurred loading digest algorithms" and not self.enc_key_combo_digest.get_active_text() == "Select digest algorithm...": 
                comando += " -md " + self.enc_key_combo_digest.get_active_text() + " "
            elif not self.enc_key_combo_digest.get_active_text() == "An error as occurred loading cipher algorithms":
                txt_lbl_erro = "Digest option checked in key settings. You must select Digest algorithm!"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
        if self.enc_key_cb_iter.get_active():
            if self.enc_key_input_iter.get_value() is not None:
                comando += " -iter " + str(self.enc_key_input_iter.get_value()).replace(".0", "") + " "
            else:
                txt_lbl_erro = "Iter option checked in key settings. You must select the number of iterations!"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
        if self.enc_key_cb_pbkdf2.get_active():
            comando += " -pbkdf2 "
        if self.enc_key_rd_nosalt.get_active():
            comando += " -nosalt "
        if self.enc_key_rd_salt.get_active():
            salt = self.enc_key_input_salt.get_text()
            if not salt:
                txt_lbl_erro = "Salt option checked! You must insert a hexadecimal valuer for Salt in key settings"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                try:
                    int(salt, 16)
                    comando += " -salt -S " + salt + " "
                except:
                    txt_lbl_erro = "Given salt in key options isn't a hexadecimal value!"
                    self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                    self.enc_lbl_erro_config.set_visible(True)
                    return
        if self.enc_key_cb_key.get_active():
            key = self.enc_key_input_key.get_text()
            if not key:
                txt_lbl_erro = "Key option checked! You must insert a hexadecimal valuer for key in key settings"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                try:
                    int(key, 16)
                    comando += " -key " + key + " "
                except:
                    txt_lbl_erro = "Given key in key options isn't a hexadecimal value!"
                    self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                    self.enc_lbl_erro_config.set_visible(True)
                    return
        if self.enc_key_cb_iv.get_active():
            iv = self.enc_key_input_iv.get_text()
            if not key:
                txt_lbl_erro = "IV option checked! You must insert a hexadecimal valuer for IV in key settings"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                try:
                    int(iv, 16)
                    comando += " -iv " + iv + " "
                except:
                    txt_lbl_erro = "Given IV in key options isn't a hexadecimal value!"
                    self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                    self.enc_lbl_erro_config.set_visible(True)
                    return
        if self.enc_key_cb_nopad.get_active():
            comando += " -nopad "

        # key - outras validações: necessário pass ou key + iv
        if not any(x in comando for x in ["-pass", "-K", "-iv"]):
            txt_lbl_erro = "A Password or KEY + IV must be defined in key options!"
            self.enc_lbl_erro_config.set_text(txt_lbl_erro)
            self.enc_lbl_erro_config.set_visible(True)
            return
        if "-K" in comando and not "-iv" in comando:
            txt_lbl_erro = "You specified a Key. IV must also be specified!"
            self.enc_lbl_erro_config.set_text(txt_lbl_erro)
            self.enc_lbl_erro_config.set_visible(True)
            return

        
        # outras
        if self.enc_outras_cb_A.get_active():
            comando += " -A "
        if self.enc_outras_cb_p.get_active():
            comando += " -p "
        if self.enc_outras_cb_P.get_active():
            comando += " -P "
        if self.enc_outras_cb_bufsize.get_active():
            if self.enc_outras_input_bufsize.get_value() is not None:
                comando += " -bufsize " + str(self.enc_outras_input_bufsize.get_value()).replace(".0", "") + " "
            else:
                txt_lbl_erro = "Biffer Size option checked in other settings. You must define the size of the buffer!"
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
        if self.enc_outras_cb_none.get_active():
            comando += " -none "
        if self.enc_outras_cb_z.get_active():
            comando += " -z "
        if self.enc_outras_rand.get_active():
            ficheiro = self.enc_filechooser_rand.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked '-rand' option in 'Other options'. You must select a Rand file."
                self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                self.enc_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -rand \"" + ficheiro.replace(" ", "\!space!/") + "\""
        ficheiro_local_writerand = ""
        if self.enc_outras_writerand.get_active():
            if self.enc_writerand_tipo_output == "ficheiro":
                ficheiro = self.enc_filechooser_ficheiro_writerand.get_filename()
                if not ficheiro:
                    txt_lbl_erro = "You must select a file for the writerand output"
                    self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                    self.enc_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = ficheiro
            elif self.enc_writerand_tipo_output == "pasta":
                pasta = self.enc_filechooser_local_writerand.get_filename()
                if not pasta:
                    txt_lbl_erro = "You must select a location for the writerand output file"
                    self.enc_lbl_erro_config.set_text(txt_lbl_erro)
                    self.enc_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = pasta + "/" + self.enc_writerand_pasta_nome_ficheiro
        if ficheiro_local_writerand:
            comando += " -writerand \"" + ficheiro_local_writerand.replace(" ", "\!space!/") + "\""

        #print(comando_pipe + " | " + comando)

        # tentar executar
        lista = comando.split()
        comando_final = []
        for p in lista:
            comando_final.append(p.replace("\!space!/", " ").replace("\"", ""))

        try:
            if not self.aba_ssh or not self.aba_ssh.obter_ssh_client():
                if comando_pipe:
                    exec_comando_pip_enc = subprocess.Popen(comando_pipe.split(), stdout=subprocess.PIPE)
                    exec_comando_enc = subprocess.Popen(comando_final, stdin=exec_comando_pip_enc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                else:
                    exec_comando_enc = subprocess.Popen(comando_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                if not self.usa_base64:
                    xxd = subprocess.Popen(["xxd", "-b"], stdin=exec_comando_enc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    stdout, stderr = xxd.communicate()
                else:
                    stdout, stderr = exec_comando_enc.communicate()
            else:
                if comando_pipe:
                    stdin,stdout,stderr= self.aba_ssh.obter_ssh_client().exec_command(comando_pipe + " | " + comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor()), timeout=15)
                else:
                    stdin,stdout,stderr= self.aba_ssh.obter_ssh_client().exec_command(comando.replace("\!space!/", " ").replace(self.aba_ssh.obter_local_mount(), self.aba_ssh.obter_local_monta_no_servidor()), timeout=15)
                stdout = stdout.readlines()
                if stdout: stdout = stdout[0] 
                else: stdout = ""
                stderr = stderr.readlines()
                if stderr: stderr = stderr[0] 
                else: stderr = ""

                if "-a" not in comando and not stderr:
                    xxd = subprocess.Popen(["xxd", "-b"], stdin=stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    stdout, stderr = xxd.communicate()

            # -- verificar qual o local para o output
            if self.enc_tipo_output == "popup":
                if not stderr or (stdout and stderr):
                    Popup_Resultado_Class(stderr + "\n" + stdout)
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the enc command! See details...", str(stderr))
                #Popup_Resultado_Class(stderr + "\n" + stdout)
            elif self.enc_tipo_output == "ficheiro" or self.enc_tipo_output == "pasta" :
                if not stderr or (stdout and stderr):
                    Popup_Resultado_Class("Command executed successfully! Check the output file")
                else:
                    Popup_Erro_Class("Error", "An error as occurred trying to execute the enc command! See details...", str(stderr))
                #Popup_Resultado_Class(stderr + "\n" + stdout)

        except Exception as e:
            Popup_Erro_Class("Error", "An error as occurred trying to execute the enc command! See details...", str(e))