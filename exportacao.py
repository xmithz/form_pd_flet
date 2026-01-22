import flet as ft
import estado

def exportar(page: ft.Page, render):

    ft.Text(
        "Este botao ira exportar as coisas",
        size=12,
        color=ft.Colors.GREY_300,
        text_align=ft.TextAlign.CENTER,
    )
    
    print(estado.respostas)