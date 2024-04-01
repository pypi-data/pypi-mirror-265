import random
import random
from typing import List
import pygame
import math
from .common import res_manager, Colors
from .config import configmap
import os

DISPLAY_WIDTH = configmap["display_width"]
DISPLAY_HEIGHT = configmap["display_height"]


class Background(pygame.sprite.Sprite):
    def __init__(self, location, config_data=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        self.image_sequence = []
        self.rect_sequence = []
        self.image_index = 0
        if self.config.get("image_sequence"):
            self.image_sequence = res_manager.load_image_sequence(
                self.config["image_sequence"]
            )
            self.rect_sequence = [
                self.image.get_rect() for self.image in self.image_sequence
            ]
            for _rect in self.rect_sequence:
                _rect.x = (DISPLAY_WIDTH - _rect.width) / 2
                # 设置图片的垂直位置
                _rect.y = location[1]
            self.image = self.image_sequence[self.image_index]
            self.rect = self.rect_sequence[self.image_index]
        else:
            self.image = res_manager.load_image(
                random.choice(self.config["images"])
            )  # 加载图片
            self.rect = self.image.get_rect()
            self.rect.x = (DISPLAY_WIDTH - self.rect.width) / 2
            # 设置图片的垂直位置
            self.rect.y = location[1]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300  # 每帧间隔毫秒数

    def update(self):
        if self.image_sequence:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.image_index = (self.image_index + 1) % len(self.image_sequence)
                self.image = self.image_sequence[self.image_index]
                self.rect = self.rect_sequence[self.image_index]

            for _rect in self.rect_sequence:
                _rect.y += 5  # Move the background down
                if _rect.y >= _rect.height:
                    _rect.y = 0

        else:
            self.rect.y += 5  # Move the background down
            if self.rect.y >= self.rect.height:
                self.rect.y = 0


class ScaleBackground(pygame.sprite.Sprite):
    def __init__(
        self, image_file, location, max_scale=2, min_scale=1.0, scale_speed=0.002
    ):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(
            image_file
        ).convert_alpha()  # 使用convert_alpha保留透明度
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.scale_speed = scale_speed
        self.current_scale = 1.0
        self.scaling_up = True  # 控制放大还是缩小

    def update(self):
        if self.scaling_up:
            self.current_scale += self.scale_speed
            if self.current_scale >= self.max_scale:
                self.scaling_up = False  # 开始缩小
        else:
            self.current_scale -= self.scale_speed
            if self.current_scale <= self.min_scale:
                self.scaling_up = True  # 开始放大

        new_width = int(self.base_image.get_width() * self.current_scale)
        new_height = int(self.base_image.get_height() * self.current_scale)
        self.image = pygame.transform.scale(self.base_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))


class FlightUnit(pygame.sprite.Sprite):
    """飞行单位"""

    def __init__(self, type: str, config_data):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        self.type = type
        self.hp = self.config["life_value"]
        self.life_value = self.config["life_value"]
        self.shield_hp = self.config["shield_value"]
        self.shield_value = self.config["shield_value"]
        self.image_sequence = []
        self.image_index = 0
        if self.config.get("image_sequence"):
            self.image_sequence = res_manager.load_image_sequence(
                self.config["image_sequence"]
            )
            self.image = self.image_sequence[self.image_index]
        else:
            self.image = res_manager.load_image(
                random.choice(self.config["images"])
            )  # 加载图片
        self.rect = self.image.get_rect()
        self.rect.x = self.config["first_pos"][0]  # 初始化x坐标
        self.rect.y = self.config["first_pos"][1]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300  # 每帧间隔毫秒数
        self.speed_x = random.randint(1, 6)  # 在x方向上设置随机速度
        self.speed_y = random.randint(1, 3)  # 在y方向上设置随机速度
        # 被消灭的时间
        self.kill_time = None
        self.fire_delay = 0
        self.trace_fire_delay = 0
        self.is_angry = False

        self.recharge_delay = 0  # 护盾充能延迟
        self.shield_recharge_step = self.config["shield_recharge_step"]  # 护盾充能步长

    def fire(self, group, direction, target_group, particle_group):
        self.trace_fire(group, target_group, particle_group)
        if self.fire_delay == 0:
            group.add(
                Bullet(
                    self.rect.width // 2 + self.rect.x,
                    self.rect.width // 2 + self.rect.y,
                    speed=self.config["bullet_speed"],
                    damage=self.config["bullet_damage"],
                    direction=direction,
                    color=Colors.get(self.config["bullet_color"]),
                    radius=self.config["bullet_radius"],
                )
            )
            if self.is_angry:
                self.fire_delay = self.config["fire_delay"] // 2
            else:
                self.fire_delay = self.config["fire_delay"]

            sound = res_manager.load_sound(self.config["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def trace_fire(self, src_group, target_group, particle_group):
        if target_group and particle_group and self.trace_fire_delay == 0:
            src_group.add(
                TraceBullet(
                    target_group,
                    particle_group,
                    self.rect.width // 2 + self.rect.x,
                    self.rect.y,
                    speed=self.config["bullet_speed"],
                    damage=self.config["bullet_damage"],
                    direction="up",
                    color=Colors.get(self.config["bullet_color"]),
                    radius=self.config["bullet_radius"],
                )
            )

            self.trace_fire_delay = self.config["trace_fire_delay"]
            sound = res_manager.load_sound(self.config["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def hit(self, damage: int):
        """被击中, 减少生命值, 狂暴状态下受到的伤害加倍"""
        damage_value = self.is_angry and damage * 2 or damage
        if self.shield_hp > 0 and self.shield_value > 0:
            self.shield_value -= damage_value
            if self.shield_value <= 0:
                self.shield_value = 0
                self.life_value += self.shield_value
        else:
            if self.life_value > 0:
                self.life_value -= damage_value
                if self.life_value <= 0:
                    self.life_value = 0
                    self.kill_time = pygame.time.get_ticks()

        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.set_volume(self.config["firehit_sound_volume"])
        sound.play()

    def on_killed(self):
        pass

    def draw_health_bar(self, surface):
        """绘制血条到给定的surface上"""
        bar_length = int(self.rect.width * 1 / 2)  # 血条长度为精灵宽度的三分之二
        bar_height = 8  # 血条的厚度
        fill = (self.life_value / self.hp) * bar_length  # 根据当前生命值计算填充长度

        # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
        outline_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            bar_length,
            bar_height,
        )  # 血条外框位置
        fill_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            fill,
            bar_height,
        )  # 血条填充位置

        pygame.draw.rect(surface, Colors.blue, outline_rect)  # 绘制血条外框
        pygame.draw.rect(surface, Colors.yellow, fill_rect)
        
        if self.shield_hp > 0:
            ## 绘制护盾值到给定的surface上
            fill = (
                self.shield_value / self.shield_hp
            ) * bar_length  # 根据当前护盾计算填充长度

            # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
            soutline_rect = pygame.Rect(
                self.rect.centerx - bar_length // 2,
                self.rect.top + self.rect.height + 10,
                bar_length,
                bar_height,
            )
            sfill_rect = pygame.Rect(
                self.rect.centerx - bar_length // 2,
                self.rect.top + self.rect.height + 10,
                fill,
                bar_height,
            )

            pygame.draw.rect(surface, Colors.blue, soutline_rect)
            pygame.draw.rect(surface, Colors.orange, sfill_rect)        

    def update(self):
        self.recharge_delay += 1
        if (
            self.shield_hp > 0
            and self.shield_recharge_step  > 0
            and self.shield_value < self.shield_hp
            and self.recharge_delay % self.shield_recharge_step == 0
        ):
            self.shield_value += 1

        if self.fire_delay > 0:
            self.fire_delay -= 1

        if self.trace_fire_delay > 0:
            self.trace_fire_delay -= 1

        if self.image_sequence:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.image_index = (self.image_index + 1) % len(self.image_sequence)
                self.image = self.image_sequence[self.image_index]

        if self.kill_time:
            if pygame.time.get_ticks() - self.kill_time > 500:  # 500毫秒后
                self.kill()
            else:
                self.on_killed()
        else:
            self.rect.x += self.speed_x  # 水平移动单位
            self.rect.y += self.speed_y  # 垂直移动单位

            if self.rect.left < 0:
                self.speed_x = abs(random.randint(1, 6))  # 反转x方向的速度

            if self.rect.right > DISPLAY_WIDTH:
                self.speed_x = -abs(random.randint(1, 6))  # 反转x方向的速度

            if self.rect.top < 0:
                self.speed_y = abs(random.randint(1, 3))  # 反转y方向的速度

            if self.rect.bottom > DISPLAY_HEIGHT // 2:
                self.speed_y = -abs(random.randint(1, 3))  # 反转y方向的速度

    def dodge_fighter(self, targets: List[pygame.sprite.Sprite]):
        pass

    @classmethod
    def get_ufo_master(cls):
        return FlightUnit("ufo_master", configmap["ufo_master"])

    @classmethod
    def get_ufo_slave(cls):
        return FlightUnit("ufo_slave", configmap["ufo_slave"])

    @classmethod
    def get_my_slave_fighter(cls):
        return FlightUnit("myf_slave", configmap["myf_slave"])


class MyMasterFighter(pygame.sprite.Sprite):
    """我方战机"""

    def __init__(self, config_data, sound_channel=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        self.sound_channel = sound_channel
        self.type = "myf_master"
        self.hp = self.config["life_value"]
        self.shield_hp = self.config["shield_value"]
        self.life_value = self.config["life_value"]
        self.image_sequence = []
        self.image_index = 0
        if self.config.get("image_sequence"):
            self.image_sequence = res_manager.load_image_sequence(
                self.config["image_sequence"]
            )
            self.image = self.image_sequence[self.image_index]
        else:
            self.image = res_manager.load_image(random.choice(self.config["image"]))

        self.rect = self.image.get_rect()
        self.rect.x = DISPLAY_WIDTH // 2  # 初始化x坐标
        self.rect.y = DISPLAY_HEIGHT - 220  # 将塔的y坐标设置为固定值
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200  # 每帧间隔毫秒数
        self.speed_x = self.config["speed_x"]
        self.speed_y = 0
        self.fire_delay = 0
        self.super_fire_delay = 0
        self.shield_value = self.config["shield_value"]  # 护盾值
        self.recharge_delay = 0  # 护盾充能延迟
        self.shield_recharge_step = self.config["shield_recharge_step"]  # 护盾充能步长

    def draw_health_bar(self, surface):
        """绘制血条到给定的surface上"""
        bar_length = int(self.rect.width * 1 / 2)
        bar_height = 8  # 血条的厚度
        fill = (self.life_value / self.hp) * bar_length  # 根据当前生命值计算填充长度

        # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
        outline_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            bar_length,
            bar_height,
        )  # 血条外框位置
        fill_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            fill,
            bar_height,
        )  # 血条填充位置

        pygame.draw.rect(surface, Colors.blue, outline_rect)  # 绘制血条外框
        pygame.draw.rect(surface, Colors.yellow, fill_rect)

        ## 绘制护盾值到给定的surface上
        fill = (
            self.shield_value / self.shield_hp
        ) * bar_length  # 根据当前护盾计算填充长度

        # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
        soutline_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height + 10,
            bar_length,
            bar_height,
        )
        sfill_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height + 10,
            fill,
            bar_height,
        )

        pygame.draw.rect(surface, Colors.blue, soutline_rect)
        pygame.draw.rect(surface, Colors.orange, sfill_rect)

    def fire(self, group, level):
        # self.recharge_delay = 0
        if self.fire_delay == 0:
            total_bullets = self.config[level]["bullet_per_num"]  # 想要发射的子弹总数
            bullet_spacing = 50//total_bullets  # 子弹之间的间距

            # 计算第一个子弹的偏移量
            offset = bullet_spacing * (total_bullets - 1) / 2

            for i in range(total_bullets):
                bullet_x = self.rect.centerx - offset + i * bullet_spacing
                bullet_y = self.rect.y + 40  # 子弹发射的垂直位置

                group.add(
                    Bullet(
                        bullet_x,
                        bullet_y,
                        speed=self.config[level]["bullet_speed"],
                        damage=self.config[level]["bullet_damage"],
                        direction="up",
                        color=Colors.get(self.config[level]["bullet_color"]),
                        radius=self.config[level]["bullet_radius"],
                    )
                )
            self.fire_delay = self.config[level]["fire_delay"]
            sound = res_manager.load_sound(self.config[level]["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def trace_fire(self, src_group, target_group, particle_group, level):
        # self.recharge_delay = 0
        if self.fire_delay == 0:
            total_bullets = self.config[level]["bullet_per_num"]  # 想要发射的子弹总数
            bullet_spacing = 50//total_bullets  # 子弹之间的间距

            # 计算第一个子弹的偏移量
            offset = bullet_spacing * (total_bullets - 1) / 2
            for i in range(total_bullets):
                bullet_x = self.rect.centerx - offset + i * bullet_spacing
                bullet_y = self.rect.y + 40  # 子弹发射的垂直位置

                src_group.add(
                    TraceBullet(
                        target_group,
                        particle_group,
                        bullet_x,
                        bullet_y,
                        speed=self.config[level]["bullet_speed"],
                        damage=self.config[level]["bullet_damage"],
                        direction="up",
                        color=Colors.get(self.config[level]["bullet_color"]),
                        radius=self.config[level]["bullet_radius"],
                    )
                )

            self.fire_delay = self.config[level]["fire_delay"]
            sound = res_manager.load_sound(self.config[level]["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def super_fire(self, src_group, target, particle_group):
        # self.recharge_delay = 0
        if self.super_fire_delay == 0:
            src_group.add(
                SuperBullet(
                    self.rect.width // 2 + self.rect.x,
                    self.rect.y,
                    target=target,
                    particle_group=particle_group,
                    config_data=self.config["super_bullet"],
                )
            )
            self.super_fire_delay = self.config["super_bullet"]["fire_delay"]
            sound = res_manager.load_sound(
                self.config["super_bullet"]["fire_sound"],
            )
            if self.sound_channel:
                self.sound_channel.play(sound)
            else:
                sound.play()

    def hit(self, damage: int):
        """被击中, 减少生命值"""
        # self.recharge_delay = 0

        if self.shield_value > 0:
            self.shield_value -= damage
            if self.shield_value <= 0:
                self.shield_value = 0
                self.life_value += self.shield_value
        else:
            if self.life_value > 0:
                self.life_value -= damage
                if self.life_value <= 0:
                    self.life_value = 0

        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.set_volume(self.config["firehit_sound_volume"])
        sound.play()

    def dodge_fighter(self, targets: List[pygame.sprite.Sprite]):
        pass

    def update(self):
        self.recharge_delay += 1
        if (
            self.shield_value < self.shield_hp
            and self.recharge_delay % self.shield_recharge_step == 0
        ):
            self.shield_value += 1

        if self.fire_delay > 0:
            self.fire_delay -= 1

        if self.super_fire_delay > 0:
            self.super_fire_delay -= 1

        if self.image_sequence:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.image_index = (self.image_index + 1) % len(self.image_sequence)
                self.image = self.image_sequence[self.image_index]
        
    def auto_move(self):
        self.rect.x += self.speed_x  # 水平移动单位

        if self.rect.left < 0:
            self.speed_x = abs(random.randint(1, 5))  # 反转x方向的速度

        if self.rect.right > DISPLAY_WIDTH:
            self.speed_x = -abs(random.randint(1, 5))  # 反转x方向的速度

    def move(self, dx):
        new_x = self.rect.x + dx * self.speed_x
        if 0 <= new_x <= DISPLAY_WIDTH - 100:
            self.rect.x = new_x


class Bullet(pygame.sprite.Sprite):
    """炮弹"""

    def __init__(
        self, x, y, speed=10, damage=1, direction="up", color=Colors.red, radius=5
    ):
        super().__init__()
        self.life_value = 1
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.radius = radius
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image = self.image.convert_alpha()

        # 从基础颜色到更亮的颜色创建渐变效果
        for r in range(radius, 0, -1):
            # 根据基础颜色和半径计算出渐变色
            color_lerp = tuple(min(255, max(0, c + (radius - r) * 12)) for c in color)
            pygame.draw.circle(self.image, color_lerp, (radius, radius), r)

        # 添加光亮点，假设光亮点颜色为纯白
        pygame.draw.circle(
            self.image, (255, 255, 255), (radius, radius // 2), radius // 4
        )

        self.rect = self.image.get_rect(center=(x, y))
        
    def hit(self, damage: int):
        pass

    def update(self):
        """更新炮弹位置"""
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed + random.choice([1, 2, 3, 4])
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()


class TraceBullet(pygame.sprite.Sprite):
    """跟踪炮弹"""

    def __init__(
        self,
        target_group,
        particle_group,
        x,
        y,
        speed=10,
        damage=1,
        direction="up",
        color=Colors.red,
        radius=5,
    ):
        super().__init__()
        self.life_value = 1
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.radius = radius
        self.target_group = target_group
        self.particle_group = particle_group
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image = self.image.convert_alpha()

        # 从基础颜色到更亮的颜色创建渐变效果
        for r in range(radius, 0, -1):
            # 根据基础颜色和半径计算出渐变色
            color_lerp = tuple(min(255, max(0, c + (radius - r) * 12)) for c in color)
            pygame.draw.circle(self.image, color_lerp, (radius, radius), r)

        # 添加光亮点，假设光亮点颜色为纯白
        pygame.draw.circle(
            self.image, (255, 255, 255), (radius, radius // 2), radius // 4
        )

        self.rect = self.image.get_rect(center=(x, y))

    def _track_target(self, targets):
        """选择生命值最低的目标进行跟踪"""
        if not targets:
            return None
        # 按生命值排序目标，选择生命值最低的
        closest_target = min(
            targets,
            key=lambda t: math.hypot(
                t.rect.centerx - self.rect.centerx, t.rect.centery - self.rect.centery
            ),
        )
        return closest_target

    def update(self, targets=None):
        """更新炮弹位置，并生成尾部粒子效果"""
        # 生成粒子效果
        for _ in range(1):  # 生成两个粒子
            self.particle_group.add(
                Particle(self.rect.centerx, self.rect.bottom, Colors.white,speed=0.2, size=3)
            )

        if not targets:
            targets = self.target_group

        # 跟踪逻辑
        if targets:
            target = self._track_target(targets)
            if target:
                # 计算移动方向
                dx, dy = (
                    target.rect.centerx - self.rect.centerx,
                    target.rect.centery - self.rect.centery,
                )
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # 单位化
                self.rect.x += self.speed * dx
                self.rect.y += self.speed * dy
        else:
            # 根据原始方向移动
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

        # 移除屏幕外的炮弹
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed=0.2, size=4):
        super().__init__()
        self.color = color
        self.speed = speed
        self.size = size  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.uniform(-1, 2)
        self.vel_y = random.uniform(-1, 2)
        self.lifetime = random.randint(20, 30)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= self.speed
        self.size -= 0.1  # 逐渐减小粒子的大小
        if self.size <= 0:
            self.kill()
        else:
            # 每次更新时重新创建圆形图像
            self.image = pygame.Surface(
                (int(self.size) * 2, int(self.size) * 2), pygame.SRCALPHA
            )
            self.image = self.image.convert_alpha()  # 确保支持透明度
            pygame.draw.circle(
                self.image, self.color, (int(self.size), int(self.size)), int(self.size)
            )
            self.rect = self.image.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )


class SuperBullet(pygame.sprite.Sprite):
    def __init__(
        self, x, y, target: pygame.sprite.Sprite, particle_group: None, config_data=None
    ):
        super().__init__()
        self.config = config_data
        self.particle_group = particle_group
        self.x = x
        self.y = y
        self.target = target  # 目标对象是另一个Sprite
        self.damage = self.config["damage"]
        self.speed = self.config["speed"]
        # 加载图像时保留原始图像用于旋转
        self.original_image = res_manager.load_image(self.config["image"])
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.life_value = self.config["life_value"]  # 假设初始生命值为100

    def attack(self):
        for _ in range(3):  # 生成两个粒子
            self.particle_group.add(
                Particle(self.rect.centerx, self.rect.centery, Colors.orange)
            )

        # 计算到目标的距离和角度
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # 距离目标120时，速度加倍
        if dist < self.config["acc_distance_1"]:
            self.speed *= 1.1

        # 距离目标120时，速度加倍
        if dist < self.config["acc_distance_2"]:
            self.speed *= 1.2

        # 调整炮弹位置
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # 旋转图像。注意Pygame中的角度是逆时针方向，需要转换为角度，并调整以使0度向上
        angle_degrees = math.degrees(angle) + 90
        self.image = pygame.transform.rotate(
            self.original_image, -angle_degrees
        )  # 注意这里的角度需要是负的，因为Pygame旋转方向与数学方向相反
        self.rect = self.image.get_rect(
            center=(self.rect.center)
        )  # 更新rect以保持中心位置不变

        # 边界检测
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()

    def hit(self, damage):
        """处理被击中"""
        self.life_value -= damage
        if self.life_value <= 0:
            self.kill()
        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.play()

    def update(self):
        self.attack()


class ShockParticle(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, color, speed=0.5):
        super().__init__()
        self.color = color
        self.speed = speed
        self.size = random.randint(9, b=15)  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # 随机生成一个角度
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.float_x = float(center_x)  # 添加这行
        self.float_y = float(center_y)  # 添加这行

        self.lifetime = random.randint(50, 100)  # 给粒子更长的生命周期

    def update(self):
        # 更新浮点数位置
        self.float_x += self.vel_x
        self.float_y += self.vel_y

        # 更新速度，使粒子加速
        self.vel_x *= 1.02
        self.vel_y *= 1.01

        # 减少生命周期，逐渐减小粒子的大小
        self.lifetime -= 0.3
        self.size -= 0.3

        if self.lifetime <= 0 or self.size <= 0:
            self.kill()  # 当生命周期结束或大小减小到0时，移除粒子
        else:
            # 重新创建图像以匹配新的大小，并保持中心位置不变
            self.image = pygame.Surface(
                (max(int(self.size * 2), 1), max(int(self.size * 2), 1)),
                pygame.SRCALPHA,
            )
            self.image = self.image.convert_alpha()
            pygame.draw.circle(
                self.image,
                self.color,
                (int(self.size), int(self.size)),
                max(int(self.size), 1),
            )

            # 更新rect对象，以便在绘制时使用正确的位置
            # 这里使用浮点数位置并转换为整数，保证粒子的中心位置绘制时不会因为尺寸变化而移动
            self.rect = self.image.get_rect(
                center=(int(self.float_x), int(self.float_y))
            )
