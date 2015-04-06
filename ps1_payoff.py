#PROBLEM SET 1 - Problem 2
#payoff debt in one year

ou_bal = raw_input("What is the outstanding balance on the credit card? ")
AIR = raw_input("What is the APR on the card? ")

#checks for min. payment required to pay off debt in one year
def check_payment():
    pmnt = 10
    while True:
        #uses pay_off function to see if debt is paid off using current min. pay        
        check = pay_off(ou_bal, AIR, pmnt)
        #if debt paid off within 12 months, we have found the min. payment        
        if check[0] <= 12 and check[1] <= 0:
            print "Monthly payment to pay off debt in one year: {}\n"\
            "Number of months needed: {}\n"\
            "Balance: {}\n".format(pmnt, check[0], check[1])
            break
        #if debt not paid off within 12 months, increase min. payment by 10
        pmnt += 10 
              

#checks to see if payment given can pay off debt within 12 months
def pay_off(ou_bal, AIR, pmnt):
    MIR = float(AIR)/12
    months = 0
    curr_bal = float(ou_bal)
    for i in range(1, 13):
        if curr_bal <= 0:
            #payoff condition has been satisfied, months may be <= 12
            return months, round(curr_bal, 2)
        months += 1
        curr_bal = curr_bal * (1 + MIR) - pmnt
    #payoff condition has NOT been satisfied
    return months, round(curr_bal, 2)
       
#run program    
check_payment()
