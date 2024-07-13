#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import os
import oss2
import time


# 批量上传文件到OSS
def upload_files(bucket, target_dir_path, exclusion_list=[]):
    oss_objects_path = []
    target_dir_path = os.path.normpath(target_dir_path).replace('\\', '/')
    for root, dirs, files in os.walk(target_dir_path):
        for file in files:
            target_file_path = os.path.normpath(os.path.join(root, file))
            target_file_relative_path = target_file_path.replace('\\', '/').replace(target_dir_path, '').lstrip('/')
            if target_file_relative_path in exclusion_list:
                continue
            object_path = 'a2f/%s' % target_file_relative_path
            upload_file(bucket, target_file_path, object_path)
            oss_objects_path.append(object_path)
    return oss_objects_path

# 上传文件到OSS
def upload_file(bucket, target_file_path, object_path):
    with open(target_file_path, 'rb') as fileobj:
        res = bucket.put_object(object_path, fileobj) # object_path为Object的完整路径，路径中不能包含Bucket名称。
        if res.status != 200:
            raise Exception('upload %s error，status:%s' % (target_file_path, res.status))

if __name__ == '__main__':
    auth = oss2.Auth('xxxx', 'xxxxx')
    # oss2.Bucket(auth, endpoint, bucket_name)
    # endpoint填写Bucket所在地域对应的endpoint，bucket_name为Bucket名称。以华东1（杭州）为例，填写为https://oss-cn-hangzhou.aliyuncs.com。
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'backupgerouth')
    oss_objects_path = []  # 存放上传成功文件对应的OSS对象相对路径
    target_path = "test.wav"
    object_path = 'a2f/test.wav'
    start_time = time.time()
    upload_file(bucket, target_path, object_path)
    oss_objects_path.append(object_path)
    # 记录结束时间
    end_time = time.time()
    # 计算运行时间
    run_time = end_time - start_time
    print("代码运行时间：", run_time, "秒")
