import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Catálogo de Componentes Flet"
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.YELLOW_50
    page.window_width = 400
    page.window_height = 700

    # --- 1. Botões (Ações e Escolhas Binárias) ---
    # Úteis para "Sim/Não", "Seguir", "Voltar" ou escolhas rápidas (ex: Carro vs Trem)
    btn_elevated = ft.ElevatedButton("Elevated (Principal)")
    btn_outlined = ft.OutlinedButton("Outlined (Secundário)")
    btn_icon = ft.IconButton(icon=ft.Icons.THUMB_UP, tooltip="Icon Button")

    # --- 2. Radio Group (Melhor para 2 a 7 opções) ---
    # O usuário vê todas as opções de uma vez.
    radio_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="op1", label="Opção 1 (Radio)"),
            ft.Radio(value="op2", label="Opção 2 (Radio)"),
            ft.Radio(value="op3", label="Opção 3 (Radio)"),
        ])
    )

    # --- 3. Dropdown (Melhor para 7 a 15 opções) ---
    # Economiza espaço vertical.
    dropdown = ft.Dropdown(
        label="Selecione (Dropdown)",
        options=[
            ft.dropdown.Option("Opção A"),
            ft.dropdown.Option("Opção B"),
            ft.dropdown.Option("Opção C"),
        ],
    )

    # --- 4. Campos de Texto e Numéricos ---
    txt_texto = ft.TextField(label="Texto Livre")
    
    # Campo numérico otimizado para celular (abre teclado numérico)
    txt_numero = ft.TextField(
        label="Duração",
        suffix=ft.Text("min"), # Texto fixo no final
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )

    # --- 5. Checkbox e Switch (Booleanos / Liga-Desliga) ---
    checkbox = ft.Checkbox(label="Checkbox (Múltipla escolha)", value=False)
    switch = ft.Switch(label="Switch (Ativar/Desativar)", value=True)
    
    # Switch com labels dos dois lados (Sol vs Chuva)
    # O componente Switch nativo só aceita um label, então usamos uma Row para criar esse layout.
    switch_duplo = ft.Row(
        controls=[
            ft.Text("Sol", size=16),
            ft.Switch(), # Sem label interno
            ft.Text("Chuva", size=16),
        ],
    )

    # --- 6. Slider (Valores em Faixa/Escala) ---
    # Bom para notas de 0 a 10 ou porcentagens
    slider = ft.Slider(min=0, max=10, divisions=10, label="Nota: {value}")

    # --- 7. DatePicker (Seletor de Data) ---
    # 1. Criar o componente
    date_picker = ft.DatePicker(
        first_date=datetime.datetime(2023, 1, 1),
        last_date=datetime.datetime(2030, 12, 31),
    )
    # 2. Adicionar ao overlay da página (obrigatório)
    page.overlay.append(date_picker)

    # 3. Função para mostrar o resultado
    txt_data_result = ft.Text("Nenhuma data selecionada")
    def on_date_change(e):
        # Atualiza o texto com a data formatada
        txt_data_result.value = f"Data: {date_picker.value.strftime('%d/%m/%Y')}" if date_picker.value else "Cancelado"
        page.update()
    
    date_picker.on_change = on_date_change

    def abrir_data(e):
        date_picker.open = True
        date_picker.update()

    btn_date = ft.ElevatedButton(
        "Abrir Calendário",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_data,
    )

    # --- 8. TimePicker (Seletor de Hora) ---
    time_picker = ft.TimePicker(confirm_text="Confirmar", help_text="Selecione a hora")
    page.overlay.append(time_picker)

    txt_time_result = ft.Text("Nenhuma hora selecionada")
    def on_time_change(e):
        txt_time_result.value = f"Hora: {time_picker.value.strftime('%H:%M')}" if time_picker.value else "Cancelado"
        page.update()
    
    time_picker.on_change = on_time_change

    def abrir_hora(e):
        time_picker.open = True
        time_picker.update()

    btn_time = ft.ElevatedButton(
        "Escolher Hora",
        icon=ft.Icons.ACCESS_TIME,
        on_click=abrir_hora,
    )

    # --- 9. Duração (Dropdowns - Alternativa "Tambor") ---
    # Simula a rapidez de um seletor de iPhone usando dois dropdowns lado a lado
    dd_horas = ft.Dropdown(
        label="H",
        width=100,
        options=[ft.dropdown.Option(str(i)) for i in range(13)], # 0 a 12h
    )
    
    dd_minutos = ft.Dropdown(
        label="Min",
        width=100,
        options=[ft.dropdown.Option(f"{i:02d}") for i in range(0, 60, 5)], # 00, 05, 10...
    )
    
    txt_duracao_result = ft.Text("Duração: --")
    
    def ver_duracao(e):
        h = dd_horas.value if dd_horas.value else "0"
        m = dd_minutos.value if dd_minutos.value else "00"
        txt_duracao_result.value = f"Tempo: {h}h {m}min"
        page.update()
        
    btn_duracao = ft.ElevatedButton("Confirmar Duração", on_click=ver_duracao)

    # --- 10. Cupertino Picker (Tambor Customizado - Minutos 5 em 5) ---
    # Usando o componente genérico para criar um seletor de duração personalizado
    
    # Listas de opções
    opcoes_horas = [str(i) for i in range(24)]
    opcoes_minutos = [f"{i:02d}" for i in range(0, 60, 5)] # 00, 05, 10...

    txt_cupertino = ft.Text("Tambor: 0h 00min")
    
    # Estado local para armazenar índices selecionados
    indices = {"h": 0, "m": 0}

    def atualizar_tambor():
        h = opcoes_horas[indices["h"]]
        m = opcoes_minutos[indices["m"]]
        txt_cupertino.value = f"Tambor: {h}h {m}min"
        page.update()

    def change_h(e):
        indices["h"] = int(e.data) # e.data retorna o índice selecionado
        atualizar_tambor()

    def change_m(e):
        indices["m"] = int(e.data)
        atualizar_tambor()

    # Container para segurar os pickers com altura definida
    container_tambor = ft.Container(
        height=150,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.CupertinoPicker(
                    selected_index=0, magnification=1.22, squeeze=1.2, use_magnifier=True,
                    item_extent=32, width=50, on_change=change_h,
                    controls=[ft.Text(h) for h in opcoes_horas],
                ),
                ft.Text("h", size=16, weight=ft.FontWeight.BOLD),
                ft.CupertinoPicker(
                    selected_index=0, magnification=1.22, squeeze=1.2, use_magnifier=True,
                    item_extent=32, width=50, on_change=change_m,
                    controls=[ft.Text(m) for m in opcoes_minutos],
                ),
                ft.Text("min", size=16, weight=ft.FontWeight.BOLD),
            ]
        )
    )

    # --- 11. Seleção Visual (Ícones Interativos) ---
    # Exemplo solicitado: Clima (Sol, Nublado, Chuva)
    btn_sol = ft.IconButton(icon=ft.Icons.WB_SUNNY, icon_size=40, tooltip="Sol")
    btn_nublado = ft.IconButton(icon=ft.Icons.CLOUD, icon_size=40, tooltip="Sol Encoberto")
    btn_chuva = ft.IconButton(icon=ft.Icons.UMBRELLA, icon_size=40, tooltip="Chuva")
    
    txt_clima_sel = ft.Text("Clima: Sol")

    def update_clima(modo):
        # Reseta todos para cinza
        btn_sol.icon_color = ft.Colors.GREY_300
        btn_nublado.icon_color = ft.Colors.GREY_300
        btn_chuva.icon_color = ft.Colors.GREY_300
        
        # Ativa o selecionado
        if modo == "sol":
            btn_sol.icon_color = ft.Colors.ORANGE
            txt_clima_sel.value = "Clima: Sol"
        elif modo == "nublado":
            btn_nublado.icon_color = ft.Colors.GREY_700
            txt_clima_sel.value = "Clima: Sol Encoberto"
        elif modo == "chuva":
            btn_chuva.icon_color = ft.Colors.BLUE
            txt_clima_sel.value = "Clima: Chuva"
        page.update()

    btn_sol.on_click = lambda e: update_clima("sol")
    btn_nublado.on_click = lambda e: update_clima("nublado")
    btn_chuva.on_click = lambda e: update_clima("chuva")
    
    # Inicializar estado visual
    update_clima("sol")

    # Adicionando tudo à página para visualização
    page.add(
        ft.Text("1. Botões", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([btn_elevated, btn_outlined, btn_icon]),
        ft.Divider(),

        ft.Text("2. Radio (Listas Curtas)", size=20, weight=ft.FontWeight.BOLD),
        radio_group,
        ft.Divider(),

        ft.Text("3. Dropdown (Listas Médias)", size=20, weight=ft.FontWeight.BOLD),
        dropdown,
        ft.Divider(),

        ft.Text("4. Inputs", size=20, weight=ft.FontWeight.BOLD),
        txt_texto,
        txt_numero,
        ft.Divider(),

        ft.Text("5. Booleanos & Slider", size=20, weight=ft.FontWeight.BOLD),
        checkbox,
        switch,
        switch_duplo,
        slider,
        ft.Divider(),

        ft.Text("6. Data e Hora", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([btn_date, txt_data_result], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([btn_time, txt_time_result], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        
        ft.Divider(),
        ft.Text("7. Duração (Estilo Tambor)", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([dd_horas, ft.Text("h"), dd_minutos, ft.Text("min")], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([btn_duracao, txt_duracao_result], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        
        ft.Divider(),
        ft.Text("8. Tambor Real (Cupertino)", size=20, weight=ft.FontWeight.BOLD),
        container_tambor,
        txt_cupertino,
        
        ft.Divider(),
        ft.Text("9. Clima (Ícones)", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([btn_sol, btn_nublado, btn_chuva, txt_clima_sel], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

if __name__ == "__main__":
    ft.app(target=main)
