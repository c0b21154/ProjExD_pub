import pygame as py
import sys
from pygame.locals import *
import tkinter as tk  #いらない
import os             #いらない
from random import randint, randrange
import time

class BG:
  def __init__(self, surface):
    # Surfaceクラスのインスタンス
    self.surf = surface
    # 背景の四角形
    self.max_obj = 500
    # 画面の横幅
    self.width = surface.get_width()
    # 画面の縦幅
    self.height = surface.get_height()
    # 四角形のx座標の位置をランダムに設定。リストで管理
    self.x = [randrange(-self.width, 2 * self.width) for i in range(self.max_obj)]
    # 四角形のy座標の位置をランダムに設定。リストで管理
    self.y = [randrange(-self.height, 2 * self.height) for i in range(self.max_obj)]
    # 四角形の大きさ
    self.side = [randint(2, 5) for i in range(self.max_obj)]
    # 移動スピード
    self.speed = [randint(1, 4) for i in range(self.max_obj)]
    # 色をランダムに設定
    self.color = [(randrange(255), randrange(255), randrange(255)) for i in range(self.max_obj)]

  def draw(self, direction):
    # snakeの移動方向と逆方向に背景の四角形も動かす。スピードのスカラ値（スピードの大きさ）を移動方向に足す・引いて動かす
    if direction == "l":
      self.x = [x + r for x, r in zip(self.x, self.speed)]
    elif direction == "r":
      self.x = [x - r for x, r in zip(self.x, self.speed)]
    elif direction == "u":
      self.y = [y + r for y, r in zip(self.y, self.speed)]
    elif direction == "d":
      self.y = [y - r for y, r in zip(self.y, self.speed)]

    # 四角形を描画（チカチカさせる）
    [py.draw.rect(self.surf, self.color[i], (self.x[i], self.y[i], self.side[i], self.side[i])) if i % 5 else py.draw.rect(self.surf, (randrange(255), randrange(255), randrange(255)),(self.x[i], self.y[i], self.side[i], self.side[i])) for i in range(self.max_obj)]


class Snake:
  # snakeの色
  COLOR = [0, 170, 0]
  # snakeの長辺の長さ
  SIDE = 15
  # snakeの長さ
  lenght = 2
  # snakeの移動速度（velocity）
  vel = 10

  def __init__(self, surface):
    # Surfaceクラスのインスタンス
    self.surface = surface
    # 画面の横幅の整数値（//は割った商の整数）
    self.x = surface.get_width() // 2
    # 画面の縦幅の整数値（//は割った商の整数）
    self.y = surface.get_height() // 4
    # 画面の縦横のタプルをリストに入れる
    self.XY = [(self.x, self.y)]
    # 移動方向、l=左、r=右、d=下、u=上
    self.direction = "d"

  def add_lenght(self):
    # 1長くする
    self.lenght += 1
    # 長辺の長さを1長くする
    self.SIDE += 1
    # RGBのGを濃くする
    self.COLOR[1] += 1
    # RGBのGの最大値は255、min関数は2つのうちに小さい方を選ぶ
    self.COLOR[1] = min(self.COLOR[1], 255)

  def get_snake(self):
    self.XY += [(self.x, self.y)]
    self.XY = self.XY[-self.lenght:]
    # snakeの体をブロックごとに描画
    for kx, ky in self.XY:
      py.draw.rect(self.surface, self.COLOR, (kx, ky , self.SIDE, self.SIDE))

  def move_snake(self, key):
    # 左へ操作
    if key == "l":
      # 左方向へ速度を加算
      self.x -= self.vel
      self.get_snake()
    # 右へ操作
    if key == "r":
      # 右方向へ速度を加算
      self.x += self.vel
      self.get_snake()
    # 下へ操作
    if key == "u":
      # 下方向へ速度を加算
      self.y -= self.vel
      self.get_snake()
    # 上へ操作
    if key == "d":
      # 上方向へ速度を加算
      self.y += self.vel
      self.get_snake()


class Effect:
  # 破片の大きさ
  RANGE = 30
  # 破片の数
  NUMBER = 15
  # 色
  color = 0
  list_effects = []
  directions = []
  sizes = []

  def __init__(self, surf):
    # Surfaceクラスのインスタンス
    self.surf = surf

  def run(self, trigger, x, y):
    # effectトリガーがTrueなら以下を実行
    if trigger:
      self.color = 200
      # effectの破片それぞれの座標をランダムで設定してリストに入れる
      self.list_effects = [(randint(x - self.RANGE + 12, x + self.RANGE + 12),
      randint(y - self.RANGE + 12, y + self.RANGE - 12))
      for i in range(self.NUMBER)]
      # 破片の速度ベクトルをランダムに設定。リストで管理
      self.directions = [(randint(-1, 1), randint(-1, 1)) for i in range(self.NUMBER)]
      # 破片の大きさをランダムで設定。リストで管理
      self.sizes = [(randint(1, 7), randint(1, 7)) for i in range(self.NUMBER)]

    # 破片を描画
    for i, xy in enumerate(self.list_effects):
      py.draw.rect(self.surf, (max(self.color, 120), 0, 0), (*xy, *self.sizes[i]))

    # 速度ベクトルの方向へ破片を動かす
    self.list_effects = [(xy[0] - d[0], xy[1] - d[1]) for xy, d in zip(self.list_effects, self.directions)]

    # 破片を黒にして見えなくする
    self.color -= 3


class Enemy:
  COLOR=(139,0,0)
  SIDE=20

  def __init__(self, surface):
   # Surfaceクラスのインスタンス
      self.surface = surface
    # foodのx座標
      self.x = randint(0,1000)
    # foodのy座標
      self.y = randint(0,600)
    # x座標の集合
      self.set_x = set()
    # y座標の集合
      self.set_y = set()
  def add_enemy(self):
    # enemyを描画
    py.draw.rect(self.surface, self.COLOR, (self.x, self.y, self.SIDE, self.SIDE))
    # enemyのx軸方向の領域。setで管理
    self.set_x = set(range(self.x, self.x + self.SIDE + 1))
    # enemyのy軸方向の領域。setで管理
    self.set_y = set(range(self.y, self.y + self.SIDE))

  def new_enemyxy(self, snake_side):
    self.x = randint(snake_side, self.surface.get_width() - snake_side)
    self.y = randint(snake_side, self.surface.get_height() - snake_side)

  def is_attacked(self, snake_x, snake_y, snake_side):
    # snakeの座標をset（集合）で管理。foodとのset（集合）とで共通集合があれば当たったと判定
    if set(range(snake_x, snake_x + snake_side + 1)) & self.set_x and set(range(snake_y, snake_y + snake_side + 1)) & self.set_y:
      return True
    return False


class Food:
  # RGBで色を設定
  COLOR = (255, 0, 0)
  # 大きさ
  SIDE = 20

  def __init__(self, surface):
    # Surfaceクラスのインスタンス
    self.surface = surface
    # foodのx座標
    self.x = randint(0,1000)
    # foodのy座標
    self.y = randint(0,600)
    # x座標の集合
    self.set_x = set()
    # y座標の集合
    self.set_y = set()

  def add_food(self):
    # foodを描画
    py.draw.rect(self.surface, self.COLOR, (self.x, self.y, self.SIDE, self.SIDE))
    # foodのx軸方向の領域。setで管理
    self.set_x = set(range(self.x, self.x + self.SIDE + 1))
    # foodのy軸方向の領域。setで管理
    self.set_y = set(range(self.y, self.y + self.SIDE))

  def new_foodxy(self, snake_side):
    self.x = randint(snake_side, self.surface.get_width() - snake_side)
    self.y = randint(snake_side, self.surface.get_height() - snake_side)

  def is_eaten(self, snake_x, snake_y, snake_side):
    if set(range(snake_x, snake_x + snake_side + 1)) & self.set_x and set(range(snake_y, snake_y + snake_side + 1)) & self.set_y:
      return True
    return False

    
class Game:
  SIZE = WIDTH, HEIGHT = (1000,600)
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  fps = 20
  score = 0

  def __init__(self): 
    py.init()
    py.display.set_caption("Snake Game")    
    # 画像を描写するために使用するSurfaceクラスからインスタンスを生成
    self.surf = py.display.set_mode(self.SIZE)
    # 時間の設定
    self.clock = py.time.Clock()
    # 背景のインスタンスを生成
    self.bg = BG(self.surf)
    # effectのインスタンスを生成
    self.effect = Effect(self.surf)
    # effectのトリガー変数
    self.effect_trigger = False
    # snakeのインスタンスを生成
    self.snake = Snake(self.surf)
    # foodのインスタンスを生成
    self.food = Food(self.surf)
    # enemyのインスタンスを作成
    self.enemy =Enemy(self.surf)
    # スコア表示のフォント
    self.font_score = py.font.Font(None, 22)
    # 終了表示のフォント
    self.font_end = py.font.Font(None, 48)
    # ボタンのフォント
    self.font_button = py.font.Font(None, 30)   
    # play関数を実行
    self.play()

  def play(self):
    """
    キー操作
    enemyに当たったときの処理
    foodを食べた時の処理
    ゲームオーバー判定
    """
    while True:
      self.surf.blit(self.font_score.render(f'SCORE:{self.score}', 1 , (255, 165, 0)), (self.WIDTH - -90, 5))
      py.display.update()
      # 終了コマンドを設定
      for event in py.event.get():
            if event.type == py.QUIT: return
      keys = py.key.get_pressed()
      # 左を押した
      if keys[K_LEFT]:
        if self.snake.direction != "r":
          self.snake.direction = "l"
      # 右を押した
      elif keys[K_RIGHT]:
        if self.snake.direction != "l":
          self.snake.direction = "r"
      # 上を押した
      elif keys[K_UP]:
        if self.snake.direction != "d":
          self.snake.direction = "u"
      # 下を押した
      elif keys[K_DOWN]:
        if self.snake.direction != "u":
          self.snake.direction = "d"

      # foodがsnakeに食べられた
      if self.food.is_eaten(self.snake.x, self.snake.y, self.snake.SIDE):       
        # snakeの長さが伸びる
        self.snake.add_lenght()
        # effectのトリガーがTrue
        self.effect_trigger = True
        # 新しいfoodを配置
        self.food.new_foodxy(self.snake.SIDE)
        #新しいenemyの追加
        self.enemy.new_enemyxy(self.snake.SIDE)
        # スコアを加算
        self.score += 1
        # fpsの増加
        self.fps += 1

      if  self.enemy.is_attacked(self.snake.x, self.snake.y, self.snake.SIDE):
        #新しいfoodの追加
        self.food.new_foodxy(self.snake.SIDE)
        #新しいenemyの追加
        self.enemy.new_enemyxy(self.snake.SIDE)
        #スコアの減少
        self.score -= 1
        #fpsの減少
        self.fps -= 1
        #enemyに当たったことが分かるように遅延させる
        time.sleep(0.2)
      # snakeが画面外に出たらゲームオーバー
      if(self.snake.x < 0 or self.snake.y < 0 or self.snake.x + self.snake.SIDE > self.WIDTH or self.snake.y + self.snake.SIDE > self.HEIGHT) or len(self.snake.XY) != len(set(self.snake.XY)):
        self.game_over()
      self.draw()

  def draw(self):
    self.surf.fill(self.BLACK)
    # スコア表示
    self.surf.blit(self.font_score.render(f'SCORE:{self.score}', 1 , (255, 165, 0)), (self.WIDTH - -90, 5))

    # 背景を描画
    self.bg.draw(self.snake.direction)
    # foodを描画
    self.food.add_food()
    # enemyを描画
    self.enemy.add_enemy()
    # snakeの移動を描画
    self.snake.move_snake(self.snake.direction)
    # effectを実行
    self.effect.run(self.effect_trigger, self.snake.x, self.snake.y)
    # effectトリガーをFalse
    self.effect_trigger = False    
    py.display.update()
    # fpsを更新
    self.clock.tick(self.fps)

  def game_over(self):
    while True:
      # スコアの結果を表示
      self.surf.blit(self.font_end.render(f'YOUR SCORE:{self.score}', 1, (255, 165, 0)), (self.WIDTH // 2 -130, self.HEIGHT // 3))
      # mouseのポインタ位置
      mouse_coord = py.mouse.get_pos()
      # mouseのクリックイベント
      mouse_events = py.mouse.get_pressed()
      # RETRYボタンにマウスホバーすると色が変わる
      if self.WIDTH // 2 - 50 < mouse_coord[0] < self.WIDTH // 2 + 50 and \
        self.HEIGHT // 2 - 50 < mouse_coord[1] < self.HEIGHT // 2 -10:
        # 緑の長方形を描画
        py.draw.rect(self.surf, self.GREEN, (self.WIDTH // 2 - 50, self.HEIGHT // 2 - 50, 100,40))
        if mouse_events[0]:
          # RETRYボタン領域をクリック
          break
      else:
        # 赤の長方形を描画
        py.draw.rect(self.surf, self.RED, (self.WIDTH // 2 -50, self.HEIGHT // 2 - 50, 100, 40))
      # RETRYの文字表示
      self.surf.blit(self.font_button.render("RETRY", 1, self.BLACK), (self.WIDTH // 2 - 33, self.HEIGHT // 2 - 40))
      self.clock.tick(self.fps)
      py.display.update()

      # 終了コマンド
      for event in py.event.get():
        if event.type == QUIT:
          py.quit()
          sys.exit()
    Game()

if __name__ == "__main__":
  Game()
