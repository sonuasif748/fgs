"""
Common funtionality method avaiable file 
"""
import re
#from functools import reduce
from enum import Enum


def str_fmt(value):
    if not value:
        return ""
    value = re.sub('[^a-zA-Z0-9 \n\.]', '', value)
    return value.replace(" ", "").lower()

if __name__ == '__main__':
    print(str_fmt("ee ' covered by PGA,1972"))
    
    
class SalaryHeads(Enum):
    hra = 'HRA'
    basicsalary = "Basic Salary"
    hostelallowance = "Hostel allowance"
    childreneducation = "Children education allowance"
    tavelingallowance = "Travelling or tour allowance"
    otherallowance = "Other allowance"
    gratuity = "Gratuity"
    overtime = "Overtime"
    advancesalary = "Adavance Salary"
    bonus = "Bonus"
    salaryarrears = "Salary Arrears"
    feescommission = "Fees & Commission"
    commutedpension = "Annuity or uncommuted pension"
    leavesalaryemployment = "Leave salary during employment"
    entertainmentallowance = "Entertaiment allowance"
    citycompensatoryallowance = "City compensatory allowance"
    ltrallowance = "Lunch / Tiffin /Refreshment allowance"
    helperallowance = "Helper/assistant allowance"
    conveyanceallowance = "Conveyance allowance"
    dailyallowance = "Daily Allowance"
    researchallowance = "Research Allowance"
    uniformallowance = "Uniform allowance"
    retrenchmentcompensation = "Retrenchment compensation"

    total = "Total"
    esi_empr = "esi_empr"
    pf_empr = "pf_empr"