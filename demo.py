# coding: utf-8

import json
import os
import random
import time

from PIL import Image
from PIL import ImageFilter
from PIL.Image import Resampling

from model.capthafactory import CaptchaFactory
from model.utils import CaptchaUtils


def char_custom_fn(single_char):
    # do something you wanted
    # return single_char.filter(ImageFilter.GaussianBlur)
    # 生成30到50之间的随机数
    random_num = random.randint(30, 50)
    single_char = single_char.resize((random_num, random_num), Resampling.LANCZOS)
    return single_char


def bg_custom_fn(bg):
    # do something you wanted
    # return bg.filter(ImageFilter.GaussianBlur)
    return bg


def main():
    project_name = "demo"
    with open("configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[char_custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    index = 100000
    while index:
        file_name = time.time()
        captcha = demo_factory.generate_captcha()
        captcha.save("output/%s/%s.jpg" % (project_name, file_name))
        # print(captcha.text, captcha.num)
        # 读取xml_main.xml文件，并将文件中的内容替换为生成的验证码
        with open("main_xml.txt", "r", encoding="utf-8") as fp:
            xml_content = fp.read()
        xml_content = xml_content.replace("-filename-", str(file_name) + ".jpg")
        char_pos = captcha.char_pos
        final_object = ""
        for i in range(len(char_pos)):
            with open("object_xml.txt", "r", encoding="utf-8") as fp:
                xml_obj = fp.read()
            xml_obj = xml_obj.replace("-x-", str(char_pos[i][0]))
            xml_obj = xml_obj.replace("-y-", str(char_pos[i][1]))
            xml_obj = xml_obj.replace("-width-", str(char_pos[i][2]+char_pos[i][0]))
            xml_obj = xml_obj.replace("-height-", str(char_pos[i][3]+char_pos[i][1]))
            xml_obj = xml_obj.replace("-class_name-", captcha.text[i])
            final_object += xml_obj
        xml_content = xml_content.replace("-object-", final_object)
        with open("output/%s/%s.xml" % (project_name, file_name), "w", encoding="utf-8") as fp:
            fp.write(xml_content)
        index -= 1
        print(index)
        time.sleep(0.01)


if __name__ == "__main__":
    main()
    print("done")
