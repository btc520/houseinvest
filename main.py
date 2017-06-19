#!/usr/bin/python
# -*- coding: UTF-8 -*-

UnitPrice = int(raw_input("单价: (1 W ) ") or "1")
Area = float(raw_input("总面积: (124 平米) ") or "124")
Firstpay =  float(raw_input("首付比例 (30%) ") or "0.3")
rentInit =  float(raw_input("第一个月出租价格 (1800 元) ") or "1800")
rentrise = float(raw_input("每年出租上涨幅度 (5%) ") or "0.05")
checkYear = int(raw_input("检查未来第N年房产价值 (第10年)") or "10")
houseRiseRate = float(raw_input("房产每年升值幅度 (5%) ") or "0.05")
Loanyear = int(raw_input("按揭年限 (30年): ") or "30")
loanrate = float (raw_input("按揭利率 (4.9%): ") or "0.049")

TotalPrice = UnitPrice * Area

FirstpayCost = TotalPrice * Firstpay
Loan = TotalPrice - FirstpayCost



Loanmonth = Loanyear * 12

equa_benj = Loan / Loanmonth

Monthlyrate = loanrate / 12
Monthlyrate_format = round(Monthlyrate*100,4)
Totalinterest = round(Loan * Monthlyrate * ( Loanmonth /2+0.5), 2)
totalCost = round(Totalinterest + TotalPrice,2)

LoanTotal = Loan + Totalinterest
#print LoanTotal

def totalRent(Loanyear, rentrise):
    #计算总租金
    rentTotal = 0
    for i in range(Loanyear):
        k = 0
        k += rentInit * (1+rentrise)**i * 12
        
        rentTotal = rentTotal + k
        
    return rentTotal

  
def DEBJ (month, Loan, Monthlyrate):
    # 等额本金计算，第X月，贷款金额，月利率
    # 偿还同等数额的本金， 本月产生剩余贷款的利息
    temp = equa_benj + (Loan - equa_benj* month) *Monthlyrate
    result = round(temp*10000,1)
    return result




def checkRent(checkYear, rentrise):
    #计算第N年租金收益
    result = rentInit * (1+rentrise) ** checkYear
    return result
    
    
def checkValue(houseRiseRate, checkYear):
    #计算第N年房产升值
    houseFuture = TotalPrice * 10000 * (1+houseRiseRate) ** checkYear
    return houseFuture

def BalanceTotal(Loanyear, TotalPrice, totalCost, houseRiseRate):
    #计算第X年总投资和房产价值平衡点
    for i in range(1,Loanyear):
        houseFuture = TotalPrice * 10000 * (1+houseRiseRate) ** i
        #print (houseFuture)
        if houseFuture>= totalCost * 10000:
            return i, round(houseFuture/10000,1)
            break



def BlanceRent(Loanyear, rentrise, Loan, Monthlyrate):
    #计算第X年收益平衡点
    for i in range(1,Loanyear):
        rentR = checkRent(i, rentrise)
        pay = DEBJ(i*12, Loan, Monthlyrate)
        #print (rentR, pay)
        if rentR>=pay:
            return i, round(rentR), round(pay)
            break

def clear(totalCost, Monthlyrate, LoanTotal, rentrise):
    totalPay = 0
    for j in range(0,30): 
        monthRent = checkRent(j, rentrise)
        #print ("--------------", monthRent)
        rentYear = monthRent * 12
        totalPay += rentYear
        #print rentYear
        for i in range(0,12):
            month = j*12+i
            #print month
            payDEBJ = DEBJ(month, Loan, Monthlyrate)
            #print payDEBJ
            totalPay += payDEBJ
            #print totalPay
            #if payDEBJ <= monthRent:
                #totalPay += 3000
                
            if totalPay >= LoanTotal * 10000:
                #print ("break out at around year %s" % round(month/12,0))
                return round(month/12,0), payDEBJ, monthRent
                break
    #print totalPay

clearYear = clear(totalCost, Monthlyrate, LoanTotal, rentrise)


# 等额本金计算
Monthpay_1 = DEBJ(0, Loan, Monthlyrate)
Monthpay_x = DEBJ(checkYear*12, Loan, Monthlyrate)

#平衡点
BalanceYear_5 = BalanceTotal(Loanyear, TotalPrice, totalCost, 0.05)
BalanceYear_10 = BalanceTotal(Loanyear, TotalPrice, totalCost, 0.1)
BlanceRentR_5 = BlanceRent(Loanyear, 0.05, Loan, Monthlyrate)
BlanceRentR_10 = BlanceRent(Loanyear, 0.1, Loan, Monthlyrate)

# 第N年
checkRentResult = round(checkRent(checkYear, rentrise),1)
checkValueResult = round(checkValue(houseRiseRate, checkYear)/10000,2)


totalRentR = round(totalRent(Loanyear, rentrise)/10000,2)

#print ("-----")
#print("开始打印计算结果...................................")
print ("-----")
#print("按揭...............................................")

print("按揭月利率 %s %%, 等额本金第一个费用 %s" % (Monthlyrate_format, Monthpay_1))

print("房产总价: %s W, 首付 %s 成的费用 %s W, 贷款: %s W, 贷款利息: %s W, 总花费（加利息）: %s W" % (TotalPrice, Firstpay*10, FirstpayCost, Loan, Totalinterest, totalCost))


print ("-----")
print ("未来 - 第 %s年分析: 房产年涨幅 %s %% 租金年涨幅 %s %%" % (checkYear, houseRiseRate*100, rentrise*100))
print ("房产价值: %s W, 出租价格 %s 元, 按揭月费用 %s " % (checkValueResult, checkRentResult, Monthpay_x))


print ("-----")
#print ("未来分析...........................................")
print ("条件:房产升值幅度 5%%  - 第 %s 收支达到平衡, 房产价值 %s 万，总投资为 %s 万" % (BalanceYear_5[0], BalanceYear_5[1], totalCost))
print ("条件:房产升值幅度 10%% - 第 %s 收支达到平衡, 房产价值 %s 万，总投资为 %s 万" % (BalanceYear_10[0], BalanceYear_10[1], totalCost))
print ("条件 租金每年涨幅 5 %%, 第 %s 年租金可以抵房贷(等额本金), 租金 %s, 当期房贷 %s" % (BlanceRentR_5[0], BlanceRentR_5[1], BlanceRentR_5[2] ))
print ("条件 租金每年涨幅 10 %%, 第 %s 年租金可以抵房贷(等额本金), 租金 %s, 当期房贷 %s" % (BlanceRentR_10[0], BlanceRentR_10[1], BlanceRentR_10[2] ))

print ("-----")
print ("条件 租金每年涨幅 5 %%, 第 %s 年可以还清贷款(等额本金), 租金 %s, 当期房贷 %s" % (clearYear[0], clearYear[2], clearYear[1] ))

#print ("未来 - 未来%s (按揭时长)年房产租赁总收入: %s W" % (Loanyear, totalRentR))
