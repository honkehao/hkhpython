L=['可选择的时间货币价值如下','单利终值','单利现值','复利终值','复利现值','普通年金终值',
   '普通年金现值','预付年金终值','预付年金现值','递延年金现值','永续年金现值','增长型永续年金']
for l in L:
    print(l)
s=input('需要计算的时间货币价值（Q/q结束）：')

#公式定义区域
SIFV=lambda pv,r,n:pv*(1+r*n)                #单利终值
SIPV=lambda fv,r,n:fv/(1+r*n)               #单利现值
CIFV=lambda pv,r,n,m:pv*(1+r/m)**(m*n)     #复利终值
CIPV=lambda fv,r,n:fv/(1+r)**n            #复利现值
OAFV=lambda A,r,n:A*((1+r)**n-1)/r       #普通年金终值
OAPV=lambda A,r,n:A*(1-(1+r)**-n)/r     #普通年金现值
ADFV=lambda OAFV,r:OAFV*(1+r)          #预付年金终值
ADPV=lambda OAPV,r:  OAPV*(1+r)         #预付年金现值
DAPV=lambda A,r,n,m: A/r*(1-1/(1+r)**n)*(1+r)**-m #递延年金现值
PPV=lambda A,r:A/r#永续年金现值
GPPV=lambda A,r,g:A/(r-g)#增长型永续年金


#代码执行区域

while True:
    if s.upper()=='Q':
        print('循环结束')
        break
    else:
        if s not in L:
            print('错误')
        elif s in L[:10:]:
            r = float(input('年利率（单位：%）:'))/100
            n = int(input('期限（单位：年）:'))
            z=0
            if s=='单利终值':
                pv=float(input('现值（单位：元）  :'))
                z=SIFV(pv,r,n)
            elif s=='单利现值':
                fv=float(input('终值（单位：元）'))
                z=SIPV(fv,r,n)
                # print('单利现值:{0:.2f}'.format(float(SIPV(fv,r,n))))
            elif s=='复利终值':
                m=int(input('每年复利的次数:'))
                pv=float(input('现值（单位：元）  :'))
                z=CIFV(pv,r,n,m)
                # print('复利终值:{0:.2f}'.format(float(CIFV(pv,r,n,m))))
            elif s=='复利现值':
                fv=float(input('终值（单位：元）'))
                z=CIPV(fv,r,n)
            elif s=='普通年金终值':
                A=float(input('年金（单位：元）:'))
                z=OAFV(A,r,n)
            elif s=='普通年金现值':
                A=float(input('年金（单位：元）:'))
                z=OAPV(A,r,n)
            elif s=='预付年金终值':
                A = float(input('每期支付金额（单位：元）:'))
                z=ADFV(OAFV(A,r,n),r)
            elif s=='预付年金现值':
                A = float(input('每期支付金额（单位：元）:'))
                z=ADPV(OAPV(A,r,n),r)
            elif s == '递延年金现值':
                A = float(input('每期支付金额（单位：元）:'))
                m=int(input('递延期（单位：年）'))
                z=DAPV(A,r,n,m)
                print('{0}:{1:.2f}元'.format(s, float(z)))
            print('{0}:{1:.2f}元'.format(s, float(z)))
            s = input('需要计算的时间货币价值（Q/q结束）：')
        elif s in L[10::]:
            A = float(input('每期支付金额（单位：元）:'))
            r = float(input('年利率（单位：%）:')) / 100
            if s=='永续年金现值':
                z=PPV(A,r)
                print('{0}:{1:.2f}元'.format(s, float(z)))
            elif s=='增长型永续年金':
                g=float(input('固定比率(单位：%):'))/100
                if r>g:
                    z=GPPV(A,r,g)
                    print('{0}:{1:.2f}元'.format(s, float(z)))





'''
我给这段代码添加了一个循环，用来让用户可以连续的计算需要的时间价值
while True:                            #使用while进行循环
    if s.upper()=='Q':                 设置循环结束语句，让用户可以更好的使用
        print('循环结束')
        break
    else:
    
'''










