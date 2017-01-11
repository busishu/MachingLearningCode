#author:Xuxu bai        
#coding=utf-8
#2016-08-23         参考邹博的LDA课程实现
import jieba
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def load_stopwords():
    stop_words = []
    fr = open('bai_lda/stop_words_ch.txt', 'r')
    lines = fr.readlines()
    for line in lines:
        stop_words.append(line.strip("\n"))
    fr.close()
    print "停用词载入完毕--------------"
    return  stop_words

def read_document(stop_words,dic):
    txt_num = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,16,18,19,20]
    dic_list = ["culture","economic","education","health"]
    doc_num = len(txt_num) * len(dic_list)
    doc = []
    flag = 0
    for dir in dic_list:
        for i in txt_num:
            path = "bai_lda/"+dir+"/"+str(i)+".txt"
#            print "\n"+path+"\n"
            fr = open(path,'r')
            line = fr.readline()
            line_str = ""
            while line:
                line_str += line
                line = fr.readline()
            fr.close()
            seg = jieba.cut(line_str,cut_all=False)
#           print "\n"+'\t'.join(seg)+"\n"
            str_seg = '\t'.join(seg).split("\t")
            stop_seg = []
            for si in str_seg:
                if si not in stop_words:
                    stop_seg.append(si)
            doc.append(stop_seg)
            for ss in str_seg:
                if ss.encode("utf-8") not in stop_words:
                   if ss in dic.keys():
                       continue
                   else:
                       dic[ss] = flag
                       flag += 1
        print "------------类别--"+dir+"--读取完毕----------------"


    return doc,doc_num

def init_topic(doc,nt,nd,nt_sum,nd_sum,dic):
    z = []

    for i in range(len(doc)):
        z_ = []
        for j in range(len(doc[i])):
            z_.append(random.randint(0,len(nt_sum)-1))

        z.append(z_)
    return z

def lda(z,nt,nd,nt_sum,nd_sum,dic,doc):
    doc_num = len(z)
    print "doc_num:"+str(doc_num)
    for time in range(10):  #迭代循环次数  这是由马氏链的平稳分布收敛决定的。
        for m in range(doc_num):    #遍历每个文档
            doc_length = len(z[m])  #文档长度（词数term）
            for i in range(doc_length):     #遍历文档m中每个词i的主题。
                term = dic[doc[m][i]]       #该词的编号
                gibbs_sampling(z,m,i,nt,nd,nt_sum,nd_sum,term)
                    #文档主题分布矩阵、文档m、词i、词-主题 分布 、文档-主题 分布、主题分布、文档长度、词i
        print "\n循环第"+str(time+1)+"次已完成  请等待\n"
    theta = calc_theta(nd,nd_sum)
    phi = calc_phi(nt,nt_sum)
    # for i in range(len(nd)):
    #     print nd[i]
    # print nd_sum
    return theta,phi

def gibbs_sampling(z,m,i,nt,nd,nt_sum,nd_sum,term):     #gibbs_sampling
    topic = z[m][i]         #主题编号 0-49
    nt[term][topic] -= 1    #在 词-主题 分布中去除当前词
    nd[m][topic] -= 1       #在 文档-主题 分布中去除当前词
    nt_sum[topic] -= 1
    nd_sum[m] -= 1

    topic_alpha = topic_num * alpha
    term_beta = len(dic) * beta

    p = [0 for x in range(topic_num)]   #p[k]属于主题k的概率  当前词属于主题k的概率
    for k in range(topic_num):
        p[k] = (nd[m][k] + alpha) / (nd_sum[m] + topic_alpha) \
               * (nt[term][k] + beta) / (nt_sum[k] + term_beta)
        if k >= 1:
            p[k] += p[k-1]
    gs = random.random() * p[topic_num-1]
    new_topic = 0
    while new_topic < topic_num:
        if p[new_topic] > gs:
            break
        new_topic += 1
    if new_topic == topic_num:
        new_topic -= 1
    nt[term][new_topic] += 1    #更新各个主题分布矩阵
    nd[m][new_topic] += 1
    nt_sum[new_topic] += 1
    nd_sum[m] += 1
    z[m][i] = new_topic

def calc_theta(nd,nd_sum):  #每个文档的主题分布
    doc_num = len(nd)
    topic_alpha = topic_num * alpha
    theta = [[0 for t in range(topic_num)] for d in range(doc_num)]
    for m in range(doc_num):
        for k in range(topic_num):
            theta[m][k] = (nd[m][k] + alpha) / (nd_sum[m] + topic_alpha)
    return theta

def calc_phi(nt,nt_sum):    #每个主题的词分布
    term_num = len(nt)
    term_beta = term_num * beta
    phi = [[0 for w in range(term_num)] for t in range(topic_num)]
    for k in range(topic_num):
        for term in range(term_num):
            phi[k][term] = (nt[term][k] + beta) / (nt_sum[k] + term_beta)
    return phi

def show_result(theta,phi,dic):
    for d in range(len(theta)):
        max_topic = theta[d].index(max(theta[d]))
        max_term_a  = phi[max_topic].index(max(phi[max_topic]))
        a = phi[max_topic][max_term_a]
        phi[max_topic][max_term_a] = 0
        max_term_b  = phi[max_topic].index(max(phi[max_topic]))
        b = phi[max_topic][max_term_b]
        phi[max_topic][max_term_b] = 0
        max_term_c = phi[max_topic].index(max(phi[max_topic]))
        c = phi[max_topic][max_term_c]
        p = ""
        for key in dic.keys():
            if max_term_a == dic[key]:
                p = p + str(key)+"("+str(a)+")"+"\t"
            if max_term_b == dic[key]:
                p = p + str(key)+"("+str(b)+")"+"\t"
            if max_term_c == dic[key]:
                p = p + str(key)+"("+str(c)+")"+"\t"
        print "第"+str(d+1)+"个文档的主题是\t"+p+"----------"+str(max_term_a)+"\t"+str(max_term_b)+"\t"+str(max_term_c)
       # print "第"+str(d+1)+"个文档的主题是:"+str(topic)+"-----主题是文档中第"+str(max_term)+"个词."+str(len(doc[d]))


if __name__ == '__main__':
    print "----START LDA---- \n"
    print "开始载入停用词------\n"
    stop_words = load_stopwords()
#    print "\n停用词表："+str(stop_words)+"\n"
    print "开始读取文档,检测文档数量,生成文档矩阵\n"
    dic = {} #文档中的term和出现次数
    doc,doc_num = read_document(stop_words,dic)
    print "\n-----------文档矩阵已生成-----------------------\n"
    alpha = 0.125
    beta = 0.01
    topic_num = 400 #指定主题总数为50
    term_num = len(dic)     #词汇的数目
    nt = [[0 for t in range(topic_num)] for term in range(term_num)]
        #nt[w][t] 第term个词属于第t个主题的次数
    nd = [[0 for t in range(topic_num)] for d in range(doc_num)]
        #nd[d][t]  第d个文档中出现第t个主题的次数
    nt_sum = [0 for t in range(topic_num)]
        #nt_sum[t] 第t个主题出现的次数
    nd_sum = [0 for d in range(doc_num)]
        #nd_sum[d] 第d个文档的长度
    print "\n-----------初始矩阵已生成-----------------\n"
    z = init_topic(doc,nt,nd,nt_sum,nd_sum,dic)
        #随机生成每个文档中每个词的主题
    theta,phi = lda(z,nt,nd,nt_sum,nd_sum,dic,doc)
        #lda主函数
    show_result(theta, phi, dic)
        #输出每个文档的主题、每个主题的关键字
