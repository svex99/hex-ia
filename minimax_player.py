# Player Template
# IMPORTANT: 	This module must have a function called play
# 				that receives a game and return a tuple of
#				two integers who represent a valid move on
#				the game.

from game_logic import *
from minimax import minimax

# game_logic
#
# 	EMPTY		
#	PLAYER[0]	
#	PLAYER[1]

# game
# 	-> current (W or B)
#		It refers to the player who must play in
#		this turn.
#	-> indexing
#		game[i,j] return the player who have played
#		on position <i;j> (compare with PLAYER[0] 
#		and PLAYER[1]). EMPTY if none player have
#		played there.
#	-> neighbour
#		creates an iterator that yields all 
#		coordinates <x;y> who are neighbour of 
#		current coordinates.
#
#		for nx, ny in game.neighbour(x, y):
#			print(nx, ny)


def play(game, player):
	# Code Here
	# Random player implementation (just delete it)

	return minimax(game, player, 3, heuristic, moves)


def moves(game, player):
	for x in range(game.size):
		for y in range(game.size):
			if game[x, y] == EMPTY:
				yield (x, y)


def valued_bfs(game: Game, beginning, end, player, pos_stack, current_val=0):
	if len(beginning) == 0:
		return current_val

	current = 0
	next_l = []
	for i in beginning:
		nextpos_gen = list(game.neighbour(i[0], i[1]))
		for nextpos in nextpos_gen:
			if nextpos in pos_stack:
				pass
			elif game[nextpos[0], nextpos[1]] == player:
				val = current
				beginning.append(nextpos)
				pos_stack.append(nextpos)
			elif game[nextpos[0], nextpos[1]] == EMPTY:
				val = 1 + current
				next_l.append(nextpos)
				pos_stack.append(nextpos)
			else:
				pass

	return valued_bfs(game, next_l, end, player, pos_stack, current_val + 1)

def heuristic(game : Game, player):
	size = len(game.board)
	pre_b_pos = [(0, i) for i in range(size)]
	post_b_pos = [(size -1, i) for i in range(size)]
	pre_w_pos = [(i, 0) for i in range(size)]
	post_w_pos = [(i, size -1) for i in range(size)]
	beginning = pre_w_pos if player == PLAYER[0] else pre_b_pos
	end = post_w_pos if player == PLAYER[0] else post_b_pos
	ret = valued_bfs(game, beginning, end, player, [])
	beginning = pre_w_pos if player == PLAYER[1] else pre_b_pos
	end = post_w_pos if player == PLAYER[1] else post_b_pos
	ret -= valued_bfs(game, beginning, end, player, [])
	return -ret


