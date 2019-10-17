import random

class Maze():
	def __init__(self, nxn= 50):
		if not  0<nxn:nxn = 50
		self.start = (nxn//2-1, 0)
		self.state = [[0 for i in range(nxn)] for j in range(nxn)]
		self.state[nxn//2-1][0] = 1
		self.neighbours = lambda x, player, state,ngrid=nxn:list(filter(lambda x:x is not False,map(lambda x:x if 0<=x[0]<=ngrid-1 and x[1]>=0 and self.access(state, x[0], x[1]) == player else False, random.sample([(x[0],x[1]-1),(x[0]-1,x[1]),(x[0],x[1]+1),(x[0]+1,x[1])], 4))))
		self.peak = lambda node, dir: [(node[0]+i[0]+j[0],node[1]+i[1]+j[1]) for i in (dir, (0,0)) for j in {(0,-1):((-1,0), (0,0), (1,0)), (0,1):((-1,0), (0,0), (1,0)), (-1,0):((0,-1), (0,0), (0,1)), (1,0):((0,-1), (0,0), (0,1))}[dir] ]
		self.direction = lambda node, node2: (node2[0]-node[0], node2[1]-node[1])
	
	def access(self, state, x, y):
		try:return state[x][y]
		except: return None
	
	def create(self): # creates a random maze.
		def core(start, state, trac=[]):
			neis = self.neighbours(start, 0, state) #neighbours placeholder
			if neis == 0:return False 
			for cell in neis:
				dir = self.direction(start, cell)
				if not all(map(lambda x: True if self.access(state, x[0], x[1]) == 0 or self.access(state, x[0], x[1]) == None else False, set(self.peak(cell, dir))-{(start)})):continue
				state[cell[0]][cell[1]] = 1
				trac.append(cell)
				core(cell, state, trac=trac)
			return trac
		steps = [self.start]+core(self.start, self.state)
		return {'maze':self.state, 'steps': steps}

	def solve(self): # creates and solves a random maze.
		state = self.create()
		start = self.start
		winings = [(i, len(self.state[0])-1) for i in range(len(self.state[0])-1)]
		def core(state, start=start, trac=[]):
			neis = self.neighbours(start, 1, state)
			if neis == 0:return False 
			for cell in neis:
				trac.append(cell)
				if cell in winings:return True
				state[cell[0]][cell[1]] = 0
				if core(state,cell, trac=trac) == True:
					state[cell[0]][cell[1]] = 1
					if start == self.start:return trac
					return True
				trac.remove(cell)
				state[cell[0]][cell[1]] = 1
			return trac
		return {'maze': self.state, 'steps': state['steps'], 'solution': core(state['maze'])}


if __name__ == "__main__":
	#let's generate a dictionary that contains a maze and its steps and also the solution steps to solve the maze.
	maze = Maze().solve()
	print(maze)