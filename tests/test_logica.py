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
)


def test_calcular_pontos_soma_sem_ficar_negativo():
    assert calcular_pontos(10, 5) == 15
    assert calcular_pontos(5, -20) == 0


def test_calcular_pontos_por_andar_so_pontua_andar_novo():
    assert calcular_pontos_por_andar(40, andar_atual=5, maior_andar=3) == 80
    assert calcular_pontos_por_andar(40, andar_atual=3, maior_andar=5) == 40


def test_penalizar_queda_remove_pontos_por_andar_perdido():
    assert penalizar_queda(100, andar_anterior=8, andar_atual=6) == 80
    assert penalizar_queda(5, andar_anterior=8, andar_atual=1) == 0


def test_tomar_dano_nao_deixa_vida_negativa():
    assert tomar_dano(3, 1) == 2
    assert tomar_dano(1, 5) == 0


def test_jogador_perdeu_com_zero_vidas():
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    assert jogador_perdeu(3) is False


def test_jogador_venceu_ao_chegar_no_andar_final():
    assert jogador_venceu(30, 30) is True
    assert jogador_venceu(29, 30) is False


def test_queda_fatal_quando_perde_muitos_andares():
    assert queda_fatal(andar_atual=4, maior_andar=10, limite_andares=5) is True
    assert queda_fatal(andar_atual=7, maior_andar=10, limite_andares=5) is False


def test_consumir_pulo_duplo():
    assert consumir_pulo_duplo(2) == (1, True)
    assert consumir_pulo_duplo(0) == (0, False)


def test_limitar_valor_abaixo_do_minimo():
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    assert limitar_valor(50, 0, 100) == 50


def test_recorde_retorna_zero_quando_arquivo_nao_existe(tmp_path):
    assert carregar_recorde(tmp_path / "recorde.txt") == 0


def test_atualizar_recorde_salva_apenas_pontuacao_maior(tmp_path):
    caminho = tmp_path / "recorde.txt"

    assert atualizar_recorde(caminho, 100) == 100
    assert carregar_recorde(caminho) == 100
    assert atualizar_recorde(caminho, 80) == 100
    assert carregar_recorde(caminho) == 100


def test_carregar_ranking_ignora_linhas_invalidas_e_ordena(tmp_path):
    caminho = tmp_path / "ranking.txt"
    salvar_resultado_ranking(caminho, "Ana", 120, "VITORIA", "2026-01-01 10:00")
    salvar_resultado_ranking(caminho, "Bia", 80, "DERROTA", "2026-01-01 10:05")
    caminho.write_text(caminho.read_text(encoding="utf-8") + "linha invalida\n", encoding="utf-8")
    salvar_resultado_ranking(caminho, "Caio", 150, "VITORIA", "2026-01-01 10:10")

    ranking = carregar_ranking(caminho)

    assert [item["nome"] for item in ranking] == ["Caio", "Ana", "Bia"]
    assert [item["pontuacao"] for item in ranking] == [150, 120, 80]
