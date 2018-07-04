# coding=utf-8
# 坦克大战
# last update: 2018-06-29
# by. XYJ
#  ____________ 玩法说明 ______________
#      上下左右键：控制玩家坦克移动
#         空格键：发射子弹
#         躲避敌方坦克的子弹
#        击中敌方坦克来获得分数
#  -----------------------------------
from Tkinter import *
import time, random

# 窗口的宽和高
WIN_WIDTH = 600
WIN_HEIGHT = 600

# 敌方坦克图片的宽和高
E_TANK_WIDTH = 45
E_TANK_HEIGHT = 45

# 敌方坦克的数量
E_TANK_NUM = 10

# 敌方子弹的宽和高
E_BULLET_WIDTH = 16
E_BULLET_HEIGHT = 16

# 玩家坦克图片的宽和高
P_TANK_WIDTH = 62
P_TANK_HEIGHT = 76

# 玩家坦克的子弹的宽和高
P_BULLET_WIDTH = 28
P_BULLET_HEIGHT = 28

# 坦克的状态
ACTIVE = "active"
EXPLODE = "explode"
USELESS = "useless"

DIRECTIONS = ["up", "left", "down", "right"]

win = Tk()
can = Canvas(win, width=WIN_WIDTH, height=WIN_HEIGHT)
can.pack()

# 导入背景图片
bg = PhotoImage(file="pic/bg.gif")
can.create_image(0, 0, image=bg, anchor="nw")

# 所有tank的底片都将被存在tanks_img字典里
# 访问底片的方式 tanks_img[坦克颜色][坦克方向]
tanks_img = {}

# 蓝色tank各个方向的底片
blue_tank = {}
for d in DIRECTIONS:
    blue_tank[d] = PhotoImage(file="pic/tank_blue_" + d + ".gif")

# 黑色tank各个方向的底片
black_tank = {}
for d in DIRECTIONS:
    black_tank[d] = PhotoImage(file="pic/tank_black_" + d + ".gif")

# 红色tank各个方向的底片
red_tank = {}
for d in DIRECTIONS:
    red_tank[d] = PhotoImage(file="pic/tank_red_" + d + ".gif")

# 玩家tank的颜色为"huge"
huge_tank = {}
for d in DIRECTIONS:
    huge_tank[d] = PhotoImage(file="pic/tank_huge_" + d + ".gif")

tanks_img["blue"] = blue_tank
tanks_img["red"] = red_tank
tanks_img["black"] = black_tank
tanks_img["huge"] = huge_tank

# tank爆炸的图片
explosion = []
for i in range(5):
    explosion.append(PhotoImage(file="pic/explosion" + str(i + 1) + ".gif"))

bullets_img = {}

# 蓝色子弹的底片
blue_bullet = {}
for d in DIRECTIONS:
    blue_bullet[d] = PhotoImage(file="pic/bullet_blue_" + d + ".gif")

# 红色子弹的底片
red_bullet = {}
for d in DIRECTIONS:
    red_bullet[d] = PhotoImage(file="pic/bullet_red_" + d + ".gif")

# 黑色子弹的底片
black_bullet = {}
for d in DIRECTIONS:
    black_bullet[d] = PhotoImage(file="pic/bullet_black_" + d + ".gif")

# 玩家子弹的底片
huge_bullet = {}
for d in DIRECTIONS:
    huge_bullet[d] = PhotoImage(file="pic/bullet_huge_" + d + ".gif")

bullets_img["blue"] = blue_bullet
bullets_img["red"] = red_bullet
bullets_img["black"] = black_bullet
bullets_img["huge"] = huge_bullet

# Tank类
class Tank():

    def __init__(self, x, y, d, c):
        # 颜色
        self.color = c
        # 方向
        self.dir = d
        # 速度(每帧移动的距离)
        self.speed = 5
        # 图形元素
        self.drawable = can.create_image(x, y,
                                         image=tanks_img[self.color][self.dir],
                                         anchor="nw")
        # 记录Tank状态
        self.state = ACTIVE
        # 切换爆炸状态的计数器
        self.e_count = 0
        # 坦克底片的长和高
        if self.color == "huge":
            self.width = P_TANK_WIDTH
            self.height = P_TANK_HEIGHT
        else:
            self.width = E_TANK_WIDTH
            self.height = E_TANK_HEIGHT

    # 更新坦克的位置和底片
    def update_pos_img(self):
        if self.state == USELESS:
            pass

        elif self.state == EXPLODE:
            # 切换底片形成爆炸动画
            can.itemconfig(self.drawable, image=explosion[self.e_count])
            self.e_count += 1
            # 如果已经切换至最后一张底片
            if self.e_count == 5:
                self.state = USELESS
                self.e_count = 0

        elif self.state == ACTIVE:
            t_pos = self.get_pos()

            # 撞墙后随机更改方向
            if t_pos[0] < 0:
                self.dir = random.choice(["down", "up", "right"])
            elif t_pos[1] < 0:
                self.dir = random.choice(["down", "left", "right"])
            elif t_pos[2] > WIN_WIDTH:
                self.dir = random.choice(["down", "up", "left"])
            elif t_pos[3] > WIN_HEIGHT:
                self.dir = random.choice(["left", "up", "right"])

            can.itemconfig(self.drawable, image=tanks_img[self.color][self.dir])

            # 移动坦克位置
            if self.dir == "up":
                can.move(self.drawable, 0, -self.speed)
            elif self.dir == "left":
                can.move(self.drawable, -self.speed, 0)
            elif self.dir == "down":
                can.move(self.drawable, 0, self.speed)
            elif self.dir == "right":
                can.move(self.drawable, self.speed, 0)

    # 创建一颗子弹
    def create_bullet(self):
        if self.color == "huge":
            b_e = P_BULLET_WIDTH

        else:
            b_w = E_BULLET_WIDTH
            b_h = E_BULLET_HEIGHT

        # 计算出bullet应该在哪里被创建出来
        b_pos = self.get_pos()
        if self.dir == "up":
            b_pos = [b_pos[0] + (self.width-b_w)/2, b_pos[1]]
        elif self.dir == "down":
            b_pos = [b_pos[0] + (self.width-b_w)/2, b_pos[1] + self.height]
        elif self.dir == "left":
            b_pos = [b_pos[0], b_pos[1] + (self.height-b_w)/2]
        elif self.dir == "right":
            b_pos = [b_pos[0] + self.width, b_pos[1] + (self.height - b_w)/2]

        b = Bullet(b_pos, self.color, self.dir, b_w)
        return b


    def get_pos(self):
        b_pos = can.coords(self.drawable)
        b_pos = b_pos + [b_pos[0] + self.width, b_pos[1] + self.height]
        return b_pos


    def set_dir_up(self, event):
        self.dir = "up"


    def set_dir_down(self, event):
        self.dir = "down"

    def set_dir_left(self, event):
        self.dir = "left"

    def set_dir_right(self, event):
        self.dir = "right"


# Bullet类
class Bullet():
    def __init__(self, pos, c, d, w):
        self.color = c
        self.width = w
        self.dir = d
        self.imgs = bullets_img[self.color]
        self.speed = 10
        self.drawable = can.create_image(pos[0], pos[1], image=self.imgs[self.dir], anchor="nw")
        self.state = ACTIVE

    def update_pos(self):
        can.itemconfig(self.drawable, image=self.imgs[self.dir])
        if self.dir == "up":
            can.move(self.drawable, 0, -self.speed)
        elif self.dir == "left":
            can.move(self.drawable, -self.speed, 0)
        elif self.dir == "down":
            can.move(self.drawable, 0, self.speed)
        elif self.dir == "right":
            can.move(self.drawable, self.speed, 0)

    def update_state(self):
        b_pos = self.get_pos()

        if b_pos[0] < 0 or b_pos[1] < 0 or \
                        b_pos[2] > WIN_WIDTH or b_pos[3] > WIN_HEIGHT:
            self.state = USELESS

    def get_pos(self):
        b_pos = can.coords(self.drawable)
        b_pos = b_pos + [b_pos[0] + self.width, b_pos[1] + self.width]
        return b_pos


# 主程序开始的地方
# 敌方的坦克和子弹列表
enemy_tanks = []
enemy_bullets = []

for i in range(E_TANK_NUM):
    x = random.randint(0, WIN_WIDTH - E_TANK_WIDTH)
    y = random.randint(0, WIN_HEIGHT - E_TANK_WIDTH)
    d = random.choice(["up", "left", "down", "right"])
    c = random.choice(["red", "blue", "black"])
    enemy_tanks.append(Tank(x, y, d, c))

# 玩家的坦克和子弹
player_tank = Tank(10, 10, "down", "huge")
player_bullets = []


def shoot(event):
    player_bullets.append(player_tank.create_bullet())


# 将按键与玩家坦克的方法进行绑定
can.bind_all('<Up>', player_tank.set_dir_up)
can.bind_all('<Left>', player_tank.set_dir_left)
can.bind_all('<Down>', player_tank.set_dir_down)
can.bind_all('<Right>', player_tank.set_dir_right)
can.bind_all('<space>', shoot)


def is_collide(a, b):
    if a[0] < b[2] and a[1] < b[3] and a[2] > b[0] and a[3] > b[1]:
        return True
    else:
        return False


def delete_useless(obj_list):
    new_obj_list = []
    for obj in obj_list:
        if obj.state == USELESS:
            can.delete(obj.drawable)
            del obj
        else:
            new_obj_list.append(obj)
    return new_obj_list


count = 0
player_lives = 10
score = 0
lives_text = can.create_text(10, 10, anchor='nw', text='lives: '+str(player_lives),
                       font=('Consolas', 15))

score_text = can.create_text(150, 10, anchor='nw', text='score: '+str(score),
                       font=('Consolas', 15))

running = True

while running:
    # 更新玩家坦克的位置和底片
    player_tank.update_pos_img()

    # 更新敌方坦克的位置和底片
    for t in enemy_tanks:
        t.update_pos_img()
        if count % 20 == 0:
            enemy_bullets.append(t.create_bullet())

    # 更新敌方子弹的位置和状态
    for b in enemy_bullets:
        b.update_state()
        b.update_pos()
        if is_collide(b.get_pos(), player_tank.get_pos()):
            b.state = USELESS
            player_tank.state = EXPLODE

    # 更新玩家子弹的位置和状态
    for b in player_bullets:
        b.update_state()
        b.update_pos()
        for t in enemy_tanks:
            if is_collide(b.get_pos(), t.get_pos()):
                b.state = USELESS
                t.state = EXPLODE

    # 删除无用的图形元素: 超出窗口的子弹和被击中的坦克
    enemy_bullets = delete_useless(enemy_bullets)
    enemy_tanks = delete_useless(enemy_tanks)
    player_bullets = delete_useless(player_bullets)

    # 分数和生命数计算
    score = (E_TANK_NUM - len(enemy_tanks))*10

    if player_tank.state == USELESS:
        player_lives -= 1
        if player_lives > 0:
            player_tank.state = ACTIVE

    can.itemconfig(lives_text, text='lives: '+str(player_lives))
    can.itemconfig(score_text, text='score: '+str(score))

    # 判定游戏是否结束
    if player_tank.state == USELESS:
        can.create_text(WIN_WIDTH/2, WIN_HEIGHT/2,
                    text='YOU LOSE!\nscore:'+str(score),
                    font=('Lithos Pro Regular', 30))
        running = False

    if len(enemy_tanks) == 0:
        can.create_text(WIN_WIDTH / 2, WIN_HEIGHT / 2,
                        text='YOU WIN!\nscore:' + str(score),
                        font=('Lithos Pro Regular', 30))
        running = False

    count += 1
    can.update()
    time.sleep(0.1)

can.mainloop()