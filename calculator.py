#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import csv
import collections

tax_rate_line = collections.namedtuple('tax_rate_line', ['start_p', 'ratio','deduction'])

tax_rate_table = [
                    tax_rate_line(80000, 0.45, 15160),
                    tax_rate_line(55000, 0.35, 7160),
                    tax_rate_line(35000, 0.3, 4410),
                    tax_rate_line(25000, 0.25, 2660),
                    tax_rate_line(12000, 0.2, 1410),
                    tax_rate_line(3000, 0.1, 210),
                    tax_rate_line(0, 0.03, 0)
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

def social_payment(inco, soc_f):                         #社会保险费用计算
    for key,value in soc_f.items():
        soc_f[key] = float(value)

    soc_ratio = soc_f['YangLao']+ soc_f['YiLiao']+ soc_f['ShiYe']+ soc_f['GongShang']+ soc_f['ShengYu']+ soc_f['GongJiJin']

    if inco < soc_f['JiShuL']:
        soc_payment = soc_f['JiShuL'] * soc_ratio
    elif inco < soc_f['JiShuH']:
        soc_payment = inco * soc_ratio
    else:
        soc_payment = soc_f['JiShuH'] * soc_ratio
    return soc_payment

def l_str(list_t):
    str_s = ''
    j = 1
    for i in list_t:
        if j < len(list_t):
            str_s = str_s + str(i) +','
        else:
            str_s += str(i)
        j += 1
    return str_s

def tax_compute(salary_f, social_f):
    salary_table = []
    for key,value in salary_f.items():
        try:
            income = int(value)
        except:
            print('Parameter Error')
            continue
        soc_payment = social_payment(income, social_f)
        tax_payable = income - soc_payment - tax_threshold 
        for tax_rat_l in tax_rate_table:
            
            if tax_payable > tax_rat_l.start_p:
                tax = tax_payable * tax_rat_l.ratio - tax_rat_l.deduction
            else:
                tax = 0
            after_tax_salary = income -soc_payment - tax
        salary_l = l_str([key, income,soc_payment,tax,after_tax_salary])
        salary_table.append(salary_l)
    return salary_table

def outfile(l_f):
    with open('taxtable.csv', 'w') as f:
        for l in l_f:
            f.write(l+'\n')

if __name__ == '__main__':
    salary_file = get_salary_file(sys.argv[1])         #获取员工工资数据文件
    social_file = get_socialsecurity_file(sys.argv[2]) #获取社保比例配置文件
    salary_tabf = tax_compute(salary_file, social_file) #应纳税计算
    outfile(salary_tabf)
