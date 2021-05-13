import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,)

pygame.init()
SQUARE_HEIGHT = 64
SQUARE_WIDTH = 64
TURNCOUNT = 0
WHITE = 0
BLACK = 1
moving_piece = None

def BoardSetup():
	# Set up the drawing window
	screen = pygame.display.set_mode([512, 512])
	board = pygame.image.load("Assets/ChessBoard.jpg").convert()
	screen.blit(board,(0,0))
	return screen

class King(pygame.sprite.Sprite):
    def __init__(self, png, pos, color):
        super(King, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def GetCornerPos(self):
    	return (self.rect.x, self.rect.y)
    def UpdatePos(self, MousePosition):
    	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def PlacePiece(self, MousePosition):
    	#checks if the move is valid
    	#if is not...
    	if (abs((MousePosition[0]) - (self.pos[0])) > (3*SQUARE_WIDTH/2)) or (abs((MousePosition[1]) - (self.pos[1])) > (3*SQUARE_HEIGHT/2)):
    		#puts the piece back
    		self.ResetPiece()
    	#if it is valid
    	else:
    		for Piece in AllPieces:
    			#if this square is already occupied by a piece
    			if (MousePosition[0] - SQUARE_WIDTH/2 == Piece.GetCornerPos()[0]) and (MousePosition[1] - SQUARE_HEIGHT/2 == Piece.GetCornerPos()[1]):
    				#if it is a piece of the same color
    				if self.color == Piece.color:
    					self.ResetPiece()
    					return False
    				else:
    					#deletes the piece
    					Piece.kill()
    		#move the piece
    		self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    		self.pos = MousePosition
    		return True
    	return False

    def ResetPiece(self):
    	self.rect = self.surf.get_rect(center = self.pos)

class Pawn(pygame.sprite.Sprite):
    def __init__(self, png, pos, color, first):
        super(Pawn, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def UpdatePos(self, MousePosition):
    	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def GetCornerPos(self):
    	return (self.rect.x, self.rect.y)
    def PlacePiece(self, MousePosition):
    	#if white
        #checks if the move is valid
        #if this piece needs to be constantly going upwards
        if (self.color == 0):
            #going straight
            if (MousePosition[0] == self.pos[0]):
                if (MousePosition[1] == self.pos[1] - SQUARE_HEIGHT):
                    if self.CollisionCheck(MousePosition[0], MousePosition[1]):
                        self.ResetPiece()
                        return False
                    self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                    self.pos = MousePosition
                    self.CheckPromotion(WHITE)
                    return True				
    			#moving twice
                elif (MousePosition[1] == self.pos[1] - SQUARE_HEIGHT*2):
                    if (self.pos[1] == 416):
                        if self.CollisionCheck(MousePosition[0], MousePosition[1]):
                            self.ResetPiece()
                            return False
                        if self.CollisionCheck(MousePosition[0], MousePosition[1]+SQUARE_HEIGHT):
                            self.ResetPiece()
                            return False 
                        self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                        self.pos = MousePosition
                        self.first = False
                        return True
                    else:
                        self.ResetPiece()
                        return False
                self.ResetPiece()
                return False
    		#diagnoally
            elif (MousePosition[1]  == self.pos[1] - SQUARE_HEIGHT):
    			#diagnoally right
                if (MousePosition[0] == self.pos[0] + SQUARE_WIDTH):
                    for Piece in AllPieces:
                        if (Piece.pos[0] == self.pos[0] + SQUARE_WIDTH) and (Piece.pos[1] == self.pos[1] - SQUARE_HEIGHT):
                            if Piece.color != self.color:
                            	Piece.kill()
                            	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                            	self.pos = MousePosition
                            	self.CheckPromotion(WHITE)
                            	return True
                            else:
                            	self.ResetPiece()
                            	return False
                    self.ResetPiece()
                    return False
    			#diagnoally left
                if (MousePosition[0] == self.pos[0] - SQUARE_HEIGHT):
                    for Piece in AllPieces:
                        if (Piece.pos[0] == self.pos[0] - SQUARE_WIDTH) and (Piece.pos[1] == self.pos[1] - SQUARE_HEIGHT):
                            if Piece.color != self.color:
                            	Piece.kill()
                            	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                            	self.pos = MousePosition
                            	self.CheckPromotion(WHITE)
                            	return True
                            else:
                            	self.ResetPiece()
                            	return False
                    self.ResetPiece()
                    return False
            else:
                self.ResetPiece()
                return False
            
        if (self.color == 1):
            #going straight
            if (MousePosition[0] == self.pos[0]):
                if (MousePosition[1] == self.pos[1] + SQUARE_HEIGHT):
                    if self.CollisionCheck(MousePosition[0], MousePosition[1]):
                        self.ResetPiece()
                        return False
                    self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                    self.pos = MousePosition
                    self.CheckPromotion(BLACK)
                    return True             
                #moving twice
                elif (MousePosition[1] == self.pos[1] + SQUARE_HEIGHT*2):
                    if (self.pos[1] == 64+32):
                        if self.CollisionCheck(MousePosition[0], MousePosition[1]):
                            self.ResetPiece()
                            return False
                        elif self.CollisionCheck(MousePosition[0], MousePosition[1]-SQUARE_HEIGHT):
                            self.ResetPiece()
                            return False 
                        self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                        self.pos = MousePosition
                        self.first = False
                        return True
                    else:
                        self.ResetPiece()
                        return False
                self.ResetPiece()
                return False
            #diagnoally
            elif (MousePosition[1]  == self.pos[1] + SQUARE_HEIGHT):
                #diagnoally right
                if (MousePosition[0] == self.pos[0] + SQUARE_WIDTH):
                    for Piece in AllPieces:
                        if (Piece.pos[0] == self.pos[0] + SQUARE_WIDTH) and (Piece.pos[1] == self.pos[1] + SQUARE_HEIGHT):
                            if self.color != Piece.color:
                            	Piece.kill()
                            	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                            	self.pos = MousePosition
                            	self.CheckPromotion(BLACK)
                            	return True
                            else:
                            	self.ResetPiece()
                            	return False
                    self.ResetPiece()
                    return False
                #diagnoally left
                if (MousePosition[0] == self.pos[0] - SQUARE_HEIGHT):
                    for Piece in AllPieces:
                        if (Piece.pos[0] == self.pos[0] - SQUARE_WIDTH) and (Piece.pos[1] == self.pos[1] + SQUARE_HEIGHT):
                            if self.color != Piece.color:
                            	Piece.kill()
                            	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
                            	self.pos = MousePosition
                            	self.CheckPromotion(BLACK)
                            	return True
                            else:
                            	self.ResetPiece()
                            	return False
                    self.ResetPiece()
                    return False
            else:
                self.ResetPiece()
                return False
    def CollisionCheck(self, MousePositionX, MousePositionY):
        MousePosition = (MousePositionX, MousePositionY)
        for Piece in AllPieces:
            if Piece.pos[0] == MousePosition[0] and Piece.pos[1] == MousePosition[1]:
                return True
        return False
    def ResetPiece(self):
    	self.rect = self.surf.get_rect(center = self.pos)
    def CheckPromotion(self, color):
    	if (self.pos[1] == SQUARE_HEIGHT/2 and color == WHITE) or (self.pos[1] == 512 - SQUARE_HEIGHT/2 and color == BLACK):
            
            UserInput = input("Enter R for a rook, N for a knight, B for bishop, Q for queen. (Default is queen)")
            
            if UserInput == "R":
                if self.color == WHITE:
                	x = Rook("Assets/WhitePieces/WhiteRook.png", self.pos, color)
                	WhitePieces.add(x)
                	AllPieces.add(x)
                else:
                	x = Rook("Assets/BlackPieces/BlackRook.png", self.pos, color)
                	BlackPieces.add(x)
                	AllPieces.add(x)
                self.kill()
            elif UserInput == "N":
                if self.color == WHITE:
                	x = Knight("Assets/WhitePieces/WhiteKnight.png", self.pos, color)
                	WhitePieces.add(x)
                	AllPieces.add(x)
                else:
                	x = Knight("Assets/BlackPieces/BlackKnight.png", self.pos, color)
                	BlackPieces.add(x)
                	AllPieces.add(x)
                self.kill()
            elif UserInput == "B":
                if self.color == WHITE:
                	x = Bishop("Assets/WhitePieces/WhiteBishop.png", self.pos, color)
                	WhitePieces.add(x)
                	AllPieces.add(x)
                else:
                	x = Bishop("Assets/BlackPieces/BlackBishop.png", self.pos, color)
                	BlackPieces.add(x)
                	AllPieces.add(x)
                self.kill()
            else:
                if self.color == WHITE:
                	x = Queen("Assets/WhitePieces/WhiteQueen.png", self.pos, color)
                	WhitePieces.add(x)
                	AllPieces.add(x)
                else:
                	x = Queen("Assets/BlackPieces/BlackQueen.png", self.pos, color)
                	BlackPieces.add(x)
                	AllPieces.add(x)
                self.kill()
   	
class Rook(pygame.sprite.Sprite):
    def __init__(self, png, pos, color):
        super(Rook, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def GetCornerPos(self):
        return (self.rect.x, self.rect.y)
    def UpdatePos(self, MousePosition):
        self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def PlacePiece(self, MousePosition):
        ###NOTE####
        #this code seems to almost repeat itself four times
        #I tried to put it in a function for the sake of efficiency, but each time 
        #the pygame window just crashed
        #this was a bug I was unable to solve

        #checking if vertical negative movment is legal
        if self.pos[0] == MousePosition[0] and self.pos[1] > MousePosition[1]:
        	#we need to loop through every square here
        	x = self.pos[1]
        	while x != MousePosition[1]:
        		x -= SQUARE_HEIGHT
        		#if we are on the last square
        		if x == MousePosition[1]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False

        #checking if vertical positive movment is legal
        elif self.pos[0] == MousePosition[0] and self.pos[1] < MousePosition[1]:
        	#we need to loop through every square here
        	x = self.pos[1]
        	while x != MousePosition[1]:
        		x += SQUARE_HEIGHT
        		#if we are on the last square
        		if x == MousePosition[1]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        #checking if horizontal positive movment is legal
        elif self.pos[1] == MousePosition[1] and self.pos[0] < MousePosition[0]:
        	#we need to loop through every square here
        	x = self.pos[0]
        	while x != MousePosition[0]:
        		x += SQUARE_WIDTH
        		#if we are on the last square
        		if x == MousePosition[0]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        elif self.pos[1] == MousePosition[1] and self.pos[0] > MousePosition[0]:
        	#we need to loop through every square here
        	x = self.pos[0]
        	while x != MousePosition[0]:
        		x -= SQUARE_WIDTH
        		#if we are on the last square
        		if x == MousePosition[0]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        self.ResetPiece()
        return False
      
    def ResetPiece(self):
        self.rect = self.surf.get_rect(center = self.pos)

class Bishop(pygame.sprite.Sprite):
    def __init__(self, png, pos, color):
        super(Bishop, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def GetCornerPos(self):
    	return (self.rect.x, self.rect.y)
    def UpdatePos(self, MousePosition):
    	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def PlacePiece(self, MousePosition):
    	#see note in rook class for reason that this is not broken up into smaller functions

    	#if the move is even diagonal
        if abs(self.pos[0] - MousePosition[0]) == (abs(self.pos[1] - MousePosition[1])): 
    	#lets generate a list of valid moves for this piece
        	#checking if diagonal negative negative movment is happening 
        	if self.pos[0] > MousePosition[0] and self.pos[1] > MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x -= SQUARE_WIDTH
        			y -= SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        
        	#checking if diagonal positive negative movment is happening 
        	if self.pos[0] < MousePosition[0] and self.pos[1] > MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x += SQUARE_WIDTH
        			y -= SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False

			#checking if diagonal negative positive movment is happening        
        	if self.pos[0] > MousePosition[0] and self.pos[1] < MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x -= SQUARE_WIDTH
        			y += SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        
        	#checking if diagonal positive positive movment is happening        
        	if self.pos[0] < MousePosition[0] and self.pos[1] < MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x += SQUARE_WIDTH
        			y += SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        else:
        	self.ResetPiece()
        	return False
        		
    def ResetPiece(self):
    	self.rect = self.surf.get_rect(center = self.pos)    	

class Queen(pygame.sprite.Sprite):
    def __init__(self, png, pos, color):
        super(Queen, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def GetCornerPos(self):
    	return (self.rect.x, self.rect.y)
    def UpdatePos(self, MousePosition):
    	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def PlacePiece(self, MousePosition):
    	#if the move is even diagonal
        if abs(self.pos[0] - MousePosition[0]) == (abs(self.pos[1] - MousePosition[1])): 
    	#lets generate a list of valid moves for this piece
        	#checking if diagonal negative negative movment is happening 
        	if self.pos[0] > MousePosition[0] and self.pos[1] > MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x -= SQUARE_WIDTH
        			y -= SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        
        	#checking if diagonal positive negative movment is happening 
        	if self.pos[0] < MousePosition[0] and self.pos[1] > MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x += SQUARE_WIDTH
        			y -= SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False

			#checking if diagonal negative positive movment is happening        
        	if self.pos[0] > MousePosition[0] and self.pos[1] < MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x -= SQUARE_WIDTH
        			y += SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        
        	#checking if diagonal positive positive movment is happening        
        	if self.pos[0] < MousePosition[0] and self.pos[1] < MousePosition[1]:
        		#we need to loop through every square here
        		x = self.pos[0]
        		y = self.pos[1]
        		while x != MousePosition[0]:
        			x += SQUARE_WIDTH
        			y += SQUARE_HEIGHT
        			#if we are on the last square
        			if x == MousePosition[0]:
        				for Piece in AllPieces:
        					#if a piece is occupying this square...
        					if Piece.pos[1] == y and Piece.pos[0] == x:
        						if Piece.color != self.color:
        							Piece.kill()
        							self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        							self.pos = MousePosition
        							return True
        						else:
        							#print("End piece collision!")
        							self.ResetPiece()
        							return False
        				#No pieces occupy the end space
        				self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        				self.pos = MousePosition
        				return True
        		
        			#check if any of the pieces...
        			for Piece in AllPieces:
        				#...happen to be on this square
        				if Piece.pos[1] == y and Piece.pos[0] == x:
        					#this is a collision
        					#print("intermediate collision")
        					self.ResetPiece()
        					return False
        
        #checking if vertical negative movment is legal
        elif self.pos[0] == MousePosition[0] and self.pos[1] > MousePosition[1]:
        	#we need to loop through every square here
        	x = self.pos[1]
        	while x != MousePosition[1]:
        		x -= SQUARE_HEIGHT
        		#if we are on the last square
        		if x == MousePosition[1]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        #checking if vertical positive movment is legal
        elif self.pos[0] == MousePosition[0] and self.pos[1] < MousePosition[1]:
        	#we need to loop through every square here
        	x = self.pos[1]
        	while x != MousePosition[1]:
        		x += SQUARE_HEIGHT
        		#if we are on the last square
        		if x == MousePosition[1]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[0] == self.pos[0] and Piece.pos[1] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        #checking if horizontal positive movment is legal
        elif self.pos[1] == MousePosition[1] and self.pos[0] < MousePosition[0]:
        	#we need to loop through every square here
        	x = self.pos[0]
        	while x != MousePosition[0]:
        		x += SQUARE_WIDTH
        		#if we are on the last square
        		if x == MousePosition[0]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        #checking if horizontal negative movment is legal
        elif self.pos[1] == MousePosition[1] and self.pos[0] > MousePosition[0]:
        	#we need to loop through every square here
        	x = self.pos[0]
        	while x != MousePosition[0]:
        		x -= SQUARE_WIDTH
        		#if we are on the last square
        		if x == MousePosition[0]:
        			for Piece in AllPieces:
        				#if a piece is occupying this square...
        				if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        					if Piece.color != self.color:
        						Piece.kill()
        						self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        						self.pos = MousePosition
        						return True
        					else:
        						#print("End piece collision!")
        						self.ResetPiece()
        						return False
        			#No pieces occupy the end space
        			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
        			self.pos = MousePosition
        			return True
        		
        		#check if any of the pieces...
        		for Piece in AllPieces:
        			#...happen to be on this square
        			if Piece.pos[1] == self.pos[1] and Piece.pos[0] == x:
        				#this is a collision
        				#print("intermediate collision")
        				self.ResetPiece()
        				return False
        else:
        	self.ResetPiece()
        	return False
        		
    def ResetPiece(self):
    	self.rect = self.surf.get_rect(center = self.pos)

class Knight(pygame.sprite.Sprite):
    def __init__(self, png, pos, color):
        super(Knight, self).__init__()
        self.surf = pygame.image.load(png)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.clicked = False
        self.pos = pos
        self.rect = self.surf.get_rect(center = self.pos)
        self.color = color      
    def GetCornerPos(self):
    	return (self.rect.x, self.rect.y)
    def UpdatePos(self, MousePosition):
    	self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    def PlacePiece(self, MousePosition):
    	#the knight has 8 possible moves... hard code?
    	#top and bottom two moves
    	if (self.pos[1] + SQUARE_HEIGHT*2 == MousePosition[1] or self.pos[1] - SQUARE_HEIGHT*2 == MousePosition[1]):
    		if (self.pos[0] + SQUARE_WIDTH == MousePosition[0] or self.pos[0] - SQUARE_WIDTH == MousePosition[0]):
    			for Piece in AllPieces:
    				if MousePosition[0] == Piece.pos[0] and MousePosition[1] == Piece.pos[1]:
    					if Piece.color != self.color:
    						Piece.kill()
    					else:
    						self.ResetPiece()
    						return False
    			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    			self.pos = MousePosition
    			return True

        #left and right two moves
    	if (self.pos[0] + SQUARE_WIDTH*2 == MousePosition[0] or self.pos[0] - SQUARE_WIDTH*2 == MousePosition[0]):
    		if (self.pos[1] + SQUARE_HEIGHT == MousePosition[1] or self.pos[1] - SQUARE_HEIGHT == MousePosition[1]):
    			for Piece in AllPieces:
    				if MousePosition[0] == Piece.pos[0] and MousePosition[1] == Piece.pos[1]:
    					if Piece.color != self.color:
    						Piece.kill()
    					else:
    						self.ResetPiece()
    						return False
    			self.rect = self.surf.get_rect(center = (MousePosition[0],MousePosition[1]))
    			self.pos = MousePosition
    			return True

    	self.ResetPiece()
    	return False
    def ResetPiece(self):
    	self.rect = self.surf.get_rect(center = self.pos)
#######UNATTRACTIVE INITILIZATION!#######################
screen = BoardSetup()
AllPieces = pygame.sprite.Group()
WhitePieces = pygame.sprite.Group()
BlackPieces = pygame.sprite.Group()
###Kings###
def PieceInit(WRookImg, WKnightImg, WBishopImg, WQueenImg, WKingImg, WPawnImg, BRookImg, BKnightImg, BBishopImg, BQueenImg, BKingImg, BPawnImg):
	WKing = King(WKingImg, (288,480), WHITE)
	WhitePieces.add(WKing)
	AllPieces.add(WKing)
	BKing = King(BKingImg, (288,32), BLACK)
	BlackPieces.add(BKing)
	AllPieces.add(BKing)
	###Queens###
	WQueen = Queen(WQueenImg, (224,480), WHITE)
	WhitePieces.add(WQueen)
	AllPieces.add(WQueen)
	BQueen = Queen(BQueenImg, (224,32), BLACK)
	BlackPieces.add(BQueen)
	AllPieces.add(BQueen)
	###all pawns#######
	for square in range(0,8):
		x = Pawn(BPawnImg, (SQUARE_HEIGHT*square +32 ,96), BLACK, True)
		BlackPieces.add(x)
		AllPieces.add(x)

		x = Pawn(WPawnImg, (SQUARE_HEIGHT*square + 32,416), WHITE, True)
		WhitePieces.add(x)
		AllPieces.add(x)
	###Rook###
	for square in range(0,2):
		x = Rook(BRookImg, (((512-SQUARE_HEIGHT)*square + 32), 32), BLACK)
		BlackPieces.add(x)
		AllPieces.add(x)

		x = Rook(WRookImg, (((512-SQUARE_HEIGHT)*square + 32), (512-32)), WHITE)
		WhitePieces.add(x)
		AllPieces.add(x)
	###Knight###
	for square in range(0,2):
		x = Knight(BKnightImg, (((512-SQUARE_HEIGHT*3)*square + 32 + SQUARE_HEIGHT), 32), BLACK)
		BlackPieces.add(x)
		AllPieces.add(x)

		x = Knight(WKnightImg, (((512-SQUARE_HEIGHT*3)*square + 32 + SQUARE_HEIGHT), (512-32)), WHITE)
		WhitePieces.add(x)
		AllPieces.add(x)
		###all bishops###
	for square in range(0,2):
		x = Bishop(BBishopImg, (SQUARE_HEIGHT*3*square +32 + SQUARE_HEIGHT*2 ,32), BLACK)
		BlackPieces.add(x)
		AllPieces.add(x)

		x = Bishop(WBishopImg, (SQUARE_HEIGHT*3*square +32 + SQUARE_HEIGHT*2 ,480), WHITE)
		WhitePieces.add(x)
		AllPieces.add(x)
	return (WKing, BKing)
#################################################################
print("Welcome to chess ui - a CS Project!")
lolSkin = input("Would you like to play with a league skin? (y/n)")
if lolSkin == "y":
	WRookImg = "Assets/WhiteLeaguePieces/FioraSquare.png"
	WKnightImg = "Assets/WhiteLeaguePieces/QuinnSquare.png"
	WBishopImg = "Assets/WhiteLeaguePieces/LuxSquare.png"
	WQueenImg = "Assets/WhiteLeaguePieces/GarenSquare.png"
	WKingImg = "Assets/WhiteLeaguePieces/Jarvan_IVSquare.png"
	WPawnImg = "Assets/WhiteLeaguePieces/GalioSquare.png"
	BRookImg = "Assets/BlackLeaguePieces/SionSquare.png"
	BKnightImg = "Assets/BlackLeaguePieces/KledSquare.png"
	BBishopImg = "Assets/BlackLeaguePieces/DravenSquare.png"
	BQueenImg = "Assets/BlackLeaguePieces/DariusSquare.png"
	BKingImg = "Assets/BlackLeaguePieces/SwainSquare.png"
	BPawnImg = "Assets/BlackLeaguePieces/UrgotSquare.png"
else:
	WRookImg = "Assets/WhitePieces/WhiteRook.png"
	WKnightImg = "Assets/WhitePieces/WhiteKnight.png"
	WBishopImg = "Assets/WhitePieces/WhiteBishop.png"
	WQueenImg = "Assets/WhitePieces/WhiteQueen.png"
	WKingImg = "Assets/WhitePieces/WhiteKing.png"
	WPawnImg = "Assets/WhitePieces/WhitePawn.png"
	BRookImg = "Assets/BlackPieces/BlackRook.png"
	BKnightImg = "Assets/BlackPieces/BlackKnight.png"
	BBishopImg = "Assets/BlackPieces/BlackBishop.png"
	BQueenImg = "Assets/BlackPieces/BlackQueen.png"
	BKingImg = "Assets/BlackPieces/BlackKing.png"
	BPawnImg = "Assets/BlackPieces/BlackPawn.png"
kings = PieceInit(WRookImg, WKnightImg, WBishopImg, WQueenImg, WKingImg, WPawnImg, BRookImg, BKnightImg, BBishopImg, BQueenImg, BKingImg, BPawnImg)
WKing = kings[0]
BKing = kings[1] 
Running = True
while Running:
	LegalMove = False
	BoardSetup()
	#starts by assuming that checkmate has been delivered.
	KingAlive = False
	for Piece in AllPieces:
		screen.blit(Piece.surf, Piece.rect)
		if TURNCOUNT % 2 == 0 and Piece == WKing:
			KingAlive = True
		elif TURNCOUNT % 2 == 1 and Piece == BKing:
			KingAlive = True
	if not KingAlive:
		if TURNCOUNT % 2 == 0:
			print("Black Wins!")
			Running = False
		else:
			print("White Wins!")
			Running = False
	
   # Did the user click the window close button
	for event in pygame.event.get():
		if pygame.mouse.get_pressed()[0]:
			for Piece in AllPieces:
				if moving_piece == Piece or moving_piece == None:
					#if mouse is hovering over piece
					if ((pygame.mouse.get_pos()[0] > Piece.GetCornerPos()[0])
					and (pygame.mouse.get_pos()[0] < Piece.GetCornerPos()[0] + SQUARE_WIDTH)
					and ((pygame.mouse.get_pos()[1] > Piece.GetCornerPos()[1])
					and (pygame.mouse.get_pos()[1] < Piece.GetCornerPos()[1] + SQUARE_HEIGHT))
					and TURNCOUNT%2 == Piece.color):
						Piece.UpdatePos(pygame.mouse.get_pos())
						moving_piece = Piece
		#realese off mouse button
		elif pygame.MOUSEBUTTONUP and (moving_piece != None):

			pos = pygame.mouse.get_pos()
			LegalMove = moving_piece.PlacePiece(((int(pos[0]/SQUARE_WIDTH)*SQUARE_WIDTH+SQUARE_WIDTH/2),
								(int(pos[1]/SQUARE_HEIGHT)*SQUARE_HEIGHT+SQUARE_HEIGHT/2)))
			
			#this returns the coordinate of the center!
        	
			moving_piece = None
		elif event.type == pygame.QUIT:
			Running = False		
	if LegalMove == True:
		TURNCOUNT += 1
    # Flip the display
	pygame.display.update()
	pygame.display.flip()
	
# Done! Time to quit.
pygame.quit()