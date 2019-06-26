#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import csv
from collections import namedtuple

tax_rate_line = namedtuple('tax_rate_line', ['start_p', 'ratio','deduction'])

tax_rate_table = [tax_rate_line(80000, 0.45, 15160),
                  tax_rate_line(55000, 0.35, 7160),
                  tax_rate_line(35000, 0.3, 4410),
                  tax_rate_line(25000, 0.25, 2660),
                  tax_rate_line(12000, 0.2, 1410),
                  tax_rate_line(3000, 0.1, 210),
                  tax_rate_line(0, 0.03, 0)
]

tax_threshold = 5000    # 起征点

class Args:
    def __init__(self):
        self.config_path = sys.argv[sys.argv.index('-c')+1]
        self.user_path = sys.argv[sys.argv.index('-d')+1]
        self.out_path = sys.argv[sys.argv.index('-o')+1]


class Userdata:
    def __init__(self):
        with open(args.user_path) as file:
            self.userdata = list(csv.reader(file))


class Config:
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        dict2 = {'shebao': 0}
        with open(args.config_path, 'r') as file:
            for l in file:
                name, value = l.split(' = ')
                if float(value) < 1:
                    dict2['shebao'] += float(value)
                else:
                    dict2[name] = float(value)
        return dict2


def social_payment(inco, soc_f):                        
    for key,value in soc_f.items():
        if inco < float(soc_f['JiShuL']):
            soc_payment = float(soc_f['JiShuL']) * soc_f['shebao']
        elif inco < float(soc_f['JiShuH']):
            soc_payment = inco * soc_f['shebao']
        else:
            soc_payment = float(soc_f['JiShuH']) * soc_f['shebao']
        
    return soc_payment

def tax_compute(salary_f, social_f):
    salary_table = []
    for l in salary_f:
        try:
            income = int(l[1])
        except:
            print('Parameter Error')
            continue
        soc_payment = social_payment(income, social_f)   #社保
        tax_payable = income - soc_payment - tax_threshold #应交税部分
        for tax_rat_l in tax_rate_table:
            if tax_payable > tax_rat_l.start_p:
                tax = tax_payable * tax_rat_l.ratio - tax_rat_l.deduction  #税
                break
            else:
                tax = 0
        after_tax_salary = income -soc_payment - tax     #税后部分
        soc_payment_l = '{:.2f}'.format(soc_payment)
        tax_l = '{:.2f}'.format(tax)
        after_tax_salary_l = '{:.2f}'.format(after_tax_salary)

        salary_l = [l[0], income,soc_payment_l,tax_l,after_tax_salary_l]
        salary_table.append(salary_l)
    return salary_table

def outfile(l_f):
    with open(args.out_path, 'w') as f:
        csv.writer(f).writerows(l_f)

if __name__ == '__main__':
    args = Args()
    config = Config()
    userdata = Userdata()        
    salary_tabf = tax_compute(userdata.userdata, config.config) 
    outfile(salary_tabf)
