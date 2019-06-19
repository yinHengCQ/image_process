from PIL import Image
import os,json,cv2
import numpy as np


def convert_image(file_name,index,err_index):
    txt_dict=dict()
    # kernel = np.ones((2, 2), np.uint8)
    try:
        with open('./data/txt_train/{}'.format(file_name), encoding='utf-8') as f:
            for line in f.readlines():
                text_list = line.strip().split(',')
                if '###' == text_list[-1]:
                    continue
                loc = (float(text_list[0]), float(text_list[1]), float(text_list[4]), float(text_list[5]))
                temp_text=text_list[-1].strip()
                if len(temp_text)>20:
                    continue
                temp_img=Image.open('./data/image_train/{}jpg'.format(file_name[:-3])).crop(loc)

                ################判断是否是竖长型图片###############################
                if len(temp_text) > 1 and (abs(float(text_list[1])-float(text_list[5]))/abs(float(text_list[0])-float(text_list[4]))>2):
                    temp_img=temp_img.rotate(90, expand=1)
                ###################################################################

                temp_width=int(32*(temp_img.width/temp_img.height))
                if temp_width>280:
                    continue
                temp_img=np.asarray(temp_img.resize((temp_width, 32)))

                cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),temp_img)
                txt_dict[str(index)] = temp_text
                index += 1

                cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY))
                txt_dict[str(index)] = temp_text
                index += 1

                cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.cvtColor(temp_img, cv2.COLOR_BGR2HSV))
                txt_dict[str(index)] = temp_text
                index += 1

                cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.cvtColor(temp_img, cv2.COLOR_BGR2LAB))
                txt_dict[str(index)] = temp_text
                index += 1

                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.cvtColor(temp_img, cv2.COLOR_BGR2HLS))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.cvtColor(temp_img, cv2.COLOR_BGR2LUV))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.morphologyEx(temp_img, cv2.MORPH_GRADIENT, kernel))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.morphologyEx(temp_img, cv2.MORPH_TOPHAT, kernel))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.erode(temp_img,kernel,iterations = 1))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.dilate(temp_img,kernel,iterations = 1))
                # txt_dict[str(index)] = temp_text
                # index += 1

                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.GaussianBlur(temp_img,(3,3),0))
                # txt_dict[str(index)] = temp_text
                # index += 1
                #
                # cv2.imwrite('./data/image_train_cut_plus/{}.jpg'.format(index),cv2.blur(temp_img, (3,3)))
                # txt_dict[str(index)] = temp_text
                # index += 1
    except:
        err_index+=1
    return index,txt_dict,err_index


def cut_train_img():
    index=0
    err_index=0
    txt_dict=dict()
    for f in os.listdir('./data/txt_train'):
        print(index,err_index)
        out_index,out_txt_dict,out_err_index=convert_image(f,index,err_index)
        index=out_index
        err_index=out_err_index
        txt_dict.update(out_txt_dict)

    with open("./train_text_init_plus.json","w",encoding="utf-8") as f:
        json.dump(txt_dict,f,ensure_ascii=False)


def generate_word_dict():
    with open("./train_text_init_plus.json", "r", encoding="utf-8") as f:
        txt_dict=json.load(f)
    word_set=set()
    for k,v in txt_dict.items():
        for i in v.strip():
            word_set.add(i)
    word_out=dict()
    word_out_temp=dict()
    for index,i in enumerate(word_set):
        word_out_temp[str(index+1)]=i
    for k,v in word_out_temp.items():
        word_out[v]=k
    with open("./train_word_dict_plus.json","w",encoding="utf-8") as f:
        json.dump(word_out,f,ensure_ascii=False)


def block_zore_label():
    with open("./train_text_init_plus.json", "r", encoding="utf-8") as f:
        txt_dict=json.load(f)
    out=dict()
    for k,v in txt_dict.items():
        if v=="-1" or v=="":
            continue
        else:
            out[k]=v
    with open("./train_text_plus.json","w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False)


cut_train_img()
generate_word_dict()
block_zore_label()

