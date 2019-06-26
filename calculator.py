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

class Args():
    def __init__(self):
        self.args = sys.argv[1:]

    def read_path(self, num):
            index = self.args.index(num)
            return self.args[index + 1]

    @property
    def config_path(self):
        return self.read_path('-c')
    
    @property
    def user_path(self):
        return self.read_path('-d')
    
    @property
    def out_path(self):
        return self.read_path('-o')

class Userdata():
    def __init__(self):
        self.userdata_d = self.read_users_data()
    def read_users_data(self):
        dict1 = {}
        try:
            with open(args.user_path, 'r') as file:
                for l in csv.reader(file):
                    dict1[l[0]] = l[1]
            return dict1
        except:
            print('wrong path')
            sys.exit()

class Config():
    def __init__(self):
        self.config_d = self.read_config() 
    def read_config(self):
        dict2 = {}
        try:
            with open(args.config_path, 'r') as file:
                for l in file.readlines():
                    l1 = (l.strip('\n')).split(' = ')
                    dict2[l1[0]] = l1[1]
            return dict2
        except:
            print('wrong path')
            sys.exit()

def social_payment(inco, soc_f):                        
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
        soc_payment_l = '{:.2f}'.format(soc_payment)
        tax_l = '{:.2f}'.format(tax)
        after_tax_salary_l = '{:.2f}'.format(after_tax_salary)

        salary_l = [key, income,soc_payment_l,tax_l,after_tax_salary_l]
        salary_table.append(salary_l)
    return salary_table

def outfile(l_f):
    with open(args.out_path, 'w') as f:
        csv.writer(f).writerows(l_f)

if __name__ == '__main__':
    args = Args()
    config = Config()
    userdata = Userdata()        
    salary_tabf = tax_compute(userdata.userdata_d, config.config_d) 
    outfile(salary_tabf)
