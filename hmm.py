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
    def __init__(self, n, sigma, humming):
        self.n = n
        self.sigma = sigma
        self.humming = humming
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
        self.S[0][0] = pow((self.y[0] - 0), 2)
        self.S[1][0] = pow((self.y[0] - 1), 2)
        for i in range(1, self.n):
            self.S[0][i] = self.S[0][i - 1] - pow((self.y[i] - 0), 2) + math.log(0.99)
            if (self.S[1][i - 1] - pow((self.y[i] - 0), 2) + math.log(0.03)) > self.S[0][i]:
                self.S[0][i] = self.S[1][i - 1] - pow((self.y[i] - 0), 2) + math.log(0.03)
                self.C[0][i] = 1
            else:
                self.C[0][i] = 0
            self.S[1][i] = self.S[0][i - 1] - pow((self.y[i] - 0), 2) + math.log(0.01)
            if (self.S[1][i - 1] - pow((self.y[i] - 1), 2) + math.log(0.97)) > self.S[1][i]:
                self.S[1][i] = self.S[1][i - 1] - pow((self.y[i] - 1), 2) + math.log(0.97)
                self.C[1][i] = 1
            else:
                self.C[1][i] = 0
        if self.S[0][self.n - 1] > self.S[1][self.n - 1]:
            self.xmap[self.n - 1] = 0
        else :
            self.xmap[self.n - 1] = 1
        for i in range(199, 0, -1):
            self.xmap[i - 1] = self.C[self.xmap[i]][i]

    def compute_humming(self):
        for i in range(0, self.n):
            if self.x[i] == self.xmap[i]:
                self.humming = self.humming+1;
        #print('humming:{0}'.format(self.humming))

    def average_humming(self, roop):
        self.humming = self.humming / self.n / roop
        print('average:{0}'.format(self.humming))

def demo():

    n = 200
    sigmas = [0.1, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
    humming = 0.0
    roop = 1000
    count = 0
    hummings = []

    for sigma in sigmas:
        hmm = HMM(n, sigma, humming) # 隠れマルコフモデルを作る．n: 入力信号の数
        for i in range(0, roop):
            hmm.generate_x()
            hmm.generate_y()
            hmm.compute_xmap()
            hmm.compute_humming()
        hmm.average_humming(roop)
        hummings.append(hmm.humming)
        t = range(n)
        plt.plot(t, hmm.x, label='x')
        plt.plot(t, hmm.y, '.g', label='y') # g は緑色， * は点
        plt.plot(t, hmm.xmap, '.r', label='xmap')

        plt.title('Original Signal, Observations')
        plt.xlabel('t') # X 軸
        plt.ylabel('x, y') # Y 軸
        plt.legend() # 描画

        plt.show() # 描画
        count = count + 1
    plt.bar(sigmas, hummings, tick_label=sigmas, width=0.1)
    plt.show() # 描画

if __name__ == '__main__':
    demo()