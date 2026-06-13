def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma pontos, mantendo a pontuacao minima em zero."""
    return max(0, pontos_atual + pontos_ganhos)


def calcular_pontos_por_andar(pontos_atual, andar_atual, maior_andar, pontos_por_andar=20):
    """Pontua apenas pelos andares novos alcancados."""
    if andar_atual <= maior_andar:
        return pontos_atual

    andares_subidos = andar_atual - maior_andar
    return calcular_pontos(pontos_atual, andares_subidos * pontos_por_andar)


def penalizar_queda(pontos_atual, andar_anterior, andar_atual, penalidade_por_andar=10):
    """Remove pontos quando o jogador cai para uma plataforma mais baixa."""
    andares_perdidos = max(0, andar_anterior - andar_atual)
    return calcular_pontos(pontos_atual, -(andares_perdidos * penalidade_por_andar))


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido, sem ficar negativa."""
    return max(0, vida_atual - dano)


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def jogador_venceu(andar_atual, andar_final):
    """Indica se o jogador chegou ao final do percurso."""
    return andar_atual >= andar_final


def queda_fatal(andar_atual, maior_andar, limite_andares=5):
    """Indica se o jogador caiu muitos andares em relacao ao melhor andar da partida."""
    return maior_andar - andar_atual >= limite_andares


def consumir_pulo_duplo(pulos_disponiveis):
    """Tenta consumir um pulo duplo e retorna (novo_total, conseguiu)."""
    if pulos_disponiveis <= 0:
        return 0, False

    return pulos_disponiveis - 1, True


def limitar_valor(valor, minimo, maximo):
    """Mantem um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposicao entre dois retangulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)
