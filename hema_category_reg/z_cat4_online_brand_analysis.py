#!/usr/bin/env pyhthon
# coding=utf-8

del_cat4_dict = {}
with open("./小红书-数码3C-增加品牌.txt") as f2:
    for line in f2:
        line = line.strip()
        if line == "": continue
        lst1 = line.split('|')
        if len(lst1) != 2: continue
        lst1 = [tmp.strip() for tmp in lst1]
        cid, cname = lst1
        del_cat4_dict[cid] = cname


def score_span(score):
    if score >=0.93:
        return "span1_[1,0.93]"
    else:
        return "span2_(0.93,0]"

def data_padding(d1):
    for zz in ["span1_[1,0.93]", "span2_(0.93,0]"]:
        if zz not in d1:
            d1[zz] = 0

    return d1

def getting_top100_sku(c4_total_gmv, cat4_all_sku_lst):
    topn = 100
    sorted_lst1 = sorted(cat4_all_sku_lst, key=lambda x: x[2], reverse=True)
    top_sku_lst = sorted_lst1[:topn]
    p_gmv = 0.0
    for z in top_sku_lst:
        p_gmv += z[2]
    sku_num = len(cat4_all_sku_lst)
    spn_sku_dict = {}
    spn_gmv_dict = {}

    for zz in cat4_all_sku_lst:
        # (sku, name, gmv, c3name, bname, score, c4id, c4name, score_flag)
        tmp_gmv = zz[2]
        tmp_sku = zz[0]
        tmp_spn = zz[8]
        if tmp_spn not in spn_gmv_dict:
            spn_gmv_dict[tmp_spn] = tmp_gmv
        else:
            zzz = spn_gmv_dict[tmp_spn]
            zzz += tmp_gmv
            spn_gmv_dict[tmp_spn] = zzz

        if tmp_spn not in spn_sku_dict:
            spn_sku_dict[tmp_spn] = [tmp_sku]
        else:
            zzzz = spn_sku_dict[tmp_spn]
            zzzz += [tmp_sku]
            spn_sku_dict[tmp_spn] = zzzz

    d1 = data_padding(spn_gmv_dict)
    d2 = data_padding(spn_sku_dict)
    d_all = {}
    for k1, v1 in d1.items():
        if c4_total_gmv == 0:
            r1 = 0
        else:
            r1 = round(1.0 * v1 / c4_total_gmv, 5)
        d_all[k1] = "%s\t%s" % (v1, r1)

    for k2, v2 in d2.items():
        if k2 not in d_all:
            print("error: %s" % k2)
            continue
        else:
            if v2 != 0:
                tmp_s = "%s\t%s" % (len(v2), round(1.0 * len(v2) / sku_num, 5))
            else:
                tmp_s = "0\t0"
            y = d_all[k2]
            y = "%s\t%s" % (y, tmp_s)
            d_all[k2] = y

    r_lst = [(k, v) for k, v in d_all.items()]
    r_lst = sorted(r_lst, key=lambda x: x[0])
    r_lst = [z3[1] for z3 in r_lst]

    if c4_total_gmv == 0:
        r3 = 0
    else:
        r3 = round(p_gmv / c4_total_gmv, 5)

    return top_sku_lst, r_lst, sku_num, round(topn / sku_num, 5), p_gmv, r3

bname_info_dict = {}
bname_gmv_dict = {}
total_gmv = 0.0
total_sku_num = 0
with open("jd_cat4_all_2021_m01.txt") as f1:
    for line in f1:
        line = line.strip()
        if line == "": continue
        lst1 = line.split("\t")
        if len(lst1) != 10:
            print(lst1)
            continue
        lst1 = [tmp.strip() for tmp in lst1]
        '''
        tmall_sku
        ,regexp_replace(tmall_title, '[\t|\r]', ' ')
        ,regexp_replace(category1_std, '[\t|\r]', ' ')
        ,regexp_replace(category2_std, '[\t|\r]', ' ')
        ,regexp_replace(category3, '[\t|\r]', ' ')
        ,regexp_replace(brand_name_std, '[\t|\r]', ' ')
        ,jd_cat4_id
        ,regexp_replace(jd_cat4_name, '[\t|\r]', ' ')
        ,sale_amount
        ,similar_score
        '''
        sku, name, _, _, c3name, bname, c4id, c4name, gmv, score = lst1
        if c4id in del_cat4_dict: continue
        try:
            gmv = float(gmv)
            score = float(score)
            score_flag = score_span(score)
        except:
            print("gmv error: %s" % line)
            continue
        total_gmv += gmv
        total_sku_num += 1
        if bname not in bname_info_dict:
            bname_info_dict[bname] = [(sku, name, gmv, c3name, bname, score, c4id, c4name, score_flag)]
        else:
            zz = bname_info_dict[bname]
            zz += [(sku, name, gmv, c3name, bname, score, c4id, c4name, score_flag)]
            bname_info_dict[bname] = zz

        if bname not in bname_gmv_dict:
            bname_gmv_dict[bname] = gmv
        else:
            zzz = bname_gmv_dict[bname]
            zzz += gmv
            bname_gmv_dict[bname] = zzz

# 四级类目的
bname_gmv_sorted_lst = [[k, v] for k, v in bname_gmv_dict.items()]
bname_gmv_sorted_lst = sorted(bname_gmv_sorted_lst, key=lambda x: x[1], reverse=True)

d_lst1 = []
d_lst2 = []
for x in bname_gmv_sorted_lst:
    tmp_bname, tmp_cgmv = x
    sku_lst, span_lst, sku_num, topn_rate, p_gmv, p_gmv_rate = getting_top100_sku(tmp_cgmv, bname_info_dict[tmp_bname])
    if tmp_cgmv <= 100000: continue
    d_lst2.append((tmp_bname, \
                   tmp_cgmv, round(1.0*tmp_cgmv/total_gmv, 5), \
                   sku_num, round(1.0*sku_num/total_sku_num, 5), \
                   "\t".join(span_lst)))

d_lst3 = sorted(d_lst2, key=lambda x: x[1], reverse=True)
s_lst = ["%s\t%s\t%s\t%s\t%s\t%s" % tmp for tmp in d_lst3]

with open("z_cat4_online_brand_analysis.txt", "w") as f2:
    f2.write("\n".join(s_lst))
    f2.flush()

