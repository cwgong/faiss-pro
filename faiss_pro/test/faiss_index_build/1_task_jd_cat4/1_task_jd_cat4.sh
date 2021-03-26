#!/usr/bin/bash
source ../base.sh

platform='jd_cat4'
dt='2021-02-02'
jd_cat1_en_name='jd_all_cat4'

in_p=${vec_hdfs}/${platform}/d_type=vec_data/dt=${dt}/cat1=${jd_cat1_en_name}

hadoop fs -test -e ${in_p}/_SUCCESS
if [ $? -ne 0 ]; then
    echo "${vec_hdfs} does not exists!"
    exit 1
fi

out_p=${faiss_hdfs}/tmp#${platform}#${jd_cat1_en_name}

hadoop fs -rm -r -skipTrash $out_p
spark-submit \
    --num-executors 30 \
    --executor-memory 4g \
    --conf spark.sql.broadcastTimeout=3000 \
    data_sharding.spk.py ${jd_cat1_en_name} $in_p $out_p
if [ $? -ne 0 ]; then
    echo "${out_p} getting legal spu error!"
    exit 1
fi


local_vec_folder=../vec_data/$platform
if [ ! -d "${local_vec_folder}" ]; then
    mkdir $local_vec_folder
fi
local_vec_folder=${local_vec_folder}/${jd_cat1_en_name}

rm -rf ${local_vec_folder}
wait
hadoop fs -get ${out_p} ${local_vec_folder}
wait
rm -f ${local_vec_folder}/_SUCCESS
wait   
                 
local_faiss_index_folder=../faiss_index_db/$platform
if [ ! -d "${local_faiss_index_folder}" ]; then
    mkdir $local_faiss_index_folder
fi
local_faiss_index_folder=$local_faiss_index_folder/${jd_cat1_en_name}

rm -rf ${local_faiss_index_folder}
wait
mkdir ${local_faiss_index_folder}

/home/supdev/anaconda3/bin/python3.8 faiss_dealing.py ${jd_cat1_en_name} ${local_vec_folder} ${local_faiss_index_folder}
if [ $? -ne 0 ]; then
    echo "${platform} ${jd_cat1_en_name} faiss_index_creating_and_merging error!"
    exit 1
fi 

exit 0
