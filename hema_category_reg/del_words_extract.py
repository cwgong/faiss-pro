from pyhive import hive
import traceback
import io
import re
from LAC import LAC
import jieba


def get_stop_word(input_file):
    lst1 = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line.strip()) != 1:continue
            lst1.append(line.strip())
    d = {}
    for m in lst1:
        if m == "": continue
        d[m] = 0
    return d


def split_sen(input_file,stop_words_file):
    word_dict = {}
    lac = LAC(mode="seg")
    idx = 0
    stop_word_dict = get_stop_word(stop_words_file)
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            idx += 1
            if idx%10000 == 0:print(idx)
            if idx > 5000:break
            line_list = line.strip().split("\t")
            if len(line_list) != 4:continue
            sku_id,title,cat2_id,cat2_name  = line_list
            if len(title) < 5:continue
            seg_list_lac = lac.run(title.strip())
            seg_list_jieba = jieba.cut(title, cut_all=True)
            #jieba
            for seg_item in seg_list_lac:
                if seg_item in stop_word_dict:continue
                if seg_item in word_dict:
                    word_dict[seg_item] += 1
                else:
                    word_dict[seg_item] = 1

            #lac
            for seg_item in seg_list_jieba:
                if seg_item in stop_word_dict: continue
                if seg_item in word_dict:
                    word_dict[seg_item] += 1
                else:
                    word_dict[seg_item] = 1

    word_list = [(k,v) for k,v in word_dict.items()]

    word_list_rev = sorted(word_list,key=lambda x:x[1],reverse=True)

    with io.open("./data/seg_result.txt","w",encoding="utf-8") as f2:
        for x in word_list_rev:
            f2.write("%s\t%s\n"%(x[0],x[1]))
        f2.flush()

def is_own_eng(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_all_eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_number(s):
   try:
       float(s)
       return True
   except ValueError:
       pass

   try:
       import unicodedata
       unicodedata.numeric(s)
       return True
   except (TypeError, ValueError):
       pass

   return False

def filter_words(input_file):
    data_list = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.split("\t")
            if len(line_list) != 2:continue
            word,num = line_list
            if len(word) < 2:continue
            if is_all_eng(word):continue
            if bool(re.search(r'\d', word)):continue
            data_list.append(line)

    with io.open("./data/seg_result_filter.txt","w",encoding="utf-8") as f2:
        for item in data_list:
            f2.write(item)



if __name__ == "__main__":
    input_file = './data/ori_hm_data.txt'
    stop_word_file = './data/stop_word.txt'
    split_sen(input_file,stop_word_file)
    filter_words("./data/seg_result.txt")