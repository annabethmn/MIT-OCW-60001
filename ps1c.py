# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 23:18:19 2020

@author: annab
"""
annual_salary= float(input("Enter annual salary..."))
monthly_salary=annual_salary/12
total_cost=1000000
down_payment=250000
annual_return=0.04
semi_annual_raise=0.07
months=0 
epsilon=100
low=0
high=10000
guess=(low+high)/2
r=0.04
current_savings=0
monthly_return=current_savings*r/12
num_guesses=0

while (abs(current_savings-down_payment))>=epsilon:
    #define variables within the scope of while loop 
    current_savings=0
    annual_salary_loop=annual_salary
    monthly_salary_loop=annual_salary_loop/12
    #update current savings monthly for 3 years
    for months in range (1,37):
        #update annual salary within scope of while loop 
        if months%6==0:
            annual_salary_loop+=semi_annual_raise*annual_salary_loop
            monthly_salary_loop=annual_salary_loop/12
        current_savings+=monthly_salary*guess/10000
        current_savings+=monthly_return
        monthly_return=current_savings*r/12
        months+=1
    if current_savings<down_payment:
        #exclude all guesses lower than previous guess
        low=guess
    else:
        #exclude all guesses higher than previous guess
        high=guess
    guess=(high+low)/2 
    num_guesses+=1
    if num_guesses>13:
        #after 13 guesses, the savings rate is close to either 0 or 100%
        break
if num_guesses>13:
    print("It is not possible to save for the down payment in 3 years")
else:
    print ("Best savings rate:", guess/10000)
    print ("Steps in bisection search:", num_guesses)

    
