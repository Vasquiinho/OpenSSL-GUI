#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Popup_Erro_Class(Gtk.Dialog):
    window = None
    def __init__(self, titulo, descricao, detalhes, termina_programa = False):
        builder = Gtk.Builder()
        builder.add_from_file("GUI/popup_erro.glade")
        builder.connect_signals(Handler_popup_erro(self))

        label_titulo = builder.get_object("popup_erro_titulo")
        label_titulo.set_text(titulo)

        label_descricao = builder.get_object("popup_erro_descricao")
        label_descricao.set_text(descricao)

        textview_detalhe = builder.get_object("popup_erro_detalhes")
        textview_detalhe.get_buffer().set_text(detalhes)

        self.window = builder.get_object("base")
        self.window.connect("delete-event", self.delete_event)
        self.window.show_all()

        self.termina_programa = termina_programa


    def delete_event(self, *args):
        self.window.destroy()
        if __name__ == "__main__" or self.termina_programa:
            exit(1)

class Handler_popup_erro:
    popup = None
    def __init__(self, popup):
        self.popup = popup

    def popup_erro_btn_fechar_clique(self, button):
        self.popup.window.destroy()
        if __name__ == "__main__" or self.popup.termina_programa:
            exit(1)


def main():
    Popup_Erro_Class("Teste", "Desc", "Detalhe\ndefsaf")
    Gtk.main()

if __name__ == "__main__":
    main()
