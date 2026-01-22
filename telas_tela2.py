import flet as ft
import estado

def tela_2(page: ft.Page, render):

    def escolher(valor):
        estado.respostas["t2_q1"] = valor
        estado.tela_atual = "t3"
        render()

    def encerrar(e):
        estado.tela_atual = "setup"
        print("Parcial:", estado.respostas)
        render()

    return ft.Column(
        controls=[
            ft.Text("Pesquisa de preferência", size=18),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Image(src="kart.png", width=150, height=100, fit="contain"),
                        ft.Text("CARRO"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                height=150,
                on_click=lambda e: escolher("A"),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Image(src="BRT.png", width=150, height=100, fit="contain"),
                        ft.Text("TREM"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                height=150,
                on_click=lambda e: escolher("B"),
            ),
            ft.OutlinedButton("Encerrar", on_click=encerrar),
        ],
        spacing=15,
    )
