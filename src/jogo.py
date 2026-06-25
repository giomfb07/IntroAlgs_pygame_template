import random

import pygame

import os

# Importa constantes e configurações do jogo
from src.config import (
    ALTURA_PLATAFORMA,
    ALTURA_TELA,
    AMARELO,
    ANDAR_FINAL,
    AZUL_ESCURO,
    AZUL_MEDIO,
    BRANCO,
    CAMINHO_RANKING,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    CAMINHO_ESTRELA,
    ESPACO_PLATAFORMAS,
    FASES,
    FPS,
    GRAVIDADE,
    IMPULSO_PULO,
    IMPULSO_PULO_DUPLO,
    LARGURA_PLATAFORMA,
    LARGURA_TELA,
    LIMITE_QUEDA_FATAL,
    PENALIDADE_QUEDA,
    PONTOS_POR_ANDAR,
    PRETO,
    PULOS_DUPLOS_INICIAIS,
    TITULO_JOGO,
    VELOCIDADE_HORIZONTAL,
    VERDE,
    VERMELHO,
    VIDAS_INICIAIS,
    obter_fase,
)
# Importa funções responsáveis por salvar e carregar dados
from src.dados import (
    atualizar_recorde,
    carregar_ranking,
    carregar_recorde,
    salvar_resultado_ranking,
)
# Importa funções auxiliares da lógica do jogo
from src.funcoes import (
    calcular_pontos,
    calcular_pontos_por_andar,
    consumir_pulo_duplo,
    jogador_perdeu,
    jogador_venceu,
    limitar_valor,
    penalizar_queda,
    queda_fatal,
    tomar_dano,
    verificar_colisao,
)
# Importa função para capturar sprites 
from src.sprites import pegar_sprite


def desenhar_texto(tela, fonte, texto, x, y, cor=BRANCO, centro=False):
    # Converte o texto em uma superfície gráfica
    superficie = fonte.render(texto, True, cor)
    # Obtém o retângulo que envolve o texto
    rect = superficie.get_rect()

    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    # Desenha o texto na tela
    tela.blit(superficie, rect)
    return rect

 # Cria uma superfície transparente e desenha uma forma simples para representar o sprite
def criar_sprite_fallback(largura, altura, cor):
    imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.ellipse(imagem, cor, imagem.get_rect())
    return imagem


def carregar_imagens():
    try:
       
        quadro_parado = pegar_sprite(CAMINHO_SPRITES, x=10, y=0, width=50, height=50, scale=2.5)
        quadro_subindo = pegar_sprite(CAMINHO_SPRITES, x=80, y=0, width=50, height=50, scale=2.5)  
        quadro_descendo = pegar_sprite(CAMINHO_SPRITES, x=180, y=0, width=50, height=50, scale=2.5)
        
        sprites_jogador = [quadro_parado, quadro_subindo, quadro_descendo]

        estrela = pegar_sprite(CAMINHO_ESTRELA, x=10, y=40, width=250, height=210, scale=0.2)

    except pygame.error:
        sprites_jogador = [criar_sprite_fallback(70, 70, VERDE) for _ in range(3)]
        estrela = criar_sprite_fallback(32, 32, AMARELO)

    balao = pygame.Surface((44, 58), pygame.SRCALPHA)
    pygame.draw.ellipse(balao, VERMELHO, (4, 0, 36, 44))
    pygame.draw.polygon(balao, VERMELHO, [(20, 43), (25, 43), (22, 50)])
    pygame.draw.line(balao, BRANCO, (22, 50), (22, 58), 2)

    return {"jogador": sprites_jogador, "estrela": estrela, "balao": balao}


def carregar_fundos():
    fundos = {}
    for fase in FASES:
        caminho = fase.get('imagem_fundo')
        if caminho and os.path.exists(caminho):
            try:
                img = pygame.image.load(caminho).convert()
                # Redimensiona para caber na tela (mantendo proporção)
                img = pygame.transform.scale(img, (LARGURA_TELA, ALTURA_TELA))
                fundos[fase['nome']] = img
            except pygame.error:
                fundos[fase['nome']] = None
        else:
            fundos[fase['nome']] = None
    return fundos



def criar_estrelas(quantidade=80):
    estrelas = []
    for _ in range(quantidade):
        estrelas.append(
            {
                # Posição aleatória
                "x": random.randrange(0, LARGURA_TELA),
                "y": random.randrange(0, ALTURA_TELA),
                # Tamanho da estrela
                "raio": random.choice([1, 1, 2]),
                # Velocidade de descida
                "velocidade": random.uniform(0.15, 0.45),
            }
        )
    return estrelas




def desenhar_fundo(tela, fundos, config_fase, estrelas=None):

    nome_fase = config_fase['nome']
    imagem = fundos.get(nome_fase)

    if imagem is not None:
        # Desenha a imagem
        tela.blit(imagem, (0, 0))
   
        if estrelas:
            for estrela in estrelas:
                estrela["y"] += estrela["velocidade"]
                if estrela["y"] > ALTURA_TELA:
                    estrela["x"] = random.randrange(0, LARGURA_TELA)
                    estrela["y"] = 0
                # Desenha a estrela
                pygame.draw.circle(tela, (255,255,255,100), (int(estrela["x"]), int(estrela["y"])), estrela["raio"])
    else:
        # Usa cor sólida 
        tela.fill(config_fase['cor_fundo'])
        if estrelas:
            for estrela in estrelas:
                estrela["y"] += estrela["velocidade"]
                if estrela["y"] > ALTURA_TELA:
                    estrela["x"] = random.randrange(0, LARGURA_TELA)
                    estrela["y"] = 0
                # Desenha a estrela
                pygame.draw.circle(tela, BRANCO, (int(estrela["x"]), int(estrela["y"])), estrela["raio"])



def criar_plataforma(andar, y, x=None):
    # Gera uma posição aleatória para a plataforma
    if x is None:
        x = random.randrange(24, LARGURA_TELA - LARGURA_PLATAFORMA - 24)

    return {
        "rect": pygame.Rect(x, y, LARGURA_PLATAFORMA, ALTURA_PLATAFORMA),
        "andar": andar,
        "visitada": False,
    }


def criar_partida(imagens):
    plataformas = []
    obstaculos = []
    estrelas = []

    # Cria as primeiras plataformas do jogo
    for andar in range(9):
        # Calcula a posição vertical da plataforma
        y = ALTURA_TELA - 70 - andar * ESPACO_PLATAFORMAS
        # Primeira plataforma fica centralizada
        x = (LARGURA_TELA - LARGURA_PLATAFORMA) // 2 if andar == 0 else None
        plataformas.append(criar_plataforma(andar, y, x))

    sprite_parado = imagens["jogador"][0]
    # Cria retângulo de colisão do jogador
    jogador_rect = sprite_parado.get_rect()
    # Posiciona o jogador sobre a primeira plataforma
    jogador_rect.midbottom = plataformas[0]["rect"].midtop

    # Retorna toda a estrutura da partida
    return {
        "jogador": {
           "sprites": imagens["jogador"],    
            "indice_sprite": 0,               
            "rect": jogador_rect,
            "x": float(jogador_rect.x),
            "y": float(jogador_rect.y),
            "vel_y": IMPULSO_PULO,
            "invulneravel": 0,
            "no_chao": True,   
        },
        "plataformas": plataformas,
        "obstaculos": obstaculos,
        "estrelas": estrelas,
        "pontos": 0,
        "vidas": VIDAS_INICIAIS,
        "pulos_duplos": PULOS_DUPLOS_INICIAIS,
        "maior_andar": 0,
        "andar_atual": 0,
        "inicio_ticks": pygame.time.get_ticks(),
        "mensagem": "",
        "resultado_salvo": False,
        "fase_atual": 0,
        "config_fase": FASES[0],
        "transicao": {
            "ativa": False,
            "timer": 0,
            "nome": ""
        }
    }


def gerar_elementos_acima(partida, imagens):
    plataformas = partida["plataformas"]
    top_y = min(plataforma["rect"].y for plataforma in plataformas)
    maior_andar = max(plataforma["andar"] for plataforma in plataformas)
    config = partida["config_fase"]

    # Continua gerando até preencher o topo
    while top_y > -120:
        maior_andar += 1
        top_y -= ESPACO_PLATAFORMAS
        # Cria nova plataforma
        plataforma = criar_plataforma(maior_andar, top_y)
        plataformas.append(plataforma)

        # Chance de obstáculo
        chance_base = config['chance_obstaculo_base']
        chance = min(chance_base + maior_andar * 0.004, 0.45)

        # Criação de balões e estrelas
        if maior_andar > 2 and random.random() < chance:
            rect = imagens["balao"].get_rect()
            rect.x = random.randrange(30, LARGURA_TELA - rect.width - 30)
            rect.y = plataforma["rect"].y - random.randrange(42, 72)
            partida["obstaculos"].append({"rect": rect, "andar": maior_andar, "ativo": True})
        if maior_andar > 1 and random.random() < 0.28:
            rect = imagens["estrela"].get_rect()
            rect.centerx = plataforma["rect"].centerx
            rect.bottom = plataforma["rect"].top - 12
            partida["estrelas"].append({"rect": rect, "coletada": False})


def remover_elementos_fora_da_tela(partida):
    # Mantém apenas plataformas visíveis
    partida["plataformas"] = [
        plataforma for plataforma in partida["plataformas"] if plataforma["rect"].top < ALTURA_TELA + 90
    ]
    # Mantém apenas obstáculos visíveis
    partida["obstaculos"] = [
        obstaculo for obstaculo in partida["obstaculos"] if obstaculo["rect"].top < ALTURA_TELA + 90
    ]
    # Mantém apenas estrelas visíveis
    partida["estrelas"] = [estrela for estrela in partida["estrelas"] if estrela["rect"].top < ALTURA_TELA + 90]


def mover_cenario(partida, deslocamento):
    for colecao in ("plataformas", "obstaculos", "estrelas"):
        for item in partida[colecao]:
            # Move verticalmente cada item para sensação de subida
            item["rect"].y += deslocamento


def finalizar_partida(partida, status, mensagem, recorde):
    # Verifica se o resultado já foi salvo
    if not partida["resultado_salvo"]:
        # Atualiza o recorde
        recorde = atualizar_recorde(CAMINHO_RECORDE, partida["pontos"])
        # Salva no ranking
        salvar_resultado_ranking(CAMINHO_RANKING, "Jogador", partida["pontos"], status)
        partida["resultado_salvo"] = True

    partida["mensagem"] = mensagem
    return "fim", recorde


def atualizar_partida(partida, imagens, teclas):
    jogador = partida["jogador"]
    rect = jogador["rect"]
    config = partida["config_fase"]

    # Obtém a posição horizontal do mouse
    mouse_x = pygame.mouse.get_pos()[0]
    # Define o ponto que o jogador deve seguir com o mouse
    alvo_x = mouse_x - rect.width / 2
    vel_h = config['vel_horizontal']

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador["x"] -= vel_h
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador["x"] += vel_h
    else:
        diferenca = alvo_x - jogador["x"]
        passo = limitar_valor(diferenca, -vel_h, vel_h)
        jogador["x"] += passo

    # Impede que o jogador saia da tela horizontalmente
    jogador["x"] = limitar_valor(jogador["x"], 0, LARGURA_TELA - rect.width)
    rect.x = int(jogador["x"])

    fundo_anterior = rect.bottom
    jogador["vel_y"] += config['gravidade']
    jogador["y"] += jogador["vel_y"]
    rect.y = int(jogador["y"])

    if jogador["invulneravel"] > 0:
        jogador["invulneravel"] -= 1

    jogador["no_chao"] = False

    for plataforma in partida["plataformas"]:
        plataforma_rect = plataforma["rect"]
        # Verifica se o jogador pousou na plataforma
        pousou = (
            jogador["vel_y"] > 0
            and fundo_anterior <= plataforma_rect.top
            and verificar_colisao(rect, plataforma_rect)
        )
        if not pousou:
            continue
        
        # Posiciona o jogador exatamente sobre a plataforma
        rect.bottom = plataforma_rect.top
        jogador["y"] = float(rect.y)
        jogador["vel_y"] = IMPULSO_PULO
        jogador["no_chao"] = True

        andar = plataforma["andar"]
        if andar > partida["maior_andar"]:
            # Adiciona pontos pelos andares conquistados
            partida["pontos"] = calcular_pontos_por_andar(
                partida["pontos"],
                andar,
                partida["maior_andar"],
                PONTOS_POR_ANDAR,
            )
            partida["maior_andar"] = andar

            # Verifica se mudou de fase
            nova_fase = obter_fase(andar)
            if nova_fase != config:
                partida["config_fase"] = nova_fase
                partida["fase_atual"] = FASES.index(nova_fase)
                partida["transicao"]["ativa"] = True
                partida["transicao"]["timer"] = 60
                partida["transicao"]["nome"] = nova_fase['nome']

        elif andar < partida["andar_atual"]:
            # Aplica penalidade por queda
            partida["pontos"] = penalizar_queda(
                partida["pontos"],
                partida["andar_atual"],
                andar,
                PENALIDADE_QUEDA,
            )

        partida["andar_atual"] = andar
        plataforma["visitada"] = True
        break

    if rect.top < ALTURA_TELA * 0.34 and jogador["vel_y"] < 0:
        deslocamento = int(ALTURA_TELA * 0.34 - rect.top)
        # Mantém jogador na mesma região da tela
        rect.y += deslocamento
        jogador["y"] = float(rect.y)
        mover_cenario(partida, deslocamento)


    if not jogador["no_chao"]:
        if jogador["vel_y"] < 0:
            jogador["indice_sprite"] = 1  
        else:
            jogador["indice_sprite"] = 2   
    else:
        jogador["indice_sprite"] = 0           

    for estrela in partida["estrelas"]:
        if not estrela["coletada"] and verificar_colisao(rect, estrela["rect"]):
            # Marca estrela como coletada
            estrela["coletada"] = True
            # Adiciona pontos
            partida["pontos"] = calcular_pontos(partida["pontos"], 10)

    # Verifica colisão com obstáculos
    for obstaculo in partida["obstaculos"]:
        # Ignora obstáculos inativos
        if not obstaculo["ativo"] or jogador["invulneravel"] > 0:
            continue
        # Detecta colisão
        if verificar_colisao(rect, obstaculo["rect"]):
            obstaculo["ativo"] = False
            jogador["invulneravel"] = FPS
            # Remove uma vida
            partida["vidas"] = tomar_dano(partida["vidas"], 1)

    # Gera novas plataformas, estrelas e obstáculos acima
    gerar_elementos_acima(partida, imagens)
    remover_elementos_fora_da_tela(partida)

    # Atualiza animação de transição entre fases
    if partida["transicao"]["ativa"]:
        partida["transicao"]["timer"] -= 1
        if partida["transicao"]["timer"] <= 0:
            partida["transicao"]["ativa"] = False

def desenhar_partida(tela, fontes, partida, imagens, recorde, fundos, estrelas):
    config = partida["config_fase"]
    desenhar_fundo(tela, fundos, config, estrelas)

    for plataforma in partida["plataformas"]:
        cor = VERDE if plataforma["andar"] == partida["andar_atual"] else AZUL_MEDIO
        pygame.draw.rect(tela, cor, plataforma["rect"], border_radius=7)
        pygame.draw.rect(tela, BRANCO, plataforma["rect"], 1, border_radius=7)

    for estrela in partida["estrelas"]:
        if not estrela["coletada"]:
            tela.blit(imagens["estrela"], estrela["rect"])

    for obstaculo in partida["obstaculos"]:
        if obstaculo["ativo"]:
            tela.blit(imagens["balao"], obstaculo["rect"])

    jogador = partida["jogador"]
    piscar = jogador["invulneravel"] > 0 and jogador["invulneravel"] % 10 < 5
    if not piscar:
        sprite_atual = jogador["sprites"][jogador["indice_sprite"]]
        x = jogador["rect"].centerx - sprite_atual.get_width() // 2
        y = jogador["rect"].bottom - sprite_atual.get_height()
        tela.blit(sprite_atual, (x, y))

    tempo = (pygame.time.get_ticks() - partida["inicio_ticks"]) // 1000
    hud = (
        f"Pontos: {partida['pontos']}  Recorde: {max(recorde, partida['pontos'])}  "
        f"Vidas: {partida['vidas']}  Pulos: {partida['pulos_duplos']}  "
        f"Andar: {partida['maior_andar']}/{ANDAR_FINAL}  Tempo: {tempo}s"
    )
    desenhar_texto(tela, fontes["pequena"], hud, 16, 14, BRANCO)
    desenhar_texto(tela, fontes["pequena"], "ESC pausa | SPACE pulo duplo | R reinicia", 16, 42, AMARELO)

    if partida["transicao"]["ativa"]:
        nome = partida["transicao"]["nome"]
        desenhar_texto(tela, fontes["titulo"], nome, LARGURA_TELA//2, ALTURA_TELA//2 - 50, AMARELO, centro=True)
        desenhar_texto(tela, fontes["media"], "Nova fase!", LARGURA_TELA//2, ALTURA_TELA//2 + 20, BRANCO, centro=True)



def desenhar_menu(tela, fontes, recorde, ranking, fundos, estrelas):
    desenhar_fundo(tela, fundos, FASES[0], estrelas)

    # Cria camada escura transparente
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((40, 40, 40, 170))  
    tela.blit(overlay, (0, 0))

    desenhar_texto(tela, fontes["titulo"], TITULO_JOGO, LARGURA_TELA // 2, 95, AMARELO, centro=True)
    desenhar_texto(
        tela,
        fontes["media"],
        "Suba pelas plataformas, desvie dos baloes e alcance o andar final.",
        LARGURA_TELA // 2,
        160,
        BRANCO,
        centro=True,
    )
    desenhar_texto(tela, fontes["media"], f"Recorde atual: {recorde} pontos", LARGURA_TELA // 2, 215, VERDE, centro=True)
    desenhar_texto(tela, fontes["media"], "ENTER inicia | Q sai", LARGURA_TELA // 2, 270, BRANCO, centro=True)

    desenhar_texto(tela, fontes["media"], "Ranking", LARGURA_TELA // 2, 340, AMARELO, centro=True)
    if not ranking:
        desenhar_texto(tela, fontes["pequena"], "Nenhuma partida registrada ainda.", LARGURA_TELA // 2, 380, BRANCO, centro=True)
    else:
        # Mostra os melhores jogadores
        for indice, item in enumerate(ranking, start=1):
            linha = f"{indice}. {item['nome']} - {item['pontuacao']} pts - {item['status']}"
            desenhar_texto(tela, fontes["pequena"], linha, LARGURA_TELA // 2, 368 + indice * 28, BRANCO, centro=True)


def desenhar_pausa(tela, fontes):
    painel = pygame.Rect(170, 205, 460, 180)
    pygame.draw.rect(tela, PRETO, painel, border_radius=10)
    pygame.draw.rect(tela, BRANCO, painel, 2, border_radius=10)
    desenhar_texto(tela, fontes["titulo"], "Pausado", LARGURA_TELA // 2, 255, AMARELO, centro=True)
    desenhar_texto(tela, fontes["media"], "ESC continua | R reinicia | Q sai", LARGURA_TELA // 2, 320, BRANCO, centro=True)


def desenhar_fim(tela, fontes, partida, recorde, ranking, fundos, estrelas):
    desenhar_fundo(tela, fundos, FASES[0], estrelas)
    desenhar_texto(tela, fontes["titulo"], partida["mensagem"], LARGURA_TELA // 2, 110, AMARELO, centro=True)
    desenhar_texto(tela, fontes["media"], f"Pontuacao final: {partida['pontos']}", LARGURA_TELA // 2, 180, BRANCO, centro=True)
    desenhar_texto(tela, fontes["media"], f"Maior andar: {partida['maior_andar']} | Recorde: {recorde}", LARGURA_TELA // 2, 220, VERDE, centro=True)
    desenhar_texto(tela, fontes["media"], "R joga novamente | ENTER menu | Q sai", LARGURA_TELA // 2, 285, BRANCO, centro=True)

    desenhar_texto(tela, fontes["media"], "Melhores partidas", LARGURA_TELA // 2, 355, AMARELO, centro=True)
    for indice, item in enumerate(ranking, start=1):
        linha = f"{indice}. {item['pontuacao']} pts - {item['status']} - {item['data']}"
        desenhar_texto(tela, fontes["pequena"], linha, LARGURA_TELA // 2, 382 + indice * 26, BRANCO, centro=True)


def executar_jogo():
    # Inicializa todos os módulos do pygame
    pygame.init()

    # Cria janela principal
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fontes = {
        "titulo": pygame.font.Font(None, 66),
        "media": pygame.font.Font(None, 32),
        "pequena": pygame.font.Font(None, 24),
    }
    imagens = carregar_imagens()
    fundos = carregar_fundos()    
    estrelas = criar_estrelas()

    recorde = carregar_recorde(CAMINHO_RECORDE)
    ranking = carregar_ranking(CAMINHO_RANKING)
    partida = criar_partida(imagens)
    estado = "menu"
    rodando = True

    while rodando:
        # Limita FPS
        relogio.tick(FPS)
        # Obtém teclas pressionadas
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if estado == "menu":
                    if evento.key == pygame.K_RETURN:
                        partida = criar_partida(imagens)
                        estado = "jogando"
                    elif evento.key == pygame.K_q:
                        rodando = False

                elif estado == "jogando":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "pausado"
                    elif evento.key == pygame.K_SPACE:
                        partida["pulos_duplos"], pulou = consumir_pulo_duplo(partida["pulos_duplos"])
                        if pulou:
                            partida["jogador"]["vel_y"] = IMPULSO_PULO_DUPLO
                    elif evento.key == pygame.K_r:
                        partida = criar_partida(imagens)

                elif estado == "pausado":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "jogando"
                    elif evento.key == pygame.K_r:
                        partida = criar_partida(imagens)
                        estado = "jogando"
                    elif evento.key == pygame.K_q:
                        rodando = False

                elif estado == "fim":
                    if evento.key == pygame.K_r:
                        partida = criar_partida(imagens)
                        estado = "jogando"
                    elif evento.key == pygame.K_RETURN:
                        ranking = carregar_ranking(CAMINHO_RANKING)
                        estado = "menu"
                    elif evento.key == pygame.K_q:
                        rodando = False

        if estado == "jogando":
            atualizar_partida(partida, imagens, teclas)

            if jogador_venceu(partida["maior_andar"], ANDAR_FINAL):
                estado, recorde = finalizar_partida(partida, "VITORIA", "Voce venceu!", recorde)
                ranking = carregar_ranking(CAMINHO_RANKING)
            elif jogador_perdeu(partida["vidas"]):
                estado, recorde = finalizar_partida(partida, "DERROTA", "Sem vidas!", recorde)
                ranking = carregar_ranking(CAMINHO_RANKING)
            elif queda_fatal(partida["andar_atual"], partida["maior_andar"], LIMITE_QUEDA_FATAL):
                estado, recorde = finalizar_partida(partida, "DERROTA", "Queda fatal!", recorde)
                ranking = carregar_ranking(CAMINHO_RANKING)
            elif partida["jogador"]["rect"].top > ALTURA_TELA:
                estado, recorde = finalizar_partida(partida, "DERROTA", "Voce caiu!", recorde)
                ranking = carregar_ranking(CAMINHO_RANKING)

        if estado == "menu":
            ranking = carregar_ranking(CAMINHO_RANKING)
            desenhar_menu(tela, fontes, recorde, ranking, fundos, estrelas)
        elif estado == "jogando":
            desenhar_partida(tela, fontes, partida, imagens, recorde, fundos, estrelas)
        elif estado == "pausado":
            desenhar_partida(tela, fontes, partida, imagens, recorde, fundos, estrelas)
            desenhar_pausa(tela, fontes)
        elif estado == "fim":
            desenhar_fim(tela, fontes, partida, recorde, ranking, fundos, estrelas)
    
        # Atualiza tela
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    executar_jogo()
