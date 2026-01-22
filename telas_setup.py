import flet as ft
import estado
import uuid
from datetime import datetime

def tela_setup(page: ft.Page, render):

    # --- S_4: Nome do Pesquisador ---
    s4_nome = ft.TextField(
        label="Nome do pesquisador",
        value=estado.setup_cache.get("S_4", ""),
        width=300,
    )

    # Texto de erro manual para o campo Nome (já que helper_text não existe nesta versão)
    s4_erro_msg = ft.Container(
        content=ft.Text("Obrigatório", color=ft.Colors.RED_900, size=12),
        visible=False,
        width=300,
        padding=ft.padding.only(left=12), # Simula o recuo padrão do Material Design
    )

    # --- S_5: Local Posto (Dropdown 1 a 7) ---
    s5_posto = ft.Dropdown(
        label="Local / Posto",
        options=[ft.dropdown.Option(f"Posto {i}") for i in range(1, 8)],
        value=estado.setup_cache.get("S_5"),
        width=300,
    )

    # --- S_6: Sentido (Switch: Interior vs São Paulo) ---
    s6_switch = ft.Switch(value=(estado.setup_cache.get("S_6") == "São Paulo"))
    s6_container = ft.Row(
        controls=[
            ft.Text("Interior", weight=ft.FontWeight.BOLD),
            s6_switch,
            ft.Text("São Paulo", weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- S_7: Condições Climáticas (Ícones) ---
    btn_sol = ft.IconButton(icon=ft.Icons.WB_SUNNY, icon_size=40, tooltip="Sol")
    btn_nublado = ft.IconButton(icon=ft.Icons.WB_CLOUDY, icon_size=40, tooltip="Encoberto")
    btn_chuva = ft.IconButton(icon=ft.Icons.UMBRELLA, icon_size=40, tooltip="Chuva")
    
    # Variável local para controlar a seleção do clima (padrão Sol se vazio)
    clima_atual = estado.setup_cache.get("S_7", "Sol")

    def update_clima_ui(modo):
        nonlocal clima_atual
        clima_atual = modo
        
        # Reseta cores
        btn_sol.icon_color = ft.Colors.GREY_300
        btn_nublado.icon_color = ft.Colors.GREY_300
        btn_chuva.icon_color = ft.Colors.GREY_300
        
        # Ativa selecionado
        if modo == "Sol":
            btn_sol.icon_color = ft.Colors.ORANGE
        elif modo == "Encoberto":
            btn_nublado.icon_color = ft.Colors.GREY_700
        elif modo == "Chuva":
            btn_chuva.icon_color = ft.Colors.BLUE
        
        page.update()

    btn_sol.on_click = lambda e: update_clima_ui("Sol")
    btn_nublado.on_click = lambda e: update_clima_ui("Encoberto")
    btn_chuva.on_click = lambda e: update_clima_ui("Chuva")
    
    # Inicializa visualmente
    update_clima_ui(clima_atual)

    # Controle de validação (Bypass)
    tentativa_sem_preencher = False

    txt_erro = ft.Text(
        "Campos obrigatórios vazios.\nClique novamente para prosseguir mesmo assim.",
        color=ft.Colors.RED,
        size=12,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    def iniciar(e):
        nonlocal tentativa_sem_preencher
        print("Botão Iniciar clicado")
        
        campos_vazios = []
        
        # Validação Nome (Define se tem erro ou limpa)
        nome_val = s4_nome.value or ""
        if not nome_val.strip():
            campos_vazios.append("Nome")
            # Forçando visual de erro manualmente
            s4_nome.border_color = ft.Colors.RED_900
            s4_erro_msg.visible = True
        else:
            s4_nome.border_color = None
            s4_erro_msg.visible = False
            
        # Validação Posto
        if not s5_posto.value:
            campos_vazios.append("Local")
            s5_posto.error_text = "Obrigatório"
        else:
            s5_posto.error_text = None

        # Força a atualização visual dos campos imediatamente
        s4_nome.update()
        s4_erro_msg.update()
        s5_posto.update()

        if campos_vazios and not tentativa_sem_preencher:
            print("Validação falhou: Aviso exibido")
            tentativa_sem_preencher = True # Autoriza na próxima
            txt_erro.value = f"Campos vazios: {', '.join(campos_vazios)}.\nClique novamente para prosseguir mesmo assim."
            txt_erro.visible = True
            txt_erro.update()
            return

        # 🔒 Salvamento dos dados (Visíveis e Ocultos)
        estado.setup_cache["S_1"] = hex(uuid.getnode()) # Device_ID
        estado.setup_cache["S_2"] = datetime.now().strftime("%Y/%m/%d") # Data
        estado.setup_cache["S_3"] = datetime.now().strftime("%H:%M")    # Hora
        estado.setup_cache["S_4"] = s4_nome.value
        estado.setup_cache["S_5"] = s5_posto.value
        estado.setup_cache["S_6"] = "São Paulo" if s6_switch.value else "Interior"
        estado.setup_cache["S_7"] = clima_atual
        print("movento para t1")
        estado.tela_atual = "t1"
        render()

    return ft.Container(
        alignment=ft.Alignment(0, 0),
        expand=True,
        content=ft.Column(
            width=360,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Configuração da Pesquisa", size=22, weight=ft.FontWeight.BOLD),

                ft.Text(
                    "Preencha os dados iniciais antes de iniciar a entrevista",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Divider(),

                # Agrupando em coluna com spacing=0 para aproximar o erro do campo
                ft.Column([s4_nome, s4_erro_msg], spacing=0),
                s5_posto,
                #ft.Text("Sentido:", weight=ft.FontWeight.BOLD),
                s6_container,
                
                ft.Text("Condições Climáticas:", weight=ft.FontWeight.BOLD),
                ft.Row(
                    [btn_sol, btn_nublado, btn_chuva], 
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ft.Divider(),
                txt_erro,

                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_FORWARD),
                            ft.Text("Iniciar entrevista"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    height=45,
                    on_click=iniciar,
                ),
            ],
        ),
    )
