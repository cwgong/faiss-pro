#!/usr/bin/env python3
#coding=utf-8
import os

def uploading_file_name(b_folder):
    f_name_lst = []
    for root, dirs, files in os.walk(b_folder):
        for f_name in files:
            if not f_name.startswith('part'): continue
            f_name = os.path.join(root, f_name)
            f_name = f_name.split("/")[-1]
            f_name_lst.append(f_name)

    f_name_lst = sorted(f_name_lst)
    return "|".join(f_name_lst)
