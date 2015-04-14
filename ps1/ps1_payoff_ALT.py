#PROBLEM SET 1 - Problem 3
#payoff debt in one year w/ bisection search

ou_bal = raw_input("What is the outstanding balance on the credit card? ")
AIR = raw_input("What is the APR on the card? ")

#checks for min. payment required to pay off debt in one year using bi.search
def check_payment():
    #max possible payment
    high = round((float(ou_bal) * (1 + (float(AIR)/12))**12)/12)
    #min possible payment    
    low = round(float(ou_bal)/12)
    while True:
        #bisection search implemented
        pmnt = round((high + low)/2.0, 2)
        check = pay_off(ou_bal, AIR, pmnt)
        if check[1] < -0.12:
            high = pmnt
        elif check[1] > 0:
            low = pmnt
        else:
            print "Monthly payment to pay off debt in one year: {}\n"\
            "Number of months needed: {}\n"\
            "Balance: {}\n".format(pmnt, check[0], round(check[1], 2))
            break       

#function that checks, given a payment, how much of balance left after 12 months
def pay_off(ou_bal, AIR, pmnt):
    MIR = float(AIR)/12
    months = 0
    curr_bal = float(ou_bal)
    for i in range(1, 13):
        months += 1
        curr_bal = curr_bal * (1 + MIR) - pmnt
    return months, curr_bal   
    
#run program
check_payment()
