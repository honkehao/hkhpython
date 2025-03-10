def Value_added_tax(amount,rate=0.13):
    '''
    定义计算增值税的函数
    :param amount: 不含税金额
    :param rate: 税率（默认13%）
    :return: 税额，含税价
    '''
    tax=amount*rate#税额=不含税金额*税率
    Tax_inclusive=amount+tax#含税价=不含税价+税额
    return round(tax,2),round(Tax_inclusive,2)

t=float(input("请输入不含税价（单位：元）："))
print('(税额,含税价)')
print(Value_added_tax(t))