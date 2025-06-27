import copy
class loans:

    #Frequency is the number of times a year that a loan is compounded.
    #Defered is the number of months over which you will not be making payments on the loan
    #Term is the term length in years. Begins after the deferement period is finished

    #                    int,    float, int,     bool,       int,        float,      int,    bool,        
    def __init__(self, principal, rate, term, compounding, frequency, start_year, defered, roll_in):
        self.principal_init = principal
        self.principal = principal
        self.cur_interest = 0
        self.payment = 0
        self.rate = rate
        self.term = term
        self.compounding = compounding
        self.roll_in = roll_in
        self.frequency = frequency
        self.start_year = start_year
        self.defered = defered
        self.principal_ot = {start_year: self.principal}
        self.interest_ot = {start_year: 0}
       
        

    def accrue(self, paying, date, time_inc):
        if self.compounding:
            temp_interest = self.principal * (self.rate/self.frequency)
            self.principal += temp_interest
            self.interest_ot[date] = self.interest_ot[date- time_inc] + temp_interest
            if paying:
                self.principal -= self.payment
            self.principal_ot[date] = self.principal
        else:
            temp_interest = self.principal * self.rate/self.frequency
            self.interest_ot[date] = self.interest_ot[date - time_inc] + temp_interest
            self.cur_interest += temp_interest
            if paying:
                if self.payment > self.cur_interest:
                    self.principal -= (self.payment - self.cur_interest)
                    self.cur_interest = 0
                else:
                    self.cur_interest -= self.payment
            self.principal_ot[date] = self.principal
                
        
    

    def  accrue_lifetime(self):
        time_inc = 1 / (self.frequency)
        date = self.start_year
        
        for i in range(int(self.defered / (12 / self.frequency))):
            date += time_inc
            self.accrue(False, date, time_inc)

        if self.payment == 0:
            if self.compounding:
                self.payment = self.comp_monthly_payment()
            else:
                if self.roll_in:
                    self.principal += self.cur_interest
                    self.cur_interest = 0
                    self.payment = self.simp_monthly_payment()
                else:
                    self.payment = self.simp_monthly_payment_no_roll(self.simp_monthly_payment(), 1, 1, 0.2)
    

        for i in range(self.term * self.frequency):
            date += time_inc
            self.accrue(True, date, time_inc)

            





    def comp_monthly_payment(self):
        return self.principal * ( (self.rate/self.frequency * (1 + self.rate/self.frequency) ** (self.term * self.frequency) ) / ((1 + self.rate/self.frequency) ** (self.term * self.frequency) - 1) )
            

    def simp_monthly_payment(self):
        return self.principal * ((1 + self.rate / self.frequency) ** (self.term * self.frequency)) / self.simp_bot(self.term * self.frequency - 1) + (self.cur_interest / (self.term * self.frequency))
    

    def simp_monthly_payment_no_roll(self, temp_payment, direction, multiplier, step):
        copy_loan = copy.deepcopy(self)
        copy_loan.payment = temp_payment * multiplier

        time_inc = 1 / (self.frequency)
        date = copy_loan.start_year
        for i in range(copy_loan.term * copy_loan.frequency):
            date += time_inc
            copy_loan.accrue(True, date, time_inc)
        
        if abs(copy_loan.principal) < 100:
            return temp_payment * multiplier
        elif direction * copy_loan.principal > 0:
            return self.simp_monthly_payment_no_roll(temp_payment, direction, multiplier + (direction * step), step)
        else:
            return self.simp_monthly_payment_no_roll(temp_payment, direction * -1, multiplier - (direction * step/2), step/2)
            


    def simp_bot(self, iterations):
        if iterations == 0:
            return 1
        return (self.rate / self.frequency + 1) ** iterations + self.simp_bot(iterations - 1)