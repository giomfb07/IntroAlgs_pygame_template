from datetime import datetime
from pathlib import Path


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuacao recorde em arquivo texto."""
    caminho = Path(caminho_arquivo)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se nao existir valor valido."""
    try:
        with Path(caminho_arquivo).open("r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            return int(conteudo) if conteudo else 0
    except (FileNotFoundError, ValueError):
        return 0


def atualizar_recorde(caminho_arquivo, pontuacao):
    """Atualiza o recorde quando a pontuacao informada for maior."""
    recorde_atual = carregar_recorde(caminho_arquivo)
    if pontuacao > recorde_atual:
        salvar_recorde(caminho_arquivo, pontuacao)
        return pontuacao
    return recorde_atual


def salvar_resultado_ranking(caminho_arquivo, nome, pontuacao, status, data_hora=None):
    """Adiciona uma partida ao ranking em formato texto separado por ponto e virgula."""
    caminho = Path(caminho_arquivo)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    data = data_hora or datetime.now().strftime("%Y-%m-%d %H:%M")
    nome_limpo = (nome or "Jogador").replace(";", " ").strip() or "Jogador"
    status_limpo = (status or "ENCERRADA").replace(";", " ").strip() or "ENCERRADA"

    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome_limpo};{int(pontuacao)};{status_limpo};{data}\n")


def carregar_ranking(caminho_arquivo, limite=5):
    """Carrega as melhores pontuacoes do ranking."""
    try:
        linhas = Path(caminho_arquivo).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []

    ranking = []
    for linha in linhas:
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

    ranking.sort(key=lambda item: item["pontuacao"], reverse=True)
    return ranking[:limite]
