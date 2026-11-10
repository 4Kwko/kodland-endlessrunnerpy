# Endless runner em Python

Jogo 2D com Pygame Zero: o personagem corre automaticamente, pula espinhos e desliza para desviar de bolas de fogo. A pontuação cresce com o tempo; uma colisão zera a pontuação e limpa os obstáculos.

Projeto de estudo e portfólio. O nome do repositório faz referência ao exercício técnico, sem indicar vínculo de emprego com a Kodland.

## Executar

Com Python e Git instalados, crie e ative um ambiente virtual e execute:

```bash
git clone https://github.com/4Kwko/kodland-endlessrunnerpy.git
cd kodland-endlessrunnerpy
python -m pip install pgzero
cd kodland-test
pgzrun main.py
```

Use o executor `pgzrun`, que fornece os objetos de tela, teclado e música esperados pelo programa. Mantenha as pastas `images/` e `music/` junto de `main.py`.

## Controles

| Ação | Controle |
| --- | --- |
| Iniciar | Clique em **Start Game** no menu. |
| Pular | Espaço, seta para cima ou W, quando estiver no chão. |
| Deslizar | Seta para baixo ou S. |
| Alternar música | Clique em **Music: ON/OFF** no menu. |
| Sair | Clique em **Exit** no menu ou feche a janela. |

## Leitura do código

O arquivo [kodland-test/main.py](kodland-test/main.py) concentra a implementação:

- `Button`, `draw_menu` e os eventos do mouse cuidam do menu.
- `update(dt)` atualiza gravidade, animação, obstáculos, colisões e pontuação.
- `make_spike_group` e `make_fireball` criam os obstáculos.
- Os sprites e as faixas de áudio ficam nas pastas do projeto.

A apresentação acima foi conferida pela leitura do código. Não há suíte de testes nem resultado de validação gráfica publicado neste repositório.

<details>
<summary>English</summary>

A 2D endless runner built with Python and Pygame Zero. The character runs automatically; use Space, Up or W to jump, and Down or S to slide. Click the menu buttons to start, toggle music or exit.

Install `pgzero`, enter the `kodland-test` directory and run `pgzrun main.py`. Keep the image and music folders next to the script. The runner injects the screen, keyboard and music objects used by the game.

This is a study and portfolio project. Its repository name does not imply employment at Kodland. The description was checked against the source; no automated test suite or graphical validation result is published here.

</details>

[Perfil de João Montagner](https://github.com/4Kwko) · [Pygame Zero: documentação do executor](https://pygame-zero.readthedocs.io/en/stable/introduction.html)
