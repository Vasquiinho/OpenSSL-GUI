#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Popup_Resultado_Class(Gtk.Dialog):
    window = None
    def __init__(self, txt):
        builder = Gtk.Builder()
        builder.add_from_file("GUI/popup_resultado.glade")
        builder.connect_signals(Handler_popup_resultado(self))

        txt_resultado = builder.get_object("popup_resultado_txt")
        txt_resultado.get_buffer().set_text(txt, len(txt))

        self.window = builder.get_object("base")
        self.window.connect("delete-event", self.delete_event)
        self.window.show_all()


    def delete_event(self, *args):
        self.window.destroy()
        if __name__ == "__main__":
            exit(1)

class Handler_popup_resultado:
    popup = None
    def __init__(self, popup):
        self.popup = popup

    def popup_resultado_btn_fechar_clique(self, button):
        self.popup.window.destroy()
        if __name__ == "__main__":
            exit(1)


#def main():
#    Popup_Resultado_Class("texto\nteste")
#    Gtk.main()

#if __name__ == "__main__":
#    main()
