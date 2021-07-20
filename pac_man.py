from abc import (ABCMeta, abstractmethod)
import random
import pygame



def play():
    pygame.init()

    # Inicialização surface + cores
    tela = pygame.display.set_mode((800, 580), 0, 0)
    verde = (0, 255, 0)
    azul = (0, 0, 150)
    vermelho = (255, 0 , 0)
    amarelo = (255, 255, 0)
    roxo = (150, 0, 255)
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    laranja = (255, 140, 0)
    rosa = (255, 15, 192)
    ciano = (0, 255, 255)

    #Declaração de variáveis externas para a direção do pacman:
    cima = 1
    baixo = 2
    dir = 3
    esq = 4

    #Mudando o nome da janela + criação de fontes:
    pygame.display.set_caption("Pac-man")
    fonteG = pygame.font.SysFont("courier new", 72, True, False)
    fonteM = pygame.font.SysFont("courier new", 30, True, False)
    fonteP = pygame.font.SysFont("courier new", 20, True, False)
    fontePP = pygame.font.SysFont("courier new", 15, True, True)


    #Classes abstratas atuando como interface:
    class ElementoJogo(metaclass=ABCMeta):

        @abstractmethod
        def draw(self, surface):
            pass

        @abstractmethod
        def calcular_regras(self):
            pass

        @abstractmethod
        def processa_eventos(self, eventos):
            pass


    class Personagem(metaclass=ABCMeta):

        @abstractmethod
        def aceita_movimento(self):
            pass

        @abstractmethod
        def reprova_movimento(self, direcoes):
            pass

        @abstractmethod
        def esquina(self, direcoes):
            pass

    #Elementos do jogo:
    class Pacman(ElementoJogo, Personagem):
        def __init__(self, tamanho):
            self.centro_x = 400
            self.centro_y = 300
            self.tamanho = tamanho
            self.raio = int(self.tamanho/2)
            self.vel_x = 0
            self.vel_y = 0
            self.coluna = 1
            self.linha = 1
            self.vidas = 3
            self.coluna_intencao = self.coluna
            self.linha_intencao = self.linha
            self.abertura_animacao = 0
            self.vel_abertura = 2

        #Aprova/reprova movimento pacman / impede de sair da tela de jogo
        def calcular_regras(self):
            self.coluna_intencao = self.coluna + self.vel_x
            self.linha_intencao = self.linha + self.vel_y
            self.centro_x = int(self.coluna * self.tamanho + self.raio)
            self.centro_y = int(self.linha * self.tamanho + self.raio)
            if self.centro_x + self.raio > 800:
                self.vel_x = -1
            if self.centro_x - self.raio < 0:
                self.vel_x = 1
            if self.centro_y + self.raio > 600:
                self.vel_y = -1
            if self.centro_y - self.raio < 0:
                self.vel_y = 1

        #Desenha pacman parado, e caso o jogo esteja pausado, o congela:
        def draw(self, surface):
            if cenario.state == 0:
                if self.vel_x == -1: #Keyleft/A
                    self.pac_left(surface)

                elif self.vel_y == 1: #Keydown/S
                    self.pac_down(surface)

                elif self.vel_y == -1: #Keyup/W
                    self.pac_up(surface)

                else: #Keyright/D/default
                    self.pac_right_default(surface)
            else:
                ponto_centro = (self.centro_x, self.centro_y)
                pygame.draw.circle(surface, amarelo, ponto_centro, self.raio, 0)
                canto_da_boca = (self.centro_x + self.raio, self.centro_y + self.abertura_animacao)
                ponto_superior = (self.centro_x + self.raio, self.centro_y - self.abertura_animacao)
                pontos = [ponto_centro, ponto_superior, canto_da_boca]
                pygame.draw.polygon(surface, preto, pontos, 0)
                olho_x = int((self.centro_x + self.raio / 3))
                olho_y = int((self.centro_y - self.raio * 0.7))
                olho_raio = int(self.raio / 10)
                pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        #Animações do pacman para todas as direções:
        def pac_down(self, surface):
            self.abertura_animacao += self.vel_abertura

            if self.abertura_animacao > self.raio:
                self.vel_abertura = -2
            if self.abertura_animacao <= 0:
                self.vel_abertura = 2

            ponto_centro = (self.centro_x, self.centro_y)
            pygame.draw.circle(surface, amarelo, ponto_centro, self.raio, 0)
            canto_da_boca = (self.centro_x - self.abertura_animacao, self.centro_y + self.raio)
            ponto_superior = (self.centro_x + self.abertura_animacao, self.centro_y + self.raio)
            pontos = [ponto_centro, ponto_superior, canto_da_boca]
            pygame.draw.polygon(surface, preto, pontos, 0)
            olho_x = int((self.centro_x + self.raio / 2))
            olho_y = int((self.centro_y - self.raio * 0.1))
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        def pac_up(self, surface):
            self.abertura_animacao += self.vel_abertura

            if self.abertura_animacao > self.raio:
                self.vel_abertura = -2
            if self.abertura_animacao <= 0:
                self.vel_abertura = 2

            ponto_centro = (self.centro_x, self.centro_y)
            pygame.draw.circle(surface, amarelo, ponto_centro, self.raio, 0)
            canto_da_boca = (self.centro_x - self.abertura_animacao, self.centro_y - self.raio)
            ponto_superior = (self.centro_x + self.abertura_animacao, self.centro_y - self.raio)
            pontos = [ponto_centro, ponto_superior, canto_da_boca]
            pygame.draw.polygon(surface, preto, pontos, 0)
            olho_x = int((self.centro_x - self.raio // 2))
            olho_y = int((self.centro_y + self.raio * 0.1))
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        def pac_left(self, surface):
            self.abertura_animacao += self.vel_abertura

            if self.abertura_animacao > self.raio:
                self.vel_abertura = -2
            if self.abertura_animacao <= 0:
                self.vel_abertura = 2

            ponto_centro = (self.centro_x, self.centro_y)
            pygame.draw.circle(surface, amarelo, ponto_centro, self.raio, 0)
            canto_da_boca = (self.centro_x - self.raio, self.centro_y + self.abertura_animacao)
            ponto_superior = (self.centro_x - self.raio, self.centro_y - self.abertura_animacao)
            pontos = [ponto_centro, ponto_superior, canto_da_boca]
            pygame.draw.polygon(surface, preto, pontos, 0)
            olho_x = int((self.centro_x - self.raio / 5))
            olho_y = int((self.centro_y - self.raio * 0.7))
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        def pac_right_default(self, surface):
            self.abertura_animacao += self.vel_abertura

            if self.abertura_animacao > self.raio:
                self.vel_abertura = -2
            if self.abertura_animacao <= 0:
                self.vel_abertura = 2

            ponto_centro = (self.centro_x, self.centro_y)
            pygame.draw.circle(surface, amarelo, ponto_centro, self.raio, 0)
            canto_da_boca = (self.centro_x + self.raio, self.centro_y + self.abertura_animacao)
            ponto_superior = (self.centro_x + self.raio, self.centro_y - self.abertura_animacao)
            pontos = [ponto_centro, ponto_superior, canto_da_boca]
            pygame.draw.polygon(surface, preto, pontos, 0)
            olho_x = int((self.centro_x + self.raio / 3))
            olho_y = int((self.centro_y - self.raio * 0.7))
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        #Captura e processamento de eventos  do mouse e do teclado:
        def processa_eventos(self, eventos):
            vel = 1
            for e in eventos:
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                        pacman.vel_x = vel
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                        pacman.vel_x = 0
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                        pacman.vel_x = -vel
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                        pacman.vel_x = 0
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                        pacman.vel_y = vel
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                        pacman.vel_y = 0
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP or e.key == pygame.K_w:
                        pacman.vel_y = -vel
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_UP or e.key == pygame.K_w:
                        pacman.vel_y = 0

        #Caso o cenário aprove o movimento do pacman ou o reprove, estas funções são chamadas:
        def aceita_movimento(self):
            self.linha = self.linha_intencao
            self.coluna = self.coluna_intencao

        def reprova_movimento(self, direcoes):
            self.coluna_intencao = self.linha
            self.linha_intencao = self.linha

        #Método oco, somente para bater com a abc:
        def esquina(self, direcoes):
            pass


    class Fantasma(ElementoJogo, Personagem):
        def __init__(self, cor, tamanho, c):
            self.coluna = c
            self.linha = 12
            self.linha_intencao = self.linha
            self.coluna_intencao = self.coluna
            self.velocidade = 1
            self.direcao = 2
            self.cor = cor
            self.tamanho = tamanho

        #Desenha o fantasma
        def draw(self, surface):
            fatia = self.tamanho // 8
            px = int(self.coluna * self.tamanho)
            py = int(self.linha * self.tamanho)
            contorno = [(px, py + self.tamanho),
                        (px + fatia, py + fatia * 2),
                        (px + fatia * 2, py + fatia // 2),
                        (px + fatia * 3, py),
                        (px + fatia * 5, py),
                        (px + fatia * 6, py + fatia // 2),
                        (px + fatia * 7, py + fatia * 2),
                        (px + fatia * 8, py + self.tamanho)]
            pygame.draw.polygon(surface, self.cor, contorno, 0)

            olho_radius_int = fatia // 2
            olho_radius_ext = fatia
            olho_e_x = int(px + fatia * 2.5)
            olho_e_y = int(py + fatia * 2.5)
            olho_d_x = int(px + fatia * 6)
            olho_d_y = int(py + fatia * 2.5)

            pygame.draw.circle(surface, branco, (olho_e_x, olho_e_y), olho_radius_ext, 0)
            pygame.draw.circle(surface, preto, (olho_e_x, olho_e_y), olho_radius_int, 0)
            pygame.draw.circle(surface, branco, (olho_d_x, olho_d_y), olho_radius_ext, 0)
            pygame.draw.circle(surface, preto, (olho_d_x, olho_d_y), olho_radius_int, 0)

        #Altera a velocidade x ou y dependendo do movimento
        def calcular_regras(self):
            if self.direcao == cima:
                self.linha_intencao -= self.velocidade
            elif self.direcao == baixo:
                self.linha_intencao += self.velocidade
            elif self.direcao == dir:
                self.coluna_intencao += self.velocidade
            elif self.direcao == esq:
                self.coluna_intencao -= self.velocidade

        #Classe oca, apenas para combinar com a abc:
        def processa_eventos(self, eventos):
            pass

        #Randomiza direção do fantasma
        def muda_direcao(self, direcoes):
            self.direcao = random.choice(direcoes)

        #Ao passar por uma esquina dá a opção de escolher virar, seguir ou voltar:
        def esquina(self, direcoes):
            self.muda_direcao(direcoes)

        #Funções chamadas quando Cenario aprova ou reprova o movmento do fantasma (caso seja reprovado, muda a direção)
        def aceita_movimento(self):
            self.linha = self.linha_intencao
            self.coluna = self.coluna_intencao

        def reprova_movimento(self, direcoes):
            self.linha_intencao = self.linha
            self.coluna_intencao = self.coluna
            self.muda_direcao(direcoes)

    #Classe principal
    class Cenario(ElementoJogo):
        def __init__(self, tamanho, pac):
            self.pacman = pac
            self.tamanho = tamanho
            self.pontos = 0
            self.personagens = [pac]
            self.state = 0
            self.restart = False
            self.matriz = [
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
                [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
                [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
                [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
                [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
                [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
                [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ]

        #Adiciona personagens à lista de personagens
        def adiciona_personagem(self, personagens):
            for p in personagens:
                self.personagens.append(p)


        def calcular_regras(self):
            # Confere e aprova/reprova movimentos
            if self.state == 0:
                for p in self.personagens:
                    lin = int(p.linha)
                    col = int(p.coluna)
                    lin_intencao = int(p.linha_intencao)
                    col_intencao = int(p.coluna_intencao)
                    direcoes = self.get_direction(lin, col)
                    if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                        p.aceita_movimento()
                    else:
                        p.reprova_movimento(direcoes)
                    if len(direcoes) >= 3:
                        p.esquina(direcoes)

                    # Conferindo se o pacman faz ou não faz ponto na casa em que está:
                    if isinstance(p, Pacman) and self.matriz[lin][col] == 1:
                        self.faz_ponto(lin, col)

                    #Conferindo se o jogador ganhou:
                    if self.pontos >= 306:
                        self.state = 3

                    #Conferindo se o fantasma acertou o pacman e tirando uma vida do jogador:
                    if isinstance(p, Fantasma) and p.linha == self.pacman.linha and p.coluna == self.pacman.coluna:
                        self.pacman.vidas -= 1
                        if self.pacman.vidas < 0:
                            self.state = 2
                        else:
                            #Caso não tenha morrido, o pacman será movido para a casa 1x1
                            self.pacman.linha = 1
                            self.pacman.coluna = 1

        #Obtem as possíveis direções para os fantasmas:
        def get_direction(self, linha, coluna):
            direcoes = []
            if self.matriz[int(linha-1)][int(coluna)] != 2:
                direcoes.append(cima)
            if self.matriz[int(linha+1)][int(coluna)] != 2:
                direcoes.append(baixo)
            if self.matriz[int(linha)][int(coluna-1)] != 2:
                direcoes.append(esq)
            if self.matriz[int(linha)][int(coluna+1)] != 2:
                direcoes.append(dir)

            return direcoes

        #Desenha o labirinto:
        def draw_line(self, surface, numero_linha, linha):
            for numero_coluna, coluna in enumerate(linha):
                x = self.tamanho * numero_coluna
                y = self.tamanho * numero_linha
                cor = preto
                if coluna == 2:
                    cor = azul
                pygame.draw.rect(surface, cor, (x, y, self.tamanho, self.tamanho), 0)
                half = self.tamanho // 2
                if coluna == 1:
                    pygame.draw.circle(surface, amarelo, (x + half, y + half), self.tamanho//10, 0)

        #Computa quantas pastilhas (pontos) foram comidas:
        def faz_ponto(self, lin, col):
            self.pontos += 1
            self.matriz[lin][col] = 0

        #cria botão de restart nas telas de vitória e gameover
        def restart_button(self, surface):
            cor_bt = branco
            x = 580
            y = 500
            larg = 200
            alt = 50
            mouse = pygame.mouse.get_pos()
            if x < mouse[0] < x + larg and y < mouse[1] < y + alt:
                cor_bt = amarelo
                if self.restart:
                    play()
            pygame.draw.rect(surface, cor_bt, (x, y, larg, alt), 4)
            img_jg_nov = fonteP.render("jogar de novo", True, cor_bt)
            surface.blit(img_jg_nov, (602, 515))

        #Dependendoo de self.state, reproduz o jogo ou as telas correspondentes:
        def draw(self, surface):
            if self.state == 1:
                self.draw_pause(surface)
            elif self.state == 0:
                self.draw_jogando(surface)
            elif self.state == 2:
                self.draw_gameover(surface)
            elif self.state == 3:
                self.draw_win(surface)

        #desenha um pacman decorativo:
        def draw_frozen_pacman(self, centro_x, centro_y, tamanho, surface):
            raio = int(tamanho / 2)
            ponto_centro = (centro_x, centro_y)
            pygame.draw.circle(surface, amarelo, ponto_centro, raio, 0)
            canto_da_boca = (centro_x + raio, centro_y)
            ponto_superior = (centro_x + raio, centro_y - raio)
            pontos = [ponto_centro, ponto_superior, canto_da_boca]
            pygame.draw.polygon(surface, preto, pontos, 0)
            olho_x = int((centro_x + raio / 3))
            olho_y = int((centro_y - raio * 0.7))
            olho_raio = int(raio / 10)
            pygame.draw.circle(surface, preto, (olho_x, olho_y), olho_raio, 0)

        def draw_gameover(self, surface):
            surface.fill(preto)
            img_go = fonteG.render("GAME OVER", True, vermelho)
            x_go = (800 - img_go.get_width()) // 2
            y_go = (580 - img_go.get_height()) // 2
            surface.blit(img_go, (x_go, y_go))
            self.draw_frozen_pacman(400, 200, 100, surface)
            surface.blit(cenario.atualiza_pontos(amarelo), (337, 350))
            self.restart_button(surface)

        def draw_win(self, surface):
            surface.fill(preto)
            img_vid = fonteM.render(f"Vidas restantes:{self.pacman.vidas}", True, rosa)
            img_go = fonteG.render("VITÓRIA!", True, laranja)
            img_mito = fonteM.render("Muito bem!", True, verde)
            img_pts = fonteM.render(f"Score:{self.pontos * (self.pacman.vidas + 1)}", True, roxo)
            x_go = (800 - img_go.get_width()) // 2
            y_go = (580 - img_go.get_height()) // 2
            surface.blit(img_go, (x_go, y_go))
            self.draw_frozen_pacman(400, 180, 100, surface)
            surface.blit(img_mito, (310, 340))
            surface.blit(img_vid, (247, 400))
            surface.blit(img_pts, (315, 370))
            self.restart_button(surface)

        def draw_pause(self, surface):
            self.draw_jogando(surface)
            img_pause = fonteM.render("Pausado", True, amarelo, preto)
            x_pause = (600)
            y_pause = (90)
            surface.blit(img_pause, (x_pause, y_pause))

        def draw_jogando(self, surface):
            for numero_linha, linha in enumerate(self.matriz):
                self.draw_line(surface, numero_linha, linha)
            self.draw_frozen_pacman(625, 230, 50, surface)
            img_vidas = fonteM.render(f"X {self.pacman.vidas}", True, amarelo)
            surface.blit(img_vidas, (660, 210))
            texto_logo = fonteM.render("PA -MAN", True, amarelo)
            texto_instrucoes = fonteP.render("Controles:", True, amarelo)
            texto_pause_tecla = fonteP.render("Tecla P:", True, laranja)
            texto_pause_desc = fonteP.render("Play/Pause", True, vermelho)
            texto_movimentacao_tecla = fonteP.render("AWSD/Setas:", True, laranja)
            texto_movimentacao_desc = fonteP.render("mover pac-man", True, vermelho)
            texto_assinatura = fontePP.render("by Lucas", True, branco)
            surface.blit(texto_instrucoes, (590, 300))
            surface.blit(texto_pause_tecla, (590, 350))
            surface.blit(texto_pause_desc, (590, 400))
            surface.blit(texto_movimentacao_tecla, (590, 450))
            surface.blit(texto_movimentacao_desc, (590, 500))
            surface.blit(texto_logo, (601, 45))
            surface.blit(texto_assinatura, (601, 70))
            self.draw_frozen_pacman(646, 60, 20, surface)
            pygame.draw.rect(surface, amarelo, (575, 30, 180, 530), 5)


        def atualiza_pontos(self, cor):
            texto_pontos = fonteM.render(f"Score:{self.pontos}", True, cor)
            return texto_pontos

        def processa_eventos(self, eventos):
            for e in eventos:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_p:
                        if self.state == 0:
                            self.state = 1
                        elif self.state == 1:
                            self.state = 0
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    x = 580
                    y = 500
                    larg = 200
                    alt = 50
                    if self.state == 2 or self.state == 3:
                        if x < mouse[0] < x+larg and y < mouse[1] < y+alt:
                            self.restart = True
                if e.type == pygame.QUIT:
                    exit()



    #Criação dos personagens + adição destes ao cenário:
    size = 600//30
    blinky = Fantasma(vermelho, size, 12)
    inky = Fantasma(ciano, size, 13)
    clyde = Fantasma(laranja, size, 14)
    pinky = Fantasma(rosa, size, 15)
    pacman = Pacman(size)
    fantasmas = [inky, blinky, pinky, clyde]
    cenario = Cenario(size, pacman)
    cenario.adiciona_personagem(fantasmas)

    #Gameloop
    while True:
        #Calculo de regras:
        pacman.calcular_regras()
        inky.calcular_regras()
        blinky.calcular_regras()
        pinky.calcular_regras()
        clyde.calcular_regras()
        cenario.calcular_regras()
        pygame.time.delay(50)

        #Desenho do cenário e dos personagens:
        tela.fill(preto)
        cenario.draw(tela)
        if cenario.state != 2:
            if cenario.state != 3:
                tela.blit(cenario.atualiza_pontos(amarelo), (586, 120))
                inky.draw(tela)
                blinky.draw(tela)
                pinky.draw(tela)
                clyde.draw(tela)
                pacman.draw(tela)

        #Processamento de eventos:
        eventos = pygame.event.get()
        pacman.processa_eventos(eventos)
        cenario.processa_eventos(eventos)
        pygame.display.update()

play()