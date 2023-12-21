import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba  
from collections import Counter  
from pyecharts import options as opts 
# import streamlit_echarts
import streamlit.components.v1 as components
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from pyecharts.charts import Scatter
from pyecharts.charts import Funnel
import re
import time

#去掉除中文外所有内容
def rm(s):  
    return re.sub(r'[^\u4e00-\u9fa5]','',s)

#确定x轴显示的个数
def x_num(word_counts):
    if len(word_counts)>20:
        n=20
    else:
        n=len(word_counts)
    return n

#数据处理,对文本进行分词，并去掉单字词
def data_processing(items):
    word_counts=Counter()
    for item in items:
        words = jieba.cut(rm(item.text))
        words = [s for s in words if len(s) != 1]
        word_counts.update(words)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    return word_counts

#将图像转化为html，然后输出到streamlit上(这里设置的是容器大小)
def getpaintings(painting):
    line2Html = painting.render_embed()
    components.html(line2Html,height=800, width=800)
    return

#生成柱状图
def paint_bar1(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    bar = Bar(init_opts=opts.InitOpts(width='800px', height='400px'))
    bar.add_xaxis(list(word_counts.keys())[:n])
    bar.add_yaxis("词频", list(word_counts.values())[:n])
    bar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),title_opts=opts.TitleOpts(title="关键词出现频率柱状图"))
    getpaintings(bar)
    return

#生成柱状图（反）
def paint_bar2(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    bar = Bar(init_opts=opts.InitOpts(width='500px', height='600px'))
    bar.add_xaxis(list(word_counts.keys())[:n])
    bar.add_yaxis("词频", list(word_counts.values())[:n])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="关键词出现频率柱状图"))
    bar.reversal_axis()
    getpaintings(bar)
    return

#生成线形图
def paint_line(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    line = Line(init_opts=opts.InitOpts(width='800px', height='400px'))
    line.add_xaxis(list(word_counts.keys())[:n])  
    line.add_yaxis("词频", list(word_counts.values())[:n])
    line.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),title_opts=opts.TitleOpts(title="关键词出现频率线形图"))  
    getpaintings(line)
    return

#生成饼状图
def paint_pie(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px'))
    pie.add("关键词出现频率饼状图", list(word_counts.items())[:n])
    getpaintings(pie)
    return

#生成词云图
def paint_wordcloud(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    wordcloud = WordCloud(init_opts=opts.InitOpts(width='800px', height='400px'))
    wordcloud.add("关键词出现频率词云图", list(word_counts.items())[:n],word_size_range=[20, 80],shape='star')
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="关键词出现频率词云图"))
    getpaintings(wordcloud)
    return

#生成漏斗图
def paint_funnel(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    funnel = Funnel(init_opts=opts.InitOpts(width='800px', height='600px'))
    funnel.add('关键词出现频率漏斗图',list(word_counts.items())[:n])
    getpaintings(funnel)
    return

#生成散点图
def paint_scatter(items):
    word_counts=data_processing(items)
    n = x_num(word_counts)
    scatter = Scatter(init_opts=opts.InitOpts(width='800px', height='400px'))
    scatter.add_xaxis(list(word_counts.keys())[:n])  
    scatter.add_yaxis("词频", list(word_counts.values())[:n])
    scatter.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),title_opts=opts.TitleOpts(title="关键词出现频率散点图"))  
    getpaintings(scatter)
    return

st.set_page_config(page_title="网站关键词出现频率", page_icon="🐛")
st.sidebar.header("python爬虫")
add_selectbox = st.sidebar.selectbox(
    "您希望以哪种图显示：",
    ("柱状图1", "柱状图2", "线形图", "饼状图", "词云图", "漏斗图", "散点图")
)
st.markdown("# 网站关键词出现频率")
url = st.text_input('请输入你想爬取的网站的url：',placeholder='例如：https://www.baidu.com')
if st.button('查询'):
    if url.strip() !='':
        try: 
            req = requests.get(url,timeout=5000)
            encoding = req.encoding if 'charset' in req.headers.get('content-type', '').lower() else None
            soup = BeautifulSoup(req.content, 'html.parser', from_encoding=encoding)
            nav_items =soup.find_all('div')+soup.find_all('a')+soup.find_all('span')
            if(data_processing(nav_items) != {}):
                with st.spinner("加载中..."):
                    time.sleep(2)
                    if add_selectbox == '柱状图1': 
                        paint_bar1(nav_items)
                    elif add_selectbox == '柱状图2':
                        paint_bar2(nav_items)
                    elif add_selectbox == '线形图':
                        paint_line(nav_items)
                    elif add_selectbox == '饼状图':
                        st.write("<h5>关键词出现频率饼状图</h5>", unsafe_allow_html=True)
                        paint_pie(nav_items)
                    elif add_selectbox == '词云图':
                        paint_wordcloud(nav_items)
                    elif add_selectbox == '漏斗图':
                        st.write("<h5>关键词出现频率漏斗图</h5>", unsafe_allow_html=True)
                        paint_funnel(nav_items)
                    elif add_selectbox == '散点图':
                        paint_scatter(nav_items)
            else:
                st.write("<h5 style='color:red'>未爬取到任何内容，请尝试其他url！</h5>",unsafe_allow_html=True) 
        except Exception as err:
            st.write("<h5 style='color:red'>出错了，请重新再试一次或换个url吧~~</h5>",unsafe_allow_html=True)
    else:
        st.write("<h5 style='color:red'>请输入url</h5>",unsafe_allow_html=True)