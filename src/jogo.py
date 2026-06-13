import random

import pygame

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
    ESPACO_PLATAFORMAS,
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
)
from src.dados import (
    atualizar_recorde,
    carregar_ranking,
    carregar_recorde,
    salvar_resultado_ranking,
)
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
from src.sprites import pegar_sprite


def desenhar_texto(tela, fonte, texto, x, y, cor=BRANCO, centro=False):
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(superficie, rect)
    return rect


def criar_sprite_fallback(largura, altura, cor):
    imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.ellipse(imagem, cor, imagem.get_rect())
    return imagem


def carregar_imagens():
    try:
        jogador = pegar_sprite(CAMINHO_SPRITES, x=110, y=120, width=190, height=190, scale=0.42)
        gema = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.25)
    except pygame.error:
        jogador = criar_sprite_fallback(70, 70, VERDE)
        gema = criar_sprite_fallback(32, 32, AMARELO)

    balao = pygame.Surface((44, 58), pygame.SRCALPHA)
    pygame.draw.ellipse(balao, VERMELHO, (4, 0, 36, 44))
    pygame.draw.polygon(balao, VERMELHO, [(20, 43), (25, 43), (22, 50)])
    pygame.draw.line(balao, BRANCO, (22, 50), (22, 58), 2)

    return {"jogador": jogador, "gema": gema, "balao": balao}


def criar_estrelas(quantidade=80):
    estrelas = []
    for _ in range(quantidade):
        estrelas.append(
            {
                "x": random.randrange(0, LARGURA_TELA),
                "y": random.randrange(0, ALTURA_TELA),
                "raio": random.choice([1, 1, 2]),
                "velocidade": random.uniform(0.15, 0.45),
            }
        )
    return estrelas


def criar_plataforma(andar, y, x=None):
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
    gemas = []

    for andar in range(9):
        y = ALTURA_TELA - 70 - andar * ESPACO_PLATAFORMAS
        x = (LARGURA_TELA - LARGURA_PLATAFORMA) // 2 if andar == 0 else None
        plataformas.append(criar_plataforma(andar, y, x))

    jogador_rect = imagens["jogador"].get_rect()
    jogador_rect.midbottom = plataformas[0]["rect"].midtop

    return {
        "jogador": {
            "imagem": imagens["jogador"],
            "rect": jogador_rect,
            "x": float(jogador_rect.x),
            "y": float(jogador_rect.y),
            "vel_y": IMPULSO_PULO,
            "invulneravel": 0,
        },
        "plataformas": plataformas,
        "obstaculos": obstaculos,
        "gemas": gemas,
        "pontos": 0,
        "vidas": VIDAS_INICIAIS,
        "pulos_duplos": PULOS_DUPLOS_INICIAIS,
        "maior_andar": 0,
        "andar_atual": 0,
        "inicio_ticks": pygame.time.get_ticks(),
        "mensagem": "",
        "resultado_salvo": False,
    }


def gerar_elementos_acima(partida, imagens):
    plataformas = partida["plataformas"]
    top_y = min(plataforma["rect"].y for plataforma in plataformas)
    maior_andar = max(plataforma["andar"] for plataforma in plataformas)

    while top_y > -120:
        maior_andar += 1
        top_y -= ESPACO_PLATAFORMAS
        plataforma = criar_plataforma(maior_andar, top_y)
        plataformas.append(plataforma)

        chance_obstaculo = min(0.18 + maior_andar * 0.004, 0.38)
        if maior_andar > 2 and random.random() < chance_obstaculo:
            rect = imagens["balao"].get_rect()
            rect.x = random.randrange(30, LARGURA_TELA - rect.width - 30)
            rect.y = plataforma["rect"].y - random.randrange(42, 72)
            partida["obstaculos"].append({"rect": rect, "andar": maior_andar, "ativo": True})

        if maior_andar > 1 and random.random() < 0.28:
            rect = imagens["gema"].get_rect()
            rect.centerx = plataforma["rect"].centerx
            rect.bottom = plataforma["rect"].top - 12
            partida["gemas"].append({"rect": rect, "coletada": False})


def remover_elementos_fora_da_tela(partida):
    partida["plataformas"] = [
        plataforma for plataforma in partida["plataformas"] if plataforma["rect"].top < ALTURA_TELA + 90
    ]
    partida["obstaculos"] = [
        obstaculo for obstaculo in partida["obstaculos"] if obstaculo["rect"].top < ALTURA_TELA + 90
    ]
    partida["gemas"] = [gema for gema in partida["gemas"] if gema["rect"].top < ALTURA_TELA + 90]


def mover_cenario(partida, deslocamento):
    for colecao in ("plataformas", "obstaculos", "gemas"):
        for item in partida[colecao]:
            item["rect"].y += deslocamento


def finalizar_partida(partida, status, mensagem, recorde):
    if not partida["resultado_salvo"]:
        recorde = atualizar_recorde(CAMINHO_RECORDE, partida["pontos"])
        salvar_resultado_ranking(CAMINHO_RANKING, "Jogador", partida["pontos"], status)
        partida["resultado_salvo"] = True

    partida["mensagem"] = mensagem
    return "fim", recorde


def atualizar_partida(partida, imagens, teclas):
    jogador = partida["jogador"]
    rect = jogador["rect"]

    mouse_x = pygame.mouse.get_pos()[0]
    alvo_x = mouse_x - rect.width / 2

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador["x"] -= VELOCIDADE_HORIZONTAL
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador["x"] += VELOCIDADE_HORIZONTAL
    else:
        diferenca = alvo_x - jogador["x"]
        passo = limitar_valor(diferenca, -VELOCIDADE_HORIZONTAL, VELOCIDADE_HORIZONTAL)
        jogador["x"] += passo

    jogador["x"] = limitar_valor(jogador["x"], 0, LARGURA_TELA - rect.width)
    rect.x = int(jogador["x"])

    fundo_anterior = rect.bottom
    jogador["vel_y"] += GRAVIDADE
    jogador["y"] += jogador["vel_y"]
    rect.y = int(jogador["y"])

    if jogador["invulneravel"] > 0:
        jogador["invulneravel"] -= 1

    for plataforma in partida["plataformas"]:
        plataforma_rect = plataforma["rect"]
        pousou = (
            jogador["vel_y"] > 0
            and fundo_anterior <= plataforma_rect.top
            and verificar_colisao(rect, plataforma_rect)
        )
        if not pousou:
            continue

        rect.bottom = plataforma_rect.top
        jogador["y"] = float(rect.y)
        jogador["vel_y"] = IMPULSO_PULO

        andar = plataforma["andar"]
        if andar > partida["maior_andar"]:
            partida["pontos"] = calcular_pontos_por_andar(
                partida["pontos"],
                andar,
                partida["maior_andar"],
                PONTOS_POR_ANDAR,
            )
            partida["maior_andar"] = andar
        elif andar < partida["andar_atual"]:
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
        rect.y += deslocamento
        jogador["y"] = float(rect.y)
        mover_cenario(partida, deslocamento)

    for gema in partida["gemas"]:
        if not gema["coletada"] and verificar_colisao(rect, gema["rect"]):
            gema["coletada"] = True
            partida["pontos"] = calcular_pontos(partida["pontos"], 10)

    for obstaculo in partida["obstaculos"]:
        if not obstaculo["ativo"] or jogador["invulneravel"] > 0:
            continue
        if verificar_colisao(rect, obstaculo["rect"]):
            obstaculo["ativo"] = False
            jogador["invulneravel"] = FPS
            partida["vidas"] = tomar_dano(partida["vidas"], 1)

    gerar_elementos_acima(partida, imagens)
    remover_elementos_fora_da_tela(partida)


def desenhar_fundo(tela, estrelas):
    tela.fill(AZUL_ESCURO)
    for estrela in estrelas:
        estrela["y"] += estrela["velocidade"]
        if estrela["y"] > ALTURA_TELA:
            estrela["x"] = random.randrange(0, LARGURA_TELA)
            estrela["y"] = 0
        pygame.draw.circle(tela, BRANCO, (int(estrela["x"]), int(estrela["y"])), estrela["raio"])


def desenhar_partida(tela, fontes, partida, imagens, recorde, estrelas):
    desenhar_fundo(tela, estrelas)

    for plataforma in partida["plataformas"]:
        cor = VERDE if plataforma["andar"] == partida["andar_atual"] else AZUL_MEDIO
        pygame.draw.rect(tela, cor, plataforma["rect"], border_radius=7)
        pygame.draw.rect(tela, BRANCO, plataforma["rect"], 1, border_radius=7)

    for gema in partida["gemas"]:
        if not gema["coletada"]:
            tela.blit(imagens["gema"], gema["rect"])

    for obstaculo in partida["obstaculos"]:
        if obstaculo["ativo"]:
            tela.blit(imagens["balao"], obstaculo["rect"])

    jogador = partida["jogador"]
    piscar = jogador["invulneravel"] > 0 and jogador["invulneravel"] % 10 < 5
    if not piscar:
        tela.blit(jogador["imagem"], jogador["rect"])

    tempo = (pygame.time.get_ticks() - partida["inicio_ticks"]) // 1000
    hud = (
        f"Pontos: {partida['pontos']}  Recorde: {max(recorde, partida['pontos'])}  "
        f"Vidas: {partida['vidas']}  Pulos: {partida['pulos_duplos']}  "
        f"Andar: {partida['maior_andar']}/{ANDAR_FINAL}  Tempo: {tempo}s"
    )
    desenhar_texto(tela, fontes["pequena"], hud, 16, 14, BRANCO)
    desenhar_texto(tela, fontes["pequena"], "ESC pausa | SPACE pulo duplo | R reinicia", 16, 42, AMARELO)


def desenhar_menu(tela, fontes, recorde, ranking, estrelas):
    desenhar_fundo(tela, estrelas)
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
        for indice, item in enumerate(ranking, start=1):
            linha = f"{indice}. {item['nome']} - {item['pontuacao']} pts - {item['status']}"
            desenhar_texto(tela, fontes["pequena"], linha, LARGURA_TELA // 2, 368 + indice * 28, BRANCO, centro=True)


def desenhar_pausa(tela, fontes):
    painel = pygame.Rect(170, 205, 460, 180)
    pygame.draw.rect(tela, PRETO, painel, border_radius=10)
    pygame.draw.rect(tela, BRANCO, painel, 2, border_radius=10)
    desenhar_texto(tela, fontes["titulo"], "Pausado", LARGURA_TELA // 2, 255, AMARELO, centro=True)
    desenhar_texto(tela, fontes["media"], "ESC continua | R reinicia | Q sai", LARGURA_TELA // 2, 320, BRANCO, centro=True)


def desenhar_fim(tela, fontes, partida, recorde, ranking, estrelas):
    desenhar_fundo(tela, estrelas)
    desenhar_texto(tela, fontes["titulo"], partida["mensagem"], LARGURA_TELA // 2, 110, AMARELO, centro=True)
    desenhar_texto(tela, fontes["media"], f"Pontuacao final: {partida['pontos']}", LARGURA_TELA // 2, 180, BRANCO, centro=True)
    desenhar_texto(tela, fontes["media"], f"Maior andar: {partida['maior_andar']} | Recorde: {recorde}", LARGURA_TELA // 2, 220, VERDE, centro=True)
    desenhar_texto(tela, fontes["media"], "R joga novamente | ENTER menu | Q sai", LARGURA_TELA // 2, 285, BRANCO, centro=True)

    desenhar_texto(tela, fontes["media"], "Melhores partidas", LARGURA_TELA // 2, 355, AMARELO, centro=True)
    for indice, item in enumerate(ranking, start=1):
        linha = f"{indice}. {item['pontuacao']} pts - {item['status']} - {item['data']}"
        desenhar_texto(tela, fontes["pequena"], linha, LARGURA_TELA // 2, 382 + indice * 26, BRANCO, centro=True)


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fontes = {
        "titulo": pygame.font.Font(None, 66),
        "media": pygame.font.Font(None, 32),
        "pequena": pygame.font.Font(None, 24),
    }
    imagens = carregar_imagens()
    estrelas = criar_estrelas()

    recorde = carregar_recorde(CAMINHO_RECORDE)
    ranking = carregar_ranking(CAMINHO_RANKING)
    partida = criar_partida(imagens)
    estado = "menu"
    rodando = True

    while rodando:
        relogio.tick(FPS)
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
            desenhar_menu(tela, fontes, recorde, ranking, estrelas)
        elif estado == "jogando":
            desenhar_partida(tela, fontes, partida, imagens, recorde, estrelas)
        elif estado == "pausado":
            desenhar_partida(tela, fontes, partida, imagens, recorde, estrelas)
            desenhar_pausa(tela, fontes)
        elif estado == "fim":
            desenhar_fim(tela, fontes, partida, recorde, ranking, estrelas)

        pygame.display.flip()

    pygame.quit()
