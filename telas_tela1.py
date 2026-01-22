import flet as ft
import estado

def tela_1(page: ft.Page, render):
    t1_q1 = ft.Dropdown(
        label="Origem",
        options=[
            ft.dropdown.Option("RMSP"),
            ft.dropdown.Option("Sorocaba"),
            ft.dropdown.Option("São Roque"),
            ft.dropdown.Option("Outros"),
        ],
        width=300,
    )
    t1_q2 = ft.TextField(label="Frequência mensal", width=300)

    def salvar_parcial():
        estado.respostas["t1_q1"] = t1_q1.value
        estado.respostas["t1_q2"] = t1_q2.value

    def seguir(e):
        salvar_parcial()
        estado.tela_atual = "t2"
        render()

    def encerrar(e):
        salvar_parcial()
        estado.tela_atual = "setup"
        print("Parcial:", estado.respostas)
        render()

    return ft.Container(
        alignment=ft.Alignment(0, 0),
        expand=True,
        content=ft.Column(
            width=360,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Identificação da Viagem", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Dados sobre origem e frequência", size=12, color=ft.Colors.GREY_600),
                
                ft.Divider(),
                
                t1_q1,
                t1_q2,
                
                ft.Divider(),
                
                ft.Row(
                    controls=[
                        ft.OutlinedButton("Encerrar", on_click=encerrar, width=120),
                        ft.ElevatedButton("Seguir", on_click=seguir, width=120),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
    )
