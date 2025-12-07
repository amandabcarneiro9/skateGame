import pygame
from PIL import Image, ImageDraw, ImageFilter
import os
import random

def create_player_sprite(width=60, height=80):
    """Cria um sprite de skatista"""
    # Criar imagem com transparência
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cabeça com mais detalhes
    head_y = 3
    head_size = 18
    # Base do rosto
    draw.ellipse([width//2 - head_size//2, head_y, width//2 + head_size//2, head_y + head_size], 
                 fill=(255, 220, 177, 255))
    # Cabelo
    draw.ellipse([width//2 - head_size//2 - 2, head_y - 3, width//2 + head_size//2 + 2, head_y + 8], 
                 fill=(50, 30, 20, 255))
    # Olhos
    draw.ellipse([width//2 - 7, head_y + 6, width//2 - 3, head_y + 10], fill=(0, 0, 0, 255))
    draw.ellipse([width//2 + 3, head_y + 6, width//2 + 7, head_y + 10], fill=(0, 0, 0, 255))
    # Nariz
    draw.ellipse([width//2 - 1, head_y + 10, width//2 + 1, head_y + 13], fill=(240, 200, 160, 255))
    # Boca
    draw.arc([width//2 - 4, head_y + 13, width//2 + 4, head_y + 17], start=0, end=180, fill=(0, 0, 0, 255), width=1)
    
    # Torso/Camisa
    torso_top = head_y + head_size
    torso_bottom = torso_top + 28
    # Camisa com mangas
    draw.rectangle([width//2 - 14, torso_top, width//2 + 14, torso_bottom], 
                   fill=(200, 50, 50, 255))  # Camisa vermelha
    # Detalhes da camisa
    draw.line([(width//2, torso_top), (width//2, torso_bottom)], fill=(180, 40, 40, 255), width=1)
    
    # Braços com mais detalhes
    # Braço esquerdo
    draw.ellipse([width//2 - 20, torso_top + 3, width//2 - 10, torso_bottom + 5], 
                 fill=(255, 220, 177, 255))  # Pele
    draw.ellipse([width//2 - 18, torso_top + 2, width//2 - 12, torso_bottom + 3], 
                 fill=(200, 50, 50, 255))  # Manga
    # Braço direito
    draw.ellipse([width//2 + 10, torso_top + 3, width//2 + 20, torso_bottom + 5], 
                 fill=(255, 220, 177, 255))  # Pele
    draw.ellipse([width//2 + 12, torso_top + 2, width//2 + 18, torso_bottom + 3], 
                 fill=(200, 50, 50, 255))  # Manga
    
    # Pernas/Calça
    leg_top = torso_bottom
    leg_bottom = leg_top + 20
    # Perna esquerda
    draw.rectangle([width//2 - 12, leg_top, width//2 - 2, leg_bottom], 
                   fill=(30, 30, 100, 255))  # Jeans azul
    draw.line([(width//2 - 7, leg_top), (width//2 - 7, leg_bottom)], fill=(20, 20, 80, 255), width=1)
    # Perna direita
    draw.rectangle([width//2 + 2, leg_top, width//2 + 12, leg_bottom], 
                   fill=(30, 30, 100, 255))  # Jeans azul
    draw.line([(width//2 + 7, leg_top), (width//2 + 7, leg_bottom)], fill=(20, 20, 80, 255), width=1)
    
    # Sapatos
    shoe_y = leg_bottom
    draw.ellipse([width//2 - 14, shoe_y, width//2 - 4, shoe_y + 6], fill=(0, 0, 0, 255))  # Sapato esquerdo
    draw.ellipse([width//2 + 4, shoe_y, width//2 + 14, shoe_y + 6], fill=(0, 0, 0, 255))  # Sapato direito
    # Cadarços
    draw.line([(width//2 - 9, shoe_y + 1), (width//2 - 9, shoe_y + 5)], fill=(255, 255, 255, 255), width=1)
    draw.line([(width//2 + 9, shoe_y + 1), (width//2 + 9, shoe_y + 5)], fill=(255, 255, 255, 255), width=1)
    
    # Skate Realista
    board_y = shoe_y + 6
    board_height = 8
    # Deck (textura de madeira)
    deck_color = (139, 90, 43, 255)  # Madeira marrom
    draw.rectangle([3, board_y, width - 3, board_y + board_height], fill=deck_color)
    # Contorno do deck
    draw.rectangle([3, board_y, width - 3, board_y + board_height], outline=(100, 60, 30, 255), width=1)
    # Design do deck/grip tape
    for i in range(3):
        y_pos = board_y + 2 + i * 2
        draw.line([(8, y_pos), (width - 8, y_pos)], fill=(80, 50, 25, 200), width=1)
    
    # Trucks (partes metálicas)
    truck_y = board_y + board_height
    # Truck esquerdo
    draw.rectangle([8, truck_y, 16, truck_y + 4], fill=(100, 100, 100, 255))  # Cinza metálico
    draw.rectangle([8, truck_y, 16, truck_y + 4], outline=(60, 60, 60, 255), width=1)
    # Truck direito
    draw.rectangle([width - 16, truck_y, width - 8, truck_y + 4], fill=(100, 100, 100, 255))
    draw.rectangle([width - 16, truck_y, width - 8, truck_y + 4], outline=(60, 60, 60, 255), width=1)
    
    # Rodas (realistas com aros)
    wheel_y = truck_y + 4
    wheel_size = 6
    # Roda esquerda
    draw.ellipse([10, wheel_y, 10 + wheel_size, wheel_y + wheel_size], fill=(0, 0, 0, 255))
    draw.ellipse([11, wheel_y + 1, 9 + wheel_size, wheel_y + wheel_size - 1], fill=(40, 40, 40, 255))  # Aro
    draw.ellipse([12, wheel_y + 2, 8 + wheel_size, wheel_y + wheel_size - 2], fill=(60, 60, 60, 255))  # Aro interno
    # Roda direita
    draw.ellipse([width - 16, wheel_y, width - 10, wheel_y + wheel_size], fill=(0, 0, 0, 255))
    draw.ellipse([width - 15, wheel_y + 1, width - 11, wheel_y + wheel_size - 1], fill=(40, 40, 40, 255))  # Aro
    draw.ellipse([width - 14, wheel_y + 2, width - 12, wheel_y + wheel_size - 2], fill=(60, 60, 60, 255))  # Aro interno
    
    # Converter para superfície pygame
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()

def create_player_sprites_animated():
    """Cria múltiplos frames para animação do jogador"""
    sprites = {}
    
    # Sprite idle/andando
    sprites['idle'] = create_player_sprite()
    
    # Sprite ollie (pulando) - mais realista
    img = Image.new('RGBA', (60, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cabeça
    draw.ellipse([21, 0, 39, 18], fill=(255, 220, 177, 255))
    draw.ellipse([20, -2, 40, 8], fill=(50, 30, 20, 255))  # Cabelo
    draw.ellipse([24, 6, 28, 10], fill=(0, 0, 0, 255))  # Olhos
    draw.ellipse([32, 6, 36, 10], fill=(0, 0, 0, 255))
    
    # Corpo (posição agachada/pulando)
    draw.rectangle([18, 15, 42, 43], fill=(200, 50, 50, 255))  # Camisa
    draw.line([(30, 15), (30, 43)], fill=(180, 40, 40, 255), width=1)
    
    # Braços para cima (movimento de pulo)
    draw.ellipse([8, 18, 18, 38], fill=(255, 220, 177, 255))  # Braço esquerdo
    draw.ellipse([10, 17, 16, 36], fill=(200, 50, 50, 255))  # Manga
    draw.ellipse([42, 18, 52, 38], fill=(255, 220, 177, 255))  # Braço direito
    draw.ellipse([44, 17, 50, 36], fill=(200, 50, 50, 255))  # Manga
    
    # Pernas dobradas (agachado)
    draw.rectangle([18, 43, 28, 63], fill=(30, 30, 100, 255))  # Perna esquerda
    draw.line([(23, 43), (23, 63)], fill=(20, 20, 80, 255), width=1)
    draw.rectangle([32, 43, 42, 63], fill=(30, 30, 100, 255))  # Perna direita
    draw.line([(37, 43), (37, 63)], fill=(20, 20, 80, 255), width=1)
    
    # Sapatos
    draw.ellipse([16, 63, 26, 69], fill=(0, 0, 0, 255))
    draw.ellipse([34, 63, 44, 69], fill=(0, 0, 0, 255))
    
    # Skate (no ar, levemente inclinado)
    board_y = 65
    deck_color = (139, 90, 43, 255)
    draw.rectangle([5, board_y, 55, board_y + 8], fill=deck_color)
    draw.rectangle([5, board_y, 55, board_y + 8], outline=(100, 60, 30, 255), width=1)
    # Trucks
    draw.rectangle([10, board_y + 8, 18, board_y + 12], fill=(100, 100, 100, 255))
    draw.rectangle([42, board_y + 8, 50, board_y + 12], fill=(100, 100, 100, 255))
    # Wheels
    draw.ellipse([12, board_y + 12, 18, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([13, board_y + 13, 17, board_y + 17], fill=(40, 40, 40, 255))
    draw.ellipse([42, board_y + 12, 48, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([43, board_y + 13, 47, board_y + 17], fill=(40, 40, 40, 255))
    
    sprites['ollie'] = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()
    
    # Sprite kickflip - mais realista
    img = Image.new('RGBA', (60, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cabeça
    draw.ellipse([21, 0, 39, 18], fill=(255, 220, 177, 255))
    draw.ellipse([20, -2, 40, 8], fill=(50, 30, 20, 255))
    draw.ellipse([24, 6, 28, 10], fill=(0, 0, 0, 255))
    draw.ellipse([32, 6, 36, 10], fill=(0, 0, 0, 255))
    
    # Corpo
    draw.rectangle([18, 15, 42, 43], fill=(200, 50, 50, 255))
    draw.line([(30, 15), (30, 43)], fill=(180, 40, 40, 255), width=1)
    
    # Braços abertos (para equilíbrio)
    draw.ellipse([5, 20, 15, 33], fill=(255, 220, 177, 255))
    draw.ellipse([7, 19, 13, 31], fill=(200, 50, 50, 255))
    draw.ellipse([45, 20, 55, 33], fill=(255, 220, 177, 255))
    draw.ellipse([47, 19, 53, 31], fill=(200, 50, 50, 255))
    
    # Pernas
    draw.rectangle([18, 43, 28, 63], fill=(30, 30, 100, 255))
    draw.line([(23, 43), (23, 63)], fill=(20, 20, 80, 255), width=1)
    draw.rectangle([32, 43, 42, 63], fill=(30, 30, 100, 255))
    draw.line([(37, 43), (37, 63)], fill=(20, 20, 80, 255), width=1)
    
    # Sapatos
    draw.ellipse([16, 63, 26, 69], fill=(0, 0, 0, 255))
    draw.ellipse([34, 63, 44, 69], fill=(0, 0, 0, 255))
    
    # Skate (rotacionado para kickflip)
    board_y = 60
    deck_color = (139, 90, 43, 255)
    draw.rectangle([10, board_y, 50, board_y + 8], fill=deck_color)
    draw.rectangle([10, board_y, 50, board_y + 8], outline=(100, 60, 30, 255), width=1)
    # Trucks
    draw.rectangle([15, board_y + 8, 23, board_y + 12], fill=(100, 100, 100, 255))
    draw.rectangle([37, board_y + 8, 45, board_y + 12], fill=(100, 100, 100, 255))
    # Wheels
    draw.ellipse([17, board_y + 12, 23, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([18, board_y + 13, 22, board_y + 17], fill=(40, 40, 40, 255))
    draw.ellipse([37, board_y + 12, 43, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([38, board_y + 13, 42, board_y + 17], fill=(40, 40, 40, 255))
    
    sprites['kickflip'] = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()
    
    # Sprite grind (agachado) - mais realista
    img = Image.new('RGBA', (60, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cabeça
    draw.ellipse([21, 10, 39, 28], fill=(255, 220, 177, 255))
    draw.ellipse([20, 8, 40, 18], fill=(50, 30, 20, 255))
    draw.ellipse([24, 16, 28, 20], fill=(0, 0, 0, 255))
    draw.ellipse([32, 16, 36, 20], fill=(0, 0, 0, 255))
    
    # Corpo (agachado)
    draw.rectangle([18, 25, 42, 53], fill=(200, 50, 50, 255))
    draw.line([(30, 25), (30, 53)], fill=(180, 40, 40, 255), width=1)
    
    # Braços (baixos para equilíbrio)
    draw.ellipse([10, 28, 20, 48], fill=(255, 220, 177, 255))
    draw.ellipse([12, 27, 18, 46], fill=(200, 50, 50, 255))
    draw.ellipse([40, 28, 50, 48], fill=(255, 220, 177, 255))
    draw.ellipse([42, 27, 48, 46], fill=(200, 50, 50, 255))
    
    # Pernas agachadas
    draw.rectangle([18, 53, 28, 73], fill=(30, 30, 100, 255))
    draw.line([(23, 53), (23, 73)], fill=(20, 20, 80, 255), width=1)
    draw.rectangle([32, 53, 42, 73], fill=(30, 30, 100, 255))
    draw.line([(37, 53), (37, 73)], fill=(20, 20, 80, 255), width=1)
    
    # Sapatos
    draw.ellipse([16, 73, 26, 79], fill=(0, 0, 0, 255))
    draw.ellipse([34, 73, 44, 79], fill=(0, 0, 0, 255))
    
    # Skate no rail (horizontal)
    board_y = 70
    deck_color = (139, 90, 43, 255)
    draw.rectangle([5, board_y, 55, board_y + 8], fill=deck_color)
    draw.rectangle([5, board_y, 55, board_y + 8], outline=(100, 60, 30, 255), width=1)
    # Trucks
    draw.rectangle([10, board_y + 8, 18, board_y + 12], fill=(100, 100, 100, 255))
    draw.rectangle([42, board_y + 8, 50, board_y + 12], fill=(100, 100, 100, 255))
    # Wheels (on rail)
    draw.ellipse([12, board_y + 12, 18, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([13, board_y + 13, 17, board_y + 17], fill=(40, 40, 40, 255))
    draw.ellipse([42, board_y + 12, 48, board_y + 18], fill=(0, 0, 0, 255))
    draw.ellipse([43, board_y + 13, 47, board_y + 17], fill=(40, 40, 40, 255))
    
    sprites['grind'] = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()
    
    return sprites

def create_obstacle_sprite(obstacle_type, width, height):
    """Cria sprites de obstáculos"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if obstacle_type == 'barrier':
        # Barreira vermelha com listras de aviso
        draw.rectangle([0, 0, width, height], fill=(200, 50, 50, 255))
        # Listras de aviso
        for i in range(0, height, 8):
            if i % 16 < 8:
                draw.rectangle([0, i, width, i + 4], fill=(255, 200, 0, 255))
        draw.rectangle([0, 0, width, height], outline=(0, 0, 0, 255), width=2)
        
    elif obstacle_type == 'low_barrier':
        # Barreira baixa laranja
        draw.rectangle([0, 0, width, height], fill=(255, 165, 0, 255))
        draw.rectangle([0, 0, width, height], outline=(0, 0, 0, 255), width=2)
        
    elif obstacle_type == 'ramp':
        # Rampa de skate realista com curvas suaves
        # Cor base - cinza de concreto
        concrete_base = (180, 180, 180, 255)
        concrete_dark = (150, 150, 150, 255)
        concrete_light = (200, 200, 200, 255)
        coping_color = (100, 100, 100, 255)  # Coping metálico no topo
        
        # Criar rampa com curvas suaves usando múltiplos polígonos/arcos
        # Lado esquerdo (aproximação)
        left_points = []
        for x in range(0, width//2 + 1):
            # Curva suave: easing quadrático
            progress = x / (width//2)
            # Fórmula de curva para transição suave
            y_offset = height * (1 - progress * progress)
            left_points.append((x, int(y_offset)))
        left_points.append((width//2, 0))
        left_points.append((0, height))
        left_points.append((0, 0))
        
        # Lado direito (aterrissagem)
        right_points = []
        for x in range(width//2, width + 1):
            progress = (x - width//2) / (width//2)
            y_offset = height * (progress * progress)
            right_points.append((x, int(y_offset)))
        right_points.append((width, height))
        right_points.append((width//2, 0))
        right_points.append((width, 0))
        
        # Desenhar superfície da rampa com textura de concreto
        # Preenchimento base
        all_points = [(0, height), (width, height), (width//2, 0)]
        draw.polygon(all_points, fill=concrete_base)
        
        # Adicionar linhas de textura (superfície de concreto)
        for i in range(0, width, 3):
            if i < width//2:
                progress = i / (width//2)
                y_pos = int(height * (1 - progress * progress))
            else:
                progress = (i - width//2) / (width//2)
                y_pos = int(height * (progress * progress))
            # Linhas de textura sutis
            if i % 6 == 0:
                draw.line([(i, y_pos), (i, height)], fill=concrete_dark, width=1)
        
        # Adicionar sombreamento para efeito 3D
        # Sombra do lado esquerdo
        for i in range(0, width//2, 2):
            progress = i / (width//2)
            y_pos = int(height * (1 - progress * progress))
            draw.line([(i, y_pos), (i, height)], fill=concrete_dark, width=1)
        
        # Destaque do lado direito
        for i in range(width//2, width, 2):
            progress = (i - width//2) / (width//2)
            y_pos = int(height * (progress * progress))
            draw.line([(i, y_pos), (i, height)], fill=concrete_light, width=1)
        
        # Coping superior (borda metálica) - topo arredondado
        coping_width = 4
        coping_rect = [width//2 - 10, -coping_width, width//2 + 10, coping_width + 2]
        draw.ellipse(coping_rect, fill=coping_color)
        # Contorno do coping
        draw.arc([width//2 - 10, -coping_width, width//2 + 10, coping_width + 2], 
                 start=0, end=180, fill=(60, 60, 60, 255), width=2)
        # Linha inferior do coping
        draw.line([(width//2 - 10, 0), (width//2 + 10, 0)], fill=(60, 60, 60, 255), width=1)
        
        # Bordas laterais (suportes verticais)
        edge_width = 2
        # Borda esquerda
        draw.rectangle([0, 0, edge_width, height], fill=(120, 120, 120, 255))
        draw.rectangle([0, 0, edge_width, height], outline=(80, 80, 80, 255), width=1)
        # Borda direita
        draw.rectangle([width - edge_width, 0, width, height], fill=(120, 120, 120, 255))
        draw.rectangle([width - edge_width, 0, width, height], outline=(80, 80, 80, 255), width=1)
        
        # Contorno
        draw.polygon(all_points, outline=(100, 100, 100, 255), width=2)
        
        # Adicionar algumas linhas de construção/detalhes
        for i in range(1, 4):
            line_y = height - (i * height // 4)
            if line_y > 0:
                # Encontrar posições x para este nível y na curva
                for x in range(0, width, 2):
                    if x < width//2:
                        progress = x / (width//2)
                        curve_y = int(height * (1 - progress * progress))
                    else:
                        progress = (x - width//2) / (width//2)
                        curve_y = int(height * (progress * progress))
                    
                    if abs(curve_y - line_y) < 2:
                        draw.ellipse([x-1, curve_y-1, x+1, curve_y+1], 
                                   fill=(140, 140, 140, 150))
        
    elif obstacle_type == 'rail':
        # Rail cinza com brilho metálico
        draw.rectangle([0, 0, width, height], fill=(128, 128, 128, 255))
        # Brilho metálico
        draw.rectangle([2, 1, width-2, height//2], fill=(180, 180, 180, 200))
        draw.rectangle([0, 0, width, height], outline=(0, 0, 0, 255), width=2)
        # Postes de suporte
        draw.rectangle([0, height, 3, height + 5], fill=(100, 100, 100, 255))
        draw.rectangle([width-3, height, width, height + 5], fill=(100, 100, 100, 255))
    
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()

def create_background(width, height):
    """Cria um fundo realista"""
    img = Image.new('RGB', (width, height), (135, 206, 235))  # Azul céu
    draw = ImageDraw.Draw(img)
    
    # Nuvens
    for i in range(3):
        x = (i + 1) * width // 4
        y = 50 + i * 30
        # Nuvem
        draw.ellipse([x-40, y, x+40, y+30], fill=(255, 255, 255, 200))
        draw.ellipse([x-20, y-10, x+20, y+20], fill=(255, 255, 255, 200))
        draw.ellipse([x, y, x+40, y+25], fill=(255, 255, 255, 200))
    
    # Sol
    draw.ellipse([width - 100, 30, width - 30, 100], fill=(255, 255, 150, 255))
    
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()

def create_ground_sprite(width, height):
    """Cria uma textura de chão realista"""
    img = Image.new('RGB', (width, height), (50, 200, 50))
    draw = ImageDraw.Draw(img)
    
    # Textura de grama
    for i in range(0, width, 2):
        for j in range(0, height, 3):
            # Folhas de grama aleatórias
            if (i + j) % 7 < 2:
                draw.line([(i, j), (i + random.randint(-1, 1), j - 2)], 
                         fill=(40, 180, 40), width=1)
    
    # Estrada/caminho no meio
    road_width = width // 3
    road_x = width // 2 - road_width // 2
    draw.rectangle([road_x, 0, road_x + road_width, height], fill=(80, 80, 80, 255))
    # Linhas da estrada
    for i in range(0, height, 20):
        draw.rectangle([road_x + road_width // 2 - 15, i, 
                       road_x + road_width // 2 + 15, i + 10], 
                      fill=(255, 255, 0, 255))
    
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()

