import re
import pandas
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import font_manager
import openpyxl


def get_html(url):
    try:
        r = requests.get(url)  # 使用get来获取网页数据
        r.raise_for_status()  # 如果返回参数不为200，抛出异常
        r.encoding = r.apparent_encoding  # 获取网页编码方式
        return r.text  # 返回获取的内容
    except:
        return '错误'


def save(html):
    # 解析网页
    soup = BeautifulSoup(html, 'html.parser')  # 指定Beautiful的解析器为“html.parser”
    with open('./data/Cartoon_data.txt', 'r+', encoding='UTF-8') as f:
        f.write(soup.text)
    # 定义好相关列表准备存储相关信息
    name = []  # 动漫名字
    bfl = []  # 播放量
    scs = []  # 收藏数
    # 动漫名字存储
    for tag in soup.find_all('div', class_='info'):
        bf = tag.a.string
        name.append(str(bf))
    print(name)
    # 播放量存储
    for tag in soup.find_all('div', class_='detail'):
        bf = tag.find('span', class_='data-box').get_text()
        # 统一单位为‘万’
        if '亿' in bf:
            num = float(re.search(r'\d(.\d)?', bf).group()) * 10000
            bf = num
        else:
            bf = re.search(r'\d*(\.)?\d', bf).group()
        bfl.append(float(bf))
    print(bfl)
    # 收藏数
    for tag in soup.find_all('div', class_='detail'):
        sc = tag.find('span', class_='data-box').next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        sc = re.search(r'\d*(\.)?\d', sc).group()
        scs.append(float(sc))
    print(scs)
    # 存储至excel表格中
    info = {'动漫名': name, '播放量(万)': bfl, '评论数(万)': pls, '收藏数(万)': scs, '综合评分': TScore}
    dm_file = pandas.DataFrame(info)
    dm_file.to_excel('Cartoon.xlsx', sheet_name="动漫数据分析")
    # 将所有列表返回
    return name, bfl, pls, scs, TScore


def view(info):
    my_font = font_manager.FontProperties(fname='./data/STHeiti Medium.ttc')  # 设置中文字体（图标中能显示中文）
    dm_name = info[0]  # 番剧名
    dm_play = info[1]  # 番剧播放量
    dm_favorite = info[2]  # 番剧收藏数
    # 为了坐标轴上能显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 播放量和收藏数对比
    # 播放量条形图
    fig, ax1 = plt.subplots()
    plt.bar(dm_name, dm_play, color='cyan')
    plt.title('播放量和收藏数数据分析')
    plt.ylabel('播放量（万）')
    ax1.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')
    # 收藏数折线图
    ax2 = ax1.twinx()  # 组合图
    ax2.plot(dm_favorite, color='yellow')  # 设置线粗细，节点样式
    plt.ylabel('收藏数（万）')
    plt.plot(1, label='播放量', color="green", linewidth=5.0)
    plt.plot(1, label='收藏数', color="yellow", linewidth=1.0, linestyle="-")
    plt.legend()
    plt.savefig(r'Compare.png', dpi=1000, bbox_inches='tight')


def main():
    url = 'https://www.bilibili.com/v/popular/rank/bangumi'  # 网址
    html = get_html(url)  # 获取返回值
    info = save(html)
    view(info)


if __name__ == '__main__':
    main()
