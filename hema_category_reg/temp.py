import io

def is_all_eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def standard_file(ori_file):
    brand_id_dict = {}
    res_dict = {}
    short_list = []
    # with io.open(input_file,"r",encoding="utf-8") as f1:
    #     for line in f1:
    #         if len(line) == 0:continue
    #         brand_id_dict[line.strip()] = ''

    with io.open(ori_file,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 3:continue
            brand_id,brand_name,gmv = line_list
            if brand_id.strip() in res_dict:continue
            res_dict[brand_id.strip()] = [brand_id.strip(),brand_name.strip(),gmv.strip()]

            brand_name_list = brand_name.strip().split("/")
            if len(brand_name_list) > 1:
                for item in brand_name_list:
                    if is_all_eng(item) and len(item) <= 3:
                        short_list.append(brand_name)

    print(len(res_dict))
    print(short_list)
    for item,v in res_dict.items():
        print("\t".join(v))

def del_brand_4ji(input_file):
    idx = 0
    data_list = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("  ")
            if len(line_list) != 2:continue
            idx += 1
            data_list.append(line_list)
    for item in data_list:
        print("|".join(item))
    print(idx)


def average_num(input_file1,input_file2,input_file3):
    data_dict_1 = {}
    data_dict_2 = {}
    data_dict_3 = {}
    data_dict_avg = {}

    with io.open(input_file1,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14:continue
            data_dict_1[line_list[0]] = line_list

    with io.open(input_file2,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14:continue
            data_dict_2[line_list[0]] = line_list

    with io.open(input_file3,"r",encoding="utf-8") as f3:
        for line in f3:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14:continue
            data_dict_3[line_list[0]] = line_list

    idx = 0
    for item in data_dict_2:
        if item in data_dict_1 and item in data_dict_3:
            idx+=1
            cat4_gmv_avg = (float(data_dict_1[item][2])+ float(data_dict_2[item][2]) + float(data_dict_3[item][2]))/3
            cat4_gmv_rate_avg = (float(data_dict_1[item][3])+ float(data_dict_2[item][3]) + float(data_dict_3[item][3]))/3
            cat4_num_avg = (float(data_dict_1[item][4])+ float(data_dict_2[item][4]) + float(data_dict_3[item][4]))/3
            cat4_num_rate_avg = (float(data_dict_1[item][5])+ float(data_dict_2[item][5]) + float(data_dict_3[item][5]))/3
            cat4_high_gmv_avg = (float(data_dict_1[item][6])+ float(data_dict_2[item][6]) + float(data_dict_3[item][6]))/3
            cat4_high_gmv_rate_avg = (float(data_dict_1[item][7])+ float(data_dict_2[item][7]) + float(data_dict_3[item][7]))/3
            cat4_hign_num_avg = (float(data_dict_1[item][8])+ float(data_dict_2[item][8]) + float(data_dict_3[item][8]))/3
            cat4_hign_num_rate_avg = (float(data_dict_1[item][9])+ float(data_dict_2[item][9]) + float(data_dict_3[item][9]))/3
            cat4_low_gmv_avg = (float(data_dict_1[item][10])+ float(data_dict_2[item][10]) + float(data_dict_3[item][10]))/3
            cat4_low_gmv_rate_avg = (float(data_dict_1[item][11])+ float(data_dict_2[item][11]) + float(data_dict_3[item][11]))/3
            cat4_low_num_avg = (float(data_dict_1[item][12])+ float(data_dict_2[item][12]) + float(data_dict_3[item][12]))/3
            cat4_low_num_rate_avg = (float(data_dict_1[item][13]) + float(data_dict_2[item][13]) + float(
                data_dict_3[item][13])) / 3

        else:
            cat4_gmv_avg = float(data_dict_2[item][2])
            cat4_gmv_rate_avg = float(data_dict_2[item][3])
            cat4_num_avg =  float(data_dict_2[item][4])
            cat4_num_rate_avg = float(data_dict_2[item][5])
            cat4_high_gmv_avg = float(data_dict_2[item][6])
            cat4_high_gmv_rate_avg = float(data_dict_2[item][7])
            cat4_hign_num_avg = float(data_dict_2[item][8])
            cat4_hign_num_rate_avg = float(data_dict_2[item][9])
            cat4_low_gmv_avg = float(data_dict_2[item][10])
            cat4_low_gmv_rate_avg = float(data_dict_2[item][11])
            cat4_low_num_avg = float(data_dict_2[item][12])
            cat4_low_num_rate_avg = float(data_dict_2[item][13])

        data_dict_avg[item] = [item,data_dict_2[item][1],cat4_gmv_avg,cat4_gmv_rate_avg,int(cat4_num_avg),cat4_num_rate_avg,\
                         cat4_high_gmv_avg,cat4_high_gmv_rate_avg,int(cat4_hign_num_avg),\
                         cat4_hign_num_rate_avg,cat4_low_gmv_avg,cat4_low_gmv_rate_avg,int(cat4_low_num_avg),\
                         cat4_low_num_rate_avg]

    data_list_avg = [(k,v) for k,v in data_dict_avg.items()]
    sort_data_list_avg = sorted(data_list_avg,key=lambda x:x[1][2],reverse=True)

    for k,v in sort_data_list_avg:
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(v[0],v[1],v[2],v[3],\
                                                                v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13]))
    print(idx)

def brand_average_num(input_file1,input_file2,input_file3):
    data_dict_1 = {}
    data_dict_2 = {}
    data_dict_3 = {}
    data_dict_avg = {}

    with io.open(input_file1,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13:continue
            data_dict_1[line_list[0]] = line_list

    with io.open(input_file2,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13:continue
            data_dict_2[line_list[0]] = line_list

    with io.open(input_file3,"r",encoding="utf-8") as f3:
        for line in f3:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13:continue
            data_dict_3[line_list[0]] = line_list

    idx = 0
    for item in data_dict_2:
        if item in data_dict_1 and item in data_dict_3:
            idx+=1
            cat4_gmv_avg = (float(data_dict_1[item][1])+ float(data_dict_2[item][1]) + float(data_dict_3[item][1]))/3
            cat4_gmv_rate_avg = (float(data_dict_1[item][2])+ float(data_dict_2[item][2]) + float(data_dict_3[item][2]))/3
            cat4_num_avg = (float(data_dict_1[item][3])+ float(data_dict_2[item][3]) + float(data_dict_3[item][3]))/3
            cat4_num_rate_avg = (float(data_dict_1[item][4])+ float(data_dict_2[item][4]) + float(data_dict_3[item][4]))/3
            cat4_high_gmv_avg = (float(data_dict_1[item][5])+ float(data_dict_2[item][5]) + float(data_dict_3[item][5]))/3
            cat4_high_gmv_rate_avg = (float(data_dict_1[item][6])+ float(data_dict_2[item][6]) + float(data_dict_3[item][6]))/3
            cat4_hign_num_avg = (float(data_dict_1[item][7])+ float(data_dict_2[item][7]) + float(data_dict_3[item][7]))/3
            cat4_hign_num_rate_avg = (float(data_dict_1[item][8])+ float(data_dict_2[item][8]) + float(data_dict_3[item][8]))/3
            cat4_low_gmv_avg = (float(data_dict_1[item][9])+ float(data_dict_2[item][9]) + float(data_dict_3[item][9]))/3
            cat4_low_gmv_rate_avg = (float(data_dict_1[item][10])+ float(data_dict_2[item][10]) + float(data_dict_3[item][10]))/3
            cat4_low_num_avg = (float(data_dict_1[item][11])+ float(data_dict_2[item][11]) + float(data_dict_3[item][11]))/3
            cat4_low_num_rate_avg = (float(data_dict_1[item][12]) + float(data_dict_2[item][12]) + float(
                data_dict_3[item][12])) / 3

        else:
            cat4_gmv_avg = float(data_dict_2[item][1])
            cat4_gmv_rate_avg = float(data_dict_2[item][2])
            cat4_num_avg =  float(data_dict_2[item][3])
            cat4_num_rate_avg = float(data_dict_2[item][4])
            cat4_high_gmv_avg = float(data_dict_2[item][5])
            cat4_high_gmv_rate_avg = float(data_dict_2[item][6])
            cat4_hign_num_avg = float(data_dict_2[item][7])
            cat4_hign_num_rate_avg = float(data_dict_2[item][8])
            cat4_low_gmv_avg = float(data_dict_2[item][9])
            cat4_low_gmv_rate_avg = float(data_dict_2[item][10])
            cat4_low_num_avg = float(data_dict_2[item][11])
            cat4_low_num_rate_avg = float(data_dict_2[item][12])

        data_dict_avg[item] = [item,cat4_gmv_avg,cat4_gmv_rate_avg,int(cat4_num_avg),cat4_num_rate_avg,\
                         cat4_high_gmv_avg,cat4_high_gmv_rate_avg,int(cat4_hign_num_avg),\
                         cat4_hign_num_rate_avg,cat4_low_gmv_avg,cat4_low_gmv_rate_avg,int(cat4_low_num_avg),\
                         cat4_low_num_rate_avg]

    data_list_avg = [(k,v) for k,v in data_dict_avg.items()]
    sort_data_list_avg = sorted(data_list_avg,key=lambda x:x[1][1],reverse=True)

    for k,v in sort_data_list_avg:
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(v[0],v[1],v[2],v[3],\
                                                                v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12]))
    print(idx)

def sum_month(input_file1, input_file2, input_file3):
    data_dict_1 = {}
    data_dict_2 = {}
    data_dict_3 = {}
    data_dict_avg = {}

    with io.open(input_file1, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14: continue
            data_dict_1[line_list[0]] = line_list

    with io.open(input_file2, "r", encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14: continue
            data_dict_2[line_list[0]] = line_list

    with io.open(input_file3, "r", encoding="utf-8") as f3:
        for line in f3:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14: continue
            data_dict_3[line_list[0]] = line_list

    for item in data_dict_2:
        if item in data_dict_1 and item in data_dict_3:
            data_dict_avg[item] = [item,data_dict_2[item][1],data_dict_1[item][2],\
                                   data_dict_2[item][2],data_dict_3[item][2],\
                                   data_dict_1[item][3],data_dict_2[item][3],data_dict_3[item][3],\
                                   data_dict_1[item][4],data_dict_2[item][4],data_dict_3[item][4],data_dict_1[item][5],\
                                   data_dict_2[item][5],data_dict_3[item][5]]

    for k,v in data_dict_avg.items():
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(v[0],v[1],v[4],v[3],v[2],v[7],v[6],v[5],v[10],v[9],v[8],v[13],v[12],v[11]))


def brand_sum_month(input_file1, input_file2, input_file3):
    data_dict_1 = {}
    data_dict_2 = {}
    data_dict_3 = {}
    data_dict_avg = {}

    with io.open(input_file1, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13: continue
            data_dict_1[line_list[0]] = line_list

    with io.open(input_file2, "r", encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13: continue
            data_dict_2[line_list[0]] = line_list

    with io.open(input_file3, "r", encoding="utf-8") as f3:
        for line in f3:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 13: continue
            data_dict_3[line_list[0]] = line_list

    for item in data_dict_2:
        if item in data_dict_1 and item in data_dict_3:
            data_dict_avg[item] = [item,data_dict_1[item][1],\
                                   data_dict_2[item][1],data_dict_3[item][1],data_dict_1[item][2],\
                                   data_dict_2[item][2],data_dict_3[item][2],\
                                   data_dict_1[item][3],data_dict_2[item][3],data_dict_3[item][3],\
                                   data_dict_1[item][4],data_dict_2[item][4],data_dict_3[item][4]]

    for k,v in data_dict_avg.items():
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(v[0],v[3],v[2],v[1],v[6],v[5],v[4],v[9],v[8],v[7],v[12],v[11],v[10]))

def other_gmv(input_file):
    other_list = []
    gmv_all = 0.0
    with io.open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14: continue
            brand_name = line_list[1]
            if '其他' in brand_name or '其它' in brand_name:
                other_list.append(line_list)
    for item_list in other_list:
        gmv_all += float(item_list[6])
    print(gmv_all)


def check_data_filter(filter_file, data_file):
    filter_cat4_dict = {}
    data_list = []
    with io.open(filter_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 14:continue
            filter_cat4_dict[line_list[0]] = line_list

    print(len(filter_cat4_dict))
    with io.open(data_file,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 12:continue
            if line_list[5] not in filter_cat4_dict or float(line_list[11]) < 0.93:continue
            data_list.append(line_list)

    print(len(data_list))
    with io.open("./res_data/filter_res_data.txt","w",encoding="utf-8") as f3:
        for item in data_list:
            f3.write("\t".join(item))
            f3.write("\n")



if __name__ == "__main__":
    # input_file='小红书-数码3C-增加品牌.txt'
    # ori_file='shuma3c_ori_file.txt'
    # standard_file(input_file)

    # del_brand_4ji(input_file)

    #多个月份指标求均值
    # input_file1 = 'check_data/z_cat4_online_analysis.txt'
    # input_file2 = 'check_data/z_cat4_online_analysis (2).txt'
    # input_file3 = 'check_data/z_cat4_online_analysis (3).txt'
    # average_num(input_file1, input_file2, input_file3)

    #多个月份指标概要
    # sum_month(input_file1,input_file2,input_file3)

    #多个月份品牌求均值
    # input_file1 = 'check_data_brand/z_cat4_online_brand_analysis.txt'
    # input_file2 = 'check_data_brand/z_cat4_online_brand_analysis (2).txt'
    # input_file3 = 'check_data_brand/z_cat4_online_brand_analysis (3).txt'
    # brand_average_num(input_file1, input_file2, input_file3)

    # 多个月份品牌概要
    # brand_sum_month(input_file1, input_file2, input_file3)

    #21年一月份的其他4级类占比
    # input_file = './check_data/z_cat4_online_analysis.txt'
    # other_gmv(input_file)

    #通过四级类名称过滤数据
    filter_file = 'z_filter_final.txt'
    data_file = 'seg_result.txt'
    check_data_filter(filter_file,data_file)