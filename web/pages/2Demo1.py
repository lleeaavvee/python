import streamlit as st
import pyqrcode  
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="2Generate QR code", page_icon="🖼️")
st.sidebar.header("二维码生成(demo),图片暂时转换不了")
st.markdown("# 二维码生成")
add_selectbox = st.sidebar.selectbox(
    "您想要将哪种文件转化为二维码：",
    ('网址','图片')
)
if add_selectbox == '网址':
    url = st.text_input('请输入你想转化成二维码的网站的url：',placeholder='例如：https://www.baidu.com')
    if st.button('生成'):
        qrc = pyqrcode.create(url)
        qrc.png('123.png', scale=10)
        image = Image.open('123.png')
        st.image(image)
else:
    photo=st.file_uploader('请上传你想转化成二维码的图片：', type=None, accept_multiple_files=False)
    if st.button('生成'):
        bytes_data = photo.getvalue()
        bytes_data = BytesIO(bytes_data)
        upload_img = Image.open(bytes_data)
        st.image(upload_img)
