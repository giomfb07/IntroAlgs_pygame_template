from datetime import datetime
from pathlib import Path


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuacao recorde em arquivo texto."""
    # Cria um objeto Path com o caminho informado
    caminho = Path(caminho_arquivo)
    # Cria a pasta caso ela não exista
    caminho.parent.mkdir(parents=True, exist_ok=True)
    # Abre o arquivo em modo escrita
    with caminho.open("w", encoding="utf-8") as arquivo:
        # Escreve a pontuação convertida para texto
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se nao existir valor valido."""
    try:
        # Abre o arquivo para leitura
        with Path(caminho_arquivo).open("r", encoding="utf-8") as arquivo:

            # Remove espaços e quebras de linha
            conteudo = arquivo.read().strip()

            # Retorna o valor convertido para inteiro
            return int(conteudo) if conteudo else 0

    except (FileNotFoundError, ValueError):
        # Caso o arquivo não exista ou tenha texto inválido
        return 0


def atualizar_recorde(caminho_arquivo, pontuacao):
    """Atualiza o recorde quando a pontuacao informada for maior."""
    recorde_atual = carregar_recorde(caminho_arquivo)

    # Verifica se o jogador bateu o recorde
    if pontuacao > recorde_atual:
        # Salva o novo recorde
        salvar_recorde(caminho_arquivo, pontuacao)
        return pontuacao
    return recorde_atual


def salvar_resultado_ranking(caminho_arquivo, nome, pontuacao, status, data_hora=None):
    """Adiciona uma partida ao ranking em formato texto separado por ponto e virgula."""
    caminho = Path(caminho_arquivo)
    # Cria a pasta caso não exista
    caminho.parent.mkdir(parents=True, exist_ok=True)

    # Usa a data atual caso nenhuma seja informada
    data = data_hora or datetime.now().strftime("%Y-%m-%d %H:%M")
    # Remove caracteres inválidos
    nome_limpo = (nome or "Jogador").replace(";", " ").strip() or "Jogador"
    status_limpo = (status or "ENCERRADA").replace(";", " ").strip() or "ENCERRADA"
    
    # Abre o arquivo em modo adicionar
    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome_limpo};{int(pontuacao)};{status_limpo};{data}\n")


def carregar_ranking(caminho_arquivo, limite=5):
    """Carrega as melhores pontuacoes do ranking."""
    try:
        # Lê todas as linhas do arquivo
        linhas = Path(caminho_arquivo).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []

    ranking = []
    for linha in linhas:
        # Divide os campos usando ';'
        partes = linha.split(";")
        if len(partes) != 4:
            continue

        nome, pontos, status, data = partes
        try:
            pontuacao = int(pontos)
        except ValueError:
            continue

        ranking.append(
            {
                "nome": nome,
                "pontuacao": pontuacao,
                "status": status,
                "data": data,
            }
        )

    # Ordena do maior para o menor
    ranking.sort(key=lambda item: item["pontuacao"], reverse=True)
    # Retorna apenas as N melhores posições
    return ranking[:limite]
