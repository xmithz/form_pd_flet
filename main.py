from datetime import datetime
import flet as ft
import estado

from telas_setup import tela_setup
from telas_tela1 import tela_1
from telas_tela2 import tela_2
from telas_tela3 import tela_3
from telas_tela4 import tela_4
from exportacao import exportar

def main(page: ft.Page):
    page.title = "Pesquisa"

    # --- Trava de Segurança (Validade) ---
    data_limite = datetime(2026, 4, 30)

    if datetime.now() >= data_limite:
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(
            ft.Icon(ft.Icons.LOCK_CLOCK, size=60, color=ft.Colors.RED),
            ft.Text("Versão Expirada", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_900),
            ft.Text("O período de utilização desta versão encerrou em 30/04/2026.\nPor favor, instale uma nova versão.", text_align=ft.TextAlign.CENTER),
        )
        return

    # comandos nao funcionam. recomendacao é centralizar e configurar cada tela
    #page.window_width = 400
    #page.window_height = 400
    #page.window_min_width = 400
    #page.window_min_height = 400
    #page.window_resizable = False
    #page.window.center()

    def render():
        page.controls.clear()
        if estado.tela_atual == "setup":
            page.add(tela_setup(page, render))
        elif estado.tela_atual == "t1":
            page.add(tela_1(page, render))
        elif estado.tela_atual == "t2":
            page.add(tela_2(page, render))
        elif estado.tela_atual == "t3":
            page.add(tela_3(page, render))
        elif estado.tela_atual == "t4":
            page.add(tela_4(page, render))
        elif estado.tela_atual == "exp":
            page.add(exportar(page, render))
        page.update()

    render()

ft.run(main)
