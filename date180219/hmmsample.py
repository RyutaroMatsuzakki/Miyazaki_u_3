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
        self.humming = [0 for i in range(1000)]
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

        for i in range(1,self.n, 1):
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
        self.S[0][0] = - math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[0] - 0), 2)/(2*pow(self.sigma, 2)))
        self.S[1][0] = - math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[0] - 1), 2)/(2*pow(self.sigma, 2)))
        for i in range(1, self.n, 1):
            self.S[0][i] = self.S[0][i - 1]  -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 0), 2)/(2*pow(self.sigma, 2))) + math.log(0.99)
            if self.S[1][i - 1] -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 0), 2)/(2*pow(self.sigma, 2))) + math.log(0.03) > self.S[0][i]:
                self.S[0][i] = self.S[1][i - 1]  -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 0), 2)/(2*pow(self.sigma, 2))) + math.log(0.03)
                self.C[0][i] = 1
            else:
                self.C[0][i] = 0
            self.S[1][i] = self.S[0][i - 1] -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 1), 2)/(2*pow(self.sigma, 2))) + math.log(0.01)
            if self.S[1][i - 1] -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 1), 2)/(2*pow(self.sigma, 2))) + math.log(0.97) > self.S[1][i]:
                self.S[1][i] = self.S[1][i - 1] -math.log(math.sqrt(2*math.pi*pow(self.sigma, 2))) - (pow((self.y[i] - 1), 2)/(2*pow(self.sigma, 2))) + math.log(0.97)
                self.C[1][i] = 1
            else:
                self.C[1][i] = 0
        if self.S[0][self.n - 1] > self.S[1][self.n - 1]:
            self.xmap[self.n - 1] = 0
        else :
            self.xmap[self.n - 1] = 1
        for i in range(self.n-1, 0, -1):
            self.xmap[i - 1] = self.C[self.xmap[i]][i]
        for i in range(0, self.n):
            if self.xmap[i] != self.x[i]:
                print('i:{0}, x:{1}, xmap:{2}, y:{3}'.format(i, self.x[i], self.xmap[i], self.y[i]))
                print('S[0]:{0}, S[1]:{1}, C[0]:{2}, C[1]:{3}'.format(self.S[0][i], self.S[1][i], self.C[0][i], self.C[1][i]))

    def compute_humming(self, i):
        for j in range(0, self.n, 1):
            if self.x[j] != self.xmap[j]:
                self.humming[i] += 1;
        #self.humming[sigma][i] = self.humming[sigma][i] / self.n
        #print('humming:{0}'.format(self.humming))

    def average_humming(self, roop, average):
        for i in range(0, roop, 1):
            average += self.humming[i]
        average = average #/(roop * self.n)
        print('average:{0}'.format(average))
        return average

def demo():

    n = 200
    humming = 0.0
    roop = 1000
    count = 0
    sigma = 0.1
    average = 0.0

    hmm = HMM(n, sigma, humming) # 隠れマルコフモデルを作る．n: 入力信号の数
    dispersion = 0.0
    for i in range(0, roop, 1):
        average = 0.0
        hmm.generate_x()
        hmm.generate_y()
        hmm.compute_xmap()
        hmm.compute_humming(i)

    average = hmm.average_humming(roop, average)
        #ここはxとyのプロット用
    t = range(n)
    plt.plot(t, hmm.x, label='x')
    plt.plot(t, hmm.y, '.g', label='y') # g は緑色， * は点
    plt.plot(t, hmm.xmap, '.r', label='xmap')

    plt.title('Original Signal, Observations')
    plt.xlabel('t') # X 軸
    plt.ylabel('x, y') # Y 軸
    plt.legend() # 描画

    plt.show() # 描画
    print(average)
    #plt.plot(sigma, average, 'bo')
    #plt.errorbar(sigma, average, yerr = dispersions, fmt = 'ro', ecolor = 'g')
    #plt.savefig('humming.png')
    #plt.show() # 描画

if __name__ == '__main__':
    demo()
