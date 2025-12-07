import pygame
import random
import sys
from enum import Enum
from assets import AssetManager

# Inicializar Pygame
pygame.init()
pygame.mixer.init()  # Inicializar mixer de áudio

# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
GROUND_HEIGHT = SCREEN_HEIGHT - 100

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (50, 200, 50)
RED = (255, 50, 50)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Player:
    def __init__(self, x, y, asset_manager):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.vel_y = 0
        self.jump_power = -15
        self.on_ground = False
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.asset_manager = asset_manager
        
        # Sistema de manobras
        self.current_trick = None
        self.trick_progress = 0
        self.trick_duration = 0
        self.rotation = 0  # Para rotações de 360 graus
        self.board_flip = 0  # Para kickflip/heelflip
        self.trick_completed = False
        self.trick_bonus = 0
        self.queued_trick = None  # Manobra na fila para começar ao pular
        self.last_key_state = {}  # Rastrear estados anteriores das teclas para detectar pressionamentos
        self.on_ramp = False  # Rastrear se o jogador está na rampa
        self.ramp_boost = False  # Rastrear se o jogador recebeu boost da rampa
        
    def update(self, keys, obstacles):
        # Detectar transição de não pressionado para pressionado
        key_pressed = {}
        key_pressed[pygame.K_LEFT] = keys[pygame.K_LEFT] and not self.last_key_state.get(pygame.K_LEFT, False)
        key_pressed[pygame.K_RIGHT] = keys[pygame.K_RIGHT] and not self.last_key_state.get(pygame.K_RIGHT, False)
        key_pressed[pygame.K_DOWN] = keys[pygame.K_DOWN] and not self.last_key_state.get(pygame.K_DOWN, False)
        key_pressed[pygame.K_UP] = keys[pygame.K_UP] and not self.last_key_state.get(pygame.K_UP, False)
        key_pressed[pygame.K_SPACE] = keys[pygame.K_SPACE] and not self.last_key_state.get(pygame.K_SPACE, False)
        
        # Atualizar estados anteriores das teclas
        self.last_key_state[pygame.K_LEFT] = keys[pygame.K_LEFT]
        self.last_key_state[pygame.K_RIGHT] = keys[pygame.K_RIGHT]
        self.last_key_state[pygame.K_DOWN] = keys[pygame.K_DOWN]
        self.last_key_state[pygame.K_UP] = keys[pygame.K_UP]
        self.last_key_state[pygame.K_SPACE] = keys[pygame.K_SPACE]
        
        # Lidar com entradas de manobras quando no ar (permite se a tecla for pressionada OU mantida)
        if not self.on_ground:
            if self.current_trick is None:
                # Começar nova manobra - verificar se a tecla foi pressionada ou mantida
                if keys[pygame.K_LEFT]:
                    self.start_trick('kickflip')
                elif keys[pygame.K_RIGHT]:
                    self.start_trick('heelflip')
                elif keys[pygame.K_DOWN]:
                    self.start_trick('spin360')
            # Também permite que manobras sejam iniciadas mesmo se já estiver fazendo uma (para combos)
            elif self.current_trick == 'ollie' and self.trick_progress < 15:
                # Pode transicionar de ollie para outras manobras cedo
                if keys[pygame.K_LEFT]:
                    self.start_trick('kickflip')
                elif keys[pygame.K_RIGHT]:
                    self.start_trick('heelflip')
                elif keys[pygame.K_DOWN]:
                    self.start_trick('spin360')
        else:
            # No chão - colocar manobras na fila
            if key_pressed[pygame.K_LEFT]:
                self.queued_trick = 'kickflip'
            elif key_pressed[pygame.K_RIGHT]:
                self.queued_trick = 'heelflip'
            elif key_pressed[pygame.K_DOWN]:
                self.queued_trick = 'spin360'
        
        # Pulo regular (Ollie)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if self.on_ground:
                self.vel_y = self.jump_power
                self.on_ground = False
                # Começar ollie ou manobra na fila
                if self.queued_trick:
                    self.start_trick(self.queued_trick)
                    self.queued_trick = None
                else:
                    self.start_trick('ollie')
        
        # Atualizar manobra atual
        if self.current_trick:
            self.trick_progress += 1
            self.update_trick_animation()
            
            # Verificar se a manobra está completa
            if self.trick_progress >= self.trick_duration:
                if not self.trick_completed:
                    self.trick_completed = True
                    self.trick_bonus = self.get_trick_bonus()
                # Resetar manobra ao pousar
                if self.on_ground:
                    bonus = self.trick_bonus
                    self.reset_trick()
                    return bonus
        
        # Aplicar gravidade
        self.vel_y += GRAVITY
        
        # Atualizar posição
        self.y += self.vel_y
        
        # Verificar grind (em rails/barreiras)
        self.check_grind(obstacles)
        
        # Verificar interação com rampa
        self.check_ramp(obstacles)
        
        # Colisão com o chão
        ground_y = GROUND_HEIGHT - self.height
        if self.y >= ground_y:
            self.y = ground_y
            self.vel_y = 0
            self.on_ground = True
            self.on_ramp = False
            if self.current_trick and self.trick_completed:
                bonus = self.trick_bonus
                self.reset_trick()
                return bonus
            elif self.current_trick:
                self.reset_trick()  # Manobra falhou
        
        # Atualizar animação
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:
            self.animation_frame = 0
        
        return 0
    
    def start_trick(self, trick_name):
        self.current_trick = trick_name
        self.trick_progress = 0
        self.trick_completed = False
        self.trick_bonus = 0
        
        if trick_name == 'ollie':
            self.trick_duration = 20
        elif trick_name == 'kickflip':
            self.trick_duration = 30
        elif trick_name == 'heelflip':
            self.trick_duration = 30
        elif trick_name == 'spin360':
            self.trick_duration = 40
        elif trick_name == 'grind':
            self.trick_duration = 60
    
    def update_trick_animation(self):
        if self.current_trick == 'spin360':
            self.rotation = (self.trick_progress / self.trick_duration) * 360
        elif self.current_trick == 'kickflip':
            self.board_flip = (self.trick_progress / self.trick_duration) * 360
        elif self.current_trick == 'heelflip':
            self.board_flip = -(self.trick_progress / self.trick_duration) * 360
        elif self.current_trick == 'ollie':
            # Ollie apenas tem pulo mais alto, sem animação especial
            pass
    
    def get_trick_bonus(self):
        if not self.trick_completed:
            return 0
        # Pontuações base para cada manobra
        bonuses = {
            'ollie': 10,
            'kickflip': 30,
            'heelflip': 30,
            'spin360': 50,
            'grind': 40
        }
        base_bonus = bonuses.get(self.current_trick, 0)
        
        # Multiplicador de bônus se a manobra foi feita na/de uma rampa
        if self.ramp_boost:
            base_bonus = int(base_bonus * 1.5)  # 50% de bônus para manobras na rampa
        
        return base_bonus
    
    def reset_trick(self):
        self.current_trick = None
        self.trick_progress = 0
        self.trick_duration = 0
        self.rotation = 0
        self.board_flip = 0
        self.trick_completed = False
        self.trick_bonus = 0
        self.queued_trick = None
        self.ramp_boost = False  # Resetar boost da rampa quando a manobra reseta
    
    def check_grind(self, obstacles):
        # Verificar se o jogador pode fazer grind no topo de barreiras baixas, rails ou barreiras
        player_bottom = self.y + self.height
        player_center_x = self.x + self.width // 2
        
        for obstacle in obstacles:
            if obstacle.type in ['low_barrier', 'barrier', 'rail']:
                obstacle_top = obstacle.y
                obstacle_left = obstacle.x
                obstacle_right = obstacle.x + obstacle.width
                
                # Verificar se o jogador está acima e alinhado com o obstáculo
                if (player_bottom >= obstacle_top - 5 and 
                    player_bottom <= obstacle_top + 10 and
                    player_center_x >= obstacle_left and 
                    player_center_x <= obstacle_right and
                    abs(self.vel_y) < 2):
                    # Começar grind
                    if self.current_trick != 'grind':
                        self.start_trick('grind')
                    self.y = obstacle_top - self.height
                    self.vel_y = 0
                    self.on_ground = False
                    return
    
    def check_ramp(self, obstacles):
        # Verificar se o jogador está na ou passando por uma rampa
        player_bottom = self.y + self.height
        player_center_x = self.x + self.width // 2
        player_left = self.x
        player_right = self.x + self.width
        
        was_on_ramp = self.on_ramp
        self.on_ramp = False
        
        for obstacle in obstacles:
            if obstacle.type == 'ramp':
                ramp_left = obstacle.x
                ramp_right = obstacle.x + obstacle.width
                ramp_top = obstacle.y
                ramp_bottom = obstacle.y + obstacle.height
                
                # Verificar se o jogador está colidindo com a rampa
                if (player_right > ramp_left and player_left < ramp_right and
                    player_bottom > ramp_top and self.y < ramp_bottom):
                    
                    self.on_ramp = True
                    
                    # Calcular posição na rampa (0 = esquerda, 1 = direita)
                    ramp_pos = (player_center_x - ramp_left) / obstacle.width if obstacle.width > 0 else 0.5
                    ramp_center_x = ramp_left + obstacle.width // 2
                    
                    # Dar boost ao subir a rampa (lado esquerdo, aproximando do centro)
                    if (ramp_pos > 0.2 and ramp_pos < 0.6 and 
                        not self.ramp_boost and 
                        player_center_x < ramp_center_x + 10):
                        # Dar boost vertical
                        if self.vel_y > -8:  # Apenas dar boost se não estiver já pulando muito alto
                            self.vel_y = -22  # Boost forte da rampa
                            self.ramp_boost = True
                            # Se não estiver fazendo uma manobra, começar ollie automaticamente
                            if not self.current_trick:
                                self.start_trick('ollie')
                    
                    # Ajustar posição do jogador para estar na superfície da rampa
                    # A rampa é triangular, então calcular posição Y baseada em X
                    if player_center_x < ramp_center_x:
                        # Lado esquerdo da rampa (subindo)
                        ramp_slope = (ramp_top - ramp_bottom) / (obstacle.width // 2) if obstacle.width > 0 else 0
                        relative_x = player_center_x - ramp_left
                        ramp_y = ramp_bottom - (relative_x * ramp_slope)
                    else:
                        # Lado direito da rampa (descendo)
                        ramp_slope = (ramp_bottom - ramp_top) / (obstacle.width // 2) if obstacle.width > 0 else 0
                        relative_x = player_center_x - ramp_center_x
                        ramp_y = ramp_top + (relative_x * ramp_slope)
                    
                    # Definir posição do jogador na rampa
                    target_y = ramp_y - self.height
                    if self.y + self.height > ramp_y:
                        self.y = target_y
                        self.on_ground = False
                        # Diminuir velocidade de descida na rampa, mas permitir movimento para cima
                        if self.vel_y > 0:
                            self.vel_y = max(self.vel_y * 0.5, 0.5)
                    
                    return
        
        # Resetar boost da rampa ao sair dela
        if was_on_ramp and not self.on_ramp:
            # Manter flag de boost por um tempo após sair da rampa para permitir conclusão da manobra
            pass
    
    def draw(self, screen):
        # Determinar qual sprite usar
        sprite_state = 'idle'
        if self.current_trick == 'ollie':
            sprite_state = 'ollie'
        elif self.current_trick == 'kickflip':
            sprite_state = 'kickflip'
        elif self.current_trick == 'grind':
            sprite_state = 'grind'
        elif self.current_trick:
            sprite_state = 'ollie'  # Padrão para ollie em outras manobras
        
        # Obter o sprite
        sprite = self.asset_manager.get_player_sprite(sprite_state)
        
        # Ponto central para rotação
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Aplicar rotação se estiver fazendo 360
        if self.current_trick == 'spin360' and self.rotation != 0:
            rotated = pygame.transform.rotate(sprite, self.rotation)
            rot_rect = rotated.get_rect(center=(center_x, center_y))
            screen.blit(rotated, rot_rect)
        # Aplicar flip do skate para kickflip/heelflip
        elif self.current_trick in ['kickflip', 'heelflip'] and self.board_flip != 0:
            # Criar uma cópia e rotacionar apenas a área do skate (simplificado - rotaciona sprite inteiro)
            flipped = pygame.transform.rotate(sprite, self.board_flip * 0.3)  # Efeito de flip sutil
            flip_rect = flipped.get_rect(center=(center_x, center_y))
            screen.blit(flipped, flip_rect)
        else:
            # Sprite normal
            screen.blit(sprite, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, obstacle_type='barrier', asset_manager=None):
        self.x = x
        self.type = obstacle_type
        self.passed = False
        self.asset_manager = asset_manager
        
        if obstacle_type == 'barrier':
            self.width = 30
            self.height = 60
            self.y = GROUND_HEIGHT - self.height
            self.color = RED
        elif obstacle_type == 'low_barrier':
            self.width = 30
            self.height = 30
            self.y = GROUND_HEIGHT - self.height
            self.color = ORANGE
        elif obstacle_type == 'ramp':
            self.width = 60
            self.height = 50  # Rampas muito mais altas
            self.y = GROUND_HEIGHT - self.height
            self.color = GREEN
        elif obstacle_type == 'rail':
            self.width = 40
            self.height = 10
            self.y = GROUND_HEIGHT - self.height - 20
            self.color = GRAY
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, screen):
        # Usar sprite se disponível, caso contrário usar método de desenho
        if self.asset_manager:
            sprite = self.asset_manager.get_obstacle_sprite(self.type)
            screen.blit(sprite, (self.x, self.y))
        else:
            # Método de desenho alternativo
            if self.type == 'ramp':
                points = [
                    (self.x, self.y + self.height),
                    (self.x + self.width, self.y + self.height),
                    (self.x + self.width // 2, self.y)
                ]
                pygame.draw.polygon(screen, self.color, points)
                pygame.draw.polygon(screen, BLACK, points, 2)
            elif self.type == 'rail':
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
                pygame.draw.rect(screen, self.color, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                shine_rect = pygame.Rect(self.x + 2, self.y + 1, self.width - 4, 3)
                pygame.draw.rect(screen, WHITE, shine_rect)
            else:
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
                pygame.draw.rect(screen, self.color, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Skate Game")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Carregar assets
        self.asset_manager = AssetManager()
        self.asset_manager.load_assets(SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        
        # Carregar música de fundo (mas não tocar ainda)
        self.load_background_music()
        self.music_playing = False
        
        self.reset_game()
    
    def load_background_music(self):
        """Carrega a música de fundo (mas não toca)"""
        if self.asset_manager.music_path:
            try:
                pygame.mixer.music.load(self.asset_manager.music_path)
                pygame.mixer.music.set_volume(0.5)  # Volume 50%
                print(f"Música de fundo carregada: {self.asset_manager.music_path}")
            except Exception as e:
                print(f"Erro ao carregar música: {e}")
        else:
            print("Nenhuma música de fundo configurada")
    
    def start_background_music(self):
        """Inicia a música de fundo"""
        if self.asset_manager.music_path and not self.music_playing:
            try:
                pygame.mixer.music.play(-1)  # -1 = loop infinito
                self.music_playing = True
                print("Música de fundo iniciada")
            except Exception as e:
                print(f"Erro ao tocar música: {e}")
    
    def stop_background_music(self):
        """Para a música de fundo"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            print("Música de fundo parada")
    
    def reset_game(self):
        self.player = Player(100, GROUND_HEIGHT - 80, self.asset_manager)
        self.obstacles = []
        self.score = 0
        self.speed = 5
        self.obstacle_timer = 0
        self.obstacle_spawn_rate = 90  # frames entre obstáculos
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = GameState.PLAYING
                        self.start_background_music()  # Iniciar música quando o jogo começar
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                        self.start_background_music()  # Reiniciar música ao recomeçar
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        self.stop_background_music()  # Parar música ao voltar ao menu
        return True
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        trick_bonus = self.player.update(keys, self.obstacles)
        if trick_bonus > 0:
            self.score += trick_bonus
        
        # Gerar obstáculos
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_spawn_rate:
            self.obstacle_timer = 0
            # Maior chance de rampas
            obstacle_type = random.choice(['barrier', 'barrier', 'low_barrier', 'ramp', 'ramp', 'rail'])
            self.obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_type, self.asset_manager))
        
        # Atualizar obstáculos
        for obstacle in self.obstacles[:]:
            obstacle.update(self.speed)
            
            # Verificar colisão (mas não para rampas - rampas são amigáveis!)
            if obstacle.type != 'ramp' and self.player.get_rect().colliderect(obstacle.get_rect()):
                # Verificar se é uma colisão fatal (de frente) ou se o jogador está em cima (grind)
                player_bottom = self.player.y + self.player.height
                player_top = self.player.y
                player_center_x = self.player.x + self.player.width // 2
                player_left = self.player.x
                player_right = self.player.x + self.player.width
                
                obstacle_top = obstacle.y
                obstacle_bottom = obstacle.y + obstacle.height
                obstacle_left = obstacle.x
                obstacle_right = obstacle.x + obstacle.width
                
                # Verificar se o jogador está acima do obstáculo (pode fazer grind)
                # O jogador está "em cima" se a parte de baixo dele está próxima do topo do obstáculo
                is_on_top = False
                if obstacle.type in ['low_barrier', 'barrier', 'rail']:
                    # Verificar se o jogador está acima do topo do obstáculo
                    # Margem maior para permitir pousar em cima
                    if (player_bottom >= obstacle_top - 15 and 
                        player_bottom <= obstacle_top + 20 and
                        player_center_x >= obstacle_left - 15 and 
                        player_center_x <= obstacle_right + 15):
                        is_on_top = True
                
                # Só é game over se não estiver em cima (colisão de frente/lateral)
                # Colisão de frente acontece quando o jogador bate na lateral do obstáculo
                if not is_on_top:
                    # Verificar se é colisão lateral (jogador está ao lado do obstáculo)
                    collision_from_side = (
                        (player_right > obstacle_left and player_left < obstacle_left + 5) or
                        (player_left < obstacle_right and player_right > obstacle_right - 5)
                    )
                    # Verificar se é colisão de baixo (jogador está abaixo do obstáculo)
                    collision_from_bottom = player_top < obstacle_bottom and player_bottom < obstacle_top
                    
                    # Se colidir de frente ou de baixo, é game over
                    if collision_from_side or collision_from_bottom:
                        self.state = GameState.GAME_OVER
                        self.stop_background_music()  # Parar música no game over
            
            # Pontuar
            if not obstacle.passed and obstacle.x + obstacle.width < self.player.x:
                obstacle.passed = True
                self.score += 10
            
            # Remover obstáculos fora da tela
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
        
        # Aumentar velocidade ao longo do tempo
        if self.score > 0 and self.score % 100 == 0:
            self.speed = min(self.speed + 0.1, 12)
            self.obstacle_spawn_rate = max(self.obstacle_spawn_rate - 1, 60)
    
    def draw(self):
        # Desenhar sprite de fundo
        self.screen.blit(self.asset_manager.background, (0, 0))
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Título do jogo
        title = self.font_large.render("JOGO DE SKATE", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Instrução para começar
        instruction = self.font_medium.render("Pressione ESPAÇO para Começar", True, BLACK)
        inst_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(instruction, inst_rect)
        
        # Explicação sobre o jogo
        desc1 = self.font_small.render("Desvie de obstáculos e faça manobras para ganhar pontos!", True, BLACK)
        desc1_rect = desc1.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(desc1, desc1_rect)
        
        desc2 = self.font_small.render("Use as rampas para ganhar altura e fazer manobras incríveis!", True, BLACK)
        desc2_rect = desc2.get_rect(center=(SCREEN_WIDTH // 2, 230))
        self.screen.blit(desc2, desc2_rect)
        
        # Título dos controles
        controls_title = self.font_small.render("CONTROLES:", True, BLACK)
        ctrl_title_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(controls_title, ctrl_title_rect)
        
        # Controles - linha 1
        controls1 = self.font_small.render("ESPAÇO/SETA CIMA = Ollie (Pulo)", True, BLACK)
        ctrl1_rect = controls1.get_rect(center=(SCREEN_WIDTH // 2, 310))
        self.screen.blit(controls1, ctrl1_rect)
        
        # Controles - linha 2
        controls2 = self.font_small.render("SETA ESQUERDA = Kickflip | SETA DIREITA = Heelflip", True, BLACK)
        ctrl2_rect = controls2.get_rect(center=(SCREEN_WIDTH // 2, 340))
        self.screen.blit(controls2, ctrl2_rect)
        
        # Controles - linha 3
        controls3 = self.font_small.render("SETA BAIXO = 360° Spin", True, BLACK)
        ctrl3_rect = controls3.get_rect(center=(SCREEN_WIDTH // 2, 370))
        self.screen.blit(controls3, ctrl3_rect)
        
        # Dica sobre grind
        tip1 = self.font_small.render("DICA: Pouse em cima de barreiras ou rails para fazer grind!", True, BLACK)
        tip1_rect = tip1.get_rect(center=(SCREEN_WIDTH // 2, 410))
        self.screen.blit(tip1, tip1_rect)
        
        # Pontuação das manobras
        score_title = self.font_small.render("PONTUAÇÃO DAS MANOBRAS:", True, BLACK)
        score_title_rect = score_title.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(score_title, score_title_rect)
        
        score1 = self.font_small.render("Ollie: 10 pts | Kickflip/Heelflip: 30 pts", True, BLACK)
        score1_rect = score1.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(score1, score1_rect)
        
        score2 = self.font_small.render("360° Spin: 50 pts | Grind: 40 pts", True, BLACK)
        score2_rect = score2.get_rect(center=(SCREEN_WIDTH // 2, 510))
        self.screen.blit(score2, score2_rect)
        
        bonus = self.font_small.render("BÔNUS: Manobras feitas em rampas ganham +50% de pontos!", True, BLACK)
        bonus_rect = bonus.get_rect(center=(SCREEN_WIDTH // 2, 540))
        self.screen.blit(bonus, bonus_rect)
    
    def draw_game(self):
        # Desenhar sprite do chão
        self.screen.blit(self.asset_manager.ground, (0, GROUND_HEIGHT))
        
        # Desenhar linha do chão para profundidade
        pygame.draw.line(self.screen, DARK_GRAY, (0, GROUND_HEIGHT), 
                        (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        
        # Desenhar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Desenhar jogador
        self.player.draw(self.screen)
        
        # Desenhar pontuação
        score_text = self.font_medium.render(f"Pontuação: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        # Desenhar indicador de velocidade
        speed_text = self.font_small.render(f"Velocidade: {self.speed:.1f}", True, DARK_GRAY)
        self.screen.blit(speed_text, (20, 70))
        
        # Desenhar manobra atual
        if self.player.current_trick:
            trick_name = self.player.current_trick.upper()
            # Traduzir nomes das manobras
            trick_translations = {
                'OLLIE': 'OLLIE',
                'KICKFLIP': 'KICKFLIP',
                'HEELFLIP': 'HEELFLIP',
                'SPIN360': '360° SPIN',
                'GRIND': 'GRIND'
            }
            display_name = trick_translations.get(trick_name, trick_name)
            
            if self.player.ramp_boost:
                display_name += " (RAMPA!)"
            if self.player.trick_completed:
                trick_text = self.font_small.render(f"{display_name}!", True, YELLOW)
            else:
                trick_text = self.font_small.render(display_name, True, WHITE)
            self.screen.blit(trick_text, (20, 110))
        
        # Desenhar indicador de rampa
        if self.player.on_ramp:
            ramp_text = self.font_small.render("NA RAMPA!", True, GREEN)
            self.screen.blit(ramp_text, (20, 150))
    
    def draw_game_over(self):
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over = self.font_large.render("FIM DE JOGO", True, RED)
        go_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over, go_rect)
        
        final_score = self.font_medium.render(f"Pontuação Final: {self.score}", True, WHITE)
        fs_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(final_score, fs_rect)
        
        restart = self.font_small.render("Pressione ESPAÇO para Recomeçar ou ESC para Menu", True, WHITE)
        r_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart, r_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Parar música antes de sair
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

