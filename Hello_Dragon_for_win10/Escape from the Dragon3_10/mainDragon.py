# -*- coding: utf-8 -*-
import mysprite
import pygame, sys, time, math, random, threading


# print_text function
def print_text(font, x, y, text, color=(0, 0, 0)):
    imgText = font.render(text, True, color)  # 渲染字体
    screen.blit(imgText, (x, y))


def reset_arrow():
    y = random.randint(300, 370)  # arrow的随机初始位置
    arrow.position = 800, y
    bomb_hit.play()
    master.Y = arrow.Y


def start_init():
    dragon.X = 250
    walkman.X = 500
    master.position = 820, 280
    global score, health_point, overmic_play, if_caught, dragon_disY
    score = 0
    health_point = 100
    overmic_play = False
    if_caught = False
    dragon_disY = 350


# 定时循环任务
def dragon_fly():
    global dragon_disY, game_over
    dragon_disY = random.randint(200, 365)
    if not game_over:
        global timer
        timer = threading.Timer(1, dragon_fly)
        timer.start()


# 主程序开始
pygame.init()
screen = pygame.display.set_mode((1000, 500), 0, 32)  # 界面大小
pygame.display.set_caption("Hello Dragon")  # 标题
# font = pygame.font.Font(None, 18)
frame_rate = pygame.time.Clock()

# 加载音效
jump_ing = pygame.mixer.Sound('resources/sound/jump.wav')
hit_man = pygame.mixer.Sound('resources/sound/hitman.wav')
hit_dragon = pygame.mixer.Sound('resources/sound/hitdragon.wav')
bomb_hit = pygame.mixer.Sound('resources/sound/bombhit.wav')
win_mic = pygame.mixer.Sound('resources/sound/win.wav')
fail_mic = pygame.mixer.Sound('resources/sound/fail.wav')
jump_ing.set_volume(0.2)
hit_man.set_volume(0.3)
hit_dragon.set_volume(0.3)
bomb_hit.set_volume(0.2)
win_mic.set_volume(0.4)
fail_mic.set_volume(0.4)

pygame.mixer.music.load('resources/sound/background.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


# 加载字体
over_font = pygame.font.Font('resources/font/FORTE.TTF', 60)
score_font = pygame.font.Font('resources/font/FORTE.TTF', 40)
tips_font = pygame.font.Font('resources/font/COOPBL.TTF', 35)
title_font = pygame.font.Font('resources/font/MATURASC.TTF', 80)
dragon_font = pygame.font.Font('resources/font/ALGER.TTF', 50)
continue_font = pygame.font.Font('resources/font/JOKERMAN.TTF',40)
master_font = pygame.font.Font('resources/font/MATURASC.TTF', 30)

# 加载背景
background1 = pygame.image.load('resources/image/back_ground.png').convert_alpha()
background2 = pygame.image.load('resources/image/back_ground_2.png').convert_alpha()
background = [background1, background2]
x1 = 0  # 滚动背景

# 创建精灵组
group = pygame.sprite.Group()
group_man = pygame.sprite.Group()

# 加载dragon
dragon = mysprite.MySprite(screen)
dragon_model = pygame.image.load('resources/image/dragon_fly.png').convert_alpha()  # 载入图片帧
width_model, height_model = dragon_model.get_size()
dragon_model = pygame.transform.smoothscale(dragon_model, (width_model//4, height_model//4))  # 图片像素太大，压缩之
dragon.load(dragon_model, 600//4, 332//4, 4)
dragon.position = 250, 330
dragon_go = 300

# 加载walkman
walkman = mysprite.MySprite(screen)
walkman_model = pygame.image.load('resources/image/walkman.png').convert_alpha()  # 载入图片帧
width_model, height_model = walkman_model.get_size()
walkman_model = pygame.transform.smoothscale(walkman_model, (width_model//1, height_model//1))  # 图片像素太大，压缩之
walkman.load(walkman_model, 64//1, 55//1, 8)
walkman.position = 500, 380


# 加载arrow
group_arrow = pygame.sprite.Group()
arrow = mysprite.MySprite(screen)
arrow_model = pygame.image.load('resources/image/arrow.png').convert_alpha()  # 载入图片帧
width_model, height_model = arrow_model.get_size()
arrow_model = pygame.transform.smoothscale(arrow_model, (width_model//4, height_model//4))  # 图片像素太大，压缩之
arrow.load(arrow_model, 192//4, 192//4, 5)
arrow.position = -100, 320  # arrow初始位置

# 加载master
master = mysprite.MySprite(screen)
master_model = pygame.image.load('resources/image/bomb_master.png').convert_alpha()
master.load(master_model, 75, 75, 8)
master.position = 820, 280

# 加载精灵类
group.add(dragon)
group_man.add(walkman)
group_arrow.add(arrow, master)


arrow_vel = 3.0
game_over = False
if_win = False
walkman_jumping = False
jum_vel = 0.0
walkman_start_y = walkman.Y
start_flag = False
score = 0
health_point = 100
overmic_play = False
if_caught = False
dragon_disY = 350

timer = threading.Timer(2, dragon_fly)
timer.start()


# 初始界面
print_text(over_font, 300, 160, "Hi Dragon")

# 主循环
while True:
    # time_now = time.time()
    # if int(time_now) % 2 == 0:
    #     dragon_go = random.randint(250, 370)
    #     dragon.Y = dragon_go
    frame_rate.tick(100)
    ticks = pygame.time.get_ticks()

    # screen.blit(background, (0, 0))  # 绘制背景图

    if not game_over:
        x1 -= 1
    if x1 <= -1000:
        background = background[1:]+background[:1]
        background1, background2 = background
        x1 = 0
    screen.blit(background1, (x1, 0))
    screen.blit(background2, (x1+1000, 0))

    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            game_over = True
            sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            game_over = True
        elif key[pygame.K_SPACE]:
            if not walkman_jumping and start_flag:
                if not game_over:
                    walkman_jumping = True
                    jum_vel = -8.0
                    jump_ing.play()
        # elif key[pygame.K_m]:
            if game_over and start_flag:
                game_over = False
                start_flag = False
                arrow.position = -100, 320  # arrow初始位置
                start_init()
                timer = threading.Timer(2, dragon_fly)
                timer.start()

            elif not start_flag or game_over:
                start_flag = True
                reset_arrow()

    if start_flag:  # start_flag且not game_over,arrow开始运动
        if not game_over:
            arrow.X -= arrow_vel
            if arrow.X < -20:
                reset_arrow()

    # arrow与walkman碰撞
    if pygame.sprite.collide_rect_ratio(0.75)(arrow, walkman):
        reset_arrow()
        walkman.X -= 30
        hit_man.play()
        score -= 100
        if not health_point == 0:
            health_point -= 25

    # arrow与dragon碰撞
    if pygame.sprite.collide_rect_ratio(0.75)(arrow, dragon):
        reset_arrow()
        dragon.X -= 30
        score += 100
        hit_dragon.play()
    # walkman与dragon碰撞
    if pygame.sprite.collide_rect_ratio(0.75)(walkman, dragon):
        game_over = True
        if_win = False
        if_caught = True
    # dragon被打出屏幕外
    if dragon.X < -110:
        game_over = True
        if_win = True

    if health_point == 0:
        game_over = True
    # Jump
    if walkman_jumping:
        walkman.Y += jum_vel
        jum_vel += 0.27
        if walkman.Y > walkman_start_y:
            walkman_jumping = False
            walkman.Y = walkman_start_y
            jum_vel = 0

    if not game_over:
        group.update(ticks, 100)  # 比ticks慢
        group_man.update(ticks)
        group_arrow.update(ticks, 150)
        if dragon_disY > dragon.Y:
            dragon.Y += 1
        elif dragon_disY < dragon.Y:
            dragon.Y -= 1

    group.draw(screen)
    group_man.draw(screen)
    group_arrow.draw(screen)

    # Testing
    # print_text(font, 0, 0, "Sprite:"+str(dragon))
    # print_text(font, 0, 10, "ticks:"+str(time.localtime()))
    # print_text(font, 0, 20, "Game Over: "+str(game_over)+"    "+"Start_flag: "+str(start_flag))
    # print_text(font, 0, 30, "health  " + str(health_point))
    # print_text(font, 0, 40, "ticks  " + str(int(ticks)))

    # Print Score
    print_text(score_font, 800, 20, "Score:  " + str(score))
    print_text(score_font, 50, 10, "Health Point")

    # Draw Health_point
    pygame.draw.line(screen, (0, 0, 0), (50, 60), (280, 60), 3)
    pygame.draw.line(screen, (0, 0, 0), (50, 80), (280, 80), 3)
    pygame.draw.line(screen, (0, 0, 0), (280, 60), (280, 80), 3)
    pygame.draw.rect(screen, (0, 0, 0), (50, 60, 2.3 * health_point, 20), 0)

    if game_over and start_flag:
        print_text(over_font, 350, 150, "GAME OVER")
        print_text(continue_font, 320, 435, "Press Space to Continue", color=(255, 255, 255))

        if if_win:
            print_text(tips_font, 430, 250, "You Win !")
            print_text(tips_font, 370, 320, "Goodbye Mr.Dragon  !")
            if_win = False
            if not overmic_play:
                win_mic.play()
                overmic_play = True
        else:
            print_text(tips_font, 430, 250, "You Fail !")
            if if_caught:
                print_text(tips_font, 370, 320, "Caught by Dragon !")
            if not overmic_play:
                fail_mic.play()
                overmic_play = True

    if not (start_flag or game_over):
        print_text(title_font, 250, 150, "Hello Dragon")
        print_text(continue_font, 330, 435, "Press Space to Start", color=(255, 255, 255))
        print_text(master_font, 780, 350, "Pyroblast!!")
    pygame.display.update()
