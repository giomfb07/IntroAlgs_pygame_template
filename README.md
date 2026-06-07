# Beyond The Sky

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Emanuel Phillipe Ribeiro Ferreira Carvalho
- Giovanna Marques Freire Barbosa
- Pedro Miguel Souza Dias 

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

> Em Beyond The Sky, o personagem tem uma única ação: pular de plataforma em plataforma. O personagem realiza pequenos “jumps/saltos”, e o jogador precisa mirar, usando o cursor do mouse, nas plataformas geradas acima dele. Os objetivos são: fazer com que o avatar sempre esteja no andar mais alto, não caia para as plataformas de baixo (perde pontos se ocorrer) e desvie dos obstáculos, aos quais se encostar perde-se 1/3 de vida. Caso este caia muitos andares de uma vez só, perde-se a partida. Com isso, estando mais alto do que na última tentativa, o jogador atinge um novo recorde de pontuação e vence em cima de suas partidas anteriores.

## Objetivo do jogador

> O objetivo do jogador é manter o personagem no andar mais alto possível pulando de plataforma de plataforma, aumentando sua pontuação a cada um. Ademais, o jogador deve evitar cair para baixo de sua plataforma atual e desviar dos obstáculos que o fazem perder vidas (3 no total).

## Regras do jogo  

- O jogador se movimenta usando o cursor do mouse e pulo duplo
- O jogador se movimenta usando pulo duplo, limitado a 2 vezes por partida
- O avatar tem 3 vidas
- O avatar perde uma vida se colidir com um inimigo
- Cada altura alcançada irá aumentar a pontuação do avatar
- O avatar perde pontos se cair nas plataformas de baixo 
- A partida termina quando o avatar chegar no final do percurso
- A partida termina quando o avatar colidir com 3 inimigos
- A partida termina quando o avatar cai de todas as plataformas

## Controles

- **MOUSE para a esquerda:** Movimenta o personagem para a esquerda.
- **MOUSE para a direita:** Movimenta o personagem para a direita.
- **Tecla ESC:** Pausa a partida atual.
- **Tecla SPACE:** Personagem aciona um pulo duplo.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/giomfb07/IntroAlgs_pygame_template.git
cd IntroAlgs_pygame_template
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```
