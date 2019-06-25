#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import csv
import collections

tax_rate_line = collections.nametuple('tax_rate_table', [end_p, ratio, deduction])

tax_rate_table = [
                    tax_rate_line(0, 0.03, 0)
                    tax_rate_line(3000, 0.1, 210)
                    tax_rate_line(12000, 0.2, 1410)
                    tax_rate_line(25000, 0.25, 2660)
                    tax_rate_line(35000, 0.3, 4410)
                    tax_rate_line(55000, 0.35, 7160)
                    tax_rate_line(80000, 0.45, 15160)
                    ]
tax_threshold = 5000

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

def social_payment(inco, soc_f):                  #社会保险费用计算
    soc_ratio = sum(soc_f[YangLao], soc_f[YiLiao], soc_f[ShiYe], soc_f[GongShang], soc_f[ShengYu], soc_f[GongJiJin])

    if inco < soc_f[JiShuiL]:
        soc_payment = soc_f[JiShuiL] * soc_ratio
    elif inco < soc_f[JiShuiH]:
        soc_payment = inco * soc_ratio
    else:
        soc_payment = soc_f[JiShuiH] * soc_ratio
    return soc_payment

def tax_compute(salary_f, social_f):
    for value in salary_f:
        try:
            income = int(value)
        except:
            print('Parameter Error')
            continue
    tax_payable = income - social_payment(income, social_f) - tax_threshold


if __name__ == '__main__':
    salary_file = get_salary_file(sys.argv[1])         #获取员工工资数据文件
    social_file = get_socialsecurity_file(sys.argv[2]) #获取社保比例配置文件
    tax_compute(salary_file, social_file)              #应纳税计算
