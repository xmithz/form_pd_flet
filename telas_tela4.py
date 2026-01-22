import flet as ft
import estado

def tela_4(page: ft.Page, render):

    # Armazena as seleções atuais localmente
    selecoes = {
        "t4_q1": None, # Sexo
        "t4_q2": None, # Faixa Etária
        "t4_q3": None  # Renda
    }

    # Dicionário para guardar referências aos labels (títulos) para mudar a cor no erro
    labels_controle = {}

    # Função auxiliar para criar grupos de botões de seleção única
    def criar_seletor(label, opcoes, chave):
        botoes = []
        
        def on_click(e):
            valor = e.control.data
            selecoes[chave] = valor
            
            # Atualiza visualmente os botões do grupo
            for btn in botoes:
                txt = btn.content
                if btn.data == valor:
                    btn.style.bgcolor = {"": ft.Colors.BLUE_200}
                    txt.weight = ft.FontWeight.BOLD
                else:
                    btn.style.bgcolor = {"": ft.Colors.GREY_100}
                    txt.weight = ft.FontWeight.NORMAL
                btn.update()

        for opt in opcoes:
            btn = ft.ElevatedButton(
                content=ft.Text(opt, color=ft.Colors.BLACK, size=13),
                data=opt,
                width=100,
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    bgcolor={"": ft.Colors.GREY_100},
                    color={"": ft.Colors.BLACK},
                    elevation={"": 0},
                    padding={"": 0},
                )
            )
            botoes.append(btn)
        
        txt_label = ft.Text(label, weight=ft.FontWeight.BOLD)
        labels_controle[chave] = txt_label

        return ft.Column(
            controls=[
                txt_label,
                ft.Row(
                    controls=botoes,
                    spacing=10,
                    run_spacing=10,
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # --- 4_1: Sexo ---
    grupo_sexo = criar_seletor("Sexo", ["M", "F", "NI"], "t4_q1")

    # --- 4_2: Faixa Etária ---
    grupo_idade = criar_seletor("Faixa Etária", ["14-17", "18-34", "35-50", "50-64", "65+", "NI"], "t4_q2")

    # --- 4_3: Percepção Renda ---
    grupo_renda = criar_seletor("Percepção de Renda", ["Baixa", "Média", "Alta"], "t4_q3")

    # --- 4_9: Observações ---
    txt_obs = ft.TextField(
        label="Observações",
        multiline=True,
        min_lines=3,
        max_lines=3,
        width=300,
    )

    # Controle de validação
    tentativa_sem_preencher = False
    txt_erro = ft.Text(
        "",
        color=ft.Colors.RED,
        size=12,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    def finalizar(e):
        nonlocal tentativa_sem_preencher
        
        campos_vazios = []
        
        # Validação com feedback visual nos títulos
        if not selecoes["t4_q1"]: 
            campos_vazios.append("Sexo")
            labels_controle["t4_q1"].color = ft.Colors.RED
        else:
            labels_controle["t4_q1"].color = ft.Colors.BLACK
            
        if not selecoes["t4_q2"]: 
            campos_vazios.append("Faixa Etária")
            labels_controle["t4_q2"].color = ft.Colors.RED
        else:
            labels_controle["t4_q2"].color = ft.Colors.BLACK
            
        if not selecoes["t4_q3"]: 
            campos_vazios.append("Renda")
            labels_controle["t4_q3"].color = ft.Colors.RED
        else:
            labels_controle["t4_q3"].color = ft.Colors.BLACK

        # Atualiza visualmente os labels
        for lbl in labels_controle.values():
            lbl.update()
        
        if campos_vazios and not tentativa_sem_preencher:
            tentativa_sem_preencher = True
            txt_erro.value = f"Campos obrigatórios vazios: {', '.join(campos_vazios)}.\nClique novamente para finalizar mesmo assim."
            txt_erro.visible = True
            txt_erro.update()
            return

        # Salvar dados
        estado.respostas["t4_q1"] = selecoes["t4_q1"]
        estado.respostas["t4_q2"] = selecoes["t4_q2"]
        estado.respostas["t4_q3"] = selecoes["t4_q3"]
        estado.respostas["t4_q9"] = txt_obs.value

        print("ENTREVISTA FINALIZADA:", estado.respostas)
        estado.tela_atual = "setup"
        render()

    return ft.Container(
        alignment=ft.Alignment(0, 0),
        expand=True,
        content=ft.Column(
            width=360,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Perfil do Entrevistado", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                grupo_sexo,
                grupo_idade,
                grupo_renda,
                
                ft.Divider(),
                txt_obs,
                
                txt_erro,
                
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK),
                            ft.Text("Finalizar Pesquisa"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    height=45,
                    width=300,
                    on_click=finalizar,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                    )
                ),
                ft.Container(height=20), # Espaço extra no final
            ],
        ),
    )
