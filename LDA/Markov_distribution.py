#author:bai
#coding=utf-8
#2016-08-25 马氏链的平稳分布以及细致平稳条件
import math
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def markov_dis(iter = 20):
    #状态转移矩阵
    #P = [[0.65,0.28,0.07],[0.15,0.67,0.18],[0.12,0.36,0.52]]
    P = [[0.2,0.4,0.4],[0.1,0.1,0.8],[0.3,0.3,0.4]]
    #P = [[0.65,0.28,0.07],[0.15,0.67,0.18],[0.12,0.36,0.52]]
    #P = [[0.65,0.28,0.07],[0.15,0.67,0.18],[0.12,0.36,0.52]]
    #初始概率分布
    init_pi = [0.1,0.1,0.8]
    i = 0
    a = 0.1;b = 0.1;c = 0.1
    while i < iter:

        if((a == init_pi[0]) & (b == init_pi[1]) & (c == init_pi[2])):
            print "在迭代了"+str(i-1)+"次后收敛."
            break

        a = init_pi[0]
        b = init_pi[1]
        c = init_pi[2]

        init_pi[0] = a * P[0][0] + b * P[1][0] + c * P[2][0]
        init_pi[1] = a * P[0][1] + b * P[1][1] + c * P[2][1]
        init_pi[2] = a * P[0][2] + b * P[1][2] + c * P[2][2]
        i += 1

        print init_pi

if __name__ == '__main__':
    markov_dis(30)
