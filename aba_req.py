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

class Aba_Req:

    # -- elementos e variáveis
    req_comando = "openssl req"
    req_btn_executar = None
    req_lbl_erro_config = None

    # subject info
    req_subject_name = None
    req_subject_country = None
    req_subject_region = None
    req_subject_city = None
    req_subject_organisation = None
    req_subject_orgunit = None
    req_subject_email = None

    # input
    req_cb_input_format = None
    req_inform_type = None
    req_cb_input_file = None
    req_filechooser_input = None
    req_cb_input_config = None
    req_filechooser_input_config = None
    req_input_file_passin = None
    req_cb_input_passin = None

    #key
    req_cb_input_key_format = None
    req_input_key_type = None
    req_cb_input_key = None
    req_filechooser_input_key = None
    req_cb_output_key = None
    req_filechooser_output_key = None
    req_cb_output_pubkey = None
    req_key_cb_new_key = None
    req_key_cb_nodes = None
    req_key_password = None

    # x509
    req_cb_x509 = None
    req_cb_x509_days = None
    req_x509_days_input = None
    req_cb_x509_seriano = None
    req_x509_seriano_input = None
    # -- treeview
    req_tv_x509_extensions = None
    req_tv_model = None
    req_tv_liststore = None
    req_tv_x509_cb_critico = None
    req_tv_x509_cb_nome = None
    req_liststore_x509_ext_names = None
    req_tv_x509_cb_valor = None
    req_btn_tv_append_liststore = None
    req_btn_tv_remove_liststore = None
    # -- liststores values
    req_liststore_x509_basicConstraints = None
    req_liststore_x509_keyUsage = None
    req_liststore_x509_subjectKeyIdentifier = None
    req_liststore_x509_crlDistributionPoints = None
    req_liststore_x509_extendedKeyUsage = None
    req_liststore_x509_subjectAltName = None
    req_liststore_x509_authorityKeyIdentifier = None
    req_liststore_x509_certificatePolicies = None
    liststorevalues = None

    # output settings
    req_rd_output_format_1 = None
    req_rd_output_format_2 = None
    req_output_format = "PEM" # PEM, DER
    req_rd_output_type_1 = None
    req_rd_output_type_2 = None
    req_rd_output_type_3 = None
    req_output_type = "popup" # popup, ficheiro, pasta
    req_area_output_ficheiro = None
    req_filechooser_output = None
    req_area_output_pasta = None
    req_filechooser_output_pasta = None
    req_txt_output_pasta_extra = None
    req_output_pasta_nome_ficheiro = "gui_openssl_req_output_file"

    # outras
    req_outras_subject = None
    req_outras_text = None
    req_outras_noout = None
    req_outras_modulus = None
    req_outras_verify = None
    req_outras_digest = None
    req_outras_algoritmos_digest = None
    req_outras_erro_algoritmos_digest = False
    req_outras_precert = None
    req_outras_utf8 = None
    req_outras_batch = None
    req_outras_rand = None
    req_area_ficheiro_rand = None
    req_filechooser_rand = None
    req_outras_writerand = None
    req_area_writerand = None
    req_rd_writerand_output_file = None
    req_rd_writerand_output_folder = None
    req_area_writerand_ficheiro = None
    req_filechooser_ficheiro_writerand = None
    req_area_writerand_pasta = None
    req_filechooser_local_writerand = None
    req_txt_writerand_pasta_extra = None
    req_writerand_nome_ficheiro = "gui_openssl_writerand_output"
    req_writerand_tipo_output = "ficheiro"

    def __init__(self, builder):
        self.builder = builder

        self.req_btn_executar = self.builder.get_object("req_btn_executar")
        self.req_btn_executar.connect("clicked", self.__btn_executar_clicked)
        self.req_lbl_erro_config = self.builder.get_object("req_lbl_erro_config")
        self.req_lbl_erro_config.set_no_show_all(True)

        # subject
        self.req_subject_country = self.builder.get_object("req_subject_country")
        self.req_subject_name = self.builder.get_object("req_subject_name")
        self.req_subject_region = self.builder.get_object("req_subject_region")
        self.req_subject_city = self.builder.get_object("req_subject_city")
        self.req_subject_organisation = self.builder.get_object("req_subject_organisation")
        self.req_subject_orgunit = self.builder.get_object("req_subject_orgunit")
        self.req_subject_email = self.builder.get_object("req_subject_email")

        # input
        self.req_cb_input_format = self.builder.get_object("req_cb_input_format")
        self.req_cb_input_format.connect("toggled", self.__cb_input_format_toggled)
        self.req_inform_type = self.builder.get_object("req_inform_type")
        self.req_cb_input_file = self.builder.get_object("req_cb_input_file")
        self.req_cb_input_file.connect("toggled", self.__cb_input_file_toggled)
        self.req_filechooser_input = self.builder.get_object("req_filechooser_input")
        self.req_cb_input_config = self.builder.get_object("req_cb_input_config")
        self.req_cb_input_config.connect("toggled", self.__cb_config_key_file_toggled)
        self.req_filechooser_input_config = self.builder.get_object("req_filechooser_input_config")
        self.req_input_file_passin = self.builder.get_object("req_input_file_passin")
        self.req_cb_input_passin = self.builder.get_object("req_cb_input_passin")
        self.req_cb_input_passin.connect("toggled", self.__cb_input_passin_toggled)

        # key
        self.req_cb_input_key_format = self.builder.get_object("req_cb_input_key_format")
        self.req_cb_input_key_format.connect("toggled", self.__cb_key_format_toggled)
        self.req_input_key_type = self.builder.get_object("req_input_key_type")
        self.req_cb_input_key = self.builder.get_object("req_cb_input_key")
        self.req_cb_input_key.connect("toggled", self.__cb_key_input_key_file_toggled)
        self.req_filechooser_input_key = self.builder.get_object("req_filechooser_input_key")
        self.req_cb_output_key = self.builder.get_object("req_cb_output_key")
        self.req_cb_output_key.connect("toggled", self.__cb_key_output_key_file_toggled)
        self.req_filechooser_output_key = self.builder.get_object("req_filechooser_output_key")
        self.req_cb_output_pubkey = self.builder.get_object("req_cb_output_pubkey")
        self.req_key_cb_new_key = self.builder.get_object("req_key_cb_new_key")
        self.req_key_cb_nodes = self.builder.get_object("req_key_cb_nodes")
        self.req_key_cb_nodes.connect("toggled", self.__cb_key_nodes_toggled)
        self.req_key_password = self.builder.get_object("req_key_password")

        # x509
        self.req_cb_x509 = self.builder.get_object("req_cb_x509")
        self.req_cb_x509_days = self.builder.get_object("req_cb_x509_days")
        self.req_cb_x509_days.connect("toggled", self.__cb_x509_days_toggled)
        self.req_x509_days_input = self.builder.get_object("req_x509_days_input")
        self.req_cb_x509_seriano = self.builder.get_object("req_cb_x509_seriano")
        self.req_cb_x509_seriano.connect("toggled", self.__cb_x509_serialno_toggled)
        self.req_x509_seriano_input = self.builder.get_object("req_x509_seriano_input")
        # -- treeview
        self.req_tv_x509_extensions = self.builder.get_object("req_tv_x509_extensions")
        self.req_tv_model = self.req_tv_x509_extensions.get_model()
        self.req_tv_liststore = self.builder.get_object("req_tv_liststore")
        self.req_tv_x509_cb_critico = self.builder.get_object("req_tv_x509_cb_critico")
        self.req_tv_x509_cb_critico.connect("toggled", self.__cb_critical_toggled)
        self.req_tv_x509_cb_nome = self.builder.get_object("req_tv_x509_cb_nome")
        self.req_tv_x509_cb_nome.connect("changed", self.__cb_name_changed)
        self.req_tv_x509_cb_nome.connect("edited", self.__cb_name_edited)
        self.req_liststore_x509_ext_names = self.builder.get_object("req_liststore_x509_ext_names")
        self.req_tv_x509_cb_valor = self.builder.get_object("req_tv_x509_cb_valor")
        self.req_tv_x509_cb_valor.connect("changed", self.__cb_value_changed)
        self.req_tv_x509_cb_valor.connect("edited", self.__cb_value_edited)
        self.req_btn_tv_append_liststore = self.builder.get_object("req_btn_tv_append_liststore")
        self.req_btn_tv_append_liststore.connect("clicked", self.__btn_append_tv_clicked)
        self.req_btn_tv_remove_liststore = builder.get_object("req_btn_tv_remove_liststore")
        self.req_btn_tv_remove_liststore.connect("clicked", self.__btn_remove_selected_tv_clicked)
        # -- liststores values
        self.req_liststore_x509_basicConstraints = self.builder.get_object("req_liststore_x509_basicConstraints")
        self.req_liststore_x509_keyUsage = self.builder.get_object("req_liststore_x509_keyUsage")
        self.req_liststore_x509_subjectKeyIdentifier = self.builder.get_object("req_liststore_x509_subjectKeyIdentifier")
        self.req_liststore_x509_crlDistributionPoints = self.builder.get_object("req_liststore_x509_crlDistributionPoints")
        self.req_liststore_x509_extendedKeyUsage = self.builder.get_object("req_liststore_x509_extendedKeyUsage")
        self.req_liststore_x509_subjectAltName = self.builder.get_object("req_liststore_x509_subjectAltName")
        self.req_liststore_x509_authorityKeyIdentifier = self.builder.get_object("req_liststore_x509_authorityKeyIdentifier")
        self.req_liststore_x509_certificatePolicies = self.builder.get_object("req_liststore_x509_certificatePolicies")
        # -- cb_tv_names_changed
        self.req_tv_x509_cb_nome.connect("changed", self.__liststore_x509_names_changed)

        # output
        self.req_rd_output_format_1 = self.builder.get_object("req_rd_output_format_1")
        self.req_rd_output_format_2 = self.builder.get_object("req_rd_output_format_2")
        self.req_rd_output_format_1.connect("toggled", self.__rd_formato_output_on_toggled)
        self.req_rd_output_format_2.connect("toggled", self.__rd_formato_output_on_toggled)
        self.req_rd_output_type_1 = self.builder.get_object("req_rd_output_type_1")
        self.req_rd_output_type_2 = self.builder.get_object("req_rd_output_type_2")
        self.req_rd_output_type_3 = self.builder.get_object("req_rd_output_type_3")
        self.req_rd_output_type_1.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.req_rd_output_type_2.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.req_rd_output_type_3.connect("toggled", self.__rd_tipo_output_on_toggled)
        self.req_area_output_ficheiro = self.builder.get_object("req_area_output_ficheiro")
        self.req_area_output_ficheiro.set_no_show_all(True)
        self.req_filechooser_output = self.builder.get_object("req_filechooser_output")
        self.req_area_output_pasta = self.builder.get_object("req_area_output_pasta")
        self.req_area_output_pasta.set_no_show_all(True)
        self.req_filechooser_output_pasta = self.builder.get_object("req_filechooser_output_pasta")
        self.req_txt_output_pasta_extra = self.builder.get_object("req_txt_output_pasta_extra")
        self.req_txt_output_pasta_extra.set_text("A file named '"+ self.req_output_pasta_nome_ficheiro +"' will be created at the choosen location")

        # outras
        self.req_outras_subject = self.builder.get_object("req_outras_subject")
        self.req_outras_text = self.builder.get_object("req_outras_text")
        self.req_outras_noout = self.builder.get_object("req_outras_noout")
        self.req_outras_modulus = self.builder.get_object("req_outras_modulus")
        self.req_outras_verify = self.builder.get_object("req_outras_verify")
        self.req_outras_digest = self.builder.get_object("req_outras_digest")
        self.req_outras_digest.connect("toggled", self.__cb_outras_digest)
        self.req_outras_algoritmos_digest = self.builder.get_object("req_outras_algoritmos_digest")
        # -- carregar lista de algoritmos e preencher lista
        pedido_lista_algortimos_checksum = subprocess.Popen(["openssl", "list", "-digest-commands"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pedido_lista_algortimos_checksum.communicate()
        if not stderr:
            for algoritmo in stdout.split():
                self.req_outras_algoritmos_digest.append_text(algoritmo)
        else:
            print("An error as occurred loading digest algorithms")
            self.req_outras_erro_algoritmos_digest = True
            self.req_outras_algoritmos_digest.append_text("An error as occurred loading digest algorithms")
        self.req_outras_precert = self.builder.get_object("req_outras_precert")
        self.req_outras_utf8 = self.builder.get_object("req_outras_utf8")
        self.req_outras_batch = self.builder.get_object("req_outras_batch")
        self.req_outras_rand = self.builder.get_object("req_outras_rand")
        self.req_outras_rand.connect("toggled", self.__cb_outras_rand_toggled)
        self.req_area_ficheiro_rand = self.builder.get_object("req_area_ficheiro_rand")
        self.req_area_ficheiro_rand.set_no_show_all(True)
        self.req_filechooser_rand = self.builder.get_object("req_filechooser_rand")
        self.req_outras_writerand = self.builder.get_object("req_outras_writerand")
        self.req_outras_writerand.connect("toggled", self.__cb_outras_writerand_toggled)
        self.req_area_writerand = self.builder.get_object("req_area_writerand")
        self.req_area_writerand.set_no_show_all(True)
        self.req_rd_writerand_output_file = self.builder.get_object("req_rd_writerand_output_file")
        self.req_rd_writerand_output_folder = self.builder.get_object("req_rd_writerand_output_folder")
        self.req_rd_writerand_output_file.connect("toggled", self.__rd_writerand_output_on_toggled)
        self.req_rd_writerand_output_folder.connect("toggled", self.__rd_writerand_output_on_toggled)
        self.req_area_writerand_ficheiro = self.builder.get_object("req_area_writerand_ficheiro")
        self.req_filechooser_ficheiro_writerand = self.builder.get_object("req_filechooser_ficheiro_writerand")
        self.req_area_writerand_pasta = self.builder.get_object("req_area_writerand_pasta")
        self.req_filechooser_local_writerand = self.builder.get_object("req_filechooser_local_writerand")
        self.req_txt_writerand_pasta_extra = self.builder.get_object("req_txt_writerand_pasta_extra")
        self.req_txt_writerand_pasta_extra.set_text("A file named '" + self.req_writerand_nome_ficheiro + "' will be created at the choosen location")


    def __liststore_x509_names_changed(self, cb, path, iterator_cb):
        col = self.req_liststore_x509_ext_names.get(iterator_cb, 0)
        liststore = None
        if "basicConstraints" in col[0]:
            liststore = self.req_liststore_x509_basicConstraints
        elif "keyUsage" in col[0]:
            liststore = self.req_liststore_x509_keyUsage
        elif "extendedKeyUsage" in col[0]:
            liststore = self.req_liststore_x509_extendedKeyUsage
        elif "subjectKeyIdentifier" in col[0]:
            liststore = self.req_liststore_x509_subjectKeyIdentifier
        elif "authorityKeyIdentifier" in col[0]:
            liststore = self.req_liststore_x509_authorityKeyIdentifier
        elif "subjectAltName" in col[0]:
            liststore = self.req_liststore_x509_subjectAltName
        elif "crlDistributionPoints" in col[0]:
            liststore = self.req_liststore_x509_crlDistributionPoints
        elif "certificatePolicies" in col[0]:
            liststore = self.req_liststore_x509_certificatePolicies
        self.liststorevalues = liststore
        if liststore:
            self.req_tv_x509_cb_valor.set_property("model", liststore)

    def __cb_outras_rand_toggled(self, cb):
        self.req_area_ficheiro_rand.set_visible(cb.get_active())
    
    def __cb_outras_writerand_toggled(self, cb):
        self.req_area_writerand.set_visible(cb.get_active())

    def __rd_writerand_output_on_toggled(self, rd):
        if "File" in rd.get_label() and rd.get_active():
            self.req_writerand_tipo_output = "ficheiro"
            self.req_area_writerand_ficheiro.set_visible(True)
            self.req_area_writerand_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.req_writerand_tipo_output = "pasta"
            self.req_area_writerand_ficheiro.set_visible(False)
            self.req_area_writerand_pasta.set_visible(True)
        else:
            self.req_writerand_tipo_output = "ficheiro"
            self.req_area_writerand_ficheiro.set_visible(True)
            self.req_area_writerand_pasta.set_visible(False)

    def __cb_key_nodes_toggled(self, cb):
        self.req_key_password.set_sensitive(not cb.get_active())

    def __cb_input_passin_toggled(self, cb):
        self.req_input_file_passin.set_sensitive(cb.get_active())

    def __cb_input_format_toggled(self, cb):
        self.req_inform_type.set_sensitive(cb.get_active())
    
    def __cb_input_file_toggled(self, cb):
        self.req_filechooser_input.set_sensitive(cb.get_active())

    def __cb_config_key_file_toggled(self, cb):
        self.req_filechooser_input_config.set_sensitive(cb.get_active())

    def __cb_key_format_toggled(self, cb):
        self.req_input_key_type.set_sensitive(cb.get_active())
    
    def __cb_key_input_key_file_toggled(self, cb):
        self.req_filechooser_input_key.set_sensitive(cb.get_active())

    def __cb_key_output_key_file_toggled(self, cb):
        self.req_filechooser_output_key.set_sensitive(cb.get_active())

    def __cb_x509_days_toggled(self, cb):
        self.req_x509_days_input.set_sensitive(cb.get_active())
    
    def __cb_x509_serialno_toggled(self, cb):
        self.req_x509_seriano_input.set_sensitive(cb.get_active())
        
    def __cb_critical_toggled(self, cb, path):
        iterator_tv = self.req_tv_model.get_iter_from_string(path)
        column_cb = self.req_tv_model.get(iterator_tv, 2)
        if column_cb[0]:
            column_cb = 0
        else:
            column_cb = 1
        self.req_tv_liststore.set(iterator_tv, 2, column_cb)

    def __cb_name_changed(self, cb, path, iterator_cb):
        iterator = self.req_tv_model.get_iter_from_string(path)
        col = self.req_liststore_x509_ext_names.get(iterator_cb, 0)
        self.req_tv_liststore.set(iterator, 0, col[0])

    def __cb_name_edited(self, cellrendercombo, path, text):
        iterator = self.req_tv_model.get_iter_from_string(path)
        self.req_tv_liststore.set(iterator, 0, text)
    
    def __cb_value_changed(self, cb, path, iterator_cb):
        iterator = self.req_tv_model.get_iter_from_string(path)
        if self.liststorevalues:
            col = self.liststorevalues.get(iterator_cb, 0)
        self.req_tv_liststore.set(iterator, 1, col[0])

    def __cb_value_edited(self, cellrendercombo, path, text):
        iterator = self.req_tv_model.get_iter_from_string(path)
        self.req_tv_liststore.set(iterator, 1, text)

    def __btn_append_tv_clicked(self, btn):
        self.req_tv_liststore.append(("", "", 0))

    def __btn_remove_selected_tv_clicked(self, btn):
        selection = self.req_tv_x509_extensions.get_selection()
        (model, pathlist) = selection.get_selected_rows()
        if not pathlist: return

        pathlist.reverse()
        for path in pathlist:
            self.req_tv_liststore.remove(model.get_iter(path))
    
    def __rd_formato_output_on_toggled(self, rd):
        if "PEM" in rd.get_label() and rd.get_active():
            self.req_output_format = "PEM"
        elif "DER" in rd.get_label() and rd.get_active():
            self.req_output_format = "DER"
        else:
            self.req_output_format = "PEM"

    def __rd_tipo_output_on_toggled(self, rd):
        if "popup" in rd.get_label() and rd.get_active():
            self.req_output_type = "output"
            self.req_area_output_ficheiro.set_visible(False)
            self.req_area_output_pasta.set_visible(False)
        elif "File" in rd.get_label() and rd.get_active():
            self.req_output_type = "ficheiro"
            self.req_area_output_ficheiro.set_visible(True)
            self.req_area_output_pasta.set_visible(False)
        elif "Folder" in rd.get_label() and rd.get_active():
            self.req_output_type = "pasta"
            self.req_area_output_ficheiro.set_visible(False)
            self.req_area_output_pasta.set_visible(True)
        else:
            self.req_output_type = "output"
            self.req_area_output_ficheiro.set_visible(False)
            self.req_area_output_pasta.set_visible(False)

    def __cb_outras_digest(self, cb):
        self.req_outras_algoritmos_digest.set_sensitive(cb.get_active())

    def __btn_executar_clicked(self, btn):
        self.req_lbl_erro_config.set_visible(False)
        
        comando = ""
        comando += self.req_comando + " "

        # informacao subject
        comando_subject_info = ""
        if self.req_subject_name.get_text():
            comando_subject_info += "/CN=" + self.req_subject_name.get_text()
        else:
            comando_subject_info += "/CN=undefined"
        if self.req_subject_country.get_text():
            comando_subject_info += "/C=" + self.req_subject_country.get_text()
        if self.req_subject_region.get_text():
            comando_subject_info += "/ST=" + self.req_subject_region.get_text()
        if self.req_subject_city.get_text():
            comando_subject_info += "/L=" + self.req_subject_city.get_text()
        if self.req_subject_organisation.get_text():
            comando_subject_info += "/O=" + self.req_subject_organisation.get_text()
        if self.req_subject_orgunit.get_text():
            comando_subject_info += "/OU=" + self.req_subject_orgunit.get_text()
        if self.req_subject_email.get_text():
            comando_subject_info += "/emailAddress=" + self.req_subject_email.get_text()
        if comando_subject_info:
            comando += " -subj " + comando_subject_info.replace(" ", "\!space!/") + " "
        
        # opcoes input
        if self.req_cb_input_format.get_active():
            comando += " -inform " + self.req_inform_type.get_active_text() + " "
        if self.req_cb_input_file.get_active():
            ficheiro = self.req_filechooser_input.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the input file in input settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -keyform " + ficheiro.replace(" ", "\!space!/") + " "
        if self.req_cb_input_config.get_active():
            ficheiro = self.req_filechooser_input_config.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the config file in input settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -keyform " + ficheiro.replace(" ", "\!space!/") + " "
        if self.req_cb_input_passin.get_active():
            if not self.req_input_file_passin.get_text():
                txt_lbl_erro = "You must insert a password for the input file in input settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -passin pass:" + self.req_input_file_passin.get_text().replace(" ", "\!space!/")  + " "
        

        # opcoes key
        if self.req_cb_input_key_format.get_active():
            comando += " -keyform " + self.req_input_key_type.get_active_text() + " "
        if self.req_cb_input_key.get_active():
            ficheiro = self.req_filechooser_input_key.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the input file in key settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -key " + ficheiro.replace(" ", "\!space!/") + " "
        if self.req_cb_output_key.get_active():
            ficheiro = self.req_filechooser_output_key.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the output key file in key settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -keyout " + ficheiro.replace(" ", "\!space!/") + " "
        if self.req_cb_output_pubkey.get_active():
            comando += " -pubkey "
        if self.req_key_cb_new_key.get_active():
            comando += " -new "
        if self.req_key_cb_nodes.get_active():
            comando += " -nodes "
        else:
            password = self.req_key_password.get_text()
            if not password:
                txt_lbl_erro = "Nodes disabled! You must insert a password in key settings"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -passout pass:" + password.replace(" ", "\!space!/") + " "

        # obter opcoes x509
        if self.req_cb_x509.get_active():
            comando += " -x509 "
            if self.req_cb_x509_days.get_active():
                if self.req_x509_days_input.get_value() is not None:
                    comando += " -days " + str(self.req_x509_days_input.get_value()).replace(".0", "") + " "
                else:
                    comando += " -days 30 "
            if self.req_cb_x509_seriano.get_active():
                if self.req_x509_seriano_input.get_value() is not None:
                    comando += " -set_serial " + str(self.req_x509_seriano_input.get_value()).replace(".0", "") + " "
                else:
                    comando += " -set_serial 0 "
            for treemodelrow in self.req_tv_liststore:
                if (treemodelrow[2] == 1 or treemodelrow[2] == True) and treemodelrow[0] is not None and treemodelrow[1] is not None:
                    comando += " -addext " + str(treemodelrow[0]) + "=critical," + str(treemodelrow[1]) + " "
                else:
                    comando += " -addext " + str(treemodelrow[0]) + "=" + str(treemodelrow[1]) + " "
        
        # outras
        if self.req_outras_subject.get_active():
            comando += " -subject "
        if self.req_outras_text.get_active():
            comando += " -text "
        if self.req_outras_noout.get_active():
            comando += " -noout "
        if self.req_outras_modulus.get_active():
            comando += " -modulus "
        if self.req_outras_verify.get_active():
            comando += " -verify "
        if self.req_outras_digest.get_active():
            if not self.req_outras_algoritmos_digest.get_active_text() == "An error as occurred loading digest algorithms" and not self.req_outras_algoritmos_digest.get_active_text() == "Select option...": 
                comando += " -" + self.req_outras_algoritmos_digest.get_active_text() + " "
            else:
                comando += " -sha256 "
        if self.req_outras_precert.get_active():
            comando += " -precert "
        if self.req_outras_utf8.get_active():
            comando += " -utf8 "
        if self.req_outras_batch.get_active():
            comando += " -batch "

        
        if self.req_outras_rand.get_active():
            ficheiro = self.req_filechooser_rand.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You checked '-rand' option in 'Other options'. You must select a Rand file."
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                comando += " -rand " + ficheiro.replace(" ", "\!space!/")

        ficheiro_local_writerand = ""
        if self.req_outras_writerand.get_active():
            if self.req_writerand_tipo_output == "ficheiro":
                ficheiro = self.req_filechooser_ficheiro_writerand.get_filename()
                if not ficheiro:
                    txt_lbl_erro = "You must select a file for the writerand output"
                    self.req_lbl_erro_config.set_text(txt_lbl_erro)
                    self.req_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = ficheiro
            elif self.req_writerand_tipo_output == "pasta":
                pasta = self.req_filechooser_local_writerand.get_filename()
                if not pasta:
                    txt_lbl_erro = "You must select a location for the writerand output file"
                    self.req_lbl_erro_config.set_text(txt_lbl_erro)
                    self.req_lbl_erro_config.set_visible(True)
                    return
                else:
                    ficheiro_local_writerand = pasta + "/" + self.req_writerand_nome_ficheiro

        if ficheiro_local_writerand:
            comando += " -writerand " + ficheiro_local_writerand.replace(" ", "\!space!/")


        # -- verificar e selecionar o local do output do resultado
        ficheiro_local_output = ""
        if self.req_output_type == "ficheiro":
            ficheiro = self.req_filechooser_output.get_filename()
            if not ficheiro:
                txt_lbl_erro = "You must select a file for the output in output options"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = ficheiro

        elif self.req_output_type == "pasta":
            pasta = self.req_filechooser_output_pasta.get_filename()
            if not pasta:
                txt_lbl_erro = "You must select a location for the output in output options"
                self.req_lbl_erro_config.set_text(txt_lbl_erro)
                self.req_lbl_erro_config.set_visible(True)
                return
            else:
                ficheiro_local_output = pasta + "/" + self.req_output_pasta_nome_ficheiro

        if ficheiro_local_output:
            comando += " -out " + ficheiro_local_output.replace(" ", "\!space!/")

        # outras verificações
        # -- se não possuir -in, nem ser -x509, necessária opção -new ou -newkey
        if "-in" not in comando and "-x509" not in comando and "-new" not in comando:
            comando += " -new "

        lista = comando.split()
        comando_final = []
        for p in lista:
            comando_final.append(p.replace("\!space!/", " "))

        # -- tentar executar
        try:
            exec_comando_req = subprocess.Popen(comando_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            #if self.rand_formato_output == "default":
                # necessário passar pelo xxd se o output for binário, noutro caso o python tenta intrepertar cada byte
            #    xxd = subprocess.Popen(["xxd", "-b"], stdin=exec_comando_req.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            #    stdout, stderr = xxd.communicate()
            #else:
            #    stdout, stderr = exec_comando_req.communicate()
            stdout, stderr = exec_comando_req.communicate()

            # -- verificar qual o local para o output
            if self.req_output_type == "popup":
                #if not stderr or (stdout and stderr):
                #    Popup_Resultado_Class(stderr + "\n" + stdout)
                #else:
                #    Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(stderr))
                Popup_Resultado_Class(stderr + "\n" + stdout)
            elif self.req_output_type == "ficheiro" or self.req_output_type == "pasta" :
                #if not stderr or (stdout and stderr):
                #    Popup_Resultado_Class("Command executed successfully! Check the output file")
                #else:
                #    Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(stderr))
                Popup_Resultado_Class(stderr + "\n" + stdout)

        except Exception as e:
            Popup_Erro_Class("Error", "An error as occurred trying to execute the rand command! See details...", str(e))