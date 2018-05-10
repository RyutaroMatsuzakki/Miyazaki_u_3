# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt

#random.seed(20140123)


def make_matrix(a, b, fill=0.0): #  NumPy を使って高速に処理する方法がある
    m = []
    for i in range(a):
        m.append([fill]*b)
    return m

class HMM:
    def __init__(self, n, sigma):
        self.n = n
        self.sigma = sigma
        self.S = make_matrix(2, self.n)
        self.C = make_matrix(2, self.n)

        self.x = [0]*self.n
        self.xmap = [0]*self.n
        self.y = [0.0]*self.n


    def generate_x(self):
        if (random.random() < 0.5):
            self.x[0] = 0
        else:
            self.x[0] = 1

        for i in range(1,self.n):
            r = random.random()
            if ( self.x[i-1] == 0 ):
                if ( r < 0.99 ):
                    self.x[i] = 0
                else:
                    self.x[i] = 1
            else:
                if ( r < 0.97 ):
                    self.x[i] = 1
                else:
                    self.x[i] = 0
        
    def generate_y(self):
        for i in range(0,self.n):
            self.y[i] = random.gauss(self.x[i],self.sigma)

    def compute_xmap(self):
        pass

def demo():

    n = 200
    sigma = 0.7

    hmm = HMM(n, sigma) # 隠れマルコフモデルを作る．n: 入力信号の数
    hmm.generate_x()
    hmm.generate_y()
    hmm.compute_xmap()
        
    t = range(n)
    plt.plot(t, hmm.x, label='x')
    plt.plot(t, hmm.y, '.g', label='y') # g は緑色， * は点

    plt.title('Original Signal, Observations') 
    plt.xlabel('t') # X 軸
    plt.ylabel('x, y') # Y 軸
    plt.legend() # 描画

    plt.show() # 描画

if __name__ == '__main__':

    demo()


