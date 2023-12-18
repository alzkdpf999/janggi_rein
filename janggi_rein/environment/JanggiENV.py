# 장기 움직임과 보드 그리는 장소
import gym
import numpy as np
from gym import spaces
import os
import copy

import pygame as p
import random

WIDTH, HEIGHT = 640, 640
ROW, COLUMN = 40, 40
SIZE = 60
FPS = 60
IMAGE = {}

# 기물 점수
reward ={ "Zol" : 2,"Cha": 13, "Po": 7 , "Ma" : 5, "Sang" : 3, "Sa" : 3, "King" : 100}

class JanggiEnv(gym.Env):
    """
    처음 보드 만드는 함수, 장기 포진법에 따라 다르게 배치해야함
    my_setting은 초 진영(푸른색) opponent_setting 한 진영(붉은색)
    0 = 상마상마 
    1 = 마상마상
    2 = 마상상마
    3 = 상마마상
    """
    def __init__(self,my_setting,opponent_setting):
        self.board = np.array([["RCha","--","--","RSa","--","RSa","--","--","RCha"],
                     ["--","--","--","--","RKing","--","--","--","--"],
                     ["--","RPo","--","--","--","--","--","RPo","--"],
                     ["RZol","--","RZol","--","RZol","--","RZol","--","RZol"],
                     ["--","--","--","--","--","--","--","--","--"],
                     ["--","--","--","--","--","--","--","--","--"],
                     ["GZol","--","GZol","--","GZol","--","GZol","--","GZol"],
                     ["--","GPo","--","--","--","--","--","GPo","--"],
                     ["--","--","--","--","GKing","--","--","--","--"],
                     ["GCha","--","--","GSa","--","GSa","--","--","GCha"]])
        if(opponent_setting == 0):
            self.board[0,1] = "RSang"
            self.board[0,2] = "RMa"
            self.board[0,6] = "RSang"
            self.board[0,7] = "RMa"
        elif(opponent_setting == 1):
            self.board[0,1] = "RMa"
            self.board[0,2] = "RSang"
            self.board[0,6] = "RMa"
            self.board[0,7] = "RSang"
        elif(opponent_setting == 2):
            self.board[0,1] = "RMa"
            self.board[0,2] = "RSang"
            self.board[0,6] = "RSang"
            self.board[0,7] = "RMa"
        else:
            self.board[0,1] = "RSang"
            self.board[0,2] = "RMa"
            self.board[0,6] = "RMa"
            self.board[0,7] = "RSang"
        if(my_setting == 0):
            self.board[9,1] = "GSang"
            self.board[9,2] = "GMa"
            self.board[9,6] = "GSang"
            self.board[9,7] = "GMa"
        elif(my_setting == 1):
            self.board[9,1] = "GMa"
            self.board[9,2] = "GSang"
            self.board[9,6] = "GMa"
            self.board[9,7] = "GSang"
        elif(my_setting == 2):
            self.board[9,1] = "GMa"
            self.board[9,2] = "GSang"
            self.board[9,6] = "GSang"
            self.board[9,7] = "GMa"
        else:
            self.board[9,1] = "GSang"
            self.board[9,2] = "GMa"
            self.board[9,6] = "GMa"
            self.board[9,7] = "GSang"    

        # 초나라  진영 먼저 움직여야 한다.
        self.cho = True 

        self.done = False
        # 임시로 설정
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Discrete(100)
        p.init()
        p.display.set_caption("JangGi")
        self.display = p.display.set_mode((WIDTH,HEIGHT))
        self.bigJangCheck = 0
        self.current_board = copy.deepcopy(self.board)
        self.initial_board = copy.deepcopy(self.board)
        self.board_shape = self.initial_board.shape
        self.jangImg()
        self.makeBoard()
        
    def reset(self):
        self.possibleMove =[]
        self.cho = True
        self.done = False
        p.init()
        self.bigJangCheck = 0
        p.display.set_caption("JangGi")
        self.display = p.display.set_mode((WIDTH,HEIGHT))
        self.clock = p.time.Clock()
        self.current_board = copy.deepcopy(self.initial_board)
        self.makePiece()
        self.makeBoard()
        return self.current_board

    # 뷰로 보여주기
    def render(self):
        self.display.fill("#d7c38a")
        self.makeBoard()
        self.makePiece()
        p.display.update()
        self.clock.tick(FPS)

    # a= np.where(np.char.find(test, "G") != -1)
    #  b = np.stack((a[0],a[1]),axis=1)  이거 체크함수 이거 써야함 일단 임시로

    # 장기말 이미지 불러오기
    def jangImg(self):
        pieces = ["GSa","GSang","GMa","GKing","GZol","GCha","GPo","RSa","RSang","RMa","RKing","RZol","RCha","RPo"]
        for piece in pieces:
            IMAGE[piece] = p.transform.scale(p.image.load(f"{os.getcwd()}/environment/image/" + piece + ".png"),(SIZE,SIZE))

    # 보드 그리기
    def makeBoard(self):
        for i in range(0,9):
            for j in range(0,8):
                p.draw.rect(self.display,(0,0,0),p.Rect(j*SIZE+40,i*SIZE+40,60,60),width= 1)
        p.draw.line(self.display,(0,0,0), [220,40],[340,160],2)
        p.draw.line(self.display,(0,0,0), [340,40],[220,160],2)
        p.draw.line(self.display,(0,0,0), [220,460],[340,580],2)
        p.draw.line(self.display,(0,0,0), [340,460],[220,580],2)

    #  장기말 이미지 넣기
    def makePiece(self):
        for i in range(0,10):
            for j in range(0,9):
                piece = self.current_board[i,j]
                if piece != "--":
                    self.display.blit(IMAGE[piece],p.Rect(j*SIZE+10,i*SIZE+10,SIZE,SIZE))
        return self.current_board
    
    def close(self):
        p.quit()
    
    def move(self):
        if self.cho:
            turn = np.where(np.char.find(self.current_board, "G") != -1)
        else:
            turn = np.where(np.char.find(self.current_board, "R") != -1)
        turn = np.array(np.stack((turn[0],turn[1]),axis=1))

        for i,j in turn:
            clickPiece = self.current_board[i,j]
            if clickPiece[1:] == "Zol" :
                self.zolMove(i,j)
            elif clickPiece[1:] == "Ma" :
                self.maMove(i,j)
            elif clickPiece[1:] == "Sang" :
                self.sangMove(i,j)
            elif clickPiece[1:] == "King" or clickPiece[1:] == "Sa":
                self.gungSaMove(i,j)
            elif clickPiece[1:] == "Cha" :
                self.chaMove(i,j)
            elif clickPiece[1:] == "Po":
                self.poMove(i,j)
        return self.possibleMove

    # 졸병의 움직임
    def zolMove(self,startX,startY):
        board = self.current_board 
        if self.cho: # 초나라 먼저 하는
            # 왼쪽 이동, 상대 말이 있거나 비어있으면
            if not startY - 1 < 0 and board[startX,startY - 1][0] != "G":
                self.possibleMove.append((startX,startY - 1,startX,startY,self.getReward(board[startX,startY - 1][1:])))
            # 오른쪽 이동, 상대 말이 있거나 비어있으면 
            if not startY + 1 > 8 and board[startX,startY + 1][0] != "G":
                self.possibleMove.append((startX,startY +1,startX,startY,self.getReward(board[startX,startY + 1][1:])))
            # 위로 이동, 상대 말이 있거나 비어있으면
            if not startX - 1 < 0 and board[startX - 1,startY][0] != "G":
                if not (startX - 1 < 0):
                    self.possibleMove.append((startX - 1,startY,startX,startY,self.getReward(board[startX-1,startY][1:])))
            
            # 왼쪽 궁귀 부분
            if (startX == 2 and startY == 3) and board[startX - 1,startY][0] != "G":
                self.possibleMove.append((startX - 1,startY+1,startX,startY,self.getReward(board[startX-1,startY+1][1:])))
            # 오른쪽 궁귀부분
            if (startX == 2 and startY == 5) and board[startX - 1,startY][0] != "G":
                self.possibleMove.append((startX - 1,startY-1,startX,startY,self.getReward(board[startX-1,startY-1][1:])))
            # 궁 위치 부분
            if (startX == 1 and startY == 4):
                if board[startX - 1,startY+1][0] != "G":
                    self.possibleMove.append((startX - 1,startY+1,startX,startY,self.getReward(board[startX-1,startY+1][1:])))
                if board[startX - 1,startY-1][0] != "G":
                    self.possibleMove.append((startX - 1,startY-1,startX,startY,self.getReward(board[startX-1,startY-1][1:])))
        elif not self.cho: # 한나라 기준으로 

            # 왼쪽 이동, 상대 말이 있거나 비어있으면
            if not startY - 1 < 0 and board[startX,startY - 1][0] != "R":
                self.possibleMove.append((startX,startY - 1,startX,startY,self.getReward(board[startX,startY - 1][1:])))
            # 오른쪽 이동, 상대 말이 있거나 비어있으면
            if not startY + 1 > 8 and board[startX,startY + 1][0] != "R":
                self.possibleMove.append((startX,startY +1,startX,startY,self.getReward(board[startX,startY + 1][1:])))
            # 아래로 이동, 상대 말이 있거나 비어있으면
            if not startX + 1 > 9 and board[startX + 1,startY][0] != "R":
                self.possibleMove.append((startX + 1,startY,startX,startY,self.getReward(board[startX+1,startY][1:])))
            # 왼쪽 궁귀 부분 
            if (startX == 7 and startY == 3) and board[startX + 1,startY + 1][0] != "R":
                self.possibleMove.append((startX + 1,startY+1,startX,startY,self.getReward(board[startX+1,startY+1][1:])))
            # 오른쪽 궁귀부분
            if (startX == 7 and startY == 5) and board[startX + 1,startY - 1][0] != "R":
                self.possibleMove.append((startX + 1,startY-1,startX,startY,self.getReward(board[startX+1,startY-1][1:])))
            # 궁부분
            if (startX == 8 and startY == 4):
                if board[startX + 1,startY+1][0] != "R":
                    self.possibleMove.append((startX + 1,startY+1,startX,startY,self.getReward(board[startX+1,startY+1][1:])))
                if board[startX + 1,startY-1][0] != "R":
                    self.possibleMove.append((startX + 1,startY-1,startX,startY,self.getReward(board[startX+1,startY-1][1:])))
        
    
    # 말의 움직임
    def maMove(self,startX,startY):
        board = self.current_board 
        moving = ((-2,-1), (2,-1), (2,1), (-2,1), (-1,2), (-1,-2), (1,2), (1,-2))
        color = "G" if self.cho else "R"
        for i in moving:
            newX = startX + i[0]
            newY = startY + i[1]
            if 0 <= newX <= 9 and  0 <= newY <= 8 :
                newPiece = board[newX,newY]
                checkX = startX + int(i[0] / 2)
                checkY = startY + int(i[1] /2)
                if 0 <= checkX <= 9 and  0 <= checkY <= 8 :
                    if board[checkX , checkY] =="--":
                        if newPiece[0] != color:
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))

    # 상의 움직임
    def sangMove(self,startX,startY):
        board = self.current_board 
        moving = ((-3,-2), (3,-2), (3,2), (-3,2), (-2,3), (-2,-3), (2,3), (2,-3))
        color = "G" if self.cho else "R"
        for i in moving:
            newX = startX + i[0]
            newY = startY + i[1]
            if 0 <= newX <= 9 and  0 <= newY <= 8 :
                newPiece = board[newX,newY]
                checkX = startX + int(i[0] / 3)
                checkY = startY + int(i[1] /3)
                if 0 <= checkX <= 9 and  0 <= checkY <= 8  and board[checkX , checkY] =="--":
                    checkX = checkX + int(i[0] / 2)
                    checkY = checkY + int(i[1] / 2)
                    if 0 <= checkX <= 9 and  0 <= checkY <= 8 and board[checkX , checkY] == "--":
                        if newPiece[0] != color:
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
        

    # 궁,사 움직임
    def gungSaMove(self,startX,startY):
        board = self.current_board
        color = "G" if self.cho else "R"
        moving = ((-1,0), (1,0), (0,-1), (0,1))
        gungCenter = ((-1,-1), (1,1), (1,-1), (-1,1)) # 궁 중아에서 움직임
        if self.cho:
            # 귀 왼쪽 위
            if startX == 7 and startY == 3:
                newX = startX + 1
                newY = startY + 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 오른쪽 위
            if startX == 7 and startY == 5:
                newX = startX + 1
                newY = startY - 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 오른쪽 아래
            if startX == 9 and startY == 5:
                newX = startX - 1
                newY = startY - 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 왼쪽 아래
            if startX == 9 and startY == 3:
                newX = startX - 1
                newY = startY + 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 궁 중앙
            if startX == 8 and startY == 4:
                for i in gungCenter:
                    newX = startX + i[0]
                    newY = startY + i[1]
                    newPiece = board[newX,newY]
                    if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            for i in moving:
                newX = startX + i[0]
                newY = startY + i[1]
                # 궁을 벗어나면 안됨
                if 7 <= newX <= 9 and  3 <= newY <= 5:
                    newPiece = board[newX,newY]
                    if newPiece[0] != color:
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))

        elif not self.cho: 
            # 귀 왼쪽 위
            if startX == 0 and startY == 3:
                newX = startX + 1
                newY = startY + 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 오른쪽 위
            if startX == 0 and startY == 5:
                newX = startX + 1
                newY = startY - 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 오른쪽 아래
            if startX == 2 and startY == 5:
                newX = startX - 1
                newY = startY - 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 귀 왼쪽 아래
            if startX == 2 and startY == 3:
                newX = startX - 1
                newY = startY + 1
                newPiece = board[newX,newY]
                if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
            # 중앙
            if startX == 1 and startY == 4:
                for i in gungCenter:
                    newX = startX + i[0]
                    newY = startY + i[1]
                    newPiece = board[newX,newY]
                    if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:]))) 
            for i in moving:
                newX = startX + i[0]
                newY = startY + i[1]
                # 궁을 벗어나면 안됨
                if 0 <= newX <= 2 and  3 <= newY <= 5:
                    newPiece = board[newX,newY]
                    if newPiece[0] != color:
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
    
    # 차 움직임
    def chaMove(self,startX,startY):
        board = self.current_board
        color = "G" if self.cho else "R"
        moving = ((1,0),(-1,0),(0,1),(0,-1)) # 차의 방향 정해주기
        gungMoving = ((1,1),(-1,-1),(1,-1),(-1,1))

        for i in moving:
            for j in range(1,10):
                newX = startX + i[0] * j
                if(j != 9):
                    newY = startY + i[1] * j
                if 0 <= newX <= 9 and 0 <= newY <= 8:
                    newPiece = board[newX,newY]
                    if newPiece == "--": # 비어 있으면
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                    elif newPiece[0] != color: # 적 기물을 만나면 
                        self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                        break
                    else: # 아군 기물을 만나며
                        break    
        if 3 <= startY <= 5 and (0<= startX <= 2 or 7 <= startX <= 9):
            for i in gungMoving:
                for j in range(1,3):
                    newX = startX + i[0] * j
                    newY = startY + i[1] * j
                    if 3 <= newY <= 5 and (0<= newX <= 2 or 7 <= newX <= 9):
                        newPiece = board[newX,newY]
                        if newPiece == "--": # 비어 있으면
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                        elif newPiece[0] != color: # 적 기물을 만나면 
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                            break
                        else: # 아군 기물을 만나며
                            break    
    # 포 움직임
    def poMove(self,startX,startY):
        board = self.current_board
        color = "G" if self.cho else "R"
        moving = ((1,0),(-1,0),(0,1),(0,-1)) # 차의 방향 정해주기

        for i in moving:
            dari = False # 포는 앞에 상대 포를 제외한 기물이 있어야 움직일 수 있음
            for j in range(1,10):
                newX = startX + i[0] * j
                if(j != 9):
                    newY = startY + i[1] * j

                if 0 <= newX <= 9 and 0 <= newY <= 8:
                    newPiece = board[newX,newY]
                    if not dari:
                        if newPiece[1:] == "Po": # 포 방향에 다른 포가 있으면 멈춤
                            break
                        elif newPiece != "--":
                            dari = True
                    else: # 다리 있을때 움직임 추가해준다
                        if newPiece == "--":
                            self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                        elif newPiece[0] != color:
                            if newPiece[1:] == "Po": # 포끼리는 잡을 수 없음 
                                break
                            else:
                                self.possibleMove.append((newX,newY,startX,startY,self.getReward(newPiece[1:])))
                                break
        if (startX == 0 or startX == 2) and (startY == 3 or startY == 5):
            newPiece = board[1,4]
            if newPiece != "--" and newPiece[1:] != "Po":
                dari = True
                if dari:
                    if startX == 0 and startY == 3:
                        if board[startX + 2,startY + 2][1:] != "Po" and board[startX + 2,startY + 2][0] != color: 
                            self.possibleMove.append((startX + 2,startY + 2,startX,startY,self.getReward(board[startX + 2,startY + 2][1:])))
                    if startX == 0 and startY == 5:
                        if board[startX + 2,startY - 2][1:] != "Po" and board[startX + 2,startY - 2][0] != color:
                            self.possibleMove.append((startX + 2,startY - 2,startX,startY,self.getReward(board[startX + 2,startY - 2][1:])))
                    if startX == 2 and startY == 3 :
                        if board[startX - 2,startY + 2][1:] != "Po" and board[startX - 2,startY + 2][0] != color:
                            self.possibleMove.append((startX - 2,startY + 2,startX,startY,self.getReward(board[startX - 2,startY + 2][1:])))
                    if startX == 2 and startY == 5:
                        if board[startX - 2,startY - 2][1:] != "Po" and board[startX - 2,startY - 2][0] != color:
                            self.possibleMove.append((startX - 2,startY - 2,startX,startY,self.getReward(board[startX - 2,startY - 2][1:])))
        if (startX == 7 or startX == 9) and (startY == 3 or startY == 5):
            newPiece = board[8,4]
            if newPiece != "--" and newPiece[1:] != "Po":
                dari = True
                if dari:
                    if startX == 7 and startY == 3:
                        if board[startX + 2,startY + 2][1:] != "Po" and board[startX + 2,startY + 2][0] != color:
                            self.possibleMove.append((startX + 2,startY + 2,startX,startY,self.getReward(board[startX + 2,startY + 2][1:])))
                    if startX == 7 and startY == 5:
                        if board[startX + 2,startY - 2][1:] != "Po" and board[startX + 2,startY - 2][0] != color:
                            self.possibleMove.append((startX + 2,startY - 2,startX,startY,self.getReward(board[startX + 2,startY - 2][1:])))
                    if startX == 9 and startY == 3:
                        if board[startX - 2,startY + 2][1:] != "Po" and board[startX - 2,startY + 2][0] != color:
                            self.possibleMove.append((startX - 2,startY + 2,startX,startY,self.getReward(board[startX - 2,startY + 2][1:])))
                    if startX == 9 and startY == 5:
                        if board[startX - 2,startY - 2][1:] != "Po" and board[startX - 2,startY - 2][0] != color:
                            self.possibleMove.append((startX - 2,startY - 2,startX,startY,self.getReward(board[startX - 2,startY - 2][1:])))
                    
                
    # 게임을 이겼는지 졌는지         
    def gameState(self):
        pieces = ["GSang","GMa","GZol","GCha","GPo","RSang","RMa","RZol","RCha","RPo"]
        choKing = np.where(self.current_board =="GKing") # 초나라 왕의 위치 확인
        hanKing = np.where(self.current_board =="RKing") # 한나라 왕의 위치 확인
        if self.bigJangCheck == 2:
            return 0 # 무승부 처리
        if len(choKing[0])  == 0 :
            return 1 # 한나라가 승리
        if len(hanKing[0]) == 0:
            return 2 # 초나라가 승리
        
        
        if choKing[1] == hanKing[1] : # 같은 수직선 상에 있을 경우
            cx = choKing[0][0] # 수평
            cy = choKing[1][0] # 수직
            hx = hanKing[0][0] # 수평
            bigJang = self.current_board[hx+1 :cx,cy] # 왕끼리 사이에 기물이 있는지 체크
            bigJangList = np.where(bigJang =="--")[0]
            if len(bigJangList) == len(bigJang):

                self.bigJangCheck += 1
        else:
            if self.bigJangCheck == 1:
                
                self.bigJangCheck = 0
        if not any(np.ravel(np.isin(self.current_board,pieces))): # 궁과 사만 남았을때는 무승부 처리한다.
            
            return 0 # 무승부 처리
        return -1
    
    def step(self,action):
        # print(self.current_board)
        a = action
        # print("asd",a)
        piece = self.current_board[a[2],a[3]]
        
        # print(piece)
        self.current_board[a[2],a[3]] = "--"
        self.current_board[a[0],a[1]] =  piece
        self.cho = not self.cho
        self.possibleMove = [] 
        state = self.gameState()
        if state > 0: # 승패가 갈림
            self.done = True
            return self.current_board, a[4],self.done, None
        elif state == 0: # 무승부
            self.done = True
            return self.current_board, 0,self.done, None
        # print(self.current_board)
        return self.current_board, a[4],self.done, None



    # 보상 얻어오기
    def getReward(self,gimul):
        if gimul!= "-":
            if self.cho:
                return reward[gimul]
            else:
                return -reward[gimul]
        else:
            return 0
        