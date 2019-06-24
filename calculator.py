#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import csv

def get_salary_file(path):
    dict1 = {}
    try:
        with open(path, 'r') as file:
            for l in csv.reader(file):
                dict1[l[0]] = l[1]
        return dict1
    except:
        print('wrong path')
        sys.exit()

def get_socialsecurity_file(path):
    dict2 = {}
    try:
        with open(path, 'r') as file:
            for l in file.readlines():
                l1 = (l.strip('\n')).split(' = ')
                dict2[l1[0]] = l1[1]
        return dict2
    except:
        print('wrong path')
        sys.exit()

def tax_compute(d1, d2):
    for value in d1:
        try:
            income = int(value)
        except:
            print('Parameter Error')
            continue
        

if __name__ == '__main__':
    f1 = get_salary_file(sys.argv[1])                 #获取员工工资数据文件
    f2 = get_socialsecurity_file(sys.argv[2])         #获取社保比例配置文件
    tax_compute(f1,f2)
