import random
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import matplotlib.pyplot as plt


def getinfo():
    info = {
        '姓名': {'内容': '徐  乐', '位置': (174, 114), '大小': 32},
        '性别': {'内容': '男', '位置': (173, 178), '大小': 26},
        '民族': {'内容': '汉', '位置': (314, 178), '大小': 26},
        '年': {'内容': '1966', '位置': (175, 240), '大小': 26},
        '月': {'内容': '11', '位置': (280, 239), '大小': 26},
        '日': {'内容': '  2', '位置': (346, 238), '大小': 26},
        '地址1': {'内容': '安徽省宿州市埇桥区朱仙', '位置': (175, 292), '大小': 26},
        '地址2': {'内容': '庄镇', '位置': (175, 330), '大小': 26},
        '号码': {'内容': '652901196611026716', '位置': (277, 440), '大小': 36},
    }
    return info


def setname(info):
    if len(name_container) == 0:
        first_name = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '诸葛', '欧阳', '夏侯', '上官']
        last_name = ['鹏', '涛', '炎', '彬', '鹤', '轩', '越', '彬', '风', '华', '靖', '琪', '明', '诚', '高', '格',
                     '光',
                     '华', '国', '源', '冠', '宇', '晗', '昱', '涵', '润', '翰', '飞', '香菱', '孤云', '水蓉', '雅容',
                     '飞烟', '雁荷', '代芙', '醉易', '夏烟', '山梅', '若南', '恨桃', '依秋', '依波']
        for fname in first_name:
            for lname in last_name:
                if len(fname) == 1 and len(lname) == 1:
                    name = fname + '  ' + lname
                else:
                    name = fname + lname
                name_container.append(name)

    random.shuffle(name_container)
    name = name_container.pop()
    info['姓名']['内容'] = name


def setsex(info):
    sex_all = ['男', '女']
    nation_all = ['汉', '蒙古', '回', '藏', '维吾尔']
    sex = random.choice(sex_all)
    nation = random.choice(nation_all)
    info['性别']['内容'] = sex
    info['民族']['内容'] = nation


def setbirthday(info):
    year = str(random.randint(1970, 2000))
    month = str(random.randint(1, 12))
    if len(month) == 1:
        month = '  ' + month
    if month in [1, 3, 5, 7, 8, 10, 11]:
        day = str(random.randint(1, 31))
    elif month == 2:
        day = str(random.randint(1, 28))
    else:
        day = str(random.randint(1, 30))
    if len(day) == 1:
        day = '  ' + day
    info['年']['内容'] = year
    info['月']['内容'] = month
    info['日']['内容'] = day


def setaddress(info):
    province_all = ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省',
                    '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省',
                    '陕西省', '甘肃省', '青海省', '台湾省']
    city_all = ['东阳市', '西阳市', '南阳市', '北阳市']
    region_all = ['经开区', '高新区', '滨湖区', '示范区', '政务区']
    town_all = ['高塘岭镇', '星城镇', '丁字镇', '茶亭镇', '桥驿镇', '东城镇', '铜官镇', '靖港镇', '乔口镇', '乌山镇']
    province = random.choice(province_all)
    city = random.choice(city_all)
    region = random.choice(region_all)
    town = random.choice(town_all)
    address = province + city + region + town
    if len(address) > 11:
        info['地址1']['内容'] = address[:11]
        info['地址2']['内容'] = address[11:]
    else:
        info['地址1']['内容'] = address[:11]
        info['地址2']['内容'] = ''


def setnumber(info):
    num = random.randint(100000000000000000, 999999999999999999)
    num = str(num)
    info['号码']['内容'] = num


def drawinfo(img, info):
    img_array = Image.fromarray(img)
    draw = ImageDraw.Draw(img_array)
    for key, value in info.items():
        if value['内容'] == None:
            continue
        content = value['内容']
        position = value['位置']
        size = value['大小']
        font_hei = ImageFont.truetype('font/simhei.ttf', size)
        font_bt = ImageFont.truetype('font/OCR-B 10 BT.ttf', size)
        font_arial = ImageFont.truetype('font/arial.ttf', size)
        if key == '号码':
            draw.text(position, content, font=font_bt, fill=(0, 0, 0))
        elif key == '年' or key == '月' or key == '日':
            draw.text(position, content, font=font_arial, fill=(0, 0, 0))
        else:
            draw.text(position, content, font=font_hei, fill=(0, 0, 0))
    photo = np.array(img_array)
    return photo


def drawpicture(photo, faces):
    face_path = random.choice(faces)
    face = cv2.imread(face_path)
    face = cv2.resize(face, (216, 256))
    # 裁剪头像区域
    roi = photo[142:398, 480:696]
    # 创建头像掩膜
    faceGray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(faceGray, 250, 255, cv2.THRESH_BINARY)
    maskInv = cv2.bitwise_not(mask)
    # 保留除头像外的背景
    photoBg = cv2.bitwise_and(roi, roi, mask=mask)
    faceFg = cv2.bitwise_and(face, face, mask=maskInv)
    # 融合背景和头像，粘贴在原图
    dst = cv2.add(photoBg, faceFg)
    photoCopy = photo.copy()
    photoCopy[142:398, 480:696] = dst
    return photoCopy


def gamma_trans(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


if __name__ == '__main__':
    # 读取身份证模板和假人脸
    img_original = cv2.imread('datasets/template.jpg')
    faces = []
    for dirpath, dirnames, filenames in os.walk('datasets/face'):
        for filename in filenames:
            faces.append(os.path.join(dirpath, filename))
    # 设定模板，设计一个姓名容器检测姓名重复
    info = getinfo()
    name_container = []
    for i in range(500):
        # 随机生产基本信息
        setname(info)
        setsex(info)
        setbirthday(info)
        setaddress(info)
        setnumber(info)
        # 添加文本
        photo = drawinfo(img_original, info)
        # 添加假人像
        photo = drawpicture(photo, faces)
        # 调节亮度，保存图片
        photo_light = gamma_trans(photo, 0.8)
        path = 'datasets/card/' + str(i) + '.jpg'
        cv2.imwrite(path, photo_light)

    plt.imshow(photo_light[:, :, ::-1])
    plt.show()
