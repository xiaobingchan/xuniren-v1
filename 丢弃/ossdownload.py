#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import oss2
import time

if __name__ == '__main__':

    auth = oss2.Auth('xxxx', 'xxxxx')
    # oss2.Bucket(auth, endpoint, bucket_name)
    # endpoint填写Bucket所在地域对应的endpoint，bucket_name为Bucket名称。以华东1（杭州）为例，填写为https://oss-cn-hangzhou.aliyuncs.com。
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'backupgerouth')
    target_file_local_path = 'test.wav' # 本地文件路径
    oss_object_path = 'a2f/test.wav'
    # bucket.get_object_to_file('object_path', 'object_local_path')
    # object_path 填写Object完整路径，完整路径中不包含Bucket名称，例如testfolder/exampleobject.txt。
    # object_local_path 下载的Object在本地存储的文件路径，形如 D:\\localpath\\examplefile.txt。如果指定路径的文件存在会覆盖，不存在则新建。
    start_time = time.time()
    res = bucket.get_object_to_file(oss_object_path, target_file_local_path)
    # 记录结束时间
    end_time = time.time()
    # 计算运行时间
    run_time = end_time - start_time
    print("代码运行时间：", run_time, "秒")
    
      