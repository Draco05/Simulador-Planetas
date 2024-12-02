# Simulador do problema dos 3 corpos - Física Básica

# Bibliotecas importadas
import pygame
from math import sqrt, cos, sin, radians

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
pygame.display.set_caption("Simulador do Problema dos 3 corpos")

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

        raio = self.raio * escala * 1000 #fora de escala por motivos visuais
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

def adicionar_planeta(planetas, escala, deslocamento):
    x, y = pygame.mouse.get_pos()
    x = (x - deslocamento[0]) / escala
    y = (y - deslocamento[1]) / escala
    
    erro_entrada = True
    while (erro_entrada):
        erro_entrada = False
        massa = float(input("Digite a massa dor planeta em kg: "))
        if massa <= 0:
            print("Massa deve ter um valor estritamente positivo")
            erro_entrada = True
            continue

        print("Digite a cor do planeta em RGB: ")
        cor = []
        for i in ["vermelho", "verde", "azul"]:
            valor = int(input(f"Valor da cor {i}: "))
            if valor > 255 or valor < 0:
                print("Valor RGB deve estar entre 0 e 255")
                erro_entrada = True
                break
            cor.append(valor)
        
        if erro_entrada: continue

        vel = float(input("Digite o módulo da velocidade em m/s: "))
        if vel < 0:
            vel = -vel
        angulo = float(input("Digite o ângulo (em graus) do versor da velocidade em relação ao eixo x: "))
        vel_x = +vel * cos(radians(angulo))
        vel_y = -vel * sin(radians(angulo))

        raio = float(input("Digite o tamanho do raio em metros: "))
        if raio <= 0:
            print("O raio deve ser estritamente positivo")
            erro_entrada = True
        
    print("Planeta criado!")

    return Planeta(massa, cor, (vel_x, vel_y), raio, (x, y))



def evento_teclas(teclas, event, escala, deslocamento, pause, planetas, colisao):
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
        if event.key == pygame.K_SPACE:
            pause = not pause
        if event.key == pygame.K_r:
            planetas.clear()
            deslocamento[0] = 0
            deslocamento[1] = 0
            escala = ESCALA_INICIAL
            pause = True
            colisao = False
        if event.key == pygame.K_a:
            planetas.append(adicionar_planeta(planetas, escala, deslocamento))
    

    elif event.type == pygame.KEYUP: # Verifica se uma tecla foi soltada
        if event.key == pygame.K_UP:
            teclas[0] = False
        if event.key == pygame.K_DOWN:
            teclas[1] = False
        if event.key == pygame.K_LEFT:
            teclas[2] = False
        if event.key == pygame.K_RIGHT:
            teclas[3] = False
    return escala, pause, colisao

def mover_tela(deslocamento, teclas):
    deslocamento[0] += 5*(teclas[2] - teclas[3])
    deslocamento[1] += 5*(teclas[0] - teclas[1])


def main():
    rodando = True
    colisao = False
    pause = True
    clock = pygame.time.Clock()
    deslocamento = [0, 0]
    teclas_seguradas = [False, False, False, False] # up, down, left, right
    escala = ESCALA_INICIAL
    planetas = []

    while rodando:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # Verifica se uma tecla foi pressionada ou soltada
                escala, pause, colisao = evento_teclas(teclas_seguradas, event, escala, deslocamento, pause, planetas, colisao)
        JANELA.fill(PRETO)
        mover_tela(deslocamento, teclas_seguradas)
        if (not colisao) and (not pause):
            for planeta in planetas:
                forca = planeta.calcular_forcas(planetas)
                planeta.atualizar_velocidade(forca)
        for planeta in planetas:
            if (not colisao) and (not pause):
                planeta.atualizar_posicao()
                if planeta.checar_colisoes(planetas):
                    colisao = True
            planeta.imprimir(deslocamento, escala)
                
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
