import flet as ft
import estado

def tela_2(page: ft.Page, render):

    def escolher(valor):
        estado.respostas["t2_q1"] = valor
        estado.tela_atual = "t3"
        render()

    def encerrar(e):
        estado.tela_atual = "setup"
        render()

    return ft.Column(
        controls=[
            ft.Text("Pesquisa de preferência", size=18),
            ft.ElevatedButton("CARRO", on_click=lambda e: escolher("A")),
            ft.ElevatedButton("TREM", on_click=lambda e: escolher("B")),
            ft.OutlinedButton("Encerrar", on_click=encerrar),
        ],
        spacing=15,
    )
