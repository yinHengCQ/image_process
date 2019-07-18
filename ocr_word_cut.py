#coding:utf-8
from PIL import Image
import numpy as np
import random,os,json,cv2,math
from math import *


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


###########将横置图转化成单个字体随机高低###########
def convert_word_height(origin_img,word_count,random_height=10):
    width, height = origin_img.size
    per_width = int(width / word_count)
    img_array = np.asanyarray(origin_img)
    out = np.ones([height + random_height, width, 3], dtype=np.uint8) * 255
    for index in range(word_count):
        st = index * per_width
        ed = (index + 1) * per_width
        n = random.randint(height, height + random_height)
        out[n - height:n, st:ed, :] = img_array[:, st:ed, :]
    return out


def is_contains_filter_word(txt):
    filter = """Ⅳ－█━〉➉✖⑤ɡ➂➃➄➅➆➇➈↻↖ϟ❃☎︿▎➡↔✙❝❞｛｝∑ìūθ℉П☰♪ò＝ōǒ㎏ⓔ≈ã▷∞﹣⊙卍∈ε♂│‖∟¬✻€φàêôṚ｀⺕◆％ʒ□Üɔⓤ├▕β／Ｑ▍É‹＼ＦＹⓒＢＮＺ４ＨＰＫ８６ｋｊℰ⊥∅〈äⓢáÁｙｄＤｖｑｘＭＷｗｚΛ✞›｜Я∫➁﹢ㅣ⊕Θ²▸✚➀﹝﹞ⓜ↗©əⅫⅠⅤⅥⅦⅧⅨⅩⅪ［］▏éúóīǐǎǔα◀┌┘＄✲＃◇✰㊣☼♫△⑩´π∩ㄑⒸ＜＞āí๑※❄Ⓣ³ºø♬❹≦ˋ▫＋′μΦⓈ■③④∧﹤﹥∨▶Ұ〖〗Ⓗ⑳◥'?；✆÷▲▪❾①⑧⑥⑦②『．▼"#*·+★、！（）：®•丶—¥，。～◎[]./√￥☆…【】︽︾%-●()☯←➞↵〔〕？!™“”►О|\}{:;=~`$@&⑴⑵⑶∣‘’>』♥^<↑←↓→《》〞Ⓡξ⇧↹æABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"""
    for word in txt:
        if word in filter:
            return True
    return False


def cut_img_with_annotation(img_file,annotation,save_dir,word_index,specify_word_list,word_img_dict):
    x=[float(annotation[0]), float(annotation[2]), float(annotation[4]), float(annotation[6])]
    y = [float(annotation[1]), float(annotation[3]), float(annotation[5]), float(annotation[7])]
    loc = (min(x), min(y), max(x), max(y))
    if len(annotation[-1]) > 1 and (abs(loc[3] - loc[1]) / abs(loc[2] - loc[0]) > 1.8):
        pass
    else:
        temp_img = Image.open(img_file).crop(loc)
        temp_width = int(32 * (temp_img.width / temp_img.height))
        temp_img = np.asarray(temp_img.resize((temp_width, 32)))
        per_width=int(temp_width/len(annotation[-1]))
        for index in range(len(annotation[-1])):
            word=annotation[-1][index]
            if word in specify_word_list:
                Image.fromarray(temp_img[:,index*per_width:(index+1)*per_width,:]).resize((32, 32)).save("{}/{}{}.jpg".format(save_dir,word,word_index))
                word_img_dict["{}{}".format(word,word_index)]=word
                word_index += 1
    return word_img_dict,word_index


###########裁剪出含有指定文字并可裁剪的图片###########
def cut_specify_word_img(annotation_dir_path,img_dir_path,save_dir,specify_word_list,word_img_dict_file):
    word_index=0
    word_img_dict=dict()
    error_index=0
    for i in os.listdir(annotation_dir_path):
        with open(os.path.join(annotation_dir_path, i), "r", encoding="utf-8") as f:
            for line in f.readlines():
                line=line.strip().split(",")
                if is_contains_filter_word(line[-1]):
                    continue
                else:
                    for word in line[-1]:
                        if word in specify_word_list:
                           try:
                               word_img_dict, word_index = cut_img_with_annotation("{}/{}jpg".format(img_dir_path, i[:-3]), line, save_dir, word_index,specify_word_list, word_img_dict)
                           except:
                               print(error_index)
                               error_index+=1
    with open(word_img_dict_file,"w",encoding="utf-8") as f:
        json.dump(word_img_dict,f,ensure_ascii=False)


def cut_specify_word_img_demo():
    annotation_dir_path="D:/all_data/ocr1/txt_train"
    img_dir_path="D:/all_data/ocr1/image_train"
    save_dir="D:/all_data/ocr1/specify_word_img"
    specify_word_list="耻─臉曬適護輕乾屉僮憬冀绩垂蔗肺吕烈犹孵炔酮芊俪論語曰習亦說遠來慍為孝犯鮮矣亂務琅愉苓忙碌坦缠純疵婉缎蘋汕栈舶贪婪郵赌廊箍肾捏宋儒刑贈糟數優勢級灣鏜鎢鋼銑塘絲榮獲聞薦課讀會這樣決問題見啟內們執斋説創忽貢轉簡單隨唘琼疙瘩邪恶偶曾巅衔烙亨映桩仰彰帶魚飼種鹦鹉鲤抄渔飛儱釉措崔渎栓缔媛裝飾隙麥鳞躁骶稠瘀滞剧愁晋逍藝輝團際钦寓契脘闷呕泻烁铣脖笼鸽铰沿镍拭烽堪卤骼脏肪聖虱搽蕲硒败恭娴尤拷鹤祈肖蹭碘谧纵棺桉惟截毕竟惬厉陷阱哇帐喂薛荡膛媳孟召唤闯浇篷闹綱秦璐網鐘韓現館貴風歳財興舱噜膳馅烹饪鄂貌惯蕊缚鹰郎殁擬殼嘟槐鲨烷鸦珊攀洱察谐苍阔冯彦渣焗師輪捶励躺龈缦翎枫蝌蚪貨證霞骐骊紀嵌啫瑟掏亩纫碑溜咬凳钰奕竭删符倆棍屌肝虾翅袍岩楠澈骤叛啊否賞暑蒜迭枯懋某似闺沟渴亞製淨嚣貉挠拾誠殖揭昕煜忐忑熬扑楷仝飴钠柑黔踪韶挣悲挫芥腌扶挪纽馒剁爷漾嗽哮喘忏蒲辫侨咔茨徒沾窄荆鷄辜凑饿饥渭錶辧郭暇漯椹融潭詩楽裕摒慎且幽番茄闸谭策邢龚膀悟嗑骚呦府萝孜俗淑竿質諾浑镂妩披宴妥笙绑亜島渝猩贾弦缇曝皆痠涩瑙辟阵谜涮焖糠娟磕玄丢甄晾患梗卒租赁雙爹鬼沸捆曦窖徐遗貼強氟蛀痱撒挤绚蟹闵弄啰酪禦颊頰盏凄壽咒剛愣嚴瑄胭潔過縫遵矩慵寂寞疑卢霾赴狠潤韬虞腮腺嬰溫彈镊組妝皓咻祖鉅餠産挚绅弥雲餅畜敲挥哑痴脉盅雯鲶淚涌夕摘昂雇朴秧伏荔枝镭逃揚苞绻捧勃啥旨偉摈醯炣璀璨腋亭糯婭恼纶抠帥憋吻ē蛮馥榻借奴溉努珺璋丈囡酉廿铬钒玥钨闻髓征俐齊蒄搅奏媲杉矶龋層傘塗檸颠吖熥举廓榛芮盼瞿虑佑垒囤占幹養歲練棘狭買辦備旦薪馬凍疮肿殺劑濃縮硝細蘑锣诊捉証顽丘宸侦愿葱酶菠麓醉饅榈侈蕴臘赤礁鳍鲷钊蜀阙寨诀裔蒋賣閣娥萤氓萧禹亡梧嘛叔邹坪坝旁渐渡弗豚庞逐崎拱霖犀衬阜鞭逗貊頓废歪扎鹭劣疤瓣耦筛牡舌厌桐褂荒蟋蟀爵凶氯苯洽姒峡町澎湃嚼哲岸纬艦攝盜祺董堆垛芃恍灶谓昔虚詢偽話標識謹徹滢绮碍绪Ο锤娣壞敛楓哒喽狒芪胚樹廠鄉縣膠汞锻纷穷針撬锗翡扯泛順逹莊麒届澜绸溺奂拧酬勤乃仞氢灼幂湛係艶镶義磐宛屹摧毁怖魄谋殻邂逅畔撇稻蚂飮滕捍悍給予謢觸衛疹泄與換滩驴秩牟哨唢呐豫挎瀛函仟禮扁凿聆谛沼卵撸窍㝧鼽渊窦澄怀彭琮瑶搬烊趋専終妻韦橹笈舵令肘绷弛坠聘杏苪侠號弘刊蜕茧銀積減額員烛嗖盲泷畸吵泳啸酿姗è塊恪調朕穗坡毡蹈煞剥喔庚嵩践壬淌皎朽甚绽琬剖荫糜湓陌浊呂尴尬裘斐肢淤琥瑪赋朔個颂曜葫蝴籁烩茵淀郡舊鴻漸邏輯點關鍵試測驗權訣導聯編許兢歷屆戰鋒驭呢訊栽侵崋耶呜鐵觀潘詹泌蘆薈猜拳Í皙緣崖辽睫逛蛲蠕蛔拢挺皴陇晃脾涯環衍咽悸煙喧轿兆枸杞摊讴熨碼逢羔霓裳藤恰聊冢缕範烨烯丙锰藕離珞窃靡涡舖跌唑張迁鲩鲟玷勝谎斌埋咚咯崬褚驻贫蛰隋彪妃阎煖總腊該毅櫥彬鹃既庸裱逺霉滔芜祁復嫰跪伺党茯芩忌薬骄履判厄扔贅様尐痤賀衆泸鲍诠顯贰蠶褶呛吨卜郝陳場甫浒勋贯庵葵嗞節達樓呗潇恣饕餮钞晕魏辨芋弓蛎翌咀眞墊辆抖滇困脓舟沏菀笋厢仲報囍咏稍糊坨侯哩钼応逊撰凛冽淳贼帜斛粕凈夢妳煥黃噬缀蹄盔罕唾漱凸窥鞍栗矫邵啾圭戌奋晖翟绢绎榴沥觅啪贩閩蘇樟蔽傢飄烏澤髮億馏蜻蜓埃驿恤淄冕邀哗筹彤懿唛谣栎榕捡谦嬉棠栖貿圃廖侍薏苡賴顆沖瞓饵販気対酚釜沱楸淼滿竞極揉搓腕搐啤扒赐纇芍湯藓癣骷髅綫薩酰喰锶焼緖鬚閃夾雜誌連續皺菁咕禧乔鸥舆盹鸳鸯颐岑苇寇押掸罪脊姨鸾棚惧催俯臨靑臥箐贮嘻嘿舔傷軽視確撃親滙媄匹倚嗣涔鍾憨瞌瑚軒睁嫁倉庫運還屎粪爾羞蓉炙磅兑蛤蟆桨匆楞倩昨镌枞鳯坤珂褐谊壐吾橋拯棋姚歼紹绍鳄艇腱鞘吲哚邻鎏損炽搁咭迫巣曙竖漓兹僵尸蛊斧濕對計於晗胞倦鎻寡帚難惆悵尙戒窈窕鳥匮甬瑾眸蜘蛛泾檐梢筏陽稿麝暮獭狙昵瀚隅枼铆寝寢俫酐藍玺勁裆援倡漳紐約冉懵霆罘堰珏瞳壊艷嗪鎖藿歇墅掘穩閉楦芹據鯽騷鱸鯉逝柒诵汀铡羅愈吓睦啞婦苔噢棵茜哎妊娠绨绰砭荞吋嘧啶犁鸢钽痞谅鬓违楊洙變將忄耸谚筠姬瓮佐募耕豬尹禄螃從營玖惜蔘馴楂彐鬃寕庙叁卿叱咤缥缈恨嗔癫蚤沽扮絮璎罢躲宙臺渠泣犸崽蚌埠欺骗锏聿枰濠惹蝗螳秉遂瘙腥泼鐡堅啖嬷寺銮殿盎獸岚蜱瞅巡伱費葆痔魁蝎揽穆琯朦胧類椭痧萎迟雌翰煤掟巍軍琐乏署獻褲乘熳雍靜辞锳叟劫佬菡紗俺茸轭镯歆熄蠔豇寧僑羡嫉妒萍羁榉鲸帯怒婊拦呀巫褥仆酊術舜汶汛織載漩餓厲恕晔荀戳郊帛霏尷歸錯盤筆綁顏燙缉檫桓夯碩狀喬逻仇拎帘哼肆狄羙顔丧崭維鵬浚銷緑胰瘊疣桁闽雑鋪凱醫療聨懮豌幚瘤黯鴨蛭纠緯槟肚腩燒孤璟凭歓槍伐偿訂糙坛凖涧憶靈轧岂輔賠麯胁泞晧雁偕祠徕粵赣饶冤锵醚胗崩溃娅怜啄岳燊琢昱砧喫肴豐怨袆仑燈関閟吟匍匐瞰陰絶樊粽甸督驼胤锆瞎缅冶勐缨娶锭咆掩拽捣桧補鳕颁稚髙燳豺峦氙坑洼咂蝠拐兮儥壕擒绗乒乓估鼙聲炀線條紋圍茬抬钝遭曉硼璇闰巩繹貔貅臃筐喊夺咧镰耍処焱钾虐孢嘘邯郸瞄㨂選涇玮刨兩罂獅晞跆僧氮焰紊癌峻踝辩疝脐螯驹蹲诸咱蛙靖帧哄祸渄柿啃灾捞惫資婕侬榔捂潍塌砍晳粧铎偌黒皲獨挖傻狱爲鹄哉碁叻汝罄枭寫挞撻蕨踢攸捌戊蛳嗓汐鏡襟奎鍋禅莆禪矾洇稔箸吞蒟蒻両鉄猬颓痣腦蕒夲糝翁戋虽煸括榆悄匣沌缴悅掠奪惡態咿淬昡掺乍劝乞庾衮俞仗懷濯涟亵焉熠區擇纂恊钣窘煊贱醬釀麵麺籤蓋鹽隧寬闊貳錄宪骆輼娆"
    word_img_dict_file="./word_img_dict.json"
    cut_specify_word_img(annotation_dir_path,img_dir_path,save_dir,specify_word_list,word_img_dict_file)


def convert_specify_word_dict(word_img_dict_file,out_file):
    with open(word_img_dict_file,"r",encoding="utf-8") as f:
        word_img_dict=json.load(f)
    new_word_img_dict=dict()
    for k,v in word_img_dict.items():
        if v not in new_word_img_dict:
            new_word_img_dict[v] = k
        else:
            new_word_img_dict[v] +=k
    for k,v in new_word_img_dict.items():
        new_word_img_dict[k]=v.split(k)[1:]
    with open(out_file,"w",encoding="utf-8") as f:
        json.dump(new_word_img_dict,f,ensure_ascii=False)


###########将裁剪出的含有指定文字的图片进行随机搭配拼接###########
def joint_specify_word_img(word_img_dict_file,word_img_dir,out_img_dir,out_img_dict_file,max_text_length=10,total_joint_img_count=100):
    with open(word_img_dict_file,"r",encoding="utf-8") as f:
        word_img_dict=json.load(f)
    word_list=list(word_img_dict.keys())

    out_img_dict=dict()
    for img_index in range(total_joint_img_count):
        text_length=random.randint(2,max_text_length)
        img_out=Image.new('RGB', (32 * text_length, 32))
        img_out_text=""
        for index in range(text_length):
            word=random.choice(word_list)
            img_out_text+=word
            img_out.paste(Image.open("{}/{}{}.jpg".format(word_img_dir,word,random.choice(word_img_dict[word]))),(index * 32, 0, (index + 1) * 32, 32))
        img_out.save("{}/{}.jpg".format(out_img_dir,img_index))
        out_img_dict[str(img_index)]=img_out_text

    with open(out_img_dict_file,"w",encoding="utf-8") as f:
        json.dump(out_img_dict,f,ensure_ascii=False)


###########根据筛选过后的单字符图片文件夹生成指定文字字典###########
def generate_specify_word_dict_from_dir(word_img_dir,out_file):
    new_word_img_dict=dict()
    for k in os.listdir(word_img_dir):
        k=k[:-4]
        v=k[0]
        if v not in new_word_img_dict:
            new_word_img_dict[v] = k
        else:
            new_word_img_dict[v] += k
    for k,v in new_word_img_dict.items():
        new_word_img_dict[k]=v.split(k)[1:]
    with open(out_file,"w",encoding="utf-8") as f:
        json.dump(new_word_img_dict,f,ensure_ascii=False)




# cut_specify_word_img_demo()
# convert_specify_word_dict("./word_img_dict.json","./specify_word_dict.json")
joint_specify_word_img("./specify_word_dict.json","D:/all_data/ocr1/specify_word_img_bak","D:/all_data/ocr1/joint","./joint_text_dict.json")
# generate_specify_word_dict_from_dir("D:/all_data/ocr1/specify_word_img_bak","./specify_word_dict.json")
