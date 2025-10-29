# DAY58 GHOST TYPING2
# 音をつけた。ghostのスピードアップ。ダブルのときはポイント加算。
# 昨日はtrusumemorygameとsubmarineをgithubに上げるのをやった。trush・・・の方は修正が必要だった 

# テルミンアゲイン
# 音ゲーの指5本バージョンとか、違う曲とか。

# 雪合戦。敵がいるやつ

# 敵も動くようなゲームを。
# 敵はサメ？ある程度近づくと、スピードアップして寄ってくるとか。

import pyxel
from enum import Enum
import random

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
FPS = 20
PLAYER_XCENTER = SCREEN_WIDTH/2
PLAYER_YCENTER = SCREEN_HEIGHT/2

# キーのディクショナリ　{pyxel.KEY_A :"a", pyxel.KEY_B : "b", pyxel.KEY_C : "c", ...
KEY_DICT = dict(zip(list(range(97, 97+26+1)), [chr(ord("a")+ x) for x in range(26)]))

class Status(Enum):
    START = 1
    MAIN = 2
    END = 3
    
class Ghost():
    def __init__(self, x, y, word, gametime):
        self.x = x
        self.y = y

        rad = pyxel.atan2(PLAYER_YCENTER - (y+8), PLAYER_XCENTER - (x+8))
        v_sec = (gametime//FPS)//10
        base_v = PLAYER_XCENTER / (FPS*(8-v_sec))
        self.vx = base_v * pyxel.cos(rad)
        self.vy = base_v * pyxel.sin(rad)
        self.word = word
        self.original_word = word
        self.finished_word = ""
        self.is_alive = True
        self.countdown = FPS//2 # 倒された後、消えるまでのカウントダウン
        
    def update(self, input_char):
        if not self.is_alive:
            self.countdown -= 1
            return 0
            
        self.x += self.vx
        self.y += self.vy

        if self.x > 0 and self.x < SCREEN_WIDTH -8 and self.y >0 and self.y < SCREEN_HEIGHT-8 and len(self.word) > 0 and self.word[0] == input_char:
            self.word = self.word[1:]
            self.finished_word = self.finished_word + input_char
            return 1 # 消せたら1を返す

        return 0
        
    
class App():
    def __init__(self):
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT, fps = FPS)
        pyxel.load("./img/ghost_typing.pyxres")
        
        self.player_x = PLAYER_XCENTER - 8
        self.player_y = PLAYER_YCENTER - 8
        self.status = Status.START
        self.point = 0
        self.life = 3

        self.word_list = ["bird","cat","dog","monkey","snake","rabbit","gorilla","ant","shark","fish","mouse",
                          "man","horse","hippo","elephant","aligator","tiger","koala","pig","kangaloo","bug"]
        random.shuffle(self.word_list)
        pyxel.run(self.update, self.draw)

    def append_new_ghost(self):
        word = self.word_list.pop(0)
        self.word_list.append(word)
        self.ghosts.append(Ghost(-16 if self.next_ghost_isleft else SCREEN_WIDTH, pyxel.rndi(5, SCREEN_WIDTH-26), word, self.gametime))
        self.next_ghost_isleft = not self.next_ghost_isleft
        
    def update(self):
        if self.status == Status.START:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.point = 0
                self.life = 3
                self.status = Status.MAIN
                self.gametime = 0
                self.ghosts = [Ghost(0, 30, "banana",self.gametime), Ghost(SCREEN_WIDTH*4/3, 70, "bee",self.gametime)]
                self.next_ghost_isleft = True
                self.input_line = ""
                
        elif self.status == Status.MAIN:
            # chcek GAMEOVER
            if self.life < 1:
                self.status = Status.END
                return

            self.gametime += 1
            char = None
            for key in KEY_DICT:
                if pyxel.btnp(key):
#                    print(KEY_DICT[key])
                    pyxel.play(1, 1)
                    char = KEY_DICT[key]
                    self.input_line += char
                    break

            # update ghosts
            ghost_num = len(self.ghosts)
            idx = 0
            num = 0 # 一度に消せた文字数
            while ghost_num > 0 and idx < ghost_num:
                ghost = self.ghosts[idx]
                num += ghost.update(char) #消せたら加算される

                if ghost.countdown < 1:
                    del self.ghosts[idx]
                    ghost_num -= 1
                    self.append_new_ghost()
                    continue
        

                elif ghost.is_alive and (ghost.x +8 - PLAYER_XCENTER)**2 + (ghost.y + 8 - PLAYER_YCENTER)**2 <= 64:
                    self.life -= 1
                    pyxel.play(2, 2)
          
                    del self.ghosts[idx]
                    ghost_num -= 1
                    self.append_new_ghost()
                    continue

                elif ghost.is_alive and len(ghost.word) == 0:
                    self.point += len(ghost.original_word)*10
                    ghost.is_alive = False
                    pyxel.play(0, 0)

                idx += 1

            if num > 1:
                # ボーナスポイント
                self.point += 10*num
                
        elif self.status == Status.END:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.status = Status.START
            
    def draw(self):
        pyxel.cls(0)

        if self.status == Status.START:
            pyxel.text(10,20, "GHOST TYPING \n press ENTER to start", pyxel.frame_count%16)

            # draw player
            pyxel.blt(self.player_x, self.player_y, 0,  0,0, 16,16, 15)

        elif self.status == Status.MAIN:
            # draw player
            pyxel.blt(self.player_x, self.player_y, 0,  0,0 if len(self.input_line)%2 == 0 else 16, 16,16, 15)

            # draw ghosts
            for ghost in self.ghosts:
                if ghost.is_alive:
                    pyxel.blt(ghost.x, ghost.y, 0, 16,0 if ghost.vx < 0 else 16, 16,16, 15)
                    pyxel.text(ghost.x, ghost.y-6, ghost.original_word, 8) 
                    pyxel.text(ghost.x, ghost.y-6, ghost.finished_word, 15) 
                else:
                    pyxel.blt(ghost.x, ghost.y, 0, 16,32, 16,16, 15)

            # draw input lines
            pyxel.rect(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, SCREEN_HEIGHT, 8)
            pyxel.text(5, SCREEN_HEIGHT-7, "INPUT:", 0 if pyxel.frame_count%FPS < 3 else 7)
            pyxel.text(30, SCREEN_HEIGHT-7, (self.input_line+"_")[-30:], 7)

            pyxel.text(60,5, f"POINT:{self.point:>4}", 2)
            pyxel.text(110,5, f"LIFE:{self.life:>2}", 2)
            
        elif self.status == Status.END:
            pyxel.text(60,50, "GAME OVER", pyxel.frame_count%16)

            pyxel.text(60,70, f"POINT:{self.point:>4}", 2)
            pyxel.text(59,70, f"POINT:{self.point:>4}", 7)

App()

