import streamlit as st
import torch
from PIL import Image
from io import *
import glob
from datetime import datetime
import os
import wget
import time

## CFG
#cfg_model_path = "models/yourModel.pt"

cfg_enable_url_download = False
#if cfg_enable_url_download:
    #url = "https://archive.org/download/yoloTrained/yoloTrained.pt"  # Configure this if you set cfg_enable_url_download to True
    #cfg_model_path = f"models/{url.split('/')[-1:][0]}"  # config model path from url name


## END OF CFG


def pretrained_yolov5(device="CPU"):
        image_file = st.file_uploader("Загрузить изображение:", type=['png', 'jpeg', 'jpg'])
        col1, col2 = st.columns(2)
        if image_file is not None:
            img = Image.open(image_file)
            with col1:
                st.image(img, caption='Загруженное', use_column_width='always')
            ts = datetime.timestamp(datetime.now())
            imgpath = os.path.join('data/uploads', str(ts) + image_file.name)
            outputpath = os.path.join('data/outputs', os.path.basename(imgpath))
            with open(imgpath, mode="wb") as f:
                f.write(image_file.getbuffer())

            # call Model prediction--
            model = torch.hub.load("ultralytics/yolov5", "yolov5m", pretrained=True)
            model.cuda() if device == 'cuda' else model.cpu()
            pred = model(imgpath)
            pred.render()  # render bbox in image
            for im in pred.ims:
                im_base64 = Image.fromarray(im)
                im_base64.save(outputpath)

            # --Display predicton

            img_ = Image.open(outputpath)
            with col2:
                st.image(img_, caption='Результат', use_column_width='always')


def custom_yolov5s(device="CPU"):
    st.header('Обученная YOLOv5s на кастомном датасете')
    st.subheader("Датасет: виды перерабатываемого и неперерабатываемого мусора")
    st.text("В перспективе такую модель можно использовать на мусороперерабатывающий заводе для быстрой сортировки или для дронов, собирающих мусор в природных зонах вроде лесов и океанов.")
    st.image("metrcis_screenshot.png", caption="Лосс и метрики обученной модели")
    imgpath = glob.glob('data/images/*')
    imgsel = st.slider('Выбрать случайную картинку из тестовой выборки', min_value=1, max_value=len(imgpath), step=1)
    image_file = imgpath[imgsel - 1]
    submit = st.button("Начать детекцию")
    col1, col2 = st.columns(2)
    with col1:
        img = Image.open(image_file)
        st.image(img, caption='Выбранное изображение', use_column_width='always')
    with col2:
        if image_file is not None and submit:
            # call Model prediction--
            model = torch.hub.load("ultralytics/yolov5", "custom", path='data/models/yoloTrained.pt', force_reload=True)
            pred = model(image_file)
            pred.render()  # render bbox in image
            for im in pred.ims:
                im_base64 = Image.fromarray(im)
                im_base64.save(os.path.join('data/outputs', os.path.basename(image_file)))
                # --Display predicton
                img_ = Image.open(os.path.join('data/outputs', os.path.basename(image_file)))
                st.image(img_, caption='Результат')



def main():

    option = st.sidebar.radio("Модель", ['Pretrained YOLOv5m', 'Pretrained YOLOv5m - video','Custom dataset YOLOv5s'])

    st.header('Проект для DLS (семестр Осень, 2022): Detection')
    st.subheader("Автор: Марунько Анна")
    st.sidebar.markdown("https://github.com/AnnBengardt/DLS-Detection-Final_project")
    if option == "Pretrained YOLOv5m":
        pretrained_yolov5()
    elif option == "Custom dataset YOLOv5s":
        custom_yolov5s()
    elif option == "Pretrained YOLOv5m - video":
        pass


if __name__ == '__main__':
    main()


# Downlaod Model from url.
@st.cache
def loadModel(url):
    start_dl = time.time()
    model_file = wget.download(url, out="models/")
    finished_dl = time.time()
    print(f"Model Downloaded, ETA:{finished_dl - start_dl}")


if cfg_enable_url_download:
    loadModel()