#!/usr/local/bin/python3

import sys, os
#os.system("taskset -p 0xfffff %d" % os.getpid())
import random
import time

__version__="0.5"

## following code is used for multiprocessing calculating within class
#def unwrap_Matrix2D_det(object):
#	return Matrix2D._det(object)

class Matrix2D(object):
	_matrix = [[]]
	def __init__(self, x, y, init=True):
		assert ( x > 0 and y > 0 ), "self.x , self.y must be integer"
		self.x = int(x)
		self.y = int(y)
		self._matrix = [[float(0) for i in range(y)] for i in range(x)]

	def __getitem__(self,tup):
		x, y = tup
		return self._matrix[x][y]

	def __setitem__(self,tup,val):
		x, y = tup
		self._matrix[x][y] = val

	def __str__(self):
		_str = "(" + str(self.x) + "," + str(self.y) + ")" + "["
		for i in range(self.x):
			_str = _str + "\n"
			for j in range(self.y):
				_str = _str + " " + str(self._matrix[i][j])
		_str = _str + "\n]"
		return _str

	def __repr__(self):
		res = ""
		for i in range(self.x):
			res = res + "\n"
			for j in range(self.y):
				res = res + " " + str(self._matrix[i][j])
		res = res + "\n]"
		return res

	def __eq__(self, other):
		assert (self.x == other.x) and (self.y == other.y) , "self.x , self.y must equal to other.x , other.y"
		for i in range(self.x):
			for j in range(self.y):
				if self[i,j] != other[i,j]:
					return False
				else:
					return True

	def __ne__(self, other):
		assert (self.x == other.x) and (self.y == other.y) , "self.x , self.y must equal to other.x , other.y"
		for i in range(self.x):
			for j in range(self.y):
				if self[i,j] != other[i,j]:
					return True
				else:
					return False

	def __add__(self, other):
		assert (self.x == other.x) and (self.y == other.y) , "self.x , self.y must equal to other.x , other.y"
		res = Matrix2D(self.x , self.y)
		for i in range(self.x):
			for j in range(self.y):
				res[i,j] = self[i,j] + other[i,j]
		return res

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		assert (self.x == other.x) and (self.y == other.y) , "self.x , self.y must equal to other.x , other.y"
		res = Matrix2D(self.x , self.y)
		for i in range(self.x):
			for j in range(self.y):
				res[i,j] = self[i,j] - other[i,j]
		return res

	def __neg__(self):
		res = Matrix2D(self.x , self.y)
		for i in range(self.x):
			for j in range(self.y):
				res[i,j] = (-1) * self[i,j]
		return res

	# multiplication : result depends on several data type
	def __mul__(self, other):
		# matrix2D * matrix2D
		if isinstance (other, Matrix2D):
			assert self.y == other.x , "self.y must equal to other.x"
			res = Matrix2D(self.x , other.y)
			for i in range(self.x):
				for j in range(other.y):
					for k in range(self.x):
						res[i,j] = res[i,j] + self[i,k] * other[k,j]
			return res
		# matrix2D * float
		elif isinstance (other, float):
			res = Matrix2D(self.x, self.y)
			for i in range(self.x):
				for j in range(self.y):
					res[i,j] = self[i,j] * other
			return res
		# matrix2D * int
		elif isinstance (other, int):
			res = Matrix2D(self.x, self.y)
			for i in range(self.x):
				for j in range(self.y):
					res[i,j] = self[i,j] * float(other)
			return res
		# matrix2D(n*1) * list(1*n) which is taken as a 1*n's 1 div vector in math) -> 
		# result to a n*n square matrix if condition satisfied
		elif isinstance (other, list):
			assert self.y == 1 and self.x == len(other) , "self.y must equal to length of list"
			res = Matrix2D(self.x,self.x)
			for i in range(self.x):
				for j in range(self.x):
					res[i,j] = other[i] * self[i,0]
			return res

	def __rmul__(self, other):
		# matrix2D * matrix2D
		if isinstance (other, Matrix2D):
			assert self.x == other.y , "self.y must equal to other.x"
			res = Matrix2D(self.y , other.x)
			for i in range(self.y):
				for j in range(other.x):
					for k in range(self.y):
						res[i,j] = res[i,j] + self[i,k] * other[k,j]
			return res
		# float * matrix2D
		elif isinstance (other, float):
			res = Matrix2D(self.x, self.y)
			for i in range(self.x):
				for j in range(self.y):
					res[i,j] = self[i,j] * other
			return res
		# int * matrix2D
		elif isinstance (other, int):
			res = Matrix2D(self.x, self.y)
			for i in range(self.x):
				for j in range(self.y):
					res[i,j] = self[i,j] * float(other)
			return res
		# list(1*n) * matrix2D(n*1) * list(taken as a 1*n's 1 div vector in math) ->
		# result to an 1*1 matrix if condition satisfied
		elif isinstance (other, list):
			assert self.y == 1 and self.x == len(other) , "self.y must equal to length of list"
			res = Matrix2D(1,1)
			_sum = 0
			for i in range(self.x):
				_sum = _sum + self[i,0] * float(other[i])
			res[0,0] = _sum
			return res

	# get invert by Gauss Jordan: return matrix inverter or -1 if the invert not exist
	def __invert__(self):
		assert self._issquare(), "must be a square matrix (self.x == self.y)"
		if self._det() == 0:
			return -1

		n = self.x
		res = Matrix2D(n,n)
		if self._isunit():
			return res._setunit_()

		# create an Zero n*2n extened matrix
		ext = Matrix2D(n,2*n)

		# set source matrix to data of the extened matrix from [0,0] to [n-1,n-1]
		for i in range(n):
			for j in range(n):
				ext[i,j] = self[i,j]

		# set right part of extend matrix to unit matrix
		for i in range(n):
			for j in range(2*n):
				if j == (i + n):
					ext[i,j] = float(1)

		swp = float(0)
		# Partial pivoting
		for i in range(n-1 ,1, -1):
			if (ext[i-1,0] < ext[i,0]):
				for j in range (2*n):
					swp = ext[i,j]
					ext[i,j] = ext[i-1,j]
					ext[i-1,j] = swp
		#print "Partial pivoting result"
		#ext._print()

		# Reducing To Diagonal Matrix
		for i in range(n):
			for j in range(n):
				if j != i:
					if ext[i,i] == 0:
						swp = float(0)
					else:
						swp = ext[j,i]/ext[i,i]
					for k in range(2*n):
						ext[j,k] = ext[j,k] - ext[i,k]*swp

		#print "Diagonal Reducing result"
		#ext._print()

		# Reducing To Unit Matrix
		# get det within the operation
		det = float(1)
		for i in range(n):
			swp = ext[i,i]
			det = det * swp
			for j in range(2*n):
				if swp == 0:
					ext[i,j] = float(0)
				else:
					ext[i,j] = ext[i,j] / swp

		#print "Unit Reducing result"
		#ext._print()

		# set right part of extend matrix to unit matrix
		for i in range(n):
			for j in range(n):
				res[i,j] = ext[i,j+n]
		return res

	# row operation change matrix itself: row2 = row2 + row1 * scale
	# Warning again : this operation change the original matrix, 
	# and should be used carefully or you may clone a new one when using this
	def _rowop_(self, row1 , scale , row2 ):
		assert isinstance(row1, int) and isinstance(row2 , int) , "row1 and row2 must be integer"
		assert row1 < self.x and row2 < self.x , "row1 and row2 must less than self.x"
		assert isinstance(scale, int) or isinstance(scale, float), "scale must be calculable type like int or float"
		for i in range(self.y):
			self[row2,i] = self[row2,i] + self[row1,i] * float(scale)
		return self

	# col operation change matrix iteself: col2 = col2 + col1 * scale
	# Warning again : this operation change the original matrix, 
	# and should be used carefully or you may clone a new one when using this
	def _colop_(self, col1 , scale , col2 ):
		assert isinstance(col1, int) and isinstance(col2 , int) , "col1 and col2 must be integer"
		assert col1 < self.y and col2 < self.y , "col1 and col2 must be less than self.y"
		assert isinstance(scale, int) or isinstance(scale, float), "scale must be calculable type like int or float"
		for i in range(self.x):
			self[col2,i] = self[col2,i] + self[col1,i] * float(scale)
		return self

	# set all to 0
	# Warning: change the original matrix
	def _setunit_(self):
		assert self._issquare(), "must be square matrix to set unit matrix"
		for i in range(self.x):
			for j in range(self.y):
				if i == j:
					self[i,j] = float(1)
				else:
					self[i,j] = float(0)
		return self

	# set all to 0
	# Warning: change the original matrix
	def _setzero_(self):
		for i in range(self.x):
			for j in range(self.y):
				self[i,j] = float(0)
		return self

	# set random
	# Warning: change the original matrix including dim
	def _setrandom_(self, x, y, low, high):
		self.x = x
		self.y = y
		for i in range(x):
			for j in range(y):
				self[i,j] = random.randrange(low,high)
		return self

	# clone to create a new matrix same as origin without any change to original
	def _copy(self):
		res = Matrix2D(self.x , self.y)
		for i in range(self.x):
			for j in range(self.y):
				res[i,j] = self[i,j]
		return res

	# calculate determinant of matrix and return a float result
	def _det(self):
		assert self._issquare, "must be square matrix to calculate determinant"
		if self._isunit():
			return float(1)
		
		n = self.x
		if n == 2:
			res = self[0,0]*self[1,1] - self[0,1]*self[1,0]
		elif n == 3:
			a = self[0,0] * (self[1,1]*self[2,2] - self[1,2]*self[2,1])
			b = self[1,0] * (self[0,1]*self[2,2] - self[0,2]*self[2,1])
			c = self[2,0] * (self[0,1]*self[1,2] - self[0,2]*self[1,1])
			res = a - b + c

		else:
			# create an Zero n*2n extened matrix
			ext = Matrix2D(n,2*n)

			# set source matrix to data of the extened matrix from [0,0] to [n-1,n-1]
			for i in range(n):
				for j in range(n):
					ext[i,j] = self[i,j]

			# set right part of extend matrix to unit matrix
			for i in range(n):
				for j in range(2*n):
					if j == (i + n):
						ext[i,j] = float(1)

			swp = float(0)
			# Partial pivoting
			for i in range(n-1 ,1, -1):
				if (ext[i-1,0] < ext[i,0]):
					for j in range (2*n):
						swp = ext[i,j]
						ext[i,j] = ext[i-1,j]
						ext[i-1,j] = swp
			#print "Partial pivoting result"
			#ext._print()

			# Reducing To Diagonal Matrix
			for i in range(n):
				for j in range(n):
					if j != i:
						if ext[i,i] == 0:
							swp = float(0)
						else:
							swp = ext[j,i]/ext[i,i]
						for k in range(2*n):
							ext[j,k] = ext[j,k] - ext[i,k]*swp

			#print "Diagonal Reducing result"
			#ext._print()

			# Reducing To Unit Matrix
			# get det within the operation
			res = float(1)
			for i in range(n):
				swp = ext[i,i]
				res = res * swp
				for j in range(2*n):
					if swp == 0:
						ext[i,j] = float(0)
					else:
						ext[i,j] = ext[i,j] / swp
		return res

	# transfer operate, and create a new one
	def _trans(self):
		res = Matrix2D(self.y, self.x)
		for i in range(self.y):
			for j in range(self.x):
				res[i,j] = self[j,i]
		return res

	def _print(self):
		_str = "(" + str(self.x) + "," + str(self.y) + ")" + "["
		for i in range(self.x):
			_str = _str + "\n"
			for j in range(self.y):
				_str = _str + " " + str(self._matrix[i][j])
		_str = _str + "\n]"
		print(_str)

	def _save(self, filename):
		open(filename, 'w').write(str(self))

	def _issquare(self):
		if self.x == self.y:
			return True
		else:
			return False

	def _iszero(self):
		for i in range(self.x):
			for j in range(self.y):
				if self[i,j] != 0:
					return False
		return True

	def _isunit(self):
		for i in range(self.x):
			for j in range(self.y):
				if i == j:
					if self[i,j] != 1:
						return False
				else:
					if self[i,j] != 0:
						return False
		return True

	def _isrow0(self, row):
		assert isinstance(row, int) and row < self.x, "row must be integer and less than self.x"
		for i in range(self.y):
			if self[row,i] != 0:
				return False
		return True

	def _iscol0(self, col):
		assert isinstance(col, int) and col < self.y, "col must be integer and less than self.y"
		for i in range(self.x):
			if self[i,col] != 0:
				return False
		return True

	# create a new matrix by given lists if conditions satisfied
	@classmethod
	def fromlist(cls,*args):
		x = len(args)
		y = len(args[0])
		# check matrix define: all rows length must be the same
		for single_list in args[1:]:
			assert(len(single_list) == y), "all rows' length must be the same"
		res = Matrix2D(x,y)
		for i in range(x):
			for j in range(y):
				res[i,j] = float(args[i][j])
		return res

	@classmethod
	def random(cls, x, y, low ,high):
		res = Matrix2D(x, y)
		for i in range(x):
			for j in range(y):
				res[i,j] = random.randrange(low,high)
		return res

	# create a n*n matrix by given n
	@classmethod
	def zero(cls,n):
		res = Matrix2D(n,n)
		return res

	# create a n*n unit matrix by given n
	@classmethod
	def unit(cls,n):
		res = Matrix2D(n,n)
		for i in range(n):
			for j in range(n):
				if i == j:
					res[i,j] = 1
		return res

class testMatrix2D(object):
	def testeq(self,other):
		m1 = Matrix2D()

	def testInit(self):
		mtest = Matrix2D(3,3)
		for i in range(3):
			for j in range(3):
				if mtest[i,j] != 0:
					print("testInit for Matrix2D error")

	def testfromlist(self):
		mbase = Matrix2D(2,3)
		for i in range(2):
			for j in range(3):
				mbase[i,j] = 1 + i + j

		mtest = Matrix2D.fromlist([1,2,3],[4,5,6])
		if mbase != mtest:
			print("testfromlist for Matrix2D error")

	def testsub(self):
		m1 = Matrix2D.fromlist([3,1,2],[1,1,5])
		m2 = Matrix2D.fromlist([1,1,1],[1,1,1])
		m3 = m1 - m2
		m3._print()
		m4 = m2 - m1
		m4._print()

	def testmul(self):
		m1 = Matrix2D.fromlist([3,1,2],[0,1,5])
		m2 = Matrix2D.fromlist([4,3],[1,1],[6,0])
		mcheck12 = m1 * m2
		mres12 = Matrix2D.fromlist([13,10],[1,1])
		if mres12 != mcheck12:
			print("testmul matrix A * B for matrix2D error")
		mcheck12._print()
		m3 = m1 * float(3)
		m3._print()
		m4 = float(3) * m1
		m4._print()
		# test matrix * list (vector)
		m5 = Matrix2D.fromlist([3],[1],[2])
		m5._print()
		v = [1,2,3]
		m6 = m5 * v
		m6._print()
		# test list (vector) * matrix
		m7 = v * m5
		m7._print()

	def testinvert(self):
		print("test invert")
		m1 = Matrix2D.fromlist([2,2,5],[-2,1,2],[6,3,9])
		m2 = m1.__invert__()
		print("source matrix:")
		m1._print()
		if isinstance(m2,Matrix2D):
			print("result matrix:")
			m2._print()
		elif m2==-1:
			print("invert matrix not exist")

	def testdeterminant(self):
		print("test determinant")
		print("source matrix:")
		m1 = Matrix2D.fromlist([3,2,-1,4],[2,1,5,7],[0,5,2,-6],[-1,2,1,0])
		m1._print()
		print(m1._det())

	def testrandom100_100det(self):
		print("testrandom100_100det")
		m1 = Matrix2D.random(100,100,0,10)
		print("source matrix:")
		m1._print()
		print(m1._det())

if __name__ == '__main__':
	b_test = True
	if b_test:
		_test = testMatrix2D()
		_test.testInit()
		_test.testfromlist()
		_test.testmul()
		_test.testsub()
		_test.testinvert()
		_test.testdeterminant()
