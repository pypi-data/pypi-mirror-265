import pygame
import os

def get_assets(subfile):
    assetsDir = os.path.join(os.path.dirname(__file__), 'assets')
    return os.path.join(assetsDir, subfile)


class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    # 橘色
    orange = (255, 165, 0)
    # 青色
    cyan = (90, 255, 255)
    # 冷光色
    cold_light = (192, 192, 255)
    light_yellow = (255, 255, 192)

    
    
    
    
    @classmethod
    def get(cls, val):
        if val == "black":
            return cls.black
        elif val == "white":
            return cls.white
        elif val == "red":
            return cls.red
        elif val == "green":
            return cls.green
        elif val == "blue":
            return cls.blue
        elif val == "yellow":
            return cls.yellow
        elif val == "orange":
            return cls.orange
        elif val == "cyan":
            return cls.cyan
        elif val == "cold_light":
            return cls.cold_light
        elif val == "light_yellow":
            return cls.light_yellow
        else:
            return cls.white

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        
    
    def load_image_sequence(self, imgsubdir):
        images = []
        imgdir = os.path.join(os.path.dirname(__file__), f'assets/{imgsubdir}')
        for file_name in sorted(os.listdir(imgdir)):
            if file_name.endswith('.png'):
                image = self.load_image(f'{imgsubdir}/{file_name}')
                images.append(image)
        return images
    
    def load_image(self, subpath):
        filepath = os.path.join(os.path.dirname(__file__), f'assets/{subpath}')
        if filepath not in self.images:
            self.images[filepath] = pygame.image.load(filepath).convert_alpha()
        return self.images[filepath]
    
    def load_sound(self, subpath):
        filepath = os.path.join(os.path.dirname(__file__), f'assets/{subpath}')
        if filepath not in self.sounds:
            self.sounds[filepath] = pygame.mixer.Sound(filepath)
        return self.sounds[filepath]

res_manager = ResourceManager()