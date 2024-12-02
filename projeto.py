# Simulador do problema dos 3 corpos - Física Básica

# Bibliotecas importadas
import pygame
from math import sqrt

# Inicializar o Pygame
pygame.init()

# Constantes 
G = 6.67408e-11  # N m^2 / Kg^2
AU = 1.49597e11  # m
TEMPO_POR_ETAPA = 3600 * 24  # 1 dia
ESCALA_INICIAL = 50/AU  # 50 pixels por AU
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
        self.trajetoria = []

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

    def atualizar_posicao(self):
        self.pos_x += self.vel_x * TEMPO_POR_ETAPA
        self.pos_y += self.vel_y * TEMPO_POR_ETAPA

    def imprimir(self, deslocamento, escala):
        x = self.pos_x * escala + deslocamento[0]
        y = self.pos_y * escala + deslocamento[1]

        raio = self.raio * escala * 1000 # fora da escala por motivos visuais
        self.trajetoria.append((self.pos_x, self.pos_y))
        pygame.draw.circle(JANELA, self.cor, (x, y), raio)
        if len(self.trajetoria) >= 2:
            pontos = []
            for ponto in self.trajetoria:
                pontos.append((ponto[0] * escala + deslocamento[0], ponto[1] * escala + deslocamento[1]))
            pygame.draw.lines(JANELA, self.cor, False, pontos)

    def checar_colisoes(self, planetas):
        for planeta in planetas:
            if planeta != self:
                dx = planeta.pos_x - self.pos_x
                dy = planeta.pos_y - self.pos_y
                dist = sqrt(dx*dx + dy*dy)
                if dist <= (self.raio + planeta.raio) * 1000:
                    return True
        return False

def modificar_estado_teclas(teclas, event, escala, deslocamento):
     
    if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
        if event.key == pygame.K_UP:
            teclas[0] = True
        if event.key == pygame.K_DOWN:
            teclas[1] = True
        if event.key == pygame.K_LEFT:
            teclas[2] = True
        if event.key == pygame.K_RIGHT:
            teclas[3] = True
        if event.key == pygame.K_i:
            deslocamento[0] += COMPRIMENTO * (-0.25 * escala) / (2 * ESCALA_INICIAL) 
            deslocamento[1] += COMPRIMENTO * (-0.25 * escala) / (2 * ESCALA_INICIAL)
            escala *= 1.25

        if event.key == pygame.K_o:
            deslocamento[0] += COMPRIMENTO * (.2 * escala) / (2 * ESCALA_INICIAL) 
            deslocamento[1] += COMPRIMENTO * (0.2 * escala) / (2 * ESCALA_INICIAL)
            escala *= 0.8

    elif event.type == pygame.KEYUP: # Verifica se uma tecla foi soltada
        if event.key == pygame.K_UP:
            teclas[0] = False
        if event.key == pygame.K_DOWN:
            teclas[1] = False
        if event.key == pygame.K_LEFT:
            teclas[2] = False
        if event.key == pygame.K_RIGHT:
            teclas[3] = False
    return escala

def mover_tela(deslocamento, teclas):
    deslocamento[0] += 5*(teclas[2] - teclas[3])
    deslocamento[1] += 5*(teclas[0] - teclas[1])


def main():
    rodando = True
    colisao = False
    clock = pygame.time.Clock()
    deslocamento = [0, 0]
    teclas_seguradas = [False, False, False, False] # up, down, left, right
    escala = ESCALA_INICIAL

    # testes
    planetas = [Planeta(6e30, AZUL, (-12.8e3, -1e4), 6.4e7, (COMPRIMENTO / 2 / escala, (ALTURA / 2 + 150) / escala)),
                Planeta(2e30, AMARELO, (30e3, 0), 7e7, (COMPRIMENTO / 2 / escala, ALTURA / 2 / escala)),
                Planeta(5e30, VERMELHO, (50e2, -25e2), 4e7, (COMPRIMENTO / 2 / escala, (ALTURA / 2 - 200) / escala))]
    while rodando:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # Verifica se uma tecla foi pressionada ou soltada
                escala = modificar_estado_teclas(teclas_seguradas, event, escala, deslocamento)
        JANELA.fill(PRETO)
        mover_tela(deslocamento, teclas_seguradas)
        if not colisao:
            for planeta in planetas:
                forca = planeta.calcular_forcas(planetas)
                planeta.atualizar_velocidade(forca)
        for planeta in planetas:
            if not colisao:
                planeta.atualizar_posicao()
                if planeta.checar_colisoes(planetas):
                    colisao = True
            planeta.imprimir(deslocamento, escala)
                
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
