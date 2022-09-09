# 虚拟身份证生成工具

## 简介

用真实身份证背景做模板，生成假的个人信息和头像画在模板上

## 1 环境准备

python 3.9.13
pytorch 1.12.1
matplotlib 3.5.2

## 2 数据集

> datasets/card/

存放虚拟身份证的文件夹
> dataset/face/
 
存放虚拟人像的文件夹

> dataset/template.jpg

模板身份证图片

## 3 运行程序

直接运行

main.py

输出虚拟身份证图像到指定目录(默认为 **datasets/card/**)