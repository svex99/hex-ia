# Player Template
# IMPORTANT: 	This module must have a function called play
# 				that receives a game and return a tuple of
#				two integers who represent a valid move on
#				the game.

from typing import List, Tuple
from game_logic import *
from minimax import minimax
from heapq import heappop, heappush

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


def play(game: Game, player):
	empty = 0
	depth = 2
	for row in game.board:
		for cell in row:
			empty += 1 if cell == '.' else 0
	
	if empty < 10:
		depth = 4
	return minimax(game, player, depth, heuristic, moves)


adv_player = lambda p : 'W' if p == 'B' else 'B'

def find_player_min_distance(initial_state: List[Tuple[int, int]], player_type: str, game: Game):
	q = [(0 if game.board[x][y] == player_type else 1, x, y) for x, y in initial_state]
	n = len(game.board)
	dist = [[99999999] * n for _ in range(n)]
	visited = [[False] * n for  _ in range(n)]

	for x, y in initial_state:
		visited[x][y] = True
		dist[x][y] = 0 if game.board[x][y] == player_type else 1

	while q:
		cost, x, y = heappop(q)
		if player_type == 'W' and y == 3:
			return cost
		if player_type == 'B' and x == 3:
			return cost

		for nx, ny in game.neighbour(x, y):
			if game[nx, ny] == player_type:
				if dist[x][y] < dist[nx][ny]:
					visited[nx][ny] = True
					dist[nx][ny] = dist[x][y]
					heappush(q, (dist[nx][ny], nx, ny))
			elif game[nx, ny] != adv_player(player_type):
				# Empty cell
				if dist[x][y] + 1 < dist[nx][ny]:
					visited[nx][ny] = True
					dist[nx][ny] = dist[x][y] + 1
					heappush(q, (dist[nx][ny], nx, ny))

	return 99999999


def moves(game, player):
	for x in range(game.size):
		for y in range(game.size):
			if game[x, y] == EMPTY:
				yield (x, y)

def heuristic(game, player):
	white_initial_state = [(i, 0) for i in range(len(game.board)) if game.board[0][i] != 'B']
	black_initial_state = [(0, i) for i in range(len(game.board))  if game.board[i][0] != 'W']
	
	white_min_cost = find_player_min_distance(white_initial_state, 'W', game)
	black_min_cost = find_player_min_distance(black_initial_state, 'B', game)

	value = white_min_cost - black_min_cost

	if player == 'W':
		return -value
	return value
