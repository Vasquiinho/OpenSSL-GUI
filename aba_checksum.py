import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Aba_Checksum:
    def __init__(self, builder):
        # ---------------- TAB CHECKSUMS ----------------
        # -- carregar lista de algoritmos e preencher lista
        pedido_lista_algortimos_checksum = subprocess.Popen(["openssl", "list", "-digest-commands"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pedido_lista_algortimos_checksum.communicate()

        cb_checksums_algoritmos = builder.get_object("cb_checksums_lista_algoritmos")
        if not stderr:
            for algoritmo in stdout.split():
                cb_checksums_algoritmos.append_text(algoritmo)
        else:
            print("An error as occurred loading checksum algorithms")
            cb_checksums_algoritmos.append_text("An error as occurred loading checksum algorithms")
            builder.get_object("aba_checksums").set_sensitive(False)

        cb_checksums_algoritmos.connect("changed", self.__cb_checksums_algoritmos_changed)

    
    def __cb_checksums_algoritmos_changed(self, cb):
        print(cb.get_active_text())
