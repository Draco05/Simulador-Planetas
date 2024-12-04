# Simulador do problema dos 3 corpos - Física Básica

# Bibliotecas importadas
import pygame
from math import sqrt, cos, sin, radians
from random import randint

# Inicializar o Pygame
pygame.init()

# Constantes 
G = 6.67408e-11  # N m^2 / Kg^2
AU = 1.49597e11  # m
TEMPO_POR_ETAPA = 3600  # 1 hora
ESCALA_INICIAL = 1000/AU  # 1000 pixels por AU
FPS = 60  # frames por segundo

# Cores
PRETO = pygame.Color(0, 0, 0)
BRANCO = pygame.Color(255, 255, 255)
VERMELHO = pygame.Color(255, 0, 0)
VERDE = pygame.Color(0, 255, 0)
AZUL = pygame.Color(0, 0, 255)
AMARELO = pygame.Color(255, 255, 0)
LARANJA = pygame.Color(246, 120, 40)

# Janela do programa
COMPRIMENTO, ALTURA = 800, 800
JANELA = pygame.display.set_mode((COMPRIMENTO, ALTURA))
pygame.display.set_caption("Simulador do Problema dos 3 Corpos")

# Botões utilizados
pause_botao = pygame.font.SysFont("Arial", 20).render("Modo: Pause", True, BRANCO)
reset_botao = pygame.font.SysFont("Arial", 20).render("Resetar", True, BRANCO)
colisao_botao = pygame.font.SysFont("Arial", 20).render("Modo: Colisão", True, BRANCO)


# Definição da classe Planeta
class Planeta:
    # Inicialização do Objeto da classe
    def __init__(self, massa, cor, velocidade_inicial, raio, posicao):
        self.massa = massa # kg
        self.cor = cor # valor RGB
        self.vel_x = velocidade_inicial[0] # m/s
        self.vel_y = velocidade_inicial[1] # m/s
        self.raio = raio # m
        self.pos_x = posicao[0] # m
        self.pos_y = posicao[1] # m
        self.trajetoria = [] # lista de coordenadas (x,y)

    # Calcular a força gravitacional do planeta com todos os outros planetas
    def calcular_forcas(self, planetas):
        # argumentos:
        #   planetas: lista de todos os planetas
        # retona:
        #   forca_x: força resultante no eixo x
        #   forca_y: força resultante no eixo y

        forca_x, forca_y = 0, 0
        for planeta in planetas:
            # ignora o caso de calcular a força gravitacional do planeta com ele mesmo
            if planeta != self:
                # calcula a distância entre os planetas ao quadrado
                dx = planeta.pos_x - self.pos_x
                dy = planeta.pos_y - self.pos_y
                dist_2 = dx * dx + dy * dy

                # ignora caso a divisão seja por 0
                if dist_2 == 0:
                      continue
                # Utiliza a expressão Fg = M*m*G / r^2 para calcular a força gravitacional
                forca = (self.massa * planeta.massa * G) / dist_2
                
                # Soma acumulativa das forças em cada componente 
                forca_x += dx / sqrt(dist_2) * forca
                forca_y += dy / sqrt(dist_2) * forca

        return forca_x, forca_y

    # atualiza a velocidade do planeta baseado na força resultante
    def atualizar_velocidade(self, forca):
        # argumentos:
            # forca: tupla que representa uma força em cada componente
        forca_x = forca[0]
        forca_y = forca[1]

        # F = m*a => a = F / m
        acel_x = forca_x / self.massa
        acel_y = forca_y / self.massa

        # Usa a aproximação que V = Vo + a * t
        self.vel_x += acel_x * TEMPO_POR_ETAPA
        self.vel_y += acel_y * TEMPO_POR_ETAPA

    # atualiza a posição do planeta baseado em sua velocidade
    def atualizar_posicao(self):
        # Usa a aproximação que S = So + V * t
        self.pos_x += self.vel_x * TEMPO_POR_ETAPA
        self.pos_y += self.vel_y * TEMPO_POR_ETAPA

    # imprime o planeta na janela
    def imprimir(self, deslocamento, escala):
        # argumentos:
        #   deslocamento: também conhecido como offset, é a quantidade de pixels que os objetos devem ser movidos devido ao movimento da tela
        #   escala: proporção entre pixels por AU

        # transformação da posição em metros para pixels no referencial da tela
        x = self.pos_x * escala + deslocamento[0]
        y = self.pos_y * escala + deslocamento[1]
        raio = self.raio * escala
        
        # adiciona posição atual na trajetória
        self.trajetoria.append((self.pos_x, self.pos_y))

        # imprime planeta
        pygame.draw.circle(JANELA, self.cor, (x, y), raio)

        #imprime trajetória
        if len(self.trajetoria) >= 2:
            pontos = []
            for ponto in self.trajetoria:
                pontos.append((ponto[0] * escala + deslocamento[0], ponto[1] * escala + deslocamento[1]))
            pygame.draw.lines(JANELA, self.cor, False, pontos)
        
    # checa se ocorreu uma colisão entre dois planetas
    def checar_colisoes(self, planetas):
        #argumentos:
        #   planetas: lista de todos os planetas
        #retorna:
        #   tupla de coordenadas onde ocorreu a colisão. (0, 0) caso não ocorreu colisão
        #   boleano se ocorreu colisão ou não

        for planeta in planetas:
            # ignora o caso do planeta com ele mesmo 
            if planeta != self:
                # calcula distância entre planetas
                dx = planeta.pos_x - self.pos_x
                dy = planeta.pos_y - self.pos_y
                dist = sqrt(dx*dx + dy*dy)
                
                # um planeta "dentro" do outro 
                if dist <= (self.raio + planeta.raio):
                    return ((self.pos_x + planeta.pos_x)/2, (self.pos_y + planeta.pos_y)/2), True
        return (0, 0), False

    # mostra informações sobre o planeta quando o mouse está em cima dele
    def checar_dados(self, escala, deslocamento):
        # argumentos:
        #   deslocamento: também conhecido como offset, é a quantidade de pixels que os objetos devem ser movidos devido ao movimento da tela
        #   escala: proporção entre pixels por AU

        mouse_pos = pygame.mouse.get_pos()
        # checa se o mouse está dentro do planeta
        if (self.pos_x - self.raio) * escala <= mouse_pos[0] - deslocamento[0] <= (self.pos_x + self.raio) * escala and (self.pos_y - self.raio) * escala <= mouse_pos[1] - deslocamento[1] <= (self.pos_y + self.raio)*escala:
            # calcula os dados usando Pixels ao invés de metros
            vel_x = self.vel_x * escala * TEMPO_POR_ETAPA * FPS
            vel_y = self.vel_y * escala * TEMPO_POR_ETAPA * FPS
            pos_x = self.pos_x * escala
            pos_y = -self.pos_y * escala
            #cria os textos das informações
            dados_vel = pygame.font.SysFont("Arial", 20).render(f"Velocidade: {vel_x:.2f}, {-vel_y:.2f} pixels / s", True, BRANCO)
            dados_pos = pygame.font.SysFont("Arial", 20).render(f"Posição: {pos_x:.2f}, {pos_y:.2f}", True, BRANCO)
            dados_escala = pygame.font.SysFont("Arial", 20).render(f"Escala: {round(escala * AU)} pixels por AU", True, BRANCO)
            #imprime os textos
            JANELA.blit(dados_vel, (0, 0))
            JANELA.blit(dados_pos, (0, 30))
            JANELA.blit(dados_escala, (0, 60))

# adiciona um planeta genérico
def adicionar_planeta(escala, deslocamento):
    # argumentos:
        #   deslocamento: também conhecido como offset, é a quantidade de pixels que os objetos devem ser movidos devido ao movimento da tela
        #   escala: proporção entre pixels por AU
    # retorna:
    #   objeto da classe Planeta com os dados inicializados

    # posição do planeta é a posição do mouse
    x, y = pygame.mouse.get_pos()
    x = (x - deslocamento[0]) / escala
    y = (y - deslocamento[1]) / escala
    
    # usando a massa do sol como referência
    massa = 2e30
    # cor aleatória
    cor = [randint(10,255) for _ in range(3)]
    # velocidades inciais sendo 0
    vel_x = 0
    vel_y = 0
    # usando raio do sol como referência
    raio = 7e8

    return Planeta(massa, cor, (vel_x, vel_y), raio, (x, y))

# tratamento dos eventos do pygame
def tratar_eventos(teclas, event, escala, deslocamento, pause, planetas, colisao, botoes, modo_sem_colisao):
    # argumentos:
    #   teclas: lista de quais teclas estão atualmente pressioanadas
    #   event: evento do pygame
    #   deslocamento: também conhecido como offset, é a quantidade de pixels que os objetos devem ser movidos devido ao movimento da tela
    #   escala: proporção entre pixels por AU
    #   pause: booleano se a simulação está pausada ou não
    #   planetas: lista de todos os planetas
    #   colisão: boleano que representa se ocorreu colisão ou não
    #   botoes: lista de botões e suas características
    #   modo_sem_colisão: booleano que representa se o modo de não considerar colisões está ativado ou não 
    #
    # retorna:
    #   escala: nova escala
    #   pause: novo estado do pause
    #   colisao: novo estado da colisão
    #   rodando: se está rodando ou não
    #   modo_sem_colisao: novo estado do modo_sem_colisão

    rodando = True

    # Verifica se uma tecla foi pressionada
    if event.type == pygame.KEYDOWN:  
        if event.key == pygame.K_UP: # seta para cima
            teclas[0] = True
        if event.key == pygame.K_DOWN: # seta para baixo
            teclas[1] = True
        if event.key == pygame.K_LEFT: # seta para esquerda
            teclas[2] = True
        if event.key == pygame.K_RIGHT: # seta para direita
            teclas[3] = True
        if event.key == pygame.K_i: # tecla i
            # novo offset após o zoom-in
            deslocamento[0] += COMPRIMENTO * (-0.25 * escala) / (2 * ESCALA_INICIAL) 
            deslocamento[1] += COMPRIMENTO * (-0.25 * escala) / (2 * ESCALA_INICIAL)
            # nova escala
            escala *= 1.25
        if event.key == pygame.K_o: #tecla o
            # novo offset após o zoom-out
            deslocamento[0] += COMPRIMENTO * (.2 * escala) / (2 * ESCALA_INICIAL) 
            deslocamento[1] += COMPRIMENTO * (0.2 * escala) / (2 * ESCALA_INICIAL)
            # nova escala
            escala *= 0.8

    # Verifica se uma tecla foi soltada
    elif event.type == pygame.KEYUP: 
        if event.key == pygame.K_UP: #seta para cima
            teclas[0] = False
        if event.key == pygame.K_DOWN: #seta para baixo
            teclas[1] = False
        if event.key == pygame.K_LEFT: #seta para esquerda
            teclas[2] = False
        if event.key == pygame.K_RIGHT: # seta para direita
            teclas[3] = False

    # Verifica se o botão do mouse foi clicado
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for idx, botao in enumerate(botoes):
            # checa se o clique foi em um botão e faz a ação correspondente
            if botao[1][0] <= mouse_pos[0] <= botao[1][0] + botao[1][2] and botao[1][1] <= mouse_pos[1] <= botao[1][1] + botao[1][3]:
                if idx == 0:
                    # muda de estado o pause e troca o texto do botão
                    pause = not pause
                    botoes[0] = (pygame.font.SysFont("Arial", 20).render(f"Modo: {'Pause' if pause else 'Play'}", True, BRANCO), botao[1], botao[2])
                    break
                if idx == 1:
                    # resetar as informações necessárias
                    planetas.clear()
                    deslocamento[0] = 0
                    deslocamento[1] = 0
                    escala = ESCALA_INICIAL
                    pause = True
                    botoes[0] = (pause_botao, botoes[0][1], botoes[0][2])
                    colisao = False
                    break
                if idx == 2:
                    # muda de estado o modo_sem_colisão e troca o texto do botão
                    modo_sem_colisao = not modo_sem_colisao
                    botoes[2] = (pygame.font.SysFont("Arial", 20).render(f"Modo: {'Sem ' if modo_sem_colisao else ''}Colisão", True, BRANCO), botao[1], 0 if modo_sem_colisao else 25)
                    break
        else:
            # adiciona planeta caso não foi clicado em nenhum botão
            planetas.append(adicionar_planeta(escala, deslocamento))
    # checa se clicou o botão de fechar janela
    elif event.type == pygame.QUIT:
        rodando = False
    return escala, pause, colisao, rodando, modo_sem_colisao

# move o referencial da tela
def mover_tela(deslocamento, teclas):
    # altera o valor do deslocamento / offset para cada eixo em função das "setinhas" pressionadas
    deslocamento[0] += 5*(teclas[2] - teclas[3])
    deslocamento[1] += 5*(teclas[0] - teclas[1])

# programa principal
def main():
    # inicialização das variáveis utilizadas
    rodando = True
    colisao = False 
    pause = True
    modo_sem_colisao = False
    deslocamento = [0, 0]
    teclas_seguradas = [False, False, False, False] # up, down, left, right
    escala = ESCALA_INICIAL
    raio_explosao = 1
    coords_explosao = []
    planetas = []
    botoes = [(pause_botao, [87, ALTURA - 50, 150, 50], 25), (reset_botao, [324, ALTURA - 50, 150, 50], 40), (colisao_botao, [561, ALTURA-50, 150, 50], 25)]
    clock = pygame.time.Clock()

    while rodando:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        # tratamento dos eventos do pygame
        for event in pygame.event.get():
            escala, pause, colisao, rodando, modo_sem_colisao = tratar_eventos(teclas_seguradas, event, escala, deslocamento, pause, planetas, colisao, botoes, modo_sem_colisao)
        # coloca o fundo de preto
        JANELA.fill(PRETO)
        # move o referencial da tela
        mover_tela(deslocamento, teclas_seguradas)

        # faz um efeito de explosão caso ocorreu uma colisão
        if colisao and raio_explosao <= 50:
            pygame.draw.circle(JANELA, LARANJA, (coords_explosao[0] * escala, coords_explosao[1] * escala), raio_explosao)
            raio_explosao += 1
        
        # calcula a nova velocidade do planeta caso o jogo não esteja pausado
        if not pause and not colisao:
            for planeta in planetas:
                forca = planeta.calcular_forcas(planetas)
                planeta.atualizar_velocidade(forca)

        for planeta in planetas:
            # atualiza a posição de cada planeta
            if not colisao and not pause:
                planeta.atualizar_posicao()
                coords_explosao, colisao = planeta.checar_colisoes(planetas)
                colisao = False if modo_sem_colisao else colisao
            # imprime o planeta na tela
            planeta.imprimir(deslocamento, escala)
            planeta.checar_dados(escala, deslocamento)
        
        # imprime os botões
        for botao in botoes:
            if botao[1][0] <= mouse_pos[0] <= botao[1][0] + botao[1][2] and botao[1][1] <= mouse_pos[1] <= botao[1][1] + botao[1][3]:
                pygame.draw.rect(JANELA, (200, 200, 200), botao[1])
            else:
                pygame.draw.rect(JANELA, (100, 100, 100), botao[1])
            JANELA.blit(botao[0], (botao[1][0] + botao[2], ALTURA-35))

        # atualiza a tela     
        pygame.display.update()

    # fecha com o pygame
    pygame.quit()


if __name__ == '__main__':
    main()
