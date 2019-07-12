from PIL import Image
import numpy as np


word_count=7

img=Image.open("./origin_cut_img/1_new.jpg")
width,height=img.size

per_height=int(height/word_count)
img_array=np.asanyarray(img)

out=None
for index in range(word_count):
    st=index * per_height
    ed=(index+1) * per_height
    if out is None:
        out=img_array[st:ed, :, :]
    else:
        out=np.concatenate([out,img_array[st:ed, :, :]],axis=1)

Image.fromarray(out).save("./temp/temp_1.jpg")

###########将直方图转化成横置图###########
def convert_histogram(origin_img,word_count):
    width, height = origin_img.size
    bound_size = height % word_count
    if bound_size % 2 == 0:
        top, down = bound_size / 2, bound_size / 2
    else:
        top, down = bound_size // 2, bound_size // 2 + 1
    per_height = int((height - top - down) / word_count)
    img_array = np.asanyarray(origin_img)[int(top):int(height - down), :, :]
    out = None
    for index in range(word_count):
        st = index * per_height
        ed = (index + 1) * per_height
        if out is None:
            out = img_array[st:ed, :, :]
        else:
            out = np.concatenate([out, img_array[st:ed, :, :]], axis=1)
    return out


