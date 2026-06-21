# Configuracoes centrais do jogo.
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Beyond The Stars"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
AZUL_ESCURO = (12, 18, 38)
AZUL_MEDIO = (38, 72, 128)
AMARELO = (246, 215, 92)
VERDE = (72, 176, 114)
VERMELHO = (212, 78, 78)
ROXO = (120, 86, 180)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_RANKING = "data/ranking.txt"
CAMINHO_SPRITES = "assets/imagens/Slime1_Run_body.png"
CAMINHO_ESTRELA = "assets/imagens/Magical_rainbow_star.png"

VIDAS_INICIAIS = 3
PULOS_DUPLOS_INICIAIS = 2
PONTOS_POR_ANDAR = 20
PENALIDADE_QUEDA = 10
ANDAR_FINAL = 200
LIMITE_QUEDA_FATAL = 5

GRAVIDADE = 0.40
IMPULSO_PULO = -12
IMPULSO_PULO_DUPLO = -16
VELOCIDADE_HORIZONTAL = 10
ESPACO_PLATAFORMAS = 80
LARGURA_PLATAFORMA = 145
ALTURA_PLATAFORMA = 18

FASES = [
    {
        'nome': 'Fase 1',
        'cor_fundo': (10, 10, 40),
        'imagem_fundo': './assets/imagens/fundo_fase1.png', 
        'chance_obstaculo_base': 0.18,
        'gravidade': GRAVIDADE,
        'vel_horizontal': VELOCIDADE_HORIZONTAL,
        'andar_inicial': 0,
        'andar_final': 49,
    },
    {
        'nome': 'Fase 2',
        'cor_fundo': (50, 0, 80),
        'imagem_fundo': './assets/imagens/fundo_fase2.png', 
        'chance_obstaculo_base': 0.25,
        'gravidade': GRAVIDADE * 1.1,
        'vel_horizontal': VELOCIDADE_HORIZONTAL * 1.1,
        'andar_inicial': 50,
        'andar_final': 89,
    },
    {
        'nome': 'Fase 3',
        'cor_fundo': (80, 20, 20),
        'imagem_fundo': './assets/imagens/fundo_fase3.png', 
        'chance_obstaculo_base': 0.32,
        'gravidade': GRAVIDADE * 1.2,
        'vel_horizontal': VELOCIDADE_HORIZONTAL * 1.2,
        'andar_inicial': 90,
        'andar_final': 149,
    },
    {
        'nome': 'Fase 4',
        'cor_fundo': (80, 70, 20),
        'imagem_fundo': './assets/imagens/fundo_fase4.png', 
        'chance_obstaculo_base': 0.40,
        'gravidade': GRAVIDADE * 1.3,
        'vel_horizontal': VELOCIDADE_HORIZONTAL * 1.3,
        'andar_inicial': 150,
        'andar_final': 200,
    },
]

def obter_fase(andar):
    for fase in FASES:
        if fase['andar_inicial'] <= andar <= fase['andar_final']:
            return fase
    return FASES[-1]