import pygame

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
    pygame.image.load(f'./asset/florestaBg{i}.png') for i in range(1, 9)
]

# Ajustar tamanho das imagens
bg_layers = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in bg_layers]

# Velocidades para efeito parallax
bg_speeds = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3]

# Posições iniciais das camadas
bg_x_positions = [0] * 8

# Carregar imagens do jogador e do chão
ground_img = pygame.image.load('./asset/florestaBg3.png')
player_img = pygame.image.load('./asset/mario.png')
player_img = pygame.transform.scale(player_img, (80, 60))

# Configuração do personagem
player_x, player_y = 100, HEIGHT - 60 - 50
player_vel = 5
jump_power = 10
gravity = 0.5
velocity_y = 0
is_jumping = False

# Limite de movimento para a esquerda
initial_position = player_x  # O personagem não pode ir além dessa posição

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
            score += 1  # Incrementa o score ao pressionar espaço

    # Movimentação
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > initial_position:
        player_x -= player_vel  # Move o personagem para a esquerda

    if keys[pygame.K_RIGHT]:  # Movimento para a direita é infinito
        for i in range(8):
            bg_x_positions[i] -= bg_speeds[i] * player_vel  # Move o fundo

    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = -jump_power
        is_jumping = True

    # Reset das camadas do fundo para repetir o cenário
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

    # Desenha o jogador com a nova imagem
    screen.blit(player_img, (player_x, player_y))

    # Exibir o score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Atualiza a tela
    pygame.display.update()
    clock.tick(30)

pygame.quit()
