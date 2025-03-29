import pygame
import random
import time

# Inicializa o pygame
pygame.init()

# Inicializa o mixer de som
pygame.mixer.init()

# Carrega e toca a música em loop
pygame.mixer.music.load("./asset/marioSound.wav")
pygame.mixer.music.play(-1, 0.0)  # O segundo parâmetro é o tempo de delay, 0.0 significa iniciar imediatamente

# Configurações da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Configurações da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 250)

# Fonte para exibir o score
font = pygame.font.Font(None, 36)
score = 0

# Carregar imagens do fundo
bg_layers = [
    pygame.image.load(f"./asset/florestaBg{i}.png") for i in range(1, 9)
]
bg_layers = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in bg_layers]

# Velocidades para efeito parallax
bg_speeds = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3]
bg_x_positions = [0] * 8

# Carregar imagens do jogador, chão, buraco e cogumelos
ground_img = pygame.image.load("./asset/florestaBg3.png")
player_img = pygame.image.load("./asset/mario.png")
player_img = pygame.transform.scale(player_img, (80, 60))
hole_img = pygame.image.load("./asset/hole1.png")
hole_img = pygame.transform.scale(hole_img, (60, ))  # Ajusta o tamanho da imagem
# Carregar e redimensionar as imagens dos cogumelos
mushroom1_img = pygame.image.load("./asset/murshroom1.png")
mushroom1_img = pygame.transform.scale(mushroom1_img, (24, 24))  # Redimensiona para 40x40 pixels

mushroom2_img = pygame.image.load("./asset/murshroom2.png")
mushroom2_img = pygame.transform.scale(mushroom2_img, (24, 24))  # Redimensiona para 40x40 pixels

# Carregar imagens dos pisos
piso_imgs = [pygame.image.load(f"./asset/floor{i}.png") for i in range(1, 6)]

# Carregar imagem da moeda
coin_img = pygame.image.load("./asset/coin.png")  # A imagem da moeda que você criou
coin_img = pygame.transform.scale(coin_img, (20, 20))  # Ajusta o tamanho para 20x20 pixels

# Configuração do personagem
player_x, player_y = 100, HEIGHT - 60 - 50
player_vel = 5
jump_power = 12  # Aumento do pulo em 10 pixels
gravity = 0.5
velocity_y = 0
is_jumping = False
can_jump = True
move_right = True  # Controla se o personagem pode se mover
sobre_piso = None  # Piso sobre o qual o personagem está

# Variáveis de tempo para geração de moedas
tempo_geracao_moeda = 0  # O tempo decorrido enquanto o personagem se move para a direita
intervalo_geracao_moeda = 8  # Tempo em segundos para gerar uma moeda

# Variáveis de tempo para geração de cogumelos
tempo_geracao_mushroom1 = 0
intervalos_geracao_mushroom1 = [3, 7, 10, 15]  # em segundos
tempo_geracao_mushroom2 = 0
intervalos_geracao_mushroom2 = [3, 5, 9]  # Agora a geração será duas vezes mais rápida

# Lista de elementos no chão (pisos e buracos)
elementos_chao = []
espaco_minimo = 20  # Distância mínima entre elementos

# Função para gerar moedas
def gerar_moeda():
    # Ajusta a altura para a moeda estar a 90 pixels da borda inferior
    y = HEIGHT - 90 - 20  # 20 é a altura da moeda
    x = WIDTH + random.randint(50, 150)  # Gera a posição horizontal da moeda fora da tela
    return [coin_img, x, y]

# Função para gerar cogumelos
def gerar_mushroom(tipo):
    if tipo == 1:
        # Ajusta a altura para o cogumelo1 estar a 180 pixels da borda inferior
        y = HEIGHT - 180 - 24  # 24 é a altura do cogumelo1
    elif tipo == 2:
        # Ajusta a altura para o cogumelo2 estar a 270 pixels da borda inferior (reduzido em 30 pixels)
        y = HEIGHT - 270 - 24  # 24 é a altura do cogumelo2
    x = WIDTH + random.randint(50, 150)
    if tipo == 1:
        return [mushroom1_img, x, y]
    elif tipo == 2:
        return [mushroom2_img, x, y]

# Função para gerar pisos e buracos
def gerar_elemento(ultima_posicao, ultimo_buraco):
    if random.random() < 0.3 and ultimo_buraco != 1:  # 30% de chance de gerar um buraco, mas não dois seguidos
        img = hole_img
        return [img, ultima_posicao, HEIGHT - 60 - img.get_height(), 1], 1  # Retorna o buraco e marca
    else:
        img = random.choice(piso_imgs)  # Escolhe um piso aleatório
        return [img, ultima_posicao, HEIGHT - 60 - img.get_height(), 0], 0  # Retorna o piso e marca como piso (0)

# Criando 5 elementos iniciais
ultima_posicao = 0
ultimo_buraco = 0
elementos_chao = []
for _ in range(5):
    elemento, ultimo_buraco = gerar_elemento(ultima_posicao, ultimo_buraco)
    elementos_chao.append(elemento)
    ultima_posicao = elemento[1] + elemento[0].get_width()


# Inicializando contadores
contador_moedas = 0
contador_mushrooms1 = 0
contador_mushrooms2 = 0
contador_pisos = len(elementos_chao)
contador_buracos = 0

display_running = True
clock = pygame.time.Clock()
start_time = time.time()  # Armazenar o tempo de início do jogo
tempo_geracao_inicio = 2  # Tempo em segundos para começar a gerar os objetos

while display_running:
    screen.fill(LIGHT_BLUE)

    # Desenhar camadas do fundo
    for i in range(8):
        screen.blit(bg_layers[i], (bg_x_positions[i], 0))
        screen.blit(bg_layers[i], (bg_x_positions[i] + WIDTH, 0))

    # Desenhar o chão
    screen.blit(ground_img, (0, HEIGHT - 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if can_jump:
                velocity_y = -jump_power
                is_jumping = True
                can_jump = False
                move_right = True  # Permite andar após pular
                sobre_piso = None  # Sai do piso ao pular

    # Movimentação
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_vel
        tempo_geracao_moeda = 0  # Congela o tempo quando o personagem não se move para a direita
    if keys[pygame.K_RIGHT] and move_right:
        if sobre_piso:
            player_x += player_vel  # Move sobre o piso
        else:
            for i in range(8):
                bg_x_positions[i] -= bg_speeds[i]
            for elemento in elementos_chao:
                elemento[1] -= player_vel
            tempo_geracao_moeda += 1 / 30  # Incrementa o tempo em 1/30 segundos por frame

    # Reset das camadas do fundo
    for i in range(8):
        if bg_x_positions[i] <= -WIDTH:
            bg_x_positions[i] += WIDTH

    # Física do pulo
    velocity_y += gravity
    player_y += velocity_y

    # Colisão com o chão
    if player_y >= HEIGHT - 60 - 50:
        player_y = HEIGHT - 60 - 50
        is_jumping = False
        can_jump = True
        sobre_piso = None

    # Verificar colisão com pisos, buracos
    move_right = True
    novo_sobre_piso = None
    for elemento in elementos_chao:
        elemento_rect = pygame.Rect(elemento[1] + 10, elemento[2], elemento[0].get_width() - 20,
                                    elemento[0].get_height())
        player_rect = pygame.Rect(player_x + 10, player_y, player_img.get_width() - 20, player_img.get_height())

        if elemento[0] == hole_img and player_rect.colliderect(elemento_rect):
            print("Game Over!")
            display_running = False  # Encerra o jogo

        if player_rect.colliderect(elemento_rect) and elemento[0] != hole_img:
            if velocity_y > 0 and player_y + player_img.get_height() - 10 <= elemento[2]:
                player_y = elemento[2] - player_img.get_height()
                velocity_y = 0
                is_jumping = False
                can_jump = True
                novo_sobre_piso = elemento  # Definir o piso atual
                break

    sobre_piso = novo_sobre_piso

    # Geração contínua de elementos mantendo distância mínima
    if len(elementos_chao) < 5 or elementos_chao[-1][1] < WIDTH - 150:
        novo_elemento, ultimo_buraco = gerar_elemento(elementos_chao[-1][1] + elementos_chao[-1][0].get_width(), ultimo_buraco)
        elementos_chao.append(novo_elemento)

    # Removendo elementos que saíram da tela
    elementos_chao = [elemento for elemento in elementos_chao if elemento[1] > -elemento[0].get_width()]

    # Controle de tempo de geração de moedas e cogumelos
    tempo_decorrido = time.time() - start_time  # Tempo total do jogo em segundos

    # Gerar moedas a cada intervalo, mas só se o personagem estiver em movimento
    if move_right and tempo_decorrido >= tempo_geracao_moeda:
        moeda = gerar_moeda()
        elementos_chao.append(moeda)  # Adiciona a moeda à lista de elementos
        contador_moedas += 1
        tempo_geracao_moeda = tempo_decorrido + intervalo_geracao_moeda

    # Gerar cogumelos do tipo 1 (murshroom1), mas só se o personagem estiver em movimento
    if move_right and tempo_decorrido >= tempo_geracao_mushroom1:
        mushroom1 = gerar_mushroom(1)
        elementos_chao.append(mushroom1)
        contador_mushrooms1 += 1
        tempo_geracao_mushroom1 = tempo_decorrido + intervalos_geracao_mushroom1[contador_mushrooms1 % len(intervalos_geracao_mushroom1)]

    # Gerar cogumelos do tipo 2 (murshroom2), mas só se o personagem estiver em movimento
    if move_right and tempo_decorrido >= tempo_geracao_mushroom2:
        mushroom2 = gerar_mushroom(2)
        elementos_chao.append(mushroom2)
        contador_mushrooms2 += 1
        tempo_geracao_mushroom2 = tempo_decorrido + intervalos_geracao_mushroom2[contador_mushrooms2 % len(intervalos_geracao_mushroom2)]

    # Verificando colisões com moedas, cogumelos e alterando o score
    for elemento in elementos_chao:
        elemento_rect = pygame.Rect(elemento[1], elemento[2], elemento[0].get_width(), elemento[0].get_height())
        player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())

        if elemento[0] == coin_img and player_rect.colliderect(elemento_rect):
            score += 2  # Soma 2 pontos se colidir com uma moeda
            elementos_chao.remove(elemento)  # Remove a moeda

        elif elemento[0] == mushroom1_img and player_rect.colliderect(elemento_rect):
            score += 5  # Soma 5 pontos se colidir com cogumelo1
            elementos_chao.remove(elemento)  # Remove o cogumelo

        elif elemento[0] == mushroom2_img and player_rect.colliderect(elemento_rect):
            score += 8  # Soma 8 pontos se colidir com cogumelo2
            elementos_chao.remove(elemento)  # Remove o cogumelo

    # Exibir o score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

    # Desenha os elementos do chão
    for elemento in elementos_chao:
        screen.blit(elemento[0], (elemento[1], elemento[2]))

    # Desenha o personagem
    screen.blit(player_img, (player_x, player_y))

    # Atualiza a tela
    pygame.display.update()

    # Limita o FPS
    clock.tick(60)

# Finalizar o pygame
pygame.quit()
