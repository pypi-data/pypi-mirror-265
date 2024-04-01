import asyncio
import math
import random
import pygame
from .config import configmap
from .common import (
    res_manager,
    get_assets,
    Colors,
)
from .actors import (
    FlightUnit,
    MyMasterFighter,
    Background,
    Particle,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    ScaleBackground,
    ShockParticle,
    SuperBullet,
)



IS_FULLSCREEN = configmap["fullscreen"]


class SpaceDefense(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_reserved(2)
        pygame.display.set_caption("Space Defense")
        icon = pygame.image.load(get_assets("images/icon.png"))  # 替换 'your_icon_path.png' 为你的图标文件路径
        self.auto_game = False
        self.chorus_channel = pygame.mixer.Channel(0)
        self.myf_channel = pygame.mixer.Channel(1)
        self.chorus_channel.set_volume(0.5)
        self.is_fullscreen = IS_FULLSCREEN
        if IS_FULLSCREEN:
            self.screen = pygame.display.set_mode(
                (DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        pygame.display.set_icon(icon)
        self.title_font = pygame.font.Font(None, 42)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.countdown = configmap["game_time"]
        self.my_support_delay = 0
        self.game_win = False
        self.my_score = 0
        self.ufo_score = 0
        self.my_score_step = configmap["my_score_step"]
        self.ufo_score_step = configmap["ufo_score_step"]
        self.running = True

        self.ufo_limit = configmap["ufo_slave"]["min_limit"]
        self.myf_limit = configmap["myf_slave"]["min_limit"]

        self.setup_background()
        self.load_sounds()
        self.setup_groups()
        self.setup_events()
        self.create_actors()

    def setup_background(self):
        self.background_type = configmap["background"]["type"]
        self.background = Background([0, 0], configmap["background"]["vmove"])
        self.scale_background = ScaleBackground(
            get_assets(configmap["background"]["scale"]["image"]), [0, 0]
        )
        self.bggroup = pygame.sprite.Group()
        if self.background_type == "vmove":
            self.bggroup.add(self.background)
        elif self.background_type == "scale":
            self.bggroup.add(self.scale_background)
        else:
            self.bggroup.add(self.background)

    async def restart(self):
        self.__init__()
        await self.start_game()

    def load_sounds(self):
        # 加载声音文件
        self.sufo_join_sound = pygame.mixer.Sound(get_assets("sounds/sufo_join.ogg"))
        self.sfighter_join_sound = pygame.mixer.Sound(
            get_assets("sounds/smyf_join.ogg")
        )
        # 事件声音
        self.sound_stage_start = pygame.mixer.Sound(
            get_assets("sounds/stage_start.ogg")
        )
        self.sound_stage_mid = pygame.mixer.Sound(get_assets("sounds/stage_mid.ogg"))
        self.sound_stage_angry = pygame.mixer.Sound(
            get_assets("sounds/stage_angry.ogg")
        )
        self.sound_stage_end_win = pygame.mixer.Sound(
            get_assets("sounds/stage_end_win.ogg")
        )
        self.sound_stage_end_loss = pygame.mixer.Sound(
            get_assets("sounds/stage_end_loss.ogg")
        )

    def update_my_socre(self, score_value):
        self.my_score += score_value
        if self.my_score < 0:
            self.my_score = 0

    def update_ufo_socre(self, score_value):
        self.ufo_score += score_value
        if self.ufo_score < 0:
            self.ufo_score = 0

    def play_bgm(self):
        """播放背景音乐""" ""
        pygame.mixer.music.load(get_assets(configmap["bgm"]["sound"]))
        pygame.mixer.music.set_volume(configmap["bgm"]["sound_volume"])
        pygame.mixer.music.play(-1)

    def setup_groups(self):
        # 粒子组
        self.particles = pygame.sprite.Group()
        self.shock_particles = pygame.sprite.Group()
        # 我方炮弹组
        self.my_bullets = pygame.sprite.Group()
        # 敌方炮弹组
        self.ufo_bullets = pygame.sprite.Group()
        # 我方飞行单位组
        self.my_flight_units = pygame.sprite.Group()
        # 敌方飞行单位组
        self.ufo_units = pygame.sprite.Group()

    def create_actors(self):
        # 创建敌方飞行单位
        self.ufo_master = FlightUnit.get_ufo_master()
        self.ufo_units.add(self.ufo_master)
        self.my_master_fighter = MyMasterFighter(
            configmap["myf_master"], self.myf_channel
        )
        self.my_flight_units.add(self.my_master_fighter)

    def setup_events(self):
        # 创建一个计时器事件
        self.TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMEREVENT, 1000)

        # 创建一个UFO开火计时器事件
        self.UFO_FIRE_TIMEREVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.UFO_FIRE_TIMEREVENT, millis=250)

        # UFO Slave 进场事件
        self.SUFO_TIMEREVENT = pygame.USEREVENT + 4
        pygame.time.set_timer(self.SUFO_TIMEREVENT, 3000)

        # 我方战机开火事件
        self.MY_FIGHTER_FIRE_TIMEREVENT = pygame.USEREVENT + 5
        pygame.time.set_timer(self.MY_FIGHTER_FIRE_TIMEREVENT, 250)

        self.SWITCH_BG_TIMEREVENT = pygame.USEREVENT + 6
        pygame.time.set_timer(self.SWITCH_BG_TIMEREVENT, 30000)

        self.STAGE_STATE_EVENT = pygame.USEREVENT + 10

    def create_hit_particle(self, actor_obj, num):
        for _ in range(num):
            particle = Particle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + 10,
                Colors.light_yellow,
            )
            self.particles.add(particle)

    def create_hit_shock_particle(self, actor_obj, num):
        for _ in range(num):
            particle = ShockParticle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + actor_obj.rect.height // 2,
                Colors.white,
                speed=4,
            )
            self.shock_particles.add(particle)

    def _proc_on_keydown(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.my_master_fighter.move(-1)  # 向左移动
        if keys[pygame.K_RIGHT]:
            self.my_master_fighter.move(1)  # 向右移动
        if keys[pygame.K_1]:
            self.my_master_fighter.fire(
                self.my_bullets,
                "level1",
            )
        if keys[pygame.K_2]:
            self.my_master_fighter.trace_fire(
                self.my_bullets, self.ufo_units, self.particles, "level2"
            )
        if keys[pygame.K_3]:
            self.my_master_fighter.trace_fire(
                self.my_bullets, self.ufo_bullets, self.particles, "level3"
            )
        if keys[pygame.K_5]:
            score_cast = configmap["myf_master"]["super_bullet"]["score_cast"]
            if (
                self.my_score >= score_cast
                and self.my_master_fighter.super_fire_delay == 0
            ):
                self.my_master_fighter.super_fire(
                    self.my_bullets,
                    self.ufo_master,
                    self.particles,
                )
                self.update_my_socre(-score_cast)
        if keys[pygame.K_4]:
            if self.my_support_delay == 0:
                self._call_my_support()

        if keys[pygame.K_a]:
            self.auto_game = not self.auto_game

        if keys[pygame.K_f]:
            if not self.is_fullscreen:
                self.screen = pygame.display.set_mode(
                    (DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN
                )
                self.is_fullscreen = True
            else:
                self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
                self.is_fullscreen = False

    def _proc_on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == self.TIMEREVENT:  # 如果是计时器事件
            self.countdown -= 1  # 倒计时减1
            if (
                self.ufo_master.life_value <= 0
                and self.my_master_fighter.life_value > 0
            ):
                self.game_win = True
                self.running = False
            elif self.my_master_fighter.life_value <= 0 or self.countdown <= 0:
                self.running = False
                self.game_win = False

            if self.my_support_delay > 0:
                self.my_support_delay -= 1

        elif event.type == self.UFO_FIRE_TIMEREVENT:
            for ufo in self.ufo_units:
                directions = ["down"]
                if len(self.my_flight_units) > 1:
                    directions = ["down", "down",  "left", "down", "right", "down",]

                ufo.fire(
                    group=self.ufo_bullets,
                    direction=random.choice(directions),
                    target_group=self.my_flight_units,
                    particle_group=self.particles,
                )

        elif event.type == self.MY_FIGHTER_FIRE_TIMEREVENT:
            for myf in self.my_flight_units:
                if myf.type == "myf_master" and self.auto_game:
                    self._auto_myf_master()
                if myf.type == "myf_slave":
                    my_direction = "left"
                    if myf.rect.x < self.ufo_master.rect.x:
                        my_direction = "right"
                    myf.fire(
                        group=self.my_bullets,
                        direction=my_direction,
                        target_group=self.ufo_units,
                        particle_group=self.particles,
                    )

        elif event.type == self.SUFO_TIMEREVENT:
            # UFO 自动呼叫支援
            self._auto_ufo_support()

    def _auto_myf_master(self):
        fire_type = random.choice(
            [
                "level1",
                "level2",
                "level3",
                "level2",
                "level3",
                "level2",
                "level3",
            ]
        )
        if fire_type == "level1":
            self.my_master_fighter.fire(
                self.my_bullets,
                "level1",
            )
        elif fire_type == "level2":
            self.my_master_fighter.trace_fire(
                self.my_bullets, self.ufo_units, self.particles, "level2"
            )
        elif fire_type == "level3":
            self.my_master_fighter.trace_fire(
                self.my_bullets, self.ufo_bullets, self.particles, "level3"
            )

        if self.my_support_delay == 0:
            self._call_my_support()

        score_cast = configmap["myf_master"]["super_bullet"]["score_cast"]
        if self.my_score >= score_cast and self.my_master_fighter.super_fire_delay == 0:
            self.my_master_fighter.super_fire(
                self.my_bullets,
                self.ufo_master,
                self.particles,
            )
            self.update_my_socre(-score_cast)

    def _auto_ufo_support(self):
        score_cast = configmap["ufo_slave"]["score_cast"]
        ufo_max_limit = configmap["ufo_slave"]["max_limit"]
        myf_max_limit = configmap["myf_slave"]["max_limit"]
        if self.ufo_score >= score_cast and len(self.ufo_units) - 1 < self.ufo_limit:
            sufo = FlightUnit.get_ufo_slave()
            self.ufo_score -= score_cast
            if self.ufo_score < 0:
                self.ufo_score = 0
            self.ufo_units.add(sufo)
            self.chorus_channel.play(self.sufo_join_sound)

        # 狂暴检测
        if self.countdown < 120:
            if not self.ufo_master.is_angry:
                self.ufo_master.is_angry = True
                self.ufo_limit = ufo_max_limit
                self.myf_limit = myf_max_limit
                self.chorus_channel.play(self.sound_stage_angry)

    def _call_my_support(self):
        score_cast = configmap["myf_slave"]["score_cast"]
        if (
            self.my_score >= score_cast
            and len(self.my_flight_units) - 1 < self.myf_limit
        ):
            self.my_support_delay = 3
            my_support = FlightUnit.get_my_slave_fighter()
            self.update_my_socre(-score_cast)
            self.my_flight_units.add(my_support)
            self.chorus_channel.play(self.sfighter_join_sound)

    def _proc_on_collisions(self):
        """处理碰撞检测, 伤害值， 分数值更新"""
        collisions = pygame.sprite.groupcollide(
            self.my_bullets, self.ufo_units, False, False
        )
        for my_bullet, hit_ufo_units in collisions.items():
            for ufo_unit in hit_ufo_units:
                if isinstance(my_bullet, SuperBullet):
                    if ufo_unit.type == "ufo_master":
                        ufo_unit.hit(my_bullet.damage)
                        self.create_hit_shock_particle(ufo_unit, 200)
                        self.create_hit_particle(ufo_unit, my_bullet.damage * 5)
                        super_fire_sound = res_manager.load_sound(
                            "sounds/super_firehit.ogg"
                        )
                        self.myf_channel.play(super_fire_sound)
                        my_bullet.kill()
                    else:
                        if my_bullet.life_value > 50:
                            ufo_unit.hit(10)
                            my_bullet.hit(10)
                        else:
                            ufo_unit.hit(my_bullet.damage)
                            my_bullet.kill()
                else:
                    ufo_unit.hit(my_bullet.damage)
                    self.create_hit_particle(ufo_unit, my_bullet.damage * 5)
                    self.update_my_socre(my_bullet.damage // self.my_score_step)
                    my_bullet.kill()

        ucollisions = pygame.sprite.groupcollide(
            self.ufo_bullets, self.my_flight_units, True, False
        )
        for u_bullet, hit_my_units in ucollisions.items():
            for my_unit in hit_my_units:
                my_unit.hit(u_bullet.damage)
                self.create_hit_particle(my_unit, u_bullet.damage * 3)
                self.update_ufo_socre(u_bullet.damage // self.ufo_score_step)

        bcollisions = pygame.sprite.groupcollide(
            self.my_bullets, self.ufo_bullets, False, True
        )

        for myb, ubs in bcollisions.items():
            for ub in ubs:
                self.create_hit_particle(ub, 10)
                if isinstance(myb, SuperBullet):
                    myb.hit(ub.damage)
                else:
                    myb.kill()

        pygame.sprite.groupcollide(
            self.shock_particles, self.ufo_bullets, dokilla=True, dokillb=True
        )

        pygame.sprite.groupcollide(
            self.shock_particles, self.my_bullets, dokilla=True, dokillb=True
        )

        xcollisions = pygame.sprite.groupcollide(
            self.my_flight_units, self.ufo_units, False, False
        )
        for myf, uflist in xcollisions.items():
            for uf in uflist:
                myf.hit(0.05)
                uf.hit(0.05)
                blast_sound = res_manager.load_sound("sounds/fire_blast.ogg")
                blast_sound.set_volume(0.4)
                self.myf_channel.queue(blast_sound)
                self.create_hit_particle(uf, 20)
                self.update_my_socre(-0.1)
                self.update_ufo_socre(-0.1)

        super_collisions = pygame.sprite.groupcollide(
            self.shock_particles, self.ufo_units, False, False
        )
        for mysp, uflist in super_collisions.items():
            for uf in uflist:
                uf.hit(0.001)

        super_collisions2 = pygame.sprite.groupcollide(
            self.shock_particles, self.my_flight_units, False, False
        )
        for mysp, myflist in super_collisions2.items():
            for myf in myflist:
                myf.hit(0.001)

    def _proc_draw_texts(self):
        #################### 在左下角绘制倒计时
        mins, secs = divmod(self.countdown, 60)
        timer_str = "{:02d}:{:02d}".format(mins, secs)
        countdown_text = self.title_font.render(str(timer_str), True, Colors.white)
        self.screen.blit(
            countdown_text,
            (20, self.screen.get_height() - countdown_text.get_height() - 36),
        )

        #################### 在中间显示战斗机 HP
        fighter_life_text = self.title_font.render(
            f"OUR: {round(self.my_master_fighter.life_value)} <> SCORE: {round(self.my_score)}",
            True,
            Colors.red,
        )
        self.screen.blit(
            fighter_life_text,
            (
                200,
                self.screen.get_height() - fighter_life_text.get_height() - 36,
            ),
        )

        fighter_recharge_text = self.subtitle_font.render(
            f"Shield: {round(self.my_master_fighter.shield_value)}",
            True,
            Colors.white,
        )
        self.screen.blit(
            fighter_recharge_text,
            (
                200,
                self.screen.get_height() - fighter_recharge_text.get_height() - 8,
            ),
        )

        #################### 在右下角显示UFO HP
        ufo_life_text = self.title_font.render(
            f"UFO: {round(self.ufo_master.life_value)} <> SCORE: {round(self.ufo_score)}",
            True,
            Colors.orange,
        )  # 创建分数文本
        self.screen.blit(
            ufo_life_text,
            (
                self.screen.get_width() - ufo_life_text.get_width() - 20,
                self.screen.get_height() - ufo_life_text.get_height() - 36,
            ),
        )

        ufo_shield_text = self.subtitle_font.render(
            f"Shield: {round(self.ufo_master.shield_value)}",
            True,
            Colors.white,
        )
        self.screen.blit(
            ufo_shield_text,
            (
                self.screen.get_width() - ufo_life_text.get_width() - 20,
                self.screen.get_height() - ufo_shield_text.get_height() - 8,
            ),
        )

    async def game_pre(self):
        is_play = False
        particles = pygame.sprite.Group()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break

            for _ in range(10):  # 创建粒子
                particles.add(Particle(450, 300, Colors.yellow))

            cover_image = res_manager.load_image(configmap["game_cover"]["cover_image"])
            scaled_image = pygame.transform.scale(
                cover_image, (self.screen.get_width(), self.screen.get_height())
            )
            self.screen.blit(scaled_image, (0, 0))

            particles.update()

            particles.draw(self.screen)

            pygame.display.flip()
            asyncio.sleep(0)
            if not is_play:
                is_play = True
                pygame.mixer.music.load(get_assets("sounds/stage_pre.ogg"))
                pygame.mixer.music.play()

    #######################################################
    ## start game
    #######################################################
    async def start_game(self):
        """开始游戏"""
        await self.game_pre()
        self.chorus_channel.play(self.sound_stage_start)
        self.running = True
        self.play_bgm()
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self._proc_on_event(event)
                if not self.running:
                    break

            if self.background_type == "vmove":
                self.background.update()
                self.screen.blit(
                    self.background.image,
                    (self.background.rect.x, self.background.rect.y),
                )
                self.screen.blit(
                    self.background.image,
                    (
                        self.background.rect.x,
                        self.background.rect.y - self.background.rect.height,
                    ),
                )
            elif self.background_type == "scale":
                self.screen.fill(Colors.black)
                self.bggroup.update()
                self.bggroup.draw(self.screen)

            self._proc_on_keydown()
            self._proc_on_collisions()

            self.particles.update()
            self.particles.draw(self.screen)

            self.shock_particles.update()
            self.shock_particles.draw(self.screen)

            for myf in self.my_flight_units:
                myf.dodge_fighter(self.ufo_units)

            if self.auto_game:
                self.my_master_fighter.auto_move()

            self.my_flight_units.update()
            self.my_flight_units.draw(self.screen)
            for unit in self.my_flight_units:
                unit.draw_health_bar(self.screen)

            self.ufo_units.update()
            self.ufo_units.draw(self.screen)
            for unit in self.ufo_units:
                unit.draw_health_bar(self.screen)

            self.my_bullets.update()
            self.my_bullets.draw(self.screen)

            self.ufo_bullets.update()
            self.ufo_bullets.draw(self.screen)

            pygame.draw.rect(
                self.screen, (0, 0, 0), (0, DISPLAY_HEIGHT - 70, DISPLAY_WIDTH, 70)
            )
            self._proc_draw_texts()

            pygame.display.flip()  # 更新显示
            clock.tick(60)  # 设置帧率
            asyncio.sleep(0)
        await self.game_stop()

    async def game_stop(self):
        """游戏结束画面"""
        game_font = pygame.font.Font(None, 200)
        if self.game_win:
            # 如果游戏胜利，显示胜利文本
            text = game_font.render("You Win!", True, (255, 0, 0))
            textpos = text.get_rect(
                centerx=self.screen.get_width() / 2,
                centery=self.screen.get_height() / 2,
            )
            self.screen.blit(text, textpos)
            self.chorus_channel.play(self.sound_stage_end_win)
        else:
            # 如果游戏失败，显示失败文本
            text = game_font.render("Game Over!", True, (0, 0, 255))
            textpos = text.get_rect(
                centerx=self.screen.get_width() / 2,
                centery=self.screen.get_height() / 2,
            )
            self.screen.blit(text, textpos)
            self.chorus_channel.play(self.sound_stage_end_loss)

        game_restart = False

        particles = pygame.sprite.Group()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_restart = True
                break

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return

            for _ in range(10):  # 创建粒子
                particles.add(Particle(450, 300, Colors.yellow))

            if self.game_win:
                cover_image = res_manager.load_image(
                    configmap["game_cover"]["cover_win"]
                )
            else:
                cover_image = res_manager.load_image(
                    configmap["game_cover"]["cover_loss"]
                )

            scaled_image = pygame.transform.scale(
                cover_image, (self.screen.get_width(), self.screen.get_height())
            )
            self.screen.blit(scaled_image, (0, 0))

            particles.update()
            particles.draw(self.screen)

            pygame.display.flip()
            asyncio.sleep(0)

        if game_restart:
            await self.restart()


def main():
    asyncio.run(SpaceDefense().start_game())
    

if __name__ == '__main__':
    main()