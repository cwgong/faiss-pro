#!/usr/bin/env pyhthon
#coding=utf-8


brand_name_lst = []

def score_span(score):
    if score >=0.95:
        return "span1_[1,0.95]"
    elif score < 0.95 and score >= 0.94:
        return "span2_(0.95, 0.94]"
    elif score < 0.94 and score >= 0.93:
        return "span3_(0.94, 0.93]"
    elif score < 0.93:
        return "span4_(0.93, 0]"
    else:
        return "span5_unk-span"


def getting_top100_sku(c4_total_gmv, cat4_all_sku_lst):
    sorted_lst1 = sorted(cat4_all_sku_lst, key=lambda x: x[2], reverse=True)
    top_sku_lst = sorted_lst1[:100]
    p_gmv = 0.0
    for z in top_sku_lst:
        p_gmv += z[2]
    sku_num = len(cat4_all_sku_lst)
    spn_sku_dict = {}
    spn_gmv_dict = {}
    for zz in cat4_all_sku_lst:
        tmp_gmv = zz[2]
        tmp_sku = zz[0]
        tmp_spn = zz[6]
        if tmp_spn not in spn_gmv_dict:
            spn_gmv_dict[tmp_spn] = tmp_gmv
        else:
            zzz = spn_gmv_dict[tmp_spn]
            zzz += tmp_gmv
            spn_gmv_dict[tmp_spn] = zzz

        if tmp_spn not in spn_sku_dict:
            spn_sku_dict[tmp_spn] = [tmp_sku]
        else:
            zzzz =spn_sku_dict[tmp_spn]
            zzzz += [tmp_sku]
            spn_sku_dict[tmp_spn] = zzzz

    d_all = {}
    for k1, v1 in spn_gmv_dict.items():
        d_all[k1] = "%s\t%s" % (v1, round(1.0*v1/c4_total_gmv, 5))

    for k2, v2 in spn_sku_dict.items():
        if k2 not in d_all:
            print("error: %s" % k2)
            continue
        else:
            print(k2)
            tmp_s = "%s\t%s" % (v2, round(1.0*v2/sku_num, 5))
            y = d_all[k2]
            y = "%s\t%s" % (y, tmp_s)
            d_all[k2] = y
    r_lst = [(k, v) for k, v in d_all.items()]
    r_lst = sorted(r_lst, key=lambda x: x[0], reverse=True)

    return top_sku_lst, r_lst, sku_num

cat4_info_dict = {}
cat4_gmv_dict = {}
with open("./m1_data.txt","r",encoding="utf-8") as f1:
    for line in f1:
        line = line.strip()
        if line == "": continue
        lst1 = line.split("\t")
        if len(lst1) != 8:
            print(lst1)
            continue
        lst1 = [tmp.strip() for tmp in lst1]
        sku, name, c3name, bname, gmv, c4id, c4name, score = lst1
        if score == "NULL":continue
        try:
            gmv = float(gmv)
            score = float(score)
            score_flag = score_span(score)
        except:
            print("gmv error: %s" % line)
            continue
        if c4id not in cat4_info_dict:
            cat4_info_dict[c4id] = [(sku, name, gmv, c3name, bname, score, c4id, c4name, score_flag)]
        else:
            zz = cat4_info_dict[c4id]
            zz += [(sku, name, gmv, c3name, bname, score, c4id, c4name, score_flag)]
            cat4_info_dict[c4id] = zz

        if c4id not in cat4_gmv_dict:
            cat4_gmv_dict[(c4id, c4name)] = gmv
        else:
            zzz = cat4_gmv_dict[(c4id, c4name)]
            zzz += gmv
            cat4_gmv_dict[(c4id, c4name)] = zzz

cat4_gmv_sorted_lst = [[k, v] for k, v in cat4_gmv_dict.items()]
cat4_gmv_sorted_lst = sorted(cat4_gmv_sorted_lst, key=lambda x: x[1], reverse=True)


head_tpl = "%s\t%s\t%s\t%s" # c4_id c4_name total_gmv sku_num
sku_tpl = "%s\t%s\t%s\t%s\t%s\t%s" # sku title sku_gmv tmall_c3name tmall_brand_name score
score_tmp = "%s\t%s\t%s\t%s\t%s" # score_span p_gmv p_gmv_rate p_num p_num_rate

d_lst1 = []
d_lst2 = []
for x in cat4_gmv_sorted_lst:
    tmp1, tmp_cgmv = x
    tmp_cid, tmp_cname = tmp1
    sku_lst, span_lst, sku_num = getting_top100_sku(tmp_cgmv, cat4_info_dict[tmp_cid])
    s1 = head_tpl % (tmp_cid, tmp_cname, tmp_cgmv, sku_num)
    d_lst1.append(s1)
    d_lst2.append(s1)
    for z1 in sku_lst:
        d_lst1.append(sku_tpl % ())

print(cat4_gmv_sorted_lst)