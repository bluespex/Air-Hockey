import pygame, sys, random, time

# directkeys.py is taken from https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# inspired from pyimagesearch ball tracking https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from directkeys import  W, A, S, D
from directkeys import PressKey, ReleaseKey 


# define the lower and upper boundaries of the "orange" object in the HSV color space

orangeLower = np.array([35, 90, 102])
orangeUpper = np.array([102, 255, 255])

vs = VideoStream(src=0).start()
# allow the camera or video file to warm up
time.sleep(2.0)
initial = True
flag = False
current_key_pressed = set()
circle_radius = 30
windowSize = 160
lr_counter = 0

class obstlacles:
	def __init__(self):
		self.arr = []

	def add(self,n):
		self.arr.clear()
		while n:
			x = [random.choice(range(10, screen_width - 10)) , random.choice(range(screen_height)), random.choice((+1,-1))]
			self.arr.append(x)
			n -= 1;

def obs_collide():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	sz = len(obs)
	# mn = obs[0][0]*screen_width + obb.arr[0][1]
	# mx = obb.arr[sz-1][0]*screen_width + obb.arr[sz-1][1]
	l = 0;
	e = sz-1;
	print(obs)
	while(l<=e):
		mid = int((l+e)/2)

		cur = ball.x*screen_width + ball.y
		x = obs[mid].x*screen_width + obs[mid].y
		if(x > cur):
			if ball.colliderect(obs[mid]):
				if(ball_speed_x > 0):
					opponent_score += 1
				else:
					player_score += 1
			break
			l = mid+1
		elif(x < cur):
			if ball.colliderect(obs[mid]):
				if(ball_speed_x > 0):
					opponent_score += 1
				else:
					player_score += 1
			break
			e = mid-1
		else:
			if(ball_speed_x > 0):
				opponent_score += 1
			else:
				player_score += 1
			break

def object_collide():
	global ball_speed_x, player_score, opponent_score
	for i in range(len(obs)-1):
		if ball.colliderect(obs[i]):
			if obb.arr[i][2]>=1:
				if ball_speed_x < 0:
					player_score += 1
				else:
					opponent_score +=1
			else:
				if ball_speed_x < 0:
					player_score -= 1
				else:
					opponent_score -=1
			obs.pop(i)
			obb.arr.pop(i)

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(plob_sound)
		ball_speed_y *= -1
		
	# Player Score
	if ball.left <= 0: 
		if ball.bottom <= goal_top or ball.top >= goal_bottom:
			pygame.mixer.Sound.play(plob_sound)
			ball_speed_x *= -1
		else:	
			pygame.mixer.Sound.play(score_sound)
			score_time = pygame.time.get_ticks()
			player_score += 1
		
	# Opponent Score
	if ball.right >= screen_width:
		if ball.bottom <= goal_top or ball.top >= goal_bottom:
			pygame.mixer.Sound.play(plob_sound)
			ball_speed_x *= -1
		else:
			pygame.mixer.Sound.play(score_sound)
			score_time = pygame.time.get_ticks()
			opponent_score += 1
		
	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(plob_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1	
			ball_mid = (ball.top+ball.bottom)/2
			player_mid = (player.top+player.bottom)/2
			gradient = 2*abs(player_mid-ball_mid)
			gradient /= player_mid
			ball_speed_y = gradient*10
			ball_speed_y += 0.5
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(plob_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1	
			ball_mid = (ball.top+ball.bottom)/2
			opponent_mid = (opponent.top+opponent.bottom)/2
			gradient = 2*abs(opponent_mid-ball_mid)
			gradient /= opponent_mid
			ball_speed_y = gradient*10
			ball_speed_y += 0.5
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1		


		

def player_animation():
	player.y += player_speed

	if player.top <= goal_top:
		player.top = goal_top
	if player.bottom >= goal_bottom:
		player.bottom = goal_bottom

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= goal_top:
		opponent.top = goal_top
	if opponent.bottom >= goal_bottom:
		opponent.bottom = goal_bottom

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()

	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = basic_font.render("2",False,light_grey)
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = basic_font.render("1",False,light_grey)
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 5 * random.choice((1,-1))
		ball_speed_y = 5 * random.choice((1,-1))
		score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1067
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
player = pygame.Rect(screen_width - 50, screen_height / 2 - 40, 10,80)
opponent = pygame.Rect(40, screen_height / 2 - 40, 10,80)
goal1 = pygame.Rect(30, screen_height/2 - 120, 5 , 240)
goal2 = pygame.Rect(screen_width - 30, screen_height/2 - 120, 5 , 240)
obs = []

# Game Variables
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True
goal_top = screen_height/2 - 120;
goal_bottom = screen_height/2 + 120;
obb = obstlacles()
obb.add(10)

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# sound 
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

prev_time = time.perf_counter()

while True:
	keyPressed = False

	keyPressed_lr = False
    # grab the current frame
	frame = vs.read()
	frame = cv2.flip(frame,1)
	height,width = frame.shape[:2]
 
    # resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # crteate a mask for the orange color and perform dilation and erosion to remove any small
    # blobs left in the mask
	mask = cv2.inRange(hsv, orangeLower, orangeUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
 
    # find contours in the mask and initialize the current
    # (x, y) center of the orange object

    # divide the frame into two halves so that we can have one half control the acceleration/brake 
    # and other half control the left/right steering.
	left_mask = mask[:,0:width,]
    # right_mask = mask[:,width:,]

    #find the contours in the left and right frame to find the center of the object
	cnts_left = cv2.findContours(left_mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_left = imutils.grab_contours(cnts_left)
	center_left = None

 
    # only proceed if at least one contour was found
	if len(cnts_left) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
		c = max(cnts_left, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		# find the center from the moments 0.000001 is added to the denominator so that divide by 
        # zero exception doesn't occur
		center_left = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))
    
        # only proceed if the radius meets a minimum size
		if radius > circle_radius:
            # draw the circle and centroid on the frame,
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center_left, 5, (0, 0, 255), -1)

            #the window size is kept 160 pixels in the center of the frame(80 pixels above the center and 80 below)
			if center_left[1] < (height/2 - windowSize//2):
				cv2.putText(frame,'UP',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
				# PressKey(W)
				current_key_pressed.add(A)
				keyPressed = True
				keyPressed_lr = True
				player_speed -= 0.1

			elif center_left[1] > (height/2 + windowSize//2):
				cv2.putText(frame,'DOWN',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
				# PressKey(S)
				current_key_pressed.add(D)
				keyPressed = True
				keyPressed_lr = True
				player_speed += 0.1


 
    # show the frame to our screen
	frame_copy = frame.copy()
	frame_copy = cv2.rectangle(frame_copy,(0,height//2 - windowSize//2),(width,height//2 + windowSize//2),(255,0,0),2)
	cv2.imshow("Frame", frame_copy)

	   #We need to release the pressed key if none of the key is pressed else the program will keep on sending
    # the presskey command 
	if not keyPressed and len(current_key_pressed) != 0:
		for key in current_key_pressed:
			ReleaseKey(key)
		current_key_pressed = set()

    #to release keys for left/right with keys of up/down remain pressed   
	if not keyPressed_lr and ((A in current_key_pressed) or (D in current_key_pressed)):
		if A in current_key_pressed:
			# ReleaseKey(A)
			current_key_pressed.remove(A)
			player_speed += 0.1

		elif D in current_key_pressed:
		    # ReleaseKey(D)
		    current_key_pressed.remove(D)
		    player_speed -= 0.1

	key = cv2.waitKey(1) & 0xFF


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				player_speed -= 6
			if event.key == pygame.K_s:
				player_speed += 6
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				player_speed += 6
			if event.key == pygame.K_s:
				player_speed -= 6
	
	new_time = time.perf_counter()
	if new_time - prev_time > 5.0:
		prev_time = new_time
		obb.arr.clear()
		obb.add(5)
		obs.clear()
		for ele in obb.arr:
			x = pygame.Rect(ele[0], ele[1], 30,30)
			obs.append(x)

	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()
	object_collide()

	# Visuals 
	screen.fill((37,156,135))
	for i in range(len(obs)-1):
		if obb.arr[i][2] == 1:
			pygame.draw.rect(screen, (228, 227, 227), obs[i])
		else:
			pygame.draw.rect(screen, (132, 169, 172), obs[i])

	pygame.draw.rect(screen, light_grey, goal2)
	pygame.draw.rect(screen, light_grey, goal1)
	pygame.draw.rect(screen, (223,87,14), player)
	pygame.draw.rect(screen, (236,230,97), opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))


	if score_time:
		ball_start()

	player_text = basic_font.render(f'{player_score}',False,light_grey)
	screen.blit(player_text,(screen_width/2 + 15,0))

	opponent_text = basic_font.render(f'{opponent_score}',False,light_grey)
	screen.blit(opponent_text,(screen_width/2 - 30,0))



 
    # if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

	pygame.display.flip()
	clock.tick(120)


vs.stop() 
# close all windows
cv2.destroyAllWindows()