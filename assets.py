"""
Gerenciador de Assets - Carrega e gerencia todos os sprites e imagens do jogo
"""
import pygame
import os
from sprite_generator import (
    create_player_sprites_animated,
    create_obstacle_sprite,
    create_background,
    create_ground_sprite
)

class AssetManager:
    def __init__(self):
        self.player_sprites = {}
        self.obstacle_sprites = {}
        self.background = None
        self.ground = None
        self.background_image_path = None
        self.music_path = None
        self.load_assets()
    
    def load_assets(self, screen_width=1000, screen_height=600, ground_height=500):
        """Carrega todos os assets do jogo"""
        # Carregar sprites do jogador
        self.player_sprites = create_player_sprites_animated()
        
        # Carregar sprites de obstáculos
        self.obstacle_sprites['barrier'] = create_obstacle_sprite('barrier', 30, 60)
        self.obstacle_sprites['low_barrier'] = create_obstacle_sprite('low_barrier', 30, 30)
        self.obstacle_sprites['ramp'] = create_obstacle_sprite('ramp', 60, 50)  # Rampas mais altas
        self.obstacle_sprites['rail'] = create_obstacle_sprite('rail', 40, 10)
        
        # Tentar carregar imagem de background real
        # Procura em várias localizações possíveis
        possible_bg_paths = [
            'assets/background.jpg',
            'assets/background.png',
            'background.jpg',
            'background.png',
            'assets/images/background.jpg',
            'assets/images/background.png'
        ]
        
        background_loaded = False
        for path in possible_bg_paths:
            if os.path.exists(path):
                try:
                    bg_image = pygame.image.load(path)
                    # Redimensionar para o tamanho da tela
                    self.background = pygame.transform.scale(bg_image, (screen_width, screen_height))
                    self.background_image_path = path
                    background_loaded = True
                    print(f"Background carregado: {path}")
                    break
                except Exception as e:
                    print(f"Erro ao carregar background {path}: {e}")
        
        # Se não encontrou imagem, usar background gerado
        if not background_loaded:
            self.background = create_background(screen_width, screen_height)
            print("Usando background gerado programaticamente")
        
        # Carregar chão
        self.ground = create_ground_sprite(screen_width, screen_height - ground_height)
        
        # Procurar música de fundo
        possible_music_paths = [
            'assets/music.mp3',
            'assets/music.ogg',
            'assets/music.wav',
            'music.mp3',
            'music.ogg',
            'music.wav',
            'assets/sounds/music.mp3',
            'assets/sounds/music.ogg',
            'assets/sounds/music.wav'
        ]
        
        for path in possible_music_paths:
            if os.path.exists(path):
                self.music_path = path
                print(f"Música encontrada: {path}")
                break
        
        if not self.music_path:
            print("Nenhuma música encontrada. Adicione um arquivo de música em assets/music.mp3 (ou .ogg/.wav)")
    
    def get_player_sprite(self, state='idle'):
        """Obtém sprite do jogador para o estado atual"""
        if state in self.player_sprites:
            return self.player_sprites[state]
        return self.player_sprites['idle']
    
    def get_obstacle_sprite(self, obstacle_type):
        """Obtém sprite de obstáculo"""
        if obstacle_type in self.obstacle_sprites:
            return self.obstacle_sprites[obstacle_type]
        return self.obstacle_sprites['barrier']

