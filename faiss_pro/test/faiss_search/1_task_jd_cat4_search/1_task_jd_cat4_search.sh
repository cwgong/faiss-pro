
source ../query_base.sh

cur_dt='2021-02-19'
faiss_platform='jd_cat4'
faiss_cat1_en_name='jd_all_cat4'
query_platform='tmall'
query_cat1_en_name='shipinyinliao'
faiss_sku_info_folder=../sku_info/$faiss_platform
if [ ! -d "${faiss_sku_info_folder}" ];then
   mkdir ${faiss_sku_info_folder}
fi
faiss_sku_info_folder=$faiss_sku_info_folder/$faiss_cat1_en_name
if [ ! -d "${faiss_sku_info_folder}" ];then
   mkdir ${faiss_sku_info_folder}
fi

query_sku_info_folder=../sku_info/$query_platform
if [ ! -d "${query_sku_info_folder}" ];then
   mkdir ${query_sku_info_folder}
fi
query_sku_info_folder=$query_sku_info_folder/$query_cat1_en_name
if [ ! -d "${query_sku_info_folder}" ];then
   mkdir ${query_sku_info_folder}
fi

query_vec_data_folder=../query_vec_data/$query_platform
if [ ! -d "${query_vec_data_folder}" ];then
   mkdir ${query_vec_data_folder}
fi
query_vec_data_folder=$query_vec_data_folder/$query_cat1_en_name
if [ ! -d "${query_vec_data_folder}" ];then
   mkdir ${query_vec_data_folder}
fi

attach_sku_info_folder=../attach_sku_info/$query_platform
if [ ! -d "${attach_sku_info_folder}" ];then
   mkdir ${attach_sku_info_folder}
fi
attach_sku_info_folder=$attach_sku_info_folder/$query_cat1_en_name
if [ ! -d "${attach_sku_info_folder}" ];then
   mkdir ${attach_sku_info_folder}
fi

:<<!
hive -e "select skuid, regexp_replace(title, '[\r\n\t]', '') title, category3_id_std, category3_std, category4_id, category4
from tmp.tmp_dwd_jd_wares_sku2
where category4_id is not null and category4_id <> ''
    and title not rlike '(差价|链接)'
    and skuid is not null
    and skuid!=''
    and category4 is not null and category4!=''
    and category4_id is not null and category4_id!='';" >  ${faiss_sku_info_folder}/part-00000

hive -e "select spu_id 
    ,regexp_replace(title, '[\r\n\t]', '') title
    ,category3_id_std
    ,category3_std 
from dim.dim_retailers_online_spu_sku 
where platform_type='tmall' and category1_std='食品饮料'" > ${query_sku_info_folder}/part-00000
if [ $? -ne 0 ]; then
    echo "getting tmall sku info error!"
    exit 1
fi


rm -rf ${query_vec_data_folder}
wait
hadoop fs -get ${vec_hdfs}/${query_platform}/d_type=vec_data/dt=ori/cat1=${query_cat1_en_name} ${query_vec_data_folder}
wait 
rm -f ${query_vec_data_folder}/_SUCCESS
!

:<<!
/home/supdev/anaconda3/bin/python3.8 jd_cat4_query_go.py $faiss_platform $faiss_cat1_en_name $query_platform $query_cat1_en_name
if [ $? -ne 0 ]; then
    echo "${query_platform}-${query_cat1_en_name}-faiss-query error!"
    exit 1
fi
!


hv_hdfs=${jd_cat4_search_hdfs}/dt=${cur_dt}
hadoop fs -rm -r -skipTrash ${hv_hdfs}
wait
hadoop fs -mkdir ${hv_hdfs}
wait

fname_str=`python -c "import jd_cat4_tool; print(jd_cat4_tool.uploading_file_name('${attach_sku_info_folder}'))"`
echo "${fname_str}"

OLD_IFS="$IFS"
IFS="|"
arr2=(${fname_str})
IFS="$OLD_IFS"
for fname in ${arr2[*]}
do
    up_file=${attach_sku_info_folder}/${fname}
    if [ ! -f "${up_file}" ]; then
        echo "${up_file} does not exists!"
        continue
    fi
    hadoop fs -put ${up_file} ${hv_hdfs}
    wait
    hadoop fs -test -e ${hv_hdfs}/${fname}
    if [ $? -ne 0 ]; then
        echo "${up_file} uploading error!"
        continue
    fi
done

exit 0
