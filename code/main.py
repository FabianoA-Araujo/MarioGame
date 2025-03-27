import pygame
import random

# Inicializa o pygame
pygame.init()

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

# Carregar imagens do jogador e do chão
ground_img = pygame.image.load("./asset/florestaBg3.png")
player_img = pygame.image.load("./asset/mario.png")
player_img = pygame.transform.scale(player_img, (80, 60))

# Carregar imagens dos pisos
piso_imgs = [pygame.image.load(f"./asset/floor{i}.png") for i in range(1, 6)]

# Configuração do personagem
player_x, player_y = 100, HEIGHT - 60 - 50
player_vel = 5
jump_power = 10
gravity = 0.5
velocity_y = 0
is_jumping = False
can_jump = True
move_right = True  # Controla se o personagem pode se mover

# Lista de pisos
pisos = []
espaco_minimo = 20  # Distância mínima entre pisos

# Função para gerar um novo piso
def gerar_piso():
    img = random.choice(piso_imgs)
    x = WIDTH + random.randint(50, 150)
    y = HEIGHT - 60 - img.get_height()  # Todos os pisos na base inicial
    return [img, x, y]

# Criando 5 pisos iniciais
pisos = [gerar_piso() for _ in range(5)]

display_running = True
clock = pygame.time.Clock()
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
            score += 1  # Incrementa o score ao pressionar espaço

    # Movimentação
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and move_right:
        for i in range(8):
            bg_x_positions[i] -= bg_speeds[i]
        for piso in pisos:
            piso[1] -= player_vel

    # Reset das camadas do fundo
    for i in range(8):
        if bg_x_positions[i] <= -WIDTH:
            bg_x_positions[i] = 0

    # Física do pulo
    velocity_y += gravity
    player_y += velocity_y

    # Colisão com o chão
    if player_y >= HEIGHT - 60 - 50:
        player_y = HEIGHT - 60 - 50
        is_jumping = False
        can_jump = True

    # Verificar colisão lateral com pisos
    move_right = True
    for piso in pisos:
        piso_rect = pygame.Rect(piso[1], piso[2], piso[0].get_width(), piso[0].get_height())
        player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())

        # Se o personagem está no ar e colide com um piso, ele não pode subir automaticamente
        if player_rect.colliderect(piso_rect):
            if not is_jumping:  # Só para se ele não estiver pulando
                move_right = False  # Impede o movimento para frente até que o jogador pule
            break  # Evita verificar múltiplas colisões ao mesmo tempo

    # Desenha os pisos
    for piso in pisos:
        screen.blit(piso[0], (piso[1], piso[2]))

    # Geração contínua de pisos mantendo distância mínima
    if len(pisos) < 5 or pisos[-1][1] < WIDTH - 150:
        novo_piso = gerar_piso()
        if not pisos or novo_piso[1] - pisos[-1][1] >= espaco_minimo:
            pisos.append(novo_piso)

    # Removendo pisos que saíram da tela
    pisos = [piso for piso in pisos if piso[1] > -piso[0].get_width()]

    # Desenha o jogador
    screen.blit(player_img, (player_x, player_y))

    # Exibir o score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Atualiza a tela
    pygame.display.update()
    clock.tick(30)

pygame.quit()
