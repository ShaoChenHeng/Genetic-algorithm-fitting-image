from PIL import Image, ImageDraw
import os
import gc
import random as r
import numpy as np
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
import matplotlib.pyplot as plt

class Color(object):
    '''
    定义颜色的类，这个类包含r,g,b,a表示颜色属性
    '''
    def __init__(self):
        self.r = r.randint(0, 255)
        self.g = r.randint(0, 255)
        self.b = r.randint(0, 255)
        self.a = r.randint(90, 115)

def mutate_or_not(rate):
    '''
    生成随机数，判断是否需要变异
    '''
    return True if rate > r.random() else False


class Polygons(object):
    '''
    定义多边形的类
    '''
    max_mutate_rate = 0.1   # 完全随机变异概率
    mid_mutate_rate = 0.3    # 从父代中等变异概率
    min_mutate_rate = 0.85    # 从父代略微变异概率

    def __init__(self, size=(255, 255)):    # 多边形初始化
        self.ax = r.randint(0, size[0])
        self.ay = r.randint(0, size[1])
        self.bx = r.randint(0, size[0])
        self.by = r.randint(0, size[1])
        self.cx = r.randint(0, size[0])
        self.cy = r.randint(0, size[1])
        self.dx = r.randint(0, size[0])
        self.dy = r.randint(0, size[1])
        self.ex = r.randint(0, size[0])
        self.ey = r.randint(0, size[1])
        self.fx = r.randint(0, size[0])
        self.fy = r.randint(0, size[1])
        self.n = r.randint(2, 5)      # 随机生成多边形的顶点数
        self.color = Color()
        self.img_t = None

    def mutate_from(self, parent):
        if mutate_or_not(self.max_mutate_rate):      # 完全随机变异，不从父代变异
            self.ax = r.randint(0, 255)
            self.ay = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):      # 从父代变异，但是从父代变异程度较大
            self.ax = min(max(0, parent.ax + r.randint(-15, 15)), 255)
            self.ay = min(max(0, parent.ay + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):      # 从父代变异，从父代变异程度较小，保留大部分父代特征
            self.ax = min(max(0, parent.ax + r.randint(-3, 3)), 255)
            self.ay = min(max(0, parent.ay + r.randint(-3, 3)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.bx = r.randint(0, 255)
            self.by = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.bx = min(max(0, parent.bx + r.randint(-15, 15)), 255)
            self.by = min(max(0, parent.by + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.bx = min(max(0, parent.bx + r.randint(-3, 3)), 255)
            self.by = min(max(0, parent.by + r.randint(-3, 3)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.cx = r.randint(0, 255)
            self.cy = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.cx = min(max(0, parent.cx + r.randint(-15, 15)), 255)
            self.cy = min(max(0, parent.cy + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.cx = min(max(0, parent.cx + r.randint(-3, 3)), 255)
            self.cy = min(max(0, parent.cy + r.randint(-3, 3)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.dx = r.randint(0, 255)
            self.dy = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.dx = min(max(0, parent.dx + r.randint(-15, 15)), 255)
            self.dy = min(max(0, parent.cy + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.dx = min(max(0, parent.dx + r.randint(-3, 3)), 255)
            self.dy = min(max(0, parent.dy + r.randint(-3, 3)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.ex = r.randint(0, 255)
            self.ey = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.ex = min(max(0, parent.ex + r.randint(-15, 15)), 255)
            self.ey = min(max(0, parent.ey + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.ex = min(max(0, parent.ex + r.randint(-3, 3)), 255)
            self.ey = min(max(0, parent.ey + r.randint(-3, 3)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.fx = r.randint(0, 255)
            self.fy = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.fx = min(max(0, parent.fx + r.randint(-15, 15)), 255)
            self.fy = min(max(0, parent.fy + r.randint(-15, 15)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.fx = min(max(0, parent.fx + r.randint(-3, 3)), 255)
            self.fy = min(max(0, parent.fy + r.randint(-3, 3)), 255)
        # color
        if mutate_or_not(self.max_mutate_rate):
            self.color.r = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.color.r = min(max(0, parent.color.r + r.randint(-30, 30)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.color.r = min(max(0, parent.color.r + r.randint(-5, 5)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.color.g = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.color.g = min(max(0, parent.color.g + r.randint(-30, 30)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.color.g = min(max(0, parent.color.g + r.randint(-5, 5)), 255)

        if mutate_or_not(self.max_mutate_rate):
            self.color.b = r.randint(0, 255)
        if mutate_or_not(self.mid_mutate_rate):
            self.color.b = min(max(0, parent.color.b + r.randint(-30, 30)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.color.b = min(max(0, parent.color.b + r.randint(-5, 5)), 255)

        # alpha
        if mutate_or_not(self.mid_mutate_rate):
            self.color.a = r.randint(90,115)
        if mutate_or_not(self.mid_mutate_rate):
            self.color.a = min(max(0, parent.color.a + r.randint(-30, 30)), 255)
        if mutate_or_not(self.min_mutate_rate):
            self.color.a = min(max(0, parent.color.a + r.randint(-3, 3)), 255)

    def draw_it(self, size=(256, 256)):
        '''
        画多边形
        '''

        total = [(self.ax, self.ay), (self.bx, self.by), (self.cx, self.cy), (self.dx, self.dy), (self.ex, self.ey),
                 (self.fx, self.fy)]
        x = []
        for i in range(5):
            x.append(total[i])
        self.img_t = Image.new('RGBA', size)
        draw = ImageDraw.Draw(self.img_t)
        draw.polygon(x, fill=(self.color.r, self.color.g, self.color.b, self.color.a))
        return self.img_t


class Canvas(object):
    mutate_rate = 0.01  # 变异概率
    size = (256, 256)
    target_pixels = []

    def __init__(self):
        self.polygons = []
        self.match_rate = 0
        self.img = None

    def add_ploygon(self, num=1):
        for i in range(0, num):
            polygon = Polygons()  # 生成一个多边形
            self.polygons.append(polygon)  # 把多边形加入画板

    def mutate_from_parent(self, parent):  # 从父代变异进化
        flag = False
        for polygon in parent.polygons:   # 取出画板内的每个图形，判断是否需要从父代变异
            t = polygon
            if mutate_or_not(self.mutate_rate):
                flag = True
                a = Polygons()
                a.mutate_from(t)  # 从父代变异
                self.polygons.append(a)
                continue
            self.polygons.append(t)
        if not flag:    # 如果一直没有变异，则随机抽出一个图形变异
            self.polygons.pop()
            t = parent.polygons[r.randint(0, len(parent.polygons) - 1)]
            a = Polygons()
            a.mutate_from(t)
            self.polygons.append(a)

    def calc_match_rate(self):  # 计算适应度
        if self.match_rate > 0:
            return self.match_rate
        self.match_rate = 0
        self.img = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(self.img)
        draw.polygon([(0, 0), (0, 255), (255, 255), (255, 0)], fill=(255, 255, 255, 255))
        for polygon in self.polygons:
            self.img = Image.alpha_composite(self.img, polygon.img_t or polygon.draw_it(self.size))
        arrs = [np.array(x) for x in list(self.img.split())]  # 分解为RGBA四通道
        for i in range(4):  # 对RGB通道三个矩阵分别与目标图片相应通道作差取平方加和评估相似度
            self.match_rate += np.sum(np.square(arrs[i] - self.target_pixels[i]))
    def draw_it(self, i):
        # self.img.save(os.path.join(PATH, "%s_%d_%d_%d.png" % (PREFIX, len(self.triangles), i, self.match_rate)))
        self.img.save(os.path.join(PATH, "%d.png" % (i)))

def main():
    global LOOP, PREFIX, PATH, TARGET, TRIANGLE_NUM
    # 声明全局变量
    best_mate = []  # 保存最好适应度
    worst_mate = []  # 保存每一代最差适应度
    middle_mate = []  # 保存平均适应度
    img = Image.open(TARGET).resize((256, 256)).convert('RGBA')
    size = (256, 256)
    Canvas.target_pixels = [np.array(x) for x in list(img.split())]
    # 生成一系列的图片作为父本，选择其中最好的一个进行遗传
    parentList = []
    for i in range(50):
        if(i%10==0):
            print('正在生成第%d个初代个体' % (i))
        parentList.append(Canvas())
        parentList[i].add_ploygon(TRIANGLE_NUM)
        parentList[i].calc_match_rate()
    parent = sorted(parentList, key=lambda x: x.match_rate)[0]
    del parentList
    gc.collect()  # 清楚内存空间
    # 进入遗传算法的循环
    i = 0
    while i <= MAXN:
        childList = []
        sum_data = 0
        # 从父代变异出50代
        for j in range(10):
            childList.append(Canvas())
            childList[j].mutate_from_parent(parent)
            childList[j].calc_match_rate()
        child = sorted(childList, key=lambda x: x.match_rate)[0]
        worst_child = sorted(childList, key=lambda x: x.match_rate)[9]
        # 选择其中适应度最好的一个个体
        if i % LOOP == 0:
            print('%10d parent rate %11d \t child1 rate %11d' % (i, parent.match_rate, child.match_rate))
            for k in range(10):
                sum_data += childList[k].match_rate
            ave = sum_data / 10
        del childList
        gc.collect()
        parent.calc_match_rate()
        parent = parent if parent.match_rate < child.match_rate else child
        # 如果子代比父代更适应环境，那么子代成为新的父代
        # 否则保持原样
        child = None
        if i % LOOP == 0:
            # 每隔LOOP代保存一次图片
            best_mate.append(parent.match_rate)
            worst_mate.append(worst_child.match_rate)
            middle_mate.append(ave)
            parent.draw_it(i)
            # print(parent.match_rate)
            # print ('%10d parent rate %11d \t child1 rate %11d' % (i, parent.match_rate, child.match_rate))
        i += 1
    x = [i for i in range(0, MAXN + 1, 100)]
    plt.plot(x, best_mate)
    plt.plot(x, worst_mate)
    plt.plot(x, middle_mate)

    plt.title('适应度-代数折线图')
    plt.xlabel('代数')
    plt.ylabel('适应度')
    plt.legend((u"最好", u"最坏", u"平均"), loc="best")
    plt.show()


def get_parameter():
    global MAXN, LOOP, TRIANGLE_NUM
    f = open("parameter.txt")
    line = f.readline()
    MAXN = int(line)

    line = f.readline()
    LOOP = int(line)

    line = f.readline()
    TRIANGLE_NUM = int(line)
    f.close()


'''
定义全局变量，获取待处理的图片名
'''
# NAME = input('请输入原图片文件名：')
NAME = 'model.jpg'
MAXN = 15000
LOOP = 100
PREFIX = NAME.split('/')[-1].split('.')[0]  # 取文件名
PATH = os.path.abspath('.')  # 取当前路径
PATH = os.path.join(PATH,'results')
TARGET = NAME  # 源图片文件名
TRIANGLE_NUM = 256  # 三角形个数

if __name__ == '__main__':
    #print('开始进行遗传算法')
    get_parameter()
    input()
    main()