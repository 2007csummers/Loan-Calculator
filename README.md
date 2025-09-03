# Loan Planner
***
## A Brief Synopsis
The loan planner application is a lightweight application that allows the user to create up to 14 loans. The loans are then 
simulated through their lifetime and data is recorded at each simulated payment. Some of this data can be viewed in two graphs
(principal over time and interest accrued through date). A "snapshot" of the user's loans can be saved or opened from their computer.
 
 ---
 ---

 ## A Deeper Dive 

 ### The Interface

 The main window is comprised of a single menu bar. This menu bar contains all of the functionallity of the program and is split into three sections: File, Edit, View

 **File -** Contains all functions related to accessing or saving loan profiles. 
 
- Open allows the user to open an existing .lpfs file (more on that later), loading that file's loans into the application. 

- Save As allows the user to save the current loan profile to any location on their device for future access.

**Edit -** Contains all functions related to making and managing loans.

- Add Loan allows the user to create an entirely new loan within the current loan profile. 

- Manage Loans allows the user to view all loans existing within the current loan profile and their key attributes (color on graph, rate, monthly payment, etc.). Additionally, the user can remove loans from the profile from this window.

**View -** Contains all functions related to viewing loan progress over time. The most useful section from an analysis perspective.

- Principals allows the user to see the principal (or money that is accruing interest) as a function of time over the entire lifetime of the loan.

- Interests (my personal favorite for comparisons) allows the user to see the total interest accrued on the loan as a function of time. This metric shows the rate at which you are losing money (the slope) and the total amount lost by that point in time (the value of the graph).

### The Loans

The loans in this application are all comprised of 13 attributes: principal_init, principal, cur_interest, payment, rate, term, compounding, roll_in, frequency, start_yaer, defered, principal_ot,  interest_ot

**principal_init -** The initial value of the loan in dollars (aka the amouunt of money you get).

**principal -** The runtime value of the principal in dollars. This changes throughout the simulation.

**cur_interest -** The runtime value of the total interest of the loan in dollars. This changes throughout the simulation.

**payment -** The monthly payment in dollars calculated for this loan.

**rate -** The Annual Percentage Yield (APY) of the loan (in decimal form).

**term -** The number of years spent paying the loan (not including periods of deferment if applicable). Should be integer values.

**compounding -** A boolean describing the nature of the loan's interest, True -> compound interest, False -> simple interest.

**roll_in -** A boolean describing the nature of the loan's deferment interest. Some simple interest loans will add your interest accrued during deferment to the principal after the deferment period is over and some won't. True -> interest is added to principal, False -> interest is not added to principal. ONLY FUNCTIONAL WITH SIMPLE INTEREST LOANS. LEAVE FALSE FOR COMPOUNDING LOANS.

**frequency -** The number of times a year that payments are made on the loan. The simulation also accrues interest over this same interval, which may cause slight innacuracies if interest capitalization is asynchronous to payments.

**start_year -** The year on which the loan is started. months are represented as decimals for ease of graphing.

**defered -** The number of months for which the loan is defered for prior to payments beginning.

**principal_ot -** A dictionary keyed by year (still represented with months as decimals) with values of the principal at that time. This is used for plotting the principals graphs.

**interest_ot -** A dictionary keyed by year (still represented with months as decimals) with values of the total interest accrued at that time. This is used for plotting the interests graphs.

### The Payments

The three main types of loans (compounding interest, simple interest no roll in, and simple interest roll in) all have different ways of calculating their omnthly payment.

**Compounding -**  The compounding interest payment is as simple as plugging into a basic formula learned in high school algebra. This formula is as follows:
$$
payment =P\frac{\frac{r}{f}\dot(1 + \frac{r}{f})^{tf}}{(1 + \frac{r}{f})^{tf} - 1}
$$
$$
P = principal_0
$$
$$
r = rate
$$
$$
f = frequency
$$
$$
t = term (years)
$$

**Simple roll in -** The simple interst payment is more complicated as no real formula was to be found. Because of this, I was forced to find my own solution, which, in this case, was making my own formula. 

We can split the loan into two pools - Interest and Principal

On a simple interest loan with roll in, the total interest accrued over the deferment period is added to the principal immediately after the deferment period ends.

Once this new principal has been found, interest is added to the interest pool at a rate of 

$$
P\frac{r}{f}
$$
every payment cycle. 

Assuming the most predatory practices (which I feel is reasonable to assume of a lending firm), the payment will go towards the interest pool before the remainder is put towards the principal pool. This means the principal pool will go down every payment by 

$$
payment - P\frac{r}{f}
$$

or the new principal will be

$$
 P - (payment - P\frac{r}{f})
$$
$$
= P(1 + \frac{r}{f}) - payment
$$

If we assume that all payments will be equal (which is not true in reality. Most loans will have a larger or smaller final payment.), we know that last payment will be equal to 

$$
P_f(1 + \frac{r}{f})
$$

because the principal must equal zero after the final payment. All of the values in this equation are known except for the final principal value. This can be found, however by using the aforementioned formula for new principal:

$$
P_f = P_{f - 1}(1 + \frac{r}{f}) - payment
$$

This process can be done recursively n times until n = f, or rather until n = the number of payments (which is also t * f). When you plug in the new value for P<sub>f</sub> and distribute, you get

$$
payment = P_{f-1}(1 + \frac{r}{f})^2 - payment(1 + \frac{r}{f})
$$

Or

$$
payment(1 + (1 + \frac{r}{f})) = P_{f-1}(1 + \frac{r}{f})^2
$$

If we imagine that this loan is a three year loan with one payment each year (t = 3, f = 1), we would need one more round of iteration which would look something like:

$$
payment(1 + (1 + \frac{r}{f})) = (P_0(1 + \frac{r}{f}) -payment)((1 + \frac{r}{f})^2)
$$

Or 

$$
payment(1 + (1 + \frac{r}{f}) + (1 + \frac{r}{f})^2) = P_0(1 + \frac{r}{f})^3
$$

In this situation, all of the variables besides payment are known constants, so we can solve for payment:

$$
payment = \frac{P_0(1 + \frac{r}{f})^3}{(1 + (1 + \frac{r}{f}) + (1 + \frac{r}{f})^2)}
$$

The denominator can be simplified into

$$
\displaystyle\sum_{n=0} ^{2}(1 +\frac{r}{f})^i
$$

resulting in a final equation:

$$
payment = \frac{P_0(1 + \frac{r}{f})^3}{\displaystyle\sum_{n=0} ^{2}(1 +\frac{r}{f})^i}
$$

This is obviously not a general form, but it can be generalized like so:

$$
payment = \frac{P_0(1 + \frac{r}{f})^{tf}}{\displaystyle\sum_{n=0} ^{tf - 1}(1 +\frac{r}{f})^i}
$$

$$
P_0 = principal_0
$$
$$
r = rate
$$
$$
f = frequency
$$
$$
t = term (years)
$$

**simple interst no roll in -** I took a less analyical approach to this problem and decided to create a "gradient" descent algorithm. This algorithm traverses the principal remainder vs payment graph until it reaches a "satisfactory minimum" (this i an arbitrarily assigned range of numbers between which the principal is effectively zero, resulting in a "good enough" approximation of the payment).

This descent is achieved by slightly tweaking the tested payment value repeatedly until a satisfactory principal remainder is reached. This process is made simple by the near parabolic behavior of the graph: whenever the principal remainder is too high, the payment is raised, and vice versa. When the remainder from the previous test is a different sign than the current iteration, the increment/decrement step is halved. This results in the function gradually approaching an acceptable payment.

The test values for payment are tested by running a simulation of the loan using said value and looking at the final value of the principal.

A small amount of efficiency is gained by using a start value given by the simple interest roll in payment calculation which typically isn't incredibly far off of an acceptable payment value and has the added benefit of always being more payment than needed.

### The Simulation

Each loan is simulated throughout its life in order to collect data for plotting and analysis. The simulation can be broken down into 3 main phases: payment calculation, deferment, normal lifetime.

**Payment Calculation-** This phase involves running one of the three aforementioned functions/calculations based on the type of loan. The only output of this phase is an accurate payment amount is assigned to the payment instance variable of the loan.

**Deferment -** This phase is optional. If the loan is not created with a non-zero value for the deferment instance variable, the loan skips this phase. If it does have a non-zero deferment value, the loan is simulated for that many months as described by the type of loan.

Compound interest loans will accrue and capitalize interest a frequency number of times per year.

Simple interest loans will accrue interest at a constant rate every month, adding it to the "interest pool." This pool will be added to the principal at the end of deferment if roll_in is true, or remain in this separate pool for the lifetime of the loan if roll_in is false.

**Normal Lifetime -** The normal lifetime is the period in time for which you are paying on the loan. During this period, interest is calculated identically to during the deferment period, but the payment is subtracted from the total value of the loan. 

I have opted for the safest option for payments which requires the payment to first go towards the interest, with the remainder going towards the principal. This is the safest option as it maximizes interest accrued, so you will only ever get expected or good news when applying for the loan.

The differentiation between interest and principal pools is not applicable to compound interest loans as the interest is immediately added to the principal