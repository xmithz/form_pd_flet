import flet as ft
import estado

def tela_3(page: ft.Page, render):

    # Armazena as seleções atuais localmente
    selecoes = {
        "t3_q1": None, # Modo Origem
        "t3_q2": None, # Modo Destino
        "t3_q3": None, # Transferências
        "t3_q4": None  # Escolaridade
    }

    # Controle visual dos títulos (para marcar de vinho no erro)
    labels_controle = {}

    # --- Helper: Seletor Simples (Apenas Botões) ---
    def criar_seletor_simples(label, opcoes, chave):
        botoes = []
        
        def on_click(e):
            valor = e.control.data
            selecoes[chave] = valor
            
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
                ft.Row(controls=botoes, spacing=10, run_spacing=10, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # --- Helper: Seletor Misto (Botões + Campo de Texto "Outros") ---
    def criar_seletor_misto(label, opcoes_btn, chave):
        botoes = []
        txt_outros = ft.TextField(
            label="Outros (especifique)",
            label_style=ft.TextStyle(size=12),
            width=220,
            height=40,
            text_size=12,
            content_padding=10
        )

        def atualizar_estilo_botoes(valor_selecionado):
            for btn in botoes:
                txt = btn.content
                if btn.data == valor_selecionado:
                    btn.style.bgcolor = {"": ft.Colors.BLUE_200}
                    txt.weight = ft.FontWeight.BOLD
                else:
                    btn.style.bgcolor = {"": ft.Colors.GREY_100}
                    txt.weight = ft.FontWeight.NORMAL
                btn.update()

        def on_btn_click(e):
            valor = e.control.data
            selecoes[chave] = valor
            txt_outros.value = "" # Limpa o campo de texto se clicar no botão
            txt_outros.update()
            atualizar_estilo_botoes(valor)

        def on_text_change(e):
            valor = txt_outros.value
            if valor:
                selecoes[chave] = valor
                atualizar_estilo_botoes(None) # Desmarca visualmente os botões
            else:
                selecoes[chave] = None

        txt_outros.on_change = on_text_change

        for opt in opcoes_btn:
            btn = ft.ElevatedButton(
                content=ft.Text(opt, color=ft.Colors.BLACK, size=13),
                data=opt,
                width=100,
                height=40,
                on_click=on_btn_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    bgcolor={"": ft.Colors.GREY_100},
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
                    controls=botoes + [txt_outros],
                    spacing=10,
                    run_spacing=10,
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # --- Definição das Questões ---
    
    # 3_1: Modo Origem (Misto)
    q1_origem = criar_seletor_misto("Modo de Acesso (Origem)", ["A pé", "Carro", "APP/Taxi", "Coletivo"], "t3_q1")
    
    # 3_2: Modo Destino (Misto)
    q2_destino = criar_seletor_misto("Modo de Saída (Destino)", ["A pé", "Carro", "APP/Taxi", "Coletivo"], "t3_q2")

    # 3_3: Transferências (Simples)
    q3_transf = criar_seletor_simples("Qtd. Transferências", ["0", "1", "2+"], "t3_q3")

    # 3_4: Escolaridade (Simples)
    q4_escolaridade = criar_seletor_simples("Escolaridade", ["Básico", "Médio", "Superior+"], "t3_q4")

    # --- Validação e Navegação ---
    tentativa_sem_preencher = False
    txt_erro = ft.Text("", color=ft.Colors.RED_900, size=12, visible=False, text_align=ft.TextAlign.CENTER)

    def processar_saida(destino):
        nonlocal tentativa_sem_preencher
        campos_vazios = []
        
        nomes_campos = {
            "t3_q1": "Origem",
            "t3_q2": "Destino",
            "t3_q3": "Transferências",
            "t3_q4": "Escolaridade"
        }

        # Verifica campos vazios e marca labels
        for chave, valor in selecoes.items():
            if not valor:
                campos_vazios.append(nomes_campos.get(chave, chave))
                labels_controle[chave].color = ft.Colors.RED_900 # Vinho
            else:
                labels_controle[chave].color = ft.Colors.BLACK
            labels_controle[chave].update()

        if campos_vazios and not tentativa_sem_preencher:
            tentativa_sem_preencher = True
            txt_erro.value = f"Os campos em vermelho ({', '.join(campos_vazios)}) não foram preenchidos.\nPreencha ou clique novamente para prosseguir."
            txt_erro.visible = True
            txt_erro.update()
            return

        # Salva no estado global
        estado.respostas.update(selecoes)
        
        if destino == "encerrar":
            print("PESQUISA ENCERRADA (PARCIAL):", estado.respostas)
            estado.tela_atual = "setup"
        else:
            estado.tela_atual = "t4"
        
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
                ft.Text("Detalhes do Deslocamento", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                q1_origem,
                q2_destino,
                q3_transf,
                q4_escolaridade,
                ft.Divider(),
                txt_erro,
                ft.Row(
                    controls=[
                        ft.OutlinedButton("Encerrar", on_click=lambda e: processar_saida("encerrar"), height=45, width=140),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ARROW_FORWARD),
                                    ft.Text("Continuar"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            height=45,
                            width=140,
                            on_click=lambda e: processar_saida("continuar"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
            ],
        ),
    )
