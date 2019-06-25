#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import csv
import collections

tax_rate_line = collections.nametuple('tax_rate_table', [start_p, ratio, deduction])

tax_rate_table = [
                    tax_rate_line(80000, 0.45, 15160)
                    tax_rate_line(55000, 0.35, 7160)
                    tax_rate_line(35000, 0.3, 4410)
                    tax_rate_line(25000, 0.25, 2660)
                    tax_rate_line(12000, 0.2, 1410)
                    tax_rate_line(3000, 0.1, 210)
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

def social_payment(inco, soc_f):                         #��ᱣ�շ��ü���
    for key,value in soc_f.items():
        soc_f[key] = float(value)

    soc_ratio = sum(soc_f[YangLao], soc_f[YiLiao], soc_f[ShiYe], soc_f[GongShang], soc_f[ShengYu], soc_f[GongJiJin])

    if inco < soc_f[JiShuiL]:
        soc_payment = soc_f[JiShuiL] * soc_ratio
    elif inco < soc_f[JiShuiH]:
        soc_payment = inco * soc_ratio
    else:
        soc_payment = soc_f[JiShuiH] * soc_ratio
    return soc_payment

def tax_compute(salary_f, social_f):
    count = 0
    for key,value in salary_f.items():
        try:
            income = int(value)
        except:
            print('Parameter Error')
            continue
        soc_payment = social_payment(income, social_f)
        tax_payable = income - soc_payment - tax_threshold 
        for tax_rat_l in tax_rate_table:
            if tax_payable > tax_rat_l[start_p]:
                tax = tax_paysble * tax_rat_l[ratio] - tax_rat[deduction]
            else:
                tax = 0
            after_tax_salary = income -soc_payment - tax
        salary_l = [key,income,soc_paymet,tax,after_tax_salary]
        salary_table[count] = salary_l
        count += 1
    return salary_table

if __name__ == '__main__':
    salary_file = get_salary_file(sys.argv[1])         #��ȡԱ�����������ļ�
    social_file = get_socialsecurity_file(sys.argv[2]) #��ȡ�籣���������ļ�
    tax_compute(salary_file, social_file)              #Ӧ��˰����
