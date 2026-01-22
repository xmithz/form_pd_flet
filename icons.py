import flet as ft

icones = [attr for attr in dir(ft.Icons) if attr.isupper()]

for nome in icones:
    print(nome)
