#-*- coding:utf-8 -*-
import pygame
import pygame._view
from pygame.locals import *
from sys import exit
#from Chessman import *

class chess(object):
    pygame.init()
    font = pygame.font.Font("simsun.ttc",32)
    def __init__(self,SCREEN_SIZE=(560,630)):
        #pygame.init()
        self.SCREEN_SIZE=SCREEN_SIZE
        x=SCREEN_SIZE[0]+60
        y=SCREEN_SIZE[1]+60
        self.screen = pygame.display.set_mode((x,y),0,32)
        pygame.display.set_caption('Chess')
        #self.background = pygame.image.load('sushiplate.jpg').convert()
        self.grid_dict = {}
        for x in range(9):
            for y in range(10):
                self.grid_dict[(x,y)] = self.grid(x,y)
        self.red_list = maninit(red)
        self.green_list = maninit(green)
        #self.man_list = self.red_list + self.green_list
        self.select_point = (-1,-1)
        self.select_man = None
        self.current_color = red
        self.background = pygame.image.load('back2.jpg').convert()
        self.update()
        
        #print 'end'
    def over(self,color):
        text = ''
        if color == red:
            text = u'红方'
        if color == green:
            text = u'蓝方'
        text_surface = chess.font.render(text+u'输',True,color)
        self.screen.blit(text_surface,(305,345))
        
    def update(self):
        self.screen.blit(self.background,(0,0))
        self.drawbackground(self.screen)
        self.drawcross(self.screen)
        self.drawmans()
        self.select(self.select_point[0],self.select_point[1])
    def get_mans(self):
        return self.red_list + self.green_list
    def grid(self,x,y):
        gridX=self.SCREEN_SIZE[0] * x / 8.0 + 30
        gridY=self.SCREEN_SIZE[1] * y / 9.0 + 30
        return (gridX,gridY)
    def find_grid(self,Mouse_x,Mouse_y):
        longth = 10000
        points_list = self.grid_dict.values()
        tmp_point = (0,0)
        for point in points_list:
            tmp = (Mouse_x-point[0])**2+(Mouse_y-point[1])**2
            if longth>= tmp:
                longth = tmp
                tmp_point = point
        if longth >= 35**2:
            return None
        i = points_list.index(tmp_point)
        return self.grid_dict.keys()[i]
    
    def select(self,gridX,gridY):
        #self.drawcross(self.screen,(gridX,gridY))
        if (gridX,gridY)==(-1,-1):
            return
        x,y = self.grid(gridX,gridY)
        color = red
        pygame.draw.lines(self.screen,color,False,[(x-35,y-35),(x-10,y-35)],3)
        pygame.draw.lines(self.screen,color,False,[(x+35,y-35),(x+10,y-35)],3)
        pygame.draw.lines(self.screen,color,False,[(x-35,y+35),(x-10,y+35)],3)
        pygame.draw.lines(self.screen,color,False,[(x+35,y+35),(x+10,y+35)],3)
        pygame.draw.lines(self.screen,color,False,[(x-35,y-35),(x-35,y-10)],3)
        pygame.draw.lines(self.screen,color,False,[(x+35,y-35),(x+35,y-10)],3)
        pygame.draw.lines(self.screen,color,False,[(x-35,y+35),(x-35,y+10)],3)
        pygame.draw.lines(self.screen,color,False,[(x+35,y+35),(x+35,y+10)],3)
        
    def drawcross(self,screen,extra_point=None):
        if extra_point == None:
            points =[]
            x=0
            while x<=8:
                points += [(x,3),(x,6)]
                x+=2
            points+=[(1,2),(1,7),(7,2),(7,7)]
            color = (0,0,0)
        else:
            points = [extra_point]
            color = (200,0,0)
        #color = (0,0,0)
        for point in points:
            #print type(point)
            x,y = self.grid(point[0],point[1])
            pygame.draw.lines(screen,color,False,[(x-30,y-10),(x-10,y-10)],3)
            pygame.draw.lines(screen,color,False,[(x+30,y-10),(x+10,y-10)],3)
            pygame.draw.lines(screen,color,False,[(x-30,y+10),(x-10,y+10)],3)
            pygame.draw.lines(screen,color,False,[(x+30,y+10),(x+10,y+10)],3)
            pygame.draw.lines(screen,color,False,[(x-10,y-30),(x-10,y-10)],3)
            pygame.draw.lines(screen,color,False,[(x+10,y-30),(x+10,y-10)],3)
            pygame.draw.lines(screen,color,False,[(x-10,y+30),(x-10,y+10)],3)
            pygame.draw.lines(screen,color,False,[(x+10,y+30),(x+10,y+10)],3)
        pygame.display.update()
        
    def drawbackground(self,screen):
        color = (0,0,0)
        x=y=0
        for y in range(10):
            points=[]
            points.append(self.grid(0,y))
            points.append(self.grid(8,y))
            pygame.draw.lines(screen,color,False,points,3)
        '''while y<=SCREEN_SIZE[1]:
            pygame.draw.lines(screen,color,False,[(x,y),(x+560,y)],3)
            y+=SCREEN_SIZE[1] / 9.0'''
            
        pygame.draw.lines(screen,color,False,[self.grid(0,0),self.grid(0,9)],3)
        pygame.draw.lines(screen,color,False,[self.grid(8,0),self.grid(8,9)],3)

        x=self.SCREEN_SIZE[0] / 8.0
        for x in range(9):
            pygame.draw.lines(screen,color,False,[self.grid(x,0),self.grid(x,4)],3)
            pygame.draw.lines(screen,color,False,[self.grid(x,5),self.grid(x,9)],3)
        '''while x<SCREEN_SIZE[0]:
            pygame.draw.lines(screen,color,False,[(x,0),(x,280)],3)
            pygame.draw.lines(screen,color,False,[(x,350),(x,630)],3)
            x+=SCREEN_SIZE[0] / 8.0'''
        pygame.draw.lines(screen,color,False,[self.grid(3,0),self.grid(5,2)],3)
        pygame.draw.lines(screen,color,False,[self.grid(3,2),self.grid(5,0)],3)
        pygame.draw.lines(screen,color,False,[self.grid(3,7),self.grid(5,9)],3)
        pygame.draw.lines(screen,color,False,[self.grid(3,9),self.grid(5,7)],3)
        pygame.display.update()
    def drawman(self,chess_man):
        text_surface = chess.font.render(chess_man.name,True,chess_man.color)
        a,b = chess_man.position
        #print '(a,b)=',a,b
        x,y = self.grid(a-1,b-1)
        x1 = int(x - text_surface.get_width() / 2)
        y1 = int(y - text_surface.get_height() / 2)

        #print x1,y1
        pygame.draw.circle(self.screen,(150,150,0),(int(x),int(y)),32,0)
        pygame.draw.circle(self.screen,(255,0,0),(int(x),int(y)),32,3)
        self.screen.blit(text_surface,(x1,y1))
        #print 'drawman'
        pygame.display.update()
    def drawmans(self):
        #red_list = self.red_list
        for red_man in self.red_list:
            self.drawman(red_man)
        #green_list = maninit(green)
        for green_man in self.green_list:
            self.drawman(green_man)
            
def run():
    #SCREEN_SIZE=(560,630)
    Chchess = chess()
    clock = pygame.time.Clock()
    mainloop = True
    over = False
    while mainloop:
        #time_passed = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            '''if event.type == VIDEORESIZE:
                SCREEN_SIZE = event.size
                Chchess.screen = pygame.display.set_mode(SCREEN_SIZE,RESIZABLE,32)
                pygame.display.set_caption("Window resized to "+str(event.size))
            screen_width,screen_height = SCREEN_SIZE
            Chchess.SCREEN_SIZE = SCREEN_SIZE
            #print 'for y in'''
            '''for y in range(0, screen_height,Chchess.background.get_height()):
               for x in range(0, screen_width,Chchess.background.get_width()):
                    Chchess.screen.blit(Chchess.background,(x, y))'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                #time_passed = clock.tick()
                Mouse_X,Mouse_Y = pygame.mouse.get_pos()
                #print '(Mouse_X,Mouse_Y)=',Mouse_X,Mouse_Y
                if Chchess.find_grid(Mouse_X,Mouse_Y)!=None:
                    x,y = Chchess.find_grid(Mouse_X,Mouse_Y)
                    if Chchess.select_man != None:
                        flag = Chchess.select_man.move(x,y,Chchess)
                        if flag == True:
                            if Chchess.current_color == red:
                                Chchess.current_color=green
                                #print 'green'
                            elif Chchess.current_color == green:
                                Chchess.current_color=red
                                #print 'red'
                            Chchess.select_point=(x,y)
                            for man in Chchess.get_mans():
                                if man.position == Chchess.select_man.position:
                                    if man.color != Chchess.select_man.color:
                                        man.disappear(Chchess)
                                        Chchess.update()
                                        if man.id == 5:
                                            Chchess.over(man.color)
                                            over = True
                            Chchess.select_man = None
                        else:
                            for man in Chchess.get_mans():
                                if (x+1,y+1)==man.position:
                                    if man.color == Chchess.current_color:
                                        Chchess.select_point=(x,y)
                                        Chchess.select_man = man
                    else:
                        for man in Chchess.get_mans():
                            if (x+1,y+1) == man.position:
                                if man.color == Chchess.current_color:
                                    Chchess.select_point = (x,y)
                                    Chchess.select_man = man
                    if not over:
                        Chchess.update()
            time_passed = clock.tick(100)
        pygame.display.update()
    pygame.quit()

red = (255,0,0)
green = (0,255,0)
#font = pygame.font.Font("simsun.ttc", 36)
#SCREEN_SIZE=(560,630)
name_id_list = [u'车',u'马',u'相',u'士',u'帅',u'士',u'相',u'马',
                u'车',u'炮',u'炮',u'兵',u'兵',u'兵',u'兵',u'兵']
name_id_list2 = [u'車',u'马',u'象',u'仕',u'将',u'仕',u'象',u'马',
                 u'車',u'炮',u'炮',u'卒',u'卒',u'卒',u'卒',u'卒']
#list = 
class chessman(object):
    #id = 0
    SCREEN_SIZE=(560,630)
    def __init__(self,name,color,chess_id):
        self.name = name
        self.color = color
        self.id = chess_id
        self.position = (0,0)
        #self.picture = pygame.image.load('back2.jpg').convert()
    def grid(self,x,y):
        gridX = chessman.SCREEN_SIZE[0] * x / 8.0 + 10
        gridY = chessman.SCREEN_SIZE[1] * y / 9.0 + 10
        return (gridX,gridY)
    def move(self,gridX,gridY):
        pass
    def disappear(self,Chchess):
        self.position = (-1,-1)
    def eat(self,chess_man):
        del chess_man

class che(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'车',color,chess_id)
        #self.color = color
        if self.color == red:
            if self.id == 1:
                self.position = (1,10)
            if self.id == 9:
                self.position = (9,10)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 1:
                self.position = (1,1)
            if self.id == 9:
                self.position = (9,1)
    def move(self,gridX,gridY,Chchess):
        destination = (gridX+1,gridY+1)
        hinder = get_hinder(self.position,destination,Chchess.get_mans())
        if hinder == 0:
            #print 'hinder = 0'
            if self.color == red:
                for man in Chchess.red_list:
                    if destination == man.position:
                        return False
            if self.color == green:
                for man in Chchess.green_list:
                    if destination == man.position:
                        return False
            self.position = destination
            return True
        else:
            return False
            
class ma(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'马',color,chess_id)
        if self.color == red:
            if self.id == 2:
                self.position = (2,10)
            if self.id == 8:
                self.position = (8,10)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 2:
                self.position = (2,1)
            if self.id == 8:
                self.position = (8,1)
    def move(self,gridX,gridY,Chchess):
        flag = False
        X,Y = gridX+1,gridY+1
        if self.color == red:
            for man in Chchess.red_list:
                if man.position == (X,Y):
                    return False
        if self.color == green:
            for man in Chchess.green_list:
                if man.position == (X,Y):
                    return False
        #destination = (gridX+1,gridY+1)
        #X,Y = gridX+1,gridY+1
        a,b = self.position[0],self.position[1]
        if self.position[0]==(X-1) and self.position[1]==(Y-2):
            if not judge_position((a,b+1),Chchess):
                flag = True
        elif self.position[0]==(X+1) and self.position[1]==(Y-2):
            if not judge_position((a,b+1),Chchess):
                flag = True
        elif self.position[0]==(X-2) and self.position[1]==(Y-1):
            if not judge_position((a+1,b),Chchess):
                flag = True
        elif self.position[0]==(X-2) and self.position[1]==(Y+1):
            if not judge_position((a+1,b),Chchess):
                flag = True
        elif self.position[0]==(X+2) and self.position[1]==(Y+1):
            if not judge_position((a-1,b),Chchess):
                flag = True
        elif self.position[0]==(X+2) and self.position[1]==(Y-1):
            if not judge_position((a-1,b),Chchess):
                flag = True
        elif self.position[0]==(X+1) and self.position[1]==(Y+2):
            if not judge_position((a,b-1),Chchess):
                flag = True
        elif self.position[0]==(X-1) and self.position[1]==(Y+2):
            if not judge_position((a,b-1),Chchess):
                flag = True

        if flag:
            self.position = (X,Y)
        return flag

class xiang(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'相',color,chess_id)
        if self.color == red:
            if self.id == 3:
                self.position = (3,10)
            if self.id == 7:
                self.position = (7,10)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 3:
                self.position = (3,1)
            if self.id == 7:
                self.position = (7,1)
    def move(self,gridX,gridY,Chchess):
        flag = False
        X,Y = gridX+1,gridY+1
        if self.color == red:
            for man in Chchess.red_list:
                if man.position == (X,Y):
                    return False
        if self.color == green:
            for man in Chchess.green_list:
                if man.position == (X,Y):
                    return False
        a,b = self.position[0],self.position[1]
        if self.position[0]==(X+2) and self.position[1]==(Y+2):
            if not judge_position((a-1,b-1),Chchess):
                flag = True
        elif self.position[0]==(X+2) and self.position[1]==(Y-2):
            if not judge_position((a-1,b+1),Chchess):
                flag = True
        elif self.position[0]==(X-2) and self.position[1]==(Y+2):
            if not judge_position((a+1,b-1),Chchess):
                flag = True
        elif self.position[0]==(X-2) and self.position[1]==(Y-2):
            if not judge_position((a+1,b+1),Chchess):
                flag = True
        if flag:
            self.position = (X,Y)
        return flag

class shi(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'士',color,chess_id)
        if self.color == red:
            if self.id == 4:
                self.position = (4,10)
            if self.id == 6:
                self.position = (6,10)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 4:
                self.position = (4,1)
            if self.id == 6:
                self.position = (6,1)
    def move(self,gridX,gridY,Chchess):
        flag = False
        X,Y = gridX+1,gridY+1
        #
        if self.color == red:
            for man in Chchess.red_list:
                if man.position == (X,Y):
                    return False
        if self.color == green:
            for man in Chchess.green_list:
                if man.position == (X,Y):
                    return False
        #
        if X>6 or X<4:
            return False
        if self.color == red:
            if Y<8:
                return False
        if self.color == green:
            if Y>3:
                return False
        #
        if self.position[0]==(X+1) and self.position[1]==(Y+1):
            flag = True
        elif self.position[0]==(X-1) and self.position[1]==(Y+1):
            flag = True
        elif self.position[0]==(X+1) and self.position[1]==(Y-1):
            flag = True
        elif self.position[0]==(X-1) and self.position[1]==(Y-1):
            flag = True

        if flag:
            self.position = (X,Y)
        return flag

class jiang(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'帅',color,chess_id=5)
        if self.color == red:
            self.position = (5,10)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            self.position = (5,1)
    def disappear(self,Chchess):
        self.position = (-1,-1)
        #Chchess.over(self.color)
    def move(self,gridX,gridY,Chchess):
        flag = False
        X,Y = gridX+1,gridY+1
        #
        if self.color == red:
            for man in Chchess.red_list:
                if man.position == (X,Y):
                    return False
        if self.color == green:
            for man in Chchess.green_list:
                if man.position == (X,Y):
                    return False
        #
        if X>6 or X<4:
            return False
        if self.color == red:
            if Y<8:
                return False
        if self.color == green:
            if Y>3:
                return False
        #
        if self.position[0]==(X) and self.position[1]==(Y+1):
            flag = True
        elif self.position[0]==(X) and self.position[1]==(Y-1):
            flag = True
        elif self.position[0]==(X+1) and self.position[1]==(Y):
            flag = True
        elif self.position[0]==(X-1) and self.position[1]==(Y):
            flag = True

        if flag:
            self.position = (X,Y)
        return flag

class pao(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'炮',color,chess_id)
        if self.color == red:
            if self.id == 10:
                self.position = (2,8)
            if self.id == 11:
                self.position = (8,8)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 10:
                self.position = (2,3)
            if self.id == 11:
                self.position = (8,3)
    def move(self,gridX,gridY,Chchess):
        destination = (gridX+1,gridY+1)
        hinder = get_hinder(self.position,destination,Chchess.get_mans())
        if hinder == 0:
            #print 'hinder = 0'
            if judge_position(destination,Chchess):
                return False
            self.position = destination
            return True
        elif hinder == 1:
            if judge_position(destination,Chchess):
                color = judge_position(destination,Chchess)
                if color != self.color:
                    self.position = destination
                    return True
        else:
            return False

class bing(chessman):
    def __init__(self,color,chess_id):
        chessman.__init__(self,u'兵',color,chess_id)
        if self.color == red:
            if self.id == 12:
                self.position = (1,7)
            if self.id == 13:
                self.position = (3,7)
            if self.id == 14:
                self.position = (5,7)
            if self.id == 15:
                self.position = (7,7)
            if self.id == 16:
                self.position = (9,7)
        if self.color == green:
            self.name = name_id_list2[self.id-1]
            if self.id == 12:
                self.position = (1,4)
            if self.id == 13:
                self.position = (3,4)
            if self.id == 14:
                self.position = (5,4)
            if self.id == 15:
                self.position = (7,4)
            if self.id == 16:
                self.position = (9,4)
    def move(self,gridX,gridY,Chchess):
        flag = False
        if self.color == red:
            if self.position[0]==(gridX+1):
                if self.position[1]==(gridY+2):
                    self.position = (gridX+1,gridY+1)
                    flag = True
            if self.position[1]<=5:
                if self.position[1]==(gridY+1):
                    if self.position[0]==gridX or self.position[0]==(gridX+2):
                        self.position = (gridX+1,gridY+1)
                        flag = True
        if self.color == green:
            if self.position[0]==(gridX+1):
                if self.position[1]==gridY:
                    self.position = (gridX+1,gridY+1)
                    flag = True
            if self.position[1]>=6:
                if self.position[1]==(gridY+1):
                    if self.position[0]==gridX or self.position[0]==(gridX+2):
                        self.position = (gridX+1,gridY+1)
                        flag = True
        #if flag:
            #print self.position
        return flag

def maninit(color):
    man_list = []
    man_list.append(che(color,1))
    man_list.append(che(color,9))
    man_list.append(ma(color,2))
    man_list.append(ma(color,8))
    man_list.append(xiang(color,3))
    man_list.append(xiang(color,7))
    man_list.append(shi(color,4))
    man_list.append(shi(color,6))
    man_list.append(jiang(color,5))
    man_list.append(pao(color,10))
    man_list.append(pao(color,11))
    man_list.append(bing(color,12))
    man_list.append(bing(color,13))
    man_list.append(bing(color,14))
    man_list.append(bing(color,15))
    man_list.append(bing(color,16))
    return man_list
def get_hinder(position1,position2,man_list):
    hinder = 0
    if position1[0]==position2[0]:
        for man in man_list:
            position_ = man.position
            if man.position[0]==position1[0]:
                if position1[1]<position_[1]<position2[1]:
                    hinder += 1
                    #print position1,position_,position2
                if position2[1]<position_[1]<position1[1]:
                    hinder += 1
                    #print position1,position_,position2
        return hinder
    elif position1[1]==position2[1]:
        for man in man_list:
            position_ = man.position
            if man.position[1]==position1[1]:
                if position1[0]<position_[0]<position2[0]:
                    hinder += 1
                    #print position1,position_,position2
                if position2[0]<position_[0]<position1[0]:
                    hinder += 1
                    #print position1,position_,position2
        return hinder
    else:
        return -1
        
def judge_position(position,Chchess):
    #print 'judge'
    for man in Chchess.get_mans():
        if man.position == position:
            return man.color
    return False


if __name__ == '__main__':
    run()
