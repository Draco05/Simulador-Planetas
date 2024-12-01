# Simulador do problema dos 3 corpos - Física Básica

# Bibliotecas importadas
import pygame
from math import sqrt

# Inicializar o Pygame
pygame.init()

# Constantes 
G = 6.67408e-11  # N m^2 / Kg^2
AU = 1.49597e11  # m
ESCALA = 50 / AU  # 50 pixels por AU
TEMPO_POR_ETAPA = 3600 * 24  # 1 dia
FPS = 60  # 60 dias por segundo

# Cores
PRETO = pygame.Color(0, 0, 0)
BRANCO = pygame.Color(255, 255, 255)
VERMELHO = pygame.Color(255, 0, 0)
VERDE = pygame.Color(0, 255, 0)
AZUL = pygame.Color(0, 0, 255)
AMARELO = pygame.Color(255, 255, 0)

# Janela do programa
COMPRIMENTO, ALTURA = 800, 800
JANELA = pygame.display.set_mode((COMPRIMENTO, ALTURA))


# Definição da classe Planeta
class Planeta:
    # Inicialização do Objeto da classe
    def __init__(self, massa, cor, velocidade_inicial, raio, posicao):
        self.massa = massa
        self.cor = cor
        self.vel_x = velocidade_inicial[0]
        self.vel_y = velocidade_inicial[1]
        self.raio = raio
        self.pos_x = posicao[0]
        self.pos_y = posicao[1]

    # Calcular a força gravitacional do planeta com todos os outros planetas
    def calcular_forcas(self, planetas):
        forca_x, forca_y = 0, 0

        for planeta in planetas:
            if planeta != self:
                dx = planeta.pos_x - self.pos_x
                dy = planeta.pos_y - self.pos_y
                dist_2 = dx * dx + dy * dy
                forca = (self.massa * planeta.massa * G) / dist_2
                forca_x += dx / sqrt(dist_2) * forca
                forca_y += dy / sqrt(dist_2) * forca

        return forca_x, forca_y

    def atualizar_velocidade(self, forca):
        forca_x = forca[0]
        forca_y = forca[1]

        acel_x = forca_x / self.massa
        acel_y = forca_y / self.massa

        self.vel_x += acel_x * TEMPO_POR_ETAPA
        self.vel_y += acel_y * TEMPO_POR_ETAPA

    def atualizar_posicao(self, deslocamento):
        self.pos_x += self.vel_x * TEMPO_POR_ETAPA
        self.pos_y += self.vel_y * TEMPO_POR_ETAPA

        x = self.pos_x * ESCALA + deslocamento[0]
        y = self.pos_y * ESCALA + deslocamento[1]

        raio = self.raio * ESCALA * 1000 # fora da escala por motivos visuais
        pygame.draw.circle(JANELA, self.cor, (x, y), raio)

def modificar_estado_teclas(teclas, event):
     
    if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
        if event.key == pygame.K_UP:
            teclas[0] = True
        if event.key == pygame.K_DOWN:
            teclas[1] = True
        if event.key == pygame.K_LEFT:
            teclas[2] = True
        if event.key == pygame.K_RIGHT:
            teclas[3] = True
    elif event.type == pygame.KEYUP: # Verifica se uma tecla foi soltada
        if event.key == pygame.K_UP:
            teclas[0] = False
        if event.key == pygame.K_DOWN:
            teclas[1] = False
        if event.key == pygame.K_LEFT:
            teclas[2] = False
        if event.key == pygame.K_RIGHT:
            teclas[3] = False

def mover_tela(deslocamento, teclas):
    deslocamento[0] += 2*(teclas[2] - teclas[3])
    deslocamento[1] += 2*(teclas[0] - teclas[1])


def main():
    # testes

    planetas = [Planeta(6e30, AZUL, (29.8e3, 0), 6.4e7, (COMPRIMENTO / 2 / ESCALA, (ALTURA / 2 + 150) / ESCALA)),
                Planeta(2e30, AMARELO, (0, 0), 7e7, (COMPRIMENTO / 2 / ESCALA, ALTURA / 2 / ESCALA))]
    rodando = True
    clock = pygame.time.Clock()
    deslocamento = [0, 0]
    teclas_seguradas = [False, False, False, False] # up, down, left, right
    while rodando:
        clock.tick(FPS)
        JANELA.fill(PRETO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # Verifica se uma tecla foi pressionada ou soltada
                modificar_estado_teclas(teclas_seguradas, event)
        mover_tela(deslocamento, teclas_seguradas)
        for planeta in planetas:
            forca = planeta.calcular_forcas(planetas)
            planeta.atualizar_velocidade(forca)
        for planeta in planetas:
            planeta.atualizar_posicao(deslocamento)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
