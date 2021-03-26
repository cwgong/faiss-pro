#!/usr/bin/env python3
#coding=utf-8

import sys, os
import traceback
import faiss_opt
from faiss_opt import JDFaissQuery_Ext, AttachJdCat4Info2TmallSkuWithCat3Filtering
import logging.config
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filemode='a'
)

log_instance = logging.getLogger("faiss_searchlogger")
log_file_name = 'log/faiss_search_log'
fileTimeHandler = TimedRotatingFileHandler(log_file_name, \
                                           when="D", \
                                           interval=1, \
                                           backupCount=10)
fileTimeHandler.suffix = "%Y-%m-%d.log"
formatter = logging.Formatter('%(name)-12s %(asctime)s level-%(levelname)-8s thread-%(thread)-8d %(message)s')
fileTimeHandler.setFormatter(formatter)
log_instance.addHandler(fileTimeHandler)

if __name__ == "__main__":
    try:
        '''
        fassi_platform = 'jd'
        fassi_cat1_en_name = 'jd_all_cat4'
        query_platform = 'tmall'
        query_cat1_en_name = 'shipinyinliao'
        '''
        fassi_platform = sys.argv[1]
        fassi_cat1_en_name = sys.argv[2]
        query_platform = sys.argv[3]
        query_cat1_en_name = sys.argv[4]

        faiss_db_folder = '../../faiss_index_build/faiss_index_db/%s/%s' % (fassi_platform, fassi_cat1_en_name)
        if not os.path.exists(faiss_db_folder):
            raise Exception("%s does not exists!" % faiss_db_folder)

        faiss_db_file = '%s/%s.faiss.ivfflat.index.db' % (faiss_db_folder, fassi_cat1_en_name)
        if not os.path.exists(faiss_db_file):
            raise Exception("%s does not exists!" % faiss_db_file)
        faiss_sku_file = '%s/%s.sku.index' % (faiss_db_folder, fassi_cat1_en_name)
        if not os.path.exists(faiss_sku_file):
            raise Exception("%s does not exists!" % faiss_sku_file)

        query_vec_folder = "../query_vec_data/%s/%s" % (query_platform, query_cat1_en_name)
        if not os.path.exists(query_vec_folder):
            raise Exception("%s does not exists!" % query_vec_folder)

        faiss_sku_info_folder = "../sku_info/%s/%s" % (fassi_platform, fassi_cat1_en_name)
        if not os.path.exists(query_vec_folder):
            raise Exception("%s does not exists!" % faiss_sku_info_folder)

        query_sku_info_folder = "../sku_info/%s/%s" % (query_platform, query_cat1_en_name)
        if not os.path.exists(query_sku_info_folder):
            raise Exception("%s does not exists!" % query_sku_info_folder)

        query_saving_folder = "../faiss_search_result/%s" % query_platform
        if not os.path.exists(query_saving_folder):
            os.mkdir(query_saving_folder)
        query_saving_folder = "%s/%s" % (query_saving_folder, query_cat1_en_name)
        if not os.path.exists(query_saving_folder):
            os.mkdir(query_saving_folder)

        attach_sku_saving_folder = "../attach_sku_info/%s" % query_platform
        if not os.path.exists(attach_sku_saving_folder):
            os.mkdir(attach_sku_saving_folder)
        attach_sku_saving_folder = "%s/%s" % (attach_sku_saving_folder, query_cat1_en_name)
        if not os.path.exists(attach_sku_saving_folder):
            os.mkdir(attach_sku_saving_folder)
        '''     
        file_lst = faiss_opt.getting_sorted_file_name_lst(query_vec_folder)
        if len(file_lst) == 0:
            raise Exception("vec-data-file is empty!")
        query_obj = JDFaissQuery_Ext(faiss_index_file=faiss_db_file, \
                                     faiss_sku_file=faiss_sku_file, \
                                     log_instance=log_instance)

        for fname in file_lst:
            fname = fname.split("/")[-1]
            f_path =  query_vec_folder + "/" + fname
            if not os.path.exists(f_path):
                log_instance.error("%s does not exists!" % f_path)
                continue
            log_instance.info("querying file: %s" % f_path)
            try:
                idx_saving_file = "%s/%s_idx.result" % (query_saving_folder, fname)
                sku_saving_file = "%s/%s_sku.result" % (query_saving_folder, fname)
                query_obj.faiss_search_and_detail_info_saving(query_vec_file=f_path, \
                                                              query_idx_reuslt_saving_file=idx_saving_file, \
                                                              query_sku_result_saving_file=sku_saving_file, \
                                                              topn=5)
            except:
                log_instance.error(traceback.format_exc)
                continue

        '''
        obj1 = AttachJdCat4Info2TmallSkuWithCat3Filtering(faiss_sku_info_folder=faiss_sku_info_folder, \
                                         query_sku_info_folder=query_sku_info_folder, \
                                         query_result_folder=query_saving_folder, \
                                         attach_sku_info_saving_folder=attach_sku_saving_folder, \
                                         log_instance=log_instance)
        obj1.attach_sku_info()
    except Exception as e:
        log_instance.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e
