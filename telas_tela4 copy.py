import flet as ft
import estado

def tela_4(page: ft.Page, render):

    t4_q1 = ft.Dropdown(
        label="Motivo",
        options=[
            ft.dropdown.Option("Trabalho"),
            ft.dropdown.Option("Lazer"),
            ft.dropdown.Option("Outros"),
        ],
    )

    def salvar():
        estado.respostas["t4_q1"] = t4_q1.value

    def finalizar(e):
        salvar()
        # por enquanto só imprime
        print("ENTREVISTA:", estado.respostas)
        estado.tela_atual = "setup"
        render()

    return ft.Column(
        controls=[
            ft.Text("Tela 4 – Finalização", size=18),
            t4_q1,
            ft.ElevatedButton("Finalizar", on_click=finalizar),
        ],
        spacing=15,
    )
