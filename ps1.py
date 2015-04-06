#PROBLEM SET 1 - Problem 1
#amount of debt remaining after one year of minimum payment rate

ou_bal = raw_input("What is the outstanding balance on the credit card? ")
AIR = raw_input("What is the APR on the card? ")
minMPR = raw_input("What is the minimum monthly payment rate on the card? ")

#function for finding amount of debt paid off in one year with min.payment rate
def after_year_one(ou_bal, AIR, minMPR):
    MIR = float(AIR)/12
    curr_bal = float(ou_bal)
    total_paid = 0
    for i in range(1, 13):
        payment = round(curr_bal * float(minMPR), 2)
        total_paid += payment
        interest_paid = round(MIR * curr_bal, 2)
        principle_paid = payment - interest_paid
        curr_bal -= principle_paid
        print "Month: {}\nMinimum monthly payment: {}\nPrinciple paid: {}\n"\
              "Remaining balance: {}\n".format(i, payment, principle_paid, curr_bal)
    print "Total amount paid: {}\nRemaining Balance: {}".format(total_paid, curr_bal)

#run program        
after_year_one(ou_bal, AIR, minMPR)
