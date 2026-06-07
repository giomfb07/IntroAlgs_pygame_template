# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> Beyond The Sky

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: Emanuel Phillipe Ribeiro Ferreira Carvalho
- Nome 2: Giovanna Marques Freire Barbosa
- Nome 3: Pedro Miguel Souza Dias 

## 3. Tipo de jogo

> Jogo de desviar de obstáculos e escalar.

## 4. Descrição geral do jogo

> Em Beyond The Sky, o personagem tem uma única ação: pular de plataforma em plataforma. O personagem realiza pequenos “jumps/saltos”, e o jogador precisa mirar, usando o cursor do mouse, nas plataformas geradas acima dele. Os objetivos são: fazer com que o avatar sempre esteja no andar mais alto, não caia para as plataformas de baixo (perde pontos se ocorrer) e desvie dos obstáculos, aos quais se encostar perde-se 1/3 de vida. Caso este caia muitos andares de uma vez só, perde-se a partida. Com isso, estando mais alto do que na última tentativa, o jogador atinge um novo recorde de pontuação e vence em cima de suas partidas anteriores.

## 5. Objetivo do jogador

> O objetivo do jogador é manter o personagem no andar mais alto possível pulando de plataforma de plataforma, aumentando sua pontuação a cada um. Ademais, o jogador deve evitar cair para baixo de sua plataforma atual e desviar dos obstáculos que o fazem perder vidas (3 no total).

## 6. Regras principais

- Regra 1: O jogador se movimenta usando o cursor do mouse.
- Regra 2: O jogador se movimenta usando pulo duplo, limitado a 2 vezes por partida.
- Regra 3: O avatar tem 3 vidas e perde uma vida se colidir com um inimigo.
- Regra 4: A cada altura alcançada irá aumentar a pontuação do avatar.
- Regra 5: O avatar perde pontos se cair nas plataformas de baixo.

## 7. Condição de vitória

> O jogador vence a partida atual ao atingir um andar mais alto que o da última tentativa, implicando diretamente em sua pontuação. Ou seja, se o jogador atingir uma pontuação maior que a anterior, considera-se que este venceu.

## 8. Condição de derrota ou encerramento

> A partida termina quando o avatar perder todas as vidas (3) ou se o avatar cair de todas as plataformas.

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Descrição:

> Um personagem que executa saltos a cada intervalo de tempo e é controlado por movimentos de mouse para a direita e à esquerda realizados pelo jogador.

## Obstáculos, inimigos ou desafios

Descrição:

### Obstáculos

> Os obstáculos são balões aos quais o jogador deve desviar. Estes são gerados em posições aleatórias acima do avatar e mantidos no mesmo local ao passar por eles.

### Desafios

> Como desafio, o jogador deve evitar ao máximo encostar nos balões gerados, uma vez que, cada vez que comete este deslize, uma vida, de no máximo 3, é perdida. 
> Além disso, o jogador deve evitar que o avatar “despenque” para os andares/plataformas abaixo, pois, se este cair muitos andares de uma vez só, ele perde automaticamente. Há também o risco de um balão ser encostado pelo avatar durante a queda.

## Itens, alvos ou objetos de interação

- Balões: Objetos gerados em posições aleatórias aos quais o avatar não pode encostar mais de 2 vezes, uma vez que, na 3ª, a partida é automaticamente encerrada.

## Pontuação, vidas, tempo ou progresso

> O jogador inicia a partida com 3 vidas (corações), 0 pontos e 2 pulos duplos usáveis. A cada plataforma que subir, adicionam-se +20 pontos à contagem atual. Em uma emergência, o jogador pode acionar 1 pulo duplo pressionando ESPAÇO caso ainda não tenha os gasto.

## 10. Controles previstos

- **MOUSE para a esquerda:** Movimenta o personagem para a esquerda.
- **MOUSE para a direita:** Movimenta o personagem para a direita.
- **Tecla ESC:** Pausa a partida atual.
- **Tecla SPACE:** Personagem aciona um pulo duplo.

Controles do grupo:

- **Tecla R:** A partida perdida é iniciada novamente do local de perda a fim de testes.

## 11. Organização inicial do código

- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.

Organização planejada:

> O grupo iniciará em um primeiro momento com o desenvolvimento da interface inicial do jogo, onde vê-se a pontuação máxima que o jogador já atingiu e os botões para iniciar uma nova partida e sair do jogo (fechá-lo). 
> Seguindo este ponto, terá o início da construção da interface da partida em si com uma dinâmica de geração gradual das plataformas acima do avatar. Ademais, a contagem de pontos ao decorrer da subida e o pulo duplo também serão desenvolvidos.
> Em um terceiro momento, tem-se o desenvolvimento da geração com posições aleatórias dos balões. do esquema de perda de vida ao avatar encostar neles e o limite de 2 balões “encostáveis”. Junto a isso, há a construção do algoritmo responsável por medir a quantidade de plataformas que o avatar caiu para determinar o encerramento da partida ou não.

## 12. Recursos externos previstos

Informe se o grupo pretende utilizar imagens, sons, fontes, tutoriais ou códigos externos.

Recursos previstos:

- Tutorial usado apenas como referência.
- Sons gratuitos.
- Imagens obtidas de banco gratuito.

## 13. Principais dificuldades esperadas

Liste as dificuldades que o grupo acredita que poderá enfrentar.

- Dificuldade 1: Geração gradual das plataformas e obstáculos.
- Dificuldade 2: Colisão entre avatar e obstáculos.
- Dificuldade 3: Movimentação do avatar.

## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

Esta seção é importante para evitar que o grupo escolha uma ideia grande demais.

Escopo mínimo:

> A versão mínima do jogo terá um personagem controlado pelo mouse do jogador, apresentando: 
> Plataformas geradas em posições aleatórias acima da posição do avatar; obstáculos gerados em posições aleatórias acima da posição do avatar e fixados lá até o momento da perda; pontuação a cada andar alcançado; salvamento da maior pontuação que o usuário atingir; esquema de 3 vidas por partida.

## 15. Possíveis melhorias, caso haja tempo

Liste funcionalidades extras que o grupo poderá implementar se conseguir concluir o escopo mínimo.

Melhorias possíveis:

- Melhoria 1: Novos tipos de obstáculos;
- Melhoria 2: Novos planos de fundo para as partidas;
- Melhoria 3: Aumento de dificuldade a cada nova pontuação máxima alcançada;
- Melhoria 4: Esquema de reviver em casos de perda gastando um possível tipo de moeda.
