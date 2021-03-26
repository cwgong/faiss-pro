#!/usr/bin/env python3
#coding=utf-8

import sys
from pyspark import SparkContext
from pyspark.sql import SparkSession

jd_cat1_en_name =  sys.argv[1]
in_p = sys.argv[2]
out_p = sys.argv[3]

sc = SparkContext(appName="vec_data_sharding")
rdd = sc.textFile(in_p)
total= rdd.count()
one_part_num = 510 * 10000
if total <= one_part_num:
    n = 1
    part_num = 1
else:
    n = total / one_part_num
    m = total % one_part_num
    if m == 0:
        part_num = n
    else:
        part_num = int(n) + 1
print("cat1_total_num: %s sharding_num: %s(%s) [%s]" % (total, part_num, n, jd_cat1_en_name))

rdd.repartition(part_num).saveAsTextFile(out_p)
