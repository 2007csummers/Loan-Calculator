class loans:

    #Frequency is the number of times a year that a loan is compounded.
    #Defered is the number of months over which you will not be making payments on the loan
    #Term is the term length in years. Begins after the deferement period is finished

    #                    int,    float, int,     bool,       int,        int,      int,    bool,        
    def __init__(self, principal, rate, term, compounding, frequency, start_year, defered, roll_in):
        self.principal = principal
        self.rate = rate
        self.term = term
        self.compounding = compounding
        self.roll_in = roll_in
        self.frequency = frequency
        self.start_year = start_year
        self.defered = defered
        self.principal_ot = {start_year: self.principal}
        self.interest_ot = {start_year: 0}
        self.payment = 0
        

    def accrue(self):
        if self.compounding:
            temp_interest = self.principal * (self.rate/self.frequency)
            self.principal += temp_interest
            return temp_interest
        else:
            temp_interest = self.principal * self.rate/self.frequency
            return temp_interest
    

    def  accrue_lifetime(self):
        year_count = 1.0
        year_accrue = 0

        #Logic Required to accrue interest during the defering window of the loan
        for i in range(int(((self.defered * self.frequency)/ 12) + (self.frequency * self.term))):
            interval_accrue = self.accrue()
            year_accrue = interval_accrue
            
            if i > int(self.defered * self.frequency / 12):

                if self.payment == 0:
                    if self.roll_in:
                        self.principal += self.interest_ot[self.start_year + year_count - 1] + year_accrue
                    if self.compounding:
                        self.payment = self.comp_monthly_payment()
                    else:
                        self.payment = self.simp_monthly_payment()
                if i == range(int(((self.defered * self.frequency)/ 12) + (self.frequency * self.term))):
                    self.principal = 0
                elif self.compounding:
                    self.principal -= self.payment
                else:
                    self.principal = self.principal - self.payment + interval_accrue

            if (i + 1) % self.frequency == 0:
                self.interest_ot[self.start_year + year_count] = self.interest_ot[self.start_year + year_count -1] + year_accrue
                self.principal_ot[self.start_year + year_count] = self.principal
                year_count += 1
                year_accrue = 0
        
        #self.principal = 0
        #self.principal_ot[self.start_year + year_count - 1] = 0




    def comp_monthly_payment(self):
        return self.principal * ( (self.rate/self.frequency * (1 + self.rate/self.frequency) ** (self.term * self.frequency) ) / ((1 + self.rate/self.frequency) ** (self.term * self.frequency) - 1) )
            

    def simp_monthly_payment(self):
        return self.principal * ((1 + self.rate / self.frequency) ** (self.term * self.frequency)) / self.simp_bot(self.term * self.frequency - 1)
    


    def simp_bot(self, iterations):
        if iterations == 0:
            return 1
        return (self.rate / self.frequency + 1) ** iterations + self.simp_bot(iterations - 1)