# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:23:38 2020

@author: annab
"""
#initialize variables
total_cost=float(input("Enter total cost..."))
annual_salary=float(input("Enter annual salary..."))
portion_saved=float(input("Enter portion of salary saved, as a decimal..."))
semi_annual_raise=float(input("Enter semi-annual raise, as a decimal..."))
portion_down_payment=0.25*total_cost
current_savings=0
months=0
monthly_salary=annual_salary/12
r=0.04
monthly_return=0

#increment current_savings until portion_down_payment is reached
while current_savings<portion_down_payment:
    current_savings+=monthly_salary*portion_saved 
    current_savings+=monthly_return
    monthly_return=current_savings*r/12
    months+=1
    #update annual_salary every 6 months 
    if months%6==0:
        annual_salary+=semi_annual_raise*annual_salary
        monthly_salary=annual_salary/12
        
print("It will take", months, "months to save for a down payment of", portion_down_payment)
