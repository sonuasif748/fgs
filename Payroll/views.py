from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from Employee.models import *
from Global.models import *
from Organisation.models import *
from InTax.models import *
from Attendence.models import *
from .constants import *

# Create your views here.


class Co_SalsetupList(generics.ListCreateAPIView):
    queryset = CoSalsetup.objects.all()
    serializer_class = Co_SalsetupSerializer


class Co_SalsetupDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoSalsetup.objects.all()
    serializer_class = Co_SalsetupSerializer
    
    
class Company_SalsetupList(generics.ListCreateAPIView):
    queryset = CompanySalsetup.objects.all()
    serializer_class = Company_SalsetupSerializer


class Company_SalsetupDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanySalsetup.objects.all()
    serializer_class = Company_SalsetupSerializer
    
    
class EmpCtcMasterList(generics.ListCreateAPIView):
    queryset = EmpCtcMaster.objects.all()
    serializer_class = EmpCtcMasterSerializer


class EmpCtcMasterDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmpCtcMaster.objects.all()
    serializer_class = EmpCtcMasterSerializer


class EmpMonPayrollList(generics.ListCreateAPIView):
    queryset = EmpMonPayroll.objects.all()
    serializer_class = EmpMonPayrollSerializer


class EmpMonPayrollDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmpMonPayroll.objects.all()
    serializer_class = EmpMonPayrollSerializer


class EmpMonthCtcMasterList(generics.ListCreateAPIView):
    queryset = EmpMonthCtcMaster.objects.all()
    serializer_class = EmpMonthCtcMasterSerializer


class EmpMonthCtcMasterDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmpMonthCtcMaster.objects.all()
    serializer_class = EmpMonthCtcMasterSerializer

def exemp_hra (id, amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    master = emp.empctcmaster_set.get()

    hra_recived = master.salary_head[SalaryHeads.hra.value]
    sal = master.salary_head[SalaryHeads.basicsalary.value]
    actual_rent_paid = amt
    hra = Exemptions.objects.get(sec="10(13A)", fy= master.fy)
    rent = actual_rent_paid - hra.sal_per/100 * sal
    if emp.perm_addr['city'] in metro_cities:
        actual_hra = sal * hra.hra_mc
    else:
        actual_hra = sal * hra.hra_mc
    if rent <= 0:
        rent = 0
    return min(hra_recived, actual_hra, rent)

def exemp_retrenchment(id,  ret_er_amt, ret_ee_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    master = emp.empctcmaster_set.get()
    start_date = emp.doj
    end_date = datetime.now().date()
    difference = end_date - start_date
    year_of_service = round((difference.days + difference.seconds / 86400) / 365.2425)
    actual_compen = ret_er_amt
    retrenchment = Exemptions.objects.get(sec="10(10B)", fy=master.fy)
    limit = retrenchment.ceil_pa - ret_ee_amt
    avg_sal = 120000
    exemp_retrenc = retrenchment.avg_hlfsal * avg_sal * year_of_service
    return (min(actual_compen, limit, exemp_retrenc))

def exemp_gra(id, gra_amount):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        print(e)
        return "Requested employee not there in our database"
    master = emp.empctcmaster_set.get()
    start_date = emp.doj
    end_date = datetime.now().date()
    difference = end_date - start_date
    year_of_service = round((difference.days + difference.seconds / 86400) / 365.2425)
    covered = Exemptions.objects.get(desc="Gratuity: Employee covered PGA,1972", fy=master.fy)
    notcovered = Exemptions.objects.get(desc="Gratuity: Employee not covered PGA,1972", fy=master.fy)
    actual_gratuity = master.salary_head['gratuity']
    LDS = 35000
    sal = master.salary_head[SalaryHeads.basicsalary.value]
    avg_sal = (sal * notcovered.avg_monsal) / notcovered.avg_monsal
    if year_of_service > 5:
        if "Gratuity: Employee covered PGA,1972" in gratuity_acts:
            gratuity = covered.avg_hlfsal * LDS * year_of_service
            limit = covered.ceil_pa - gra_amount
        else:
            gratuity = notcovered.avg_hlfsal * avg_sal * year_of_service
            limit = notcovered.ceil_pa - gra_amount
    else:
        gratuity = 0
        limit = 0
    return min(limit, actual_gratuity, gratuity)


def exemp_voluntary(id, vol_er_amt, vol_ee_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        print(e)
        return "Requested employee not there in our database"
    master = emp.empctcmaster_set.get()
    start_date = emp.doj
    end_date = datetime.now().date()
    difference = end_date - start_date
    year_of_service = round((difference.days + difference.seconds / 86400) / 365.2425)
    emp_dob = emp.dob
    diff = end_date - emp_dob
    age = round((diff.days + diff.seconds / 86400) / 365.2425)
    actual_compen = vol_er_amt
    voluntary = Exemptions.objects.get(sec="10(10C)")
    limit = voluntary.ceil_pa - vol_ee_amt
    LDS = 35000
    if year_of_service >= 10 or age >= 40:
        exe_vol_comp = LDS * voluntary.months * year_of_service
    exe_vol_comp = 0
    return min(exe_vol_comp, actual_compen, limit)

def exemp_leavesal_retirement(id, sal_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    master = emp.empctcmaster_set.all().order_by('-eff_date')[0]
    sal = master.salary_head[SalaryHeads.basicsalary.value]
    leavesal = Exemptions.objects.get(sec="10(10AA)")
    limit = leavesal.ceil_pa - sal_amt
    avg_sal = (sal * leavesal.avg_monsal) / leavesal.avg_monsal
    Lds = 35000
    no_of_unutilised_leaves = 25
    leave_sal_act_rec = Lds * leavesal.avg_hlfsal * no_of_unutilised_leaves
    a = 10 * avg_sal
    b = (avg_sal / 30) * no_of_unutilised_leaves
    return min(leave_sal_act_rec, limit, a, b)


def children_education(id, no_child, amt1, mno1, amt2, mno2):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        print(e)
        return "Requested employee not there in our database"
    education_allowance = Exemptions.objects.get(desc="Children education allowance")
    master = emp.empctcmaster_set.get()
    no_of_childrens = no_child
    amount = education_allowance.ceil_pm/2
    ch1_amt = amt1
    no_of_months1 = mno1
    ch2_amt = amt2
    no_of_months2 = mno2
    actual_amt = ch1_amt*no_of_months1 + ch2_amt*no_of_months2
    ch1_allo = min(amount*no_of_months1, ch1_amt*no_of_months1)
    ch2_allo = min(amount*no_of_months2, ch2_amt*no_of_months2)
    if no_of_childrens <= 2:
        edu_allo = min(actual_amt, (ch1_allo + ch2_allo))
    else:
        edu_allo = education_allowance.ceil_pm
    return edu_allo


def transport_allo(id,trans_amt, trans_months):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        print(e)
        return "Requested employee not there in our database"
    trans_allo = Exemptions.objects.get(desc="Transport allowance (Deaf,Dumb,Blind, or handicap)")
    master = emp.empctcmaster_set.get()
    actual_amt = trans_amt
    months = trans_months
    limit = trans_allo.ceil_pm
    return min(actual_amt*months, limit*months)


def hostel_allow(id, hno_child, hamt1, hmno1, hamt2, hmno2):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    hostel_allo = Exemptions.objects.get(desc="Hostel allowance")
    master = emp.empctcmaster_set.get()
    no_of_childrens = hno_child
    amount = hostel_allo.ceil_pm / 2
    ch1_amt = hamt1
    no_of_months1 = hmno1
    ch2_amt = hamt2
    no_of_months2 = hmno2
    actual_amt = ch1_amt * no_of_months1 + ch2_amt * no_of_months2
    ch1_allo = min(amount * no_of_months1, ch1_amt* no_of_months1)
    ch2_allo = min(amount * no_of_months2, ch2_amt* no_of_months2)
    if no_of_childrens <= 2:
        hstl_allo = min(actual_amt, (ch1_allo + ch2_allo))
    else:
        hstl_allo = hostel_allo.ceil_pm
    return hstl_allo

def exmp_com_pension_graapply(id, graapply_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    pension = Exemptions.objects.get(desc="Commuted pension: Gratuity applies")
    master = emp.empctcmaster_set.get()
    amount = graapply_amt
    exmpt = pension.commuted_pension * amount
    return exmpt


def exmp_com_pension_granotapply(id, granotapply_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    pension = Exemptions.objects.get(desc="Commuted pension: Gratuity does not applies")
    master = emp.empctcmaster_set.get()
    amount = granotapply_amt
    exmpt = pension.commuted_pension * amount
    return exmpt

def exmp_uniform(id, uniform_amt):
    amount = uniform_amt
    return amount

def exmp_research(id, research_amt):
    amount = research_amt
    return amount

def exmp_daily(id, daily_amt):
    amount = daily_amt
    return amount

def exmp_conveyance(id, conveyance_amt):
    amount = conveyance_amt
    return amount

def exmp_travel(id, travel_amt):
    amount = travel_amt
    return amount

def exmp_helper(id, helper_amt):
    amount = helper_amt
    return amount

    # Deductions

def atal_pension(id, atal_pension_amt801B):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    pension = Chp_VIA_Deductions.objects.get(sec="80CCD(1B)")
    limit = pension.ceili_pa
    actual_amt = atal_pension_amt801B
    return min(actual_amt, limit)

def emp_cont_nps(id, er_cont):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    sal = 35000
    employer_contribution = er_cont
    nps = Chp_VIA_Deductions.objects.get(sec="80CCD(2)")
    employee = sal * nps.sal_per
    return min(employer_contribution, employee)

def medical_treatment_maintainance(id,normal_actual_amt, severe_actual_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    medical_tratment = Chp_VIA_Deductions.objects.get(sec="80DD")
    normal_actual_amt = normal_actual_amt
    severe_actual_amt = severe_actual_amt
    normal_limit = medical_tratment.norm_disab
    severe_limit = medical_tratment.norm_disab
    if normal_actual_amt != 0:
        disab = min(normal_actual_amt, normal_limit)
    else:
        disab = min(severe_actual_amt, severe_limit)
    return disab

def interest_housing_loan(id, int_amt_80EE, loan_san_date, sdv, loan_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    house_loan = Chp_VIA_Deductions.objects.get(sec="80EE")
    loan_san_date = loan_san_date
    if house_loan.loan_sancfrm <= loan_san_date <= house_loan.loan_sancto:
        if sdv <= house_loan.sdv_property:
            if loan_amt <= house_loan.loan_amt:
                actual_amt = int_amt_80EE
    actual_amt = 0
    limit = house_loan.ceili_pa
    return min(actual_amt, limit)


def Interest_on_Electric_Vechile_loan(id, int_amt_ev, loan_san_dateEEB):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    Electric_Vechile_loan = Chp_VIA_Deductions.objects.get(sec="80EEB")
    if Electric_Vechile_loan.loan_sancfrm <= loan_san_dateEEB <= Electric_Vechile_loan.loan_sancto:
         actual_amt = int_amt_ev
    actual_amt = 0
    limit = Electric_Vechile_loan.ceili_pa
    return min(actual_amt, limit)


def Interest_on_saving_account(id, int_saving_amt_TTA):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    saving_account = Chp_VIA_Deductions.objects.get(sec="80TTA")
    actual_amt = int_saving_amt_TTA
    limit = saving_account.citizen
    return min(actual_amt, limit)


def Handcapped_Assess(id, hnormal_amt, hsevere_amt):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    normal_actual_amt = hnormal_amt
    severe_actual_amt = hsevere_amt
    handcaped = Chp_VIA_Deductions.objects.get(sec="80U")
    normal_limit = handcaped.norm_disab
    severe_limit = handcaped.severe_disab
    if hnormal_amt != 0:
        disab = min(normal_actual_amt, normal_limit)
    else:
        disab = min(severe_actual_amt, severe_limit)
    return disab


def Int_saving_sc(id, int_saving_amt_TTB):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    age = date.today().year - emp.dob.year
    saving_sc = Chp_VIA_Deductions.objects.get(sec="80TTB")
    limit = saving_sc.sr_citizen
    actual_amt = int_saving_amt_TTB
    if age >= 60:
        interest = min(limit, actual_amt)
    interest = 0
    return interest

def Int_on_house_loan_sanaction(id, int_hl80EEA, loan_san_dateEEA, sdvEEA):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    loan_sanaction = Chp_VIA_Deductions.objects.get(sec="80EEA")
    limit = loan_sanaction.ceili_pa
    if loan_sanaction.loan_sancfrm <= loan_san_dateEEA <= loan_sanaction.loan_sancto:
        if sdvEEA <= loan_sanaction.sdv_property:
            actual_amt = int_hl80EEA
    actual_amt = 0
    return min(limit, actual_amt)

def int_on_edu_loan(id, edu_loan_amt):
    amount = edu_loan_amt
    return amount

def donation_sci(id, don_sci_cash, don_sci_other):
    don_sci_cash = min(don_sci_cash, 2000)
    don_sci_other = don_sci_other
    actual = don_sci_cash+don_sci_other
    return actual

def don_pp(id, don_pp_cash, don_pp_other):
    don_pp_cash = 0
    don_pp_other = don_pp_other
    return don_pp_other

def specify_disease(id, sc_amt, nonsc_amt, insur_claim):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    specify_dis = Chp_VIA_Deductions.objects.get(sec="80DDB")
    if sc_amt != 0:
        dedu_amt = min(sc_amt, specify_dis.sr_citizen) - insur_claim
    else:
        dedu_amt = min(nonsc_amt, specify_dis.sr_citizen) - insur_claim
    if dedu_amt < 0:
        dedu_amt = 0
    return dedu_amt

def aggded_80CCE(id, lic, child_tution_fee, hl_repayment, ppf_amt, nsc_amt, int_nsc, mfelss,fd_bankorpo, nps_uti_mf, ssy,
                 eecont_spf_rpf, mf_uti, cont_ulip, scss, nabard,sd_hp, oth1, oth2, oth3,
                 contpension80CCC, eecont_apy80CCD1):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    aggded = Chp_VIA_Deductions.objects.get(sec="80CCE")
    actual = sum([lic, child_tution_fee, hl_repayment, ppf_amt, nsc_amt, int_nsc, mfelss,fd_bankorpo, nps_uti_mf, ssy,
                 eecont_spf_rpf, mf_uti, cont_ulip, scss, nabard,sd_hp, oth1, oth2, oth3,
                 contpension80CCC, eecont_apy80CCD1])
    return min(actual, aggded.ceili_pa)

def mediclaim(id, **mediamt):
    medi = Chp_VIA_Deductions.objects.get(sec="80D")
    if 'self_sc_HI' in mediamt and 'parent_sc_HI' in mediamt:
        a = min(5000, mediamt['self_sc_PHC'])
        self_amt = min(mediamt['self_sc_HI'] + a + mediamt['self_sc_ME'], medi.sr_citizen)
        b = min(mediamt['parent_sc_PHC'], 5000-a)
        bb = (b, 0)[b < 0]
        parent_amt = min(mediamt['parent_sc_HI'] + bb + mediamt['parent_sc_ME'], medi.sr_citizen)
        actual = self_amt + parent_amt
    pass
    if 'self_HI' in mediamt and 'parent_sc_HI' in mediamt:
        a = min(5000,mediamt['self_PHC'])
        self_amt = min(mediamt['self_HI'] + a, medi.citizen)
        b = min(mediamt['parent_sc_PHC'], 5000-a)
        bb = (b,0)[b < 0]
        parent_amt = min(mediamt['parent_sc_HI'] + bb + mediamt['parent_sc_ME'], medi.sr_citizen)
        actual = self_amt + parent_amt
    pass
    if 'self_HI' in mediamt and 'parent_HI' in mediamt:
        a = min(5000,mediamt['self_PHC'])
        self_amt = min(mediamt['self_HI'] + a, medi.citizen)
        b = min(mediamt['parent_PHC'], 5000-a)
        bb = (b, 0)[b < 0]
        parent_amt = min(mediamt['parent_HI'] + bb, medi.citizen)
        actual = self_amt + parent_amt
    return actual

# HP Deductions

def SOPint_hl_after(id, sopint_hl_amt_after):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    housing_loan = Chp_VIA_Deductions.objects.get(sec="24", desc='Int on housing loan after 01-04-1999')
    actual = min(housing_loan.ceili_pa, sopint_hl_amt_after)
    return actual

def LOP_std_ded(id, lop_rent_amt1, lop_month1, lop_rent_amt2, lop_month2, lop_mul_tax, lop_int_hl):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    lop_std = Chp_VIA_Deductions.objects.get(sec="24(b)")
    rent = lop_rent_amt1*lop_month1 + lop_rent_amt2*lop_month2
    NAV = rent - lop_mul_tax
    std_ded = NAV*lop_std.deduct_mx/100
    GHP = NAV - std_ded
    NHP = GHP - lop_int_hl
    return NHP

# Other Sources

def family_pension(id, family_pen_amt_pa):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    family_pen = Chp_VIA_Deductions.objects.get(sec="57")
    actual = min(family_pen.deduct_mx * family_pen_amt_pa / 100, family_pen.ceili_pa)
    return actual


def prev_emp_details(id, gross_sal, exempt_amt, PF, PT, TDS_ded):
    try:
        emp = Employee_Info.objects.get(id=id)
    except Exception as e:
        return "Requested employee not there in our database"
    prev_emp = Chp_VIA_Deductions.objects.get(desc="Previous Employement Details")
    # heads = prev_emp.prev_emp
    data = {'gross_sal':gross_sal,'exempt_amt':exempt_amt,'PF':PF, 'PT':PT,'TDS_ded':TDS_ded}
    return data



class ExmpTaxdeclaration(APIView):
    def get(self,request):
        emp_code = 6
        employee = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code)][0]
        particular = [i.particulars for i in CompanySalsetup.objects.filter(co_salsetups=employee.temp)]
        exmp = []
        for k in particular:
            exmp.append([i for i in Exemptions.objects.filter(ref_earn=k)])
        exemptions = list(filter(None, exmp))
        a = [i[0].desc for i in exemptions]
        return Response(a)
    def post(self, request):
        emp_code = 6
        employedata = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code)][0]
        particular = [i.particulars for i in CompanySalsetup.objects.filter(co_salsetups=employedata.temp)]
        exmp = []
        for k in particular:
            exmp.append([i for i in Exemptions.objects.filter(ref_earn=k)])
        exemptions = list(filter(None,exmp))
        emp_ctc = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code,temp=employedata.temp,fy=employedata.temp.fy)]
        if TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                               Template_name=employedata.temp.temp_name):
            result = [i.estimated_allowed for i in TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                               Template_name=employedata.temp.temp_name)][0]
            empest = [i.emp_estimated for i in TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                               Template_name=employedata.temp.temp_name)][0]
        else:
            result = {}
            empest = {}
        empest.update(request.data)
        for i in exemptions:
            for j in i:
                try:
                    if j.id == 1:
                        if request.data.get('hra_amount') or request.data.get('hra_amount1'):
                            if 'hra_amount' in request.data:
                                amt = request.data.get('hra_amount')
                            else:
                                total1 = request.data.get('hra_amount1')
                                total2 = request.data.get('hra_amount2')
                                amt = total1 + total2
                            result.update({j.desc:exemp_hra(emp_code, amt)})
                    pass
                    if j.id == 2:
                        if request.data.get('gra_amount') != None:
                            gra_amount = request.data.get('gra_amount')
                            result.update({j.desc: exemp_gra(emp_code, gra_amount)})
                    pass
                    if j.id == 3:
                        if request.data.get('gra_amount') != None:
                            gra_amount = request.data.get('gra_amount')
                            result.update({j.desc:exemp_gra(emp_code, gra_amount)})
                    pass
                    if j.id == 4:
                        if request.data.get('ret_er_amt') != None:
                            ret_er_amt = request.data.get('ret_er_amt')
                            ret_ee_amt = request.data.get('ret_ee_amt')
                            result.update({j.desc:exemp_retrenchment(emp_code, ret_er_amt, ret_ee_amt)})
                    pass
                    if j.id == 5:
                        if request.data.get('vol_er_amt') != None:
                            vol_er_amt = request.data.get('vol_er_amt')
                            vol_ee_amt = request.data.get('vol_ee_amt')
                            result.update({j.desc:exemp_voluntary(emp_code, vol_er_amt, vol_ee_amt)})
                    pass
                    if j.id == 6:
                        if request.data.get('sal_amt') != None:
                            sal_amt = request.data.get('sal_amt')
                            result.update({j.desc:exemp_leavesal_retirement(emp_code, sal_amt)})
                    pass
                    if j.id == 7:
                        if request.data.get('graapply_amt') != None:
                            graapply_amt = request.data.get('graapply_amt')
                            result.update({j.desc:exmp_com_pension_graapply(emp_code, graapply_amt)})
                    pass
                    if j.id == 8:
                        if request.data.get('granotapply_amt') != None:
                            granotapply_amt = request.data.get('granotapply_amt')
                            result.update({j.desc:exmp_com_pension_granotapply(emp_code, granotapply_amt)})
                    pass
                    if j.id == 9:
                        if request.data.get('no_child') != None:
                            no_child = request.data.get('no_child')
                            amt1 = request.data.get('amt1')
                            mno1 = request.data.get('mno1')
                            amt2 = request.data.get('amt2')
                            mno2 = request.data.get('mno2')
                            result.update({j.desc:children_education(emp_code, no_child, amt1, mno1, amt2, mno2)})
                    pass
                    if j.id == 10:
                        if request.data.get('hno_child') != None:
                            hno_child = request.data.get('hno_child')
                            hamt1 = request.data.get('hamt1')
                            hmno1 = request.data.get('hmno1')
                            hamt2 = request.data.get('hamt2')
                            hmno2 = request.data.get('hmno2')
                            result.update({j.desc:hostel_allow(emp_code, hno_child, hamt1, hmno1, hamt2, hmno2)})
                    pass
                    if j.id == 12:
                        if request.data.get('trans_amt') != None:
                            trans_amt = request.data.get('trans_amt')
                            trans_months = request.data.get('trans_months')
                            result.update({j.desc:transport_allo(emp_code, trans_amt, trans_months)})
                    pass
                    if j.id == 13:
                        if request.data.get('uniform_amt') != None:
                            uniform_amt = request.data.get('uniform_amt')
                            result.update({j.desc: exmp_uniform(emp_code, uniform_amt)})
                    pass
                    if j.id == 14:
                        if request.data.get('research_amt') != None:
                            research_amt = request.data.get('research_amt')
                            result.update({j.desc:exmp_research(emp_code, research_amt)})
                    pass
                    if j.id == 15:
                        if request.data.get('helper_amt') != None:
                            helper_amt = request.data.get('helper_amt')
                            result.update({j.desc:exmp_helper(emp_code, helper_amt)})
                    pass
                    if j.id == 16:
                        if request.data.get('travel_amt') != None:
                            travel_amt = request.data.get('travel_amt')
                            result.update({j.desc:exmp_travel(emp_code, travel_amt)})
                    pass
                    if j.id == 17:
                        if request.data.get('conveyance_amt') != None:
                            conveyance_amt = request.data.get('conveyance_amt')
                            result.update({j.desc:exmp_conveyance(emp_code, conveyance_amt)})
                    pass
                    if j.id == 18:
                        if request.data.get('daily_amt') != None:
                            daily_amt = request.data.get('daily_amt')
                            result.update({j.desc:exmp_daily(emp_code, daily_amt)})
                except:
                    pass
        obj, create = TaxDeclaration.objects.update_or_create(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                               Template_name=employedata.temp.temp_name,
                                                defaults={'estimated_allowed':result,'emp_estimated':empest})
        return Response(result)

class Ch6Taxdeclaration(APIView):
    def get(self,request):
        ch6_deductions = [i for i in Chp_VIA_Deductions.objects.all()]
        a = [i.desc for i in ch6_deductions]
        return Response(a)
    def post(self, request):
        emp_code = 6
        employedata = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code)][0]
        ch6_deductions = [i for i in Chp_VIA_Deductions.objects.all()]
        if TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                         Template_name=employedata.temp.temp_name):
            result = [i.estimated_allowed for i in
                      TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                                    Template_name=employedata.temp.temp_name)][0]
            empest = [i.emp_estimated for i in
                      TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                                    Template_name=employedata.temp.temp_name)][0]
        else:
            result = {}
            empest = {}
        empest.update(request.data)
        try:
            if request.data.get('atal_pension_amt801B') != None:
                atal_pension_amt801B = request.data.get('atal_pension_amt801B')
                result.update({ch6_deductions[9].desc:atal_pension(emp_code, atal_pension_amt801B)})
            pass
            if request.data.get('er_cont') != None:
                er_cont = request.data.get('er_cont')
                result.update({ch6_deductions[11].desc:emp_cont_nps(emp_code, er_cont)})
            pass
            if request.data.get('normal_actual_amt') != None:
                normal_actual_amt = request.data.get('normal_actual_amt')
                severe_actual_amt = request.data.get('severe_actual_amt')
                result.update({ch6_deductions[14].desc:medical_treatment_maintainance(emp_code, normal_actual_amt, severe_actual_amt)})
            pass
            if request.data.get('int_amt_80EE') != None:
                int_amt_80EE = request.data.get('int_amt_80EE')
                loan_san_date = request.data.get('loan_san_date')
                sdv = request.data.get('sdv')
                loan_amt = request.data.get('loan_amt')
                result.update({ch6_deductions[20].desc:interest_housing_loan(emp_code, int_amt_80EE, loan_san_date, sdv, loan_amt)})
            pass
            if request.data.get('int_amt_ev') != None:
                int_amt_ev = request.data.get('int_amt_ev')
                loan_san_dateEEB = request.data.get('loan_san_dateEEB')
                result.update({ch6_deductions[17].desc:Interest_on_Electric_Vechile_loan(emp_code, int_amt_ev, loan_san_dateEEB)})
            pass
            if request.data.get('int_saving_amt_TTA') != None:
                int_saving_amt_TTA = request.data.get('int_saving_amt_TTA')
                result.update({ch6_deductions[6].desc:Interest_on_saving_account(emp_code, int_saving_amt_TTA)})
            pass
            if request.data.get('hnormal_amt') != None:
                hnormal_amt = request.data.get('hnormal_amt')
                hsevere_amt = request.data.get('hsevere_amt')
                result.update({ch6_deductions[15].desc:Handcapped_Assess(emp_code, hnormal_amt, hsevere_amt)})
            pass
            if request.data.get('int_saving_amt_TTB') != None:
                int_saving_amt_TTB = request.data.get('int_saving_amt_TTB')
                result.update({ch6_deductions[7].desc:Int_saving_sc(emp_code, int_saving_amt_TTB)})
            pass
            if request.data.get('int_hl80EEA') != None:
                int_hl80EEA = request.data.get('int_hl80EEA')
                loan_san_dateEEA = request.data.get('loan_san_dateEEA')
                sdvEEA = request.data.get('sdvEEA')
                result.update({ch6_deductions[16].desc:Int_on_house_loan_sanaction(emp_code, int_hl80EEA, loan_san_dateEEA, sdvEEA)})
            pass
            if request.data.get('edu_loan_amt') != None:
                edu_loan_amt = request.data.get('edu_loan_amt')
                result.update({ch6_deductions[18].desc:int_on_edu_loan(emp_code, edu_loan_amt)})
            pass
            if request.data.get('don_sci_cash') != None:
                don_sci_cash = request.data.get('don_sci_cash')
                don_sci_other = request.data.get('don_sci_other')
                result.update({ch6_deductions[4].desc:donation_sci(emp_code, don_sci_cash, don_sci_other)})
            pass
            if request.data.get('don_pp_cash') != None:
                don_pp_cash = request.data.get('don_pp_cash')
                don_pp_other = request.data.get('don_pp_other')
                result.update({ch6_deductions[5].desc:don_pp(emp_code, don_pp_cash, don_pp_other)})
            pass
            if request.data.get('sc_amt') != None:
                sc_amt = request.data.get('sc_amt')
                nonsc_amt = request.data.get('nonsc_amt')
                insur_claim = request.data.get('insur_claim')
                result.update({ch6_deductions[19].desc:specify_disease(emp_code, sc_amt, nonsc_amt, insur_claim)})
            pass
            if request.data.get('lic') != None:
                lic = request.data.get('lic')
                child_tution_fee = request.data.get('child_tution_fee')
                hl_repayment = request.data.get('hl_repayment')
                ppf_amt = request.data.get('ppf_amt')
                nsc_amt = request.data.get('nsc_amt')
                int_nsc = request.data.get('int_nsc')
                mfelss = request.data.get('mfelss')
                fd_bankorpo = request.data.get('fd_bankorpo')
                nps_uti_mf = request.data.get('nps_uti_mf')
                ssy = request.data.get('ssy')
                eecont_spf_rpf = request.data.get('eecont_spf_rpf')
                mf_uti = request.data.get('mf_uti')
                cont_ulip = request.data.get('cont_ulip')
                scss = request.data.get('scss')
                nabard = request.data.get('nabard')
                sd_hp = request.data.get('sd_hp')
                oth1 = request.data.get('oth1')
                oth2 = request.data.get('oth2')
                oth3 = request.data.get('oth3')
                contpension80CCC = request.data.get('contpension80CCC')
                eecont_apy80CCD1 = request.data.get('eecont_apy80CCD1')
                result.update({ch6_deductions[8].desc:aggded_80CCE(emp_code, lic, child_tution_fee, hl_repayment, ppf_amt,
                         nsc_amt, int_nsc, mfelss, fd_bankorpo,nps_uti_mf, ssy,
                         eecont_spf_rpf, mf_uti, cont_ulip, scss, nabard, sd_hp, oth1, oth2, oth3,
                         contpension80CCC, eecont_apy80CCD1)})
            pass
            if request.data.get('gross_sal') != None:
                gross_sal = request.data.get('gross_sal')
                exempt_amt = request.data.get('exempt_amt')
                PF = request.data.get('PF')
                PT = request.data.get('PT')
                TDS_ded = request.data.get('TDS_ded')
                result.update({ch6_deductions[24].desc:prev_emp_details(emp_code, gross_sal, exempt_amt, PF, PT, TDS_ded)})
            pass
            if request.data.get('self_sc_HI') or request.data.get('self_HI'):
                self_sc_HI = request.data.get('self_sc_HI')
                self_sc_PHC = request.data.get('self_sc_PHC')
                self_sc_ME = request.data.get('self_sc_ME')
                self_HI = request.data.get('self_HI')
                self_PHC = request.data.get('self_PHC')
                parent_sc_HI = request.data.get('parent_sc_HI')
                parent_sc_PHC = request.data.get('parent_sc_PHC')
                parent_sc_ME = request.data.get('parent_sc_ME')
                parent_HI = request.data.get('parent_HI')
                paresnt_PHC = request.data.get('paresnt_PHC')
                if 'self_sc_HI' in request.data and 'parent_sc_HI' in request.data:
                    result.update({ch6_deductions[12].desc:mediclaim(emp_code, self_sc_HI=self_sc_HI,self_sc_PHC=self_sc_PHC,
                                                                   self_sc_ME=self_sc_ME, parent_sc_HI=parent_sc_HI,
                                                                   parent_sc_PHC=parent_sc_PHC,parent_sc_ME=parent_sc_ME)})
                if 'self_HI' in request.data and 'parent_sc_HI' in request.data:
                    result.update({ch6_deductions[12].desc: mediclaim(emp_code, self_HI=self_HI,self_PHC=self_PHC,
                                                                        parent_sc_HI=parent_sc_HI,
                                                                   parent_sc_PHC=parent_sc_PHC,parent_sc_ME=parent_sc_ME)})
                if 'self_HI' in request.data and 'parent_HI' in request.data:
                    result.update({ch6_deductions[12].desc: mediclaim(emp_code, self_HI=self_HI,self_PHC=self_PHC, parent_HI=parent_HI,
                                                                    paresnt_PHC=paresnt_PHC)})
            pass
            if request.data.get('sopint_hl_amt_after'):
                sopint_hl_amt_after = request.data.get('sopint_hl_amt_after')
                result.update({ch6_deductions[20].desc: SOPint_hl_after(emp_code, sopint_hl_amt_after)})
            pass
            if request.data.get('family_pen_amt_pa'):
                family_pen_amt_pa = request.data.get('family_pen_amt_pa')
                result.update({ch6_deductions[22].desc: family_pension(emp_code, family_pen_amt_pa)})
            pass
            if request.data.get('lop_rent_amt1'):
                lop_rent_amt1 = request.data.get('lop_rent_amt1')
                lop_month1 = request.data.get('lop_month1')
                lop_rent_amt2 = request.data.get('lop_rent_amt2')
                lop_month2 = request.data.get('lop_month2')
                lop_mul_tax = request.data.get('lop_mul_tax')
                lop_int_hl = request.data.get('lop_int_hl')
                result.update({'HP Income': LOP_std_ded(emp_code, lop_rent_amt1, lop_month1, lop_rent_amt2, lop_month2,
                                                                     lop_mul_tax, lop_int_hl)})
        except:
            pass
        obj, create = TaxDeclaration.objects.update_or_create(fy=employedata.temp.fy,
                                                                  emp_code=employedata.emp_code,
                                                                  Template_name=employedata.temp.temp_name,
                                                                  defaults={'estimated_allowed': result,
                                                                            'emp_estimated': empest})
        return Response(result)

class exmpt_ch6(APIView):
    def post(self, request):
        emp_code = 6
        employeedata = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code)][0]
        particular = [i.particulars for i in CompanySalsetup.objects.filter(co_salsetups=employeedata.temp)]
        exmp = []
        for k in particular:
            exmp.append([i for i in Exemptions.objects.filter(ref_earn=k)])
        exemptions = list(filter(None, exmp))
        ch6_deductions = [i for i in Chp_VIA_Deductions.objects.all()]
        result = {}
        for i in exemptions:
            for j in i:
                try:
                    if j.id == 1:
                        if request.data.get('total1') or request.data.get('total'):
                            if 'total' in request.data:
                                amt = request.data.get('total')
                            else:
                                total1 = request.data.get('total1')
                                total2 = request.data.get('total2')
                                amt = total1 + total2
                            result = {j.desc:exemp_hra(emp_code, amt)}
                    pass
                    if j.id == 2:
                        if request.data.get('gra_amount') != None:
                            gra_amount = request.data.get('gra_amount')
                            result = {j.desc: exemp_gra(emp_code, gra_amount)}
                    pass
                    if j.id == 3:
                        if request.data.get('gra_amount') != None:
                            gra_amount = request.data.get('gra_amount')
                            result = {j.desc:exemp_gra(emp_code, gra_amount)}
                    pass
                    if j.id == 4:
                        if request.data.get('ret_er_amt') != None:
                            ret_er_amt = request.data.get('ret_er_amt')
                            ret_ee_amt = request.data.get('ret_ee_amt')
                            result = {j.desc:exemp_retrenchment(emp_code, ret_er_amt, ret_ee_amt)}
                    pass
                    if j.id == 5:
                        if request.data.get('vol_er_amt') != None:
                            vol_er_amt = request.data.get('vol_er_amt')
                            vol_ee_amt = request.data.get('vol_ee_amt')
                            result = {j.desc:exemp_voluntary(emp_code, vol_er_amt, vol_ee_amt)}
                    pass
                    if j.id == 6:
                        if request.data.get('sal_amt') != None:
                            sal_amt = request.data.get('sal_amt')
                            result = {j.desc:exemp_leavesal_retirement(emp_code, sal_amt)}
                    pass
                    if j.id == 7:
                        if request.data.get('graapply_amt') != None:
                            graapply_amt = request.data.get('graapply_amt')
                            result = {j.desc:exmp_com_pension_graapply(emp_code, graapply_amt)}
                    pass
                    if j.id == 8:
                        if request.data.get('granotapply_amt') != None:
                            granotapply_amt = request.data.get('granotapply_amt')
                            result = {j.desc:exmp_com_pension_granotapply(emp_code, granotapply_amt)}
                    pass
                    if j.id == 9:
                        if request.data.get('no_child') != None:
                            no_child = request.data.get('no_child')
                            amt1 = request.data.get('amt1')
                            mno1 = request.data.get('mno1')
                            amt2 = request.data.get('amt2')
                            mno2 = request.data.get('mno2')
                            result = {j.desc:children_education(emp_code, no_child, amt1, mno1, amt2, mno2)}
                    pass
                    if j.id == 10:
                        if request.data.get('hno_child') != None:
                            hno_child = request.data.get('hno_child')
                            hamt1 = request.data.get('hamt1')
                            hmno1 = request.data.get('hmno1')
                            hamt2 = request.data.get('hamt2')
                            hmno2 = request.data.get('hmno2')
                            result = {j.desc:hostel_allow(emp_code, hno_child, hamt1, hmno1, hamt2, hmno2)}
                    pass
                    if j.id == 12:
                        if request.data.get('trans_amt') != None:
                            trans_amt = request.data.get('trans_amt')
                            trans_months = request.data.get('trans_months')
                            result = {j.desc:transport_allo(emp_code, trans_amt, trans_months)}
                    pass
                    if j.id == 13:
                        if request.data.get('uniform_amt') != None:
                            uniform_amt = request.data.get('uniform_amt')
                            result = {j.desc: exmp_uniform(emp_code, uniform_amt)}
                    pass
                    if j.id == 14:
                        if request.data.get('research_amt') != None:
                            research_amt = request.data.get('research_amt')
                            result = {j.desc:exmp_research(emp_code, research_amt)}
                    pass
                    if j.id == 15:
                        if request.data.get('helper_amt') != None:
                            helper_amt = request.data.get('helper_amt')
                            result = {j.desc:exmp_helper(emp_code, helper_amt)}
                    pass
                    if j.id == 16:
                        if request.data.get('travel_amt') != None:
                            travel_amt = request.data.get('travel_amt')
                            result = {j.desc:exmp_travel(emp_code, travel_amt)}
                    pass
                    if j.id == 17:
                        if request.data.get('conveyance_amt') != None:
                            conveyance_amt = request.data.get('conveyance_amt')
                            result = {j.desc:exmp_conveyance(emp_code, conveyance_amt)}
                    pass
                    if j.id == 18:
                        if request.data.get('daily_amt') != None:
                            daily_amt = request.data.get('daily_amt')
                            result = {j.desc:exmp_daily(emp_code, daily_amt)}
                except:
                    pass
        try:
            if request.data.get('atal_pension_amt801B') != None:
                atal_pension_amt801B = request.data.get('atal_pension_amt801B')
                result = {ch6_deductions[9].desc:atal_pension(emp_code, atal_pension_amt801B)}
            pass
            if request.data.get('er_cont') != None:
                er_cont = request.data.get('er_cont')
                result = {ch6_deductions[11].desc:emp_cont_nps(emp_code, er_cont)}
            pass
            if request.data.get('normal_actual_amt') != None:
                normal_actual_amt = request.data.get('normal_actual_amt')
                severe_actual_amt = request.data.get('severe_actual_amt')
                result = {ch6_deductions[14].desc:medical_treatment_maintainance(emp_code, normal_actual_amt, severe_actual_amt)}
            pass
            if request.data.get('int_amt_80EE') != None:
                int_amt_80EE = request.data.get('int_amt_80EE')
                loan_san_date = request.data.get('loan_san_date')
                sdv = request.data.get('sdv')
                loan_amt = request.data.get('loan_amt')
                result = {ch6_deductions[20].desc:interest_housing_loan(emp_code, int_amt_80EE, loan_san_date, sdv, loan_amt)}
            pass
            if request.data.get('int_amt_ev') != None:
                int_amt_ev = request.data.get('int_amt_ev')
                loan_san_dateEEB = request.data.get('loan_san_dateEEB')
                result = {ch6_deductions[17].desc:Interest_on_Electric_Vechile_loan(emp_code, int_amt_ev, loan_san_dateEEB)}
            pass
            if request.data.get('int_saving_amt_TTA') != None:
                int_saving_amt_TTA = request.data.get('int_saving_amt_TTA')
                result = {ch6_deductions[6].desc:Interest_on_saving_account(emp_code, int_saving_amt_TTA)}
            pass
            if request.data.get('hnormal_amt') != None:
                hnormal_amt = request.data.get('hnormal_amt')
                hsevere_amt = request.data.get('hsevere_amt')
                result = {ch6_deductions[15].desc:Handcapped_Assess(emp_code, hnormal_amt, hsevere_amt)}
            pass
            if request.data.get('int_saving_amt_TTB') != None:
                int_saving_amt_TTB = request.data.get('int_saving_amt_TTB')
                result = {ch6_deductions[7].desc:Int_saving_sc(emp_code, int_saving_amt_TTB)}
            pass
            if request.data.get('int_hl80EEA') != None:
                int_hl80EEA = request.data.get('int_hl80EEA')
                loan_san_dateEEA = request.data.get('loan_san_dateEEA')
                sdvEEA = request.data.get('sdvEEA')
                result = {ch6_deductions[16].desc:Int_on_house_loan_sanaction(emp_code, int_hl80EEA, loan_san_dateEEA, sdvEEA)}
            pass
            if request.data.get('edu_loan_amt') != None:
                edu_loan_amt = request.data.get('edu_loan_amt')
                result = {ch6_deductions[18].desc:int_on_edu_loan(emp_code, edu_loan_amt)}
            pass
            if request.data.get('don_sci_cash') != None:
                don_sci_cash = request.data.get('don_sci_cash')
                don_sci_other = request.data.get('don_sci_other')
                result = {ch6_deductions[4].desc:donation_sci(emp_code, don_sci_cash, don_sci_other)}
            pass
            if request.data.get('don_pp_cash') != None:
                don_pp_cash = request.data.get('don_pp_cash')
                don_pp_other = request.data.get('don_pp_other')
                result = {ch6_deductions[5].desc:don_pp(emp_code, don_pp_cash, don_pp_other)}
            pass
            if request.data.get('sc_amt') != None:
                sc_amt = request.data.get('sc_amt')
                nonsc_amt = request.data.get('nonsc_amt')
                insur_claim = request.data.get('insur_claim')
                result = {ch6_deductions[19].desc:specify_disease(emp_code, sc_amt, nonsc_amt, insur_claim)}
            pass
            if request.data.get('lic') != None:
                lic = request.data.get('lic')
                child_tution_fee = request.data.get('child_tution_fee')
                hl_repayment = request.data.get('hl_repayment')
                ppf_amt = request.data.get('ppf_amt')
                nsc_amt = request.data.get('nsc_amt')
                int_nsc = request.data.get('int_nsc')
                mfelss = request.data.get('mfelss')
                fd_bankorpo = request.data.get('fd_bankorpo')
                nps_uti_mf = request.data.get('nps_uti_mf')
                ssy = request.data.get('ssy')
                eecont_spf_rpf = request.data.get('eecont_spf_rpf')
                mf_uti = request.data.get('mf_uti')
                cont_ulip = request.data.get('cont_ulip')
                scss = request.data.get('scss')
                nabard = request.data.get('nabard')
                sd_hp = request.data.get('sd_hp')
                oth1 = request.data.get('oth1')
                oth2 = request.data.get('oth2')
                oth3 = request.data.get('oth3')
                contpension80CCC = request.data.get('contpension80CCC')
                eecont_apy80CCD1 = request.data.get('eecont_apy80CCD1')
                result = {ch6_deductions[8].desc:aggded_80CCE(emp_code, lic, child_tution_fee, hl_repayment, ppf_amt,
                         nsc_amt, int_nsc, mfelss, fd_bankorpo,nps_uti_mf, ssy,
                         eecont_spf_rpf, mf_uti, cont_ulip, scss, nabard, sd_hp, oth1, oth2, oth3,
                         contpension80CCC, eecont_apy80CCD1)}
            pass
            if request.data.get('gross_sal') != None:
                gross_sal = request.data.get('gross_sal')
                exempt_amt = request.data.get('exempt_amt')
                PF = request.data.get('PF')
                PT = request.data.get('PT')
                TDS_ded = request.data.get('TDS_ded')
                result = {ch6_deductions[24].desc:prev_emp_details(emp_code, gross_sal, exempt_amt, PF, PT, TDS_ded)}
            pass
            if request.data.get('self_sc_HI') or request.data.get('self_HI'):
                self_sc_HI = request.data.get('self_sc_HI')
                self_sc_PHC = request.data.get('self_sc_PHC')
                self_sc_ME = request.data.get('self_sc_ME')
                self_HI = request.data.get('self_HI')
                self_PHC = request.data.get('self_PHC')
                parent_sc_HI = request.data.get('parent_sc_HI')
                parent_sc_PHC = request.data.get('parent_sc_PHC')
                parent_sc_ME = request.data.get('parent_sc_ME')
                parent_HI = request.data.get('parent_HI')
                paresnt_PHC = request.data.get('paresnt_PHC')
                if 'self_sc_HI' in request.data and 'parent_sc_HI' in request.data:
                    result = {ch6_deductions[12].desc:mediclaim(emp_code, self_sc_HI=self_sc_HI,self_sc_PHC=self_sc_PHC,
                                                                   self_sc_ME=self_sc_ME, parent_sc_HI=parent_sc_HI,
                                                                   parent_sc_PHC=parent_sc_PHC,parent_sc_ME=parent_sc_ME)}
                if 'self_HI' in request.data and 'parent_sc_HI' in request.data:
                    result = {ch6_deductions[12].desc: mediclaim(emp_code, self_HI=self_HI,self_PHC=self_PHC,
                                                                        parent_sc_HI=parent_sc_HI,
                                                                   parent_sc_PHC=parent_sc_PHC,parent_sc_ME=parent_sc_ME)}
                if 'self_HI' in request.data and 'parent_HI' in request.data:
                    result = {ch6_deductions[12].desc: mediclaim(emp_code, self_HI=self_HI,self_PHC=self_PHC, parent_HI=parent_HI,
                                                                    paresnt_PHC=paresnt_PHC)}
            pass
            if request.data.get('sopint_hl_amt_after'):
                sopint_hl_amt_after = request.data.get('sopint_hl_amt_after')
                result = {ch6_deductions[20].desc: SOPint_hl_after(emp_code, sopint_hl_amt_after)}
            pass
            if request.data.get('family_pen_amt_pa'):
                family_pen_amt_pa = request.data.get('family_pen_amt_pa')
                result = {ch6_deductions[22].desc: family_pension(emp_code, family_pen_amt_pa)}
            pass
            if request.data.get('lop_rent_amt1'):
                lop_rent_amt1 = request.data.get('lop_rent_amt1')
                lop_month1 = request.data.get('lop_month1')
                lop_rent_amt2 = request.data.get('lop_rent_amt2')
                lop_month2 = request.data.get('lop_month2')
                lop_mul_tax = request.data.get('lop_mul_tax')
                lop_int_hl = request.data.get('lop_int_hl')
                result = {'HP Income': LOP_std_ded(emp_code, lop_rent_amt1, lop_month1, lop_rent_amt2, lop_month2,
                                                                     lop_mul_tax, lop_int_hl)}
        except:
            pass
        return Response(result)

class ExmptCh6TaxDecl(APIView):
    def post(self, request):
        emp_code = 6
        employedata = [i for i in EmpCtcMaster.objects.filter(emp_code=emp_code)][0]
        if TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                         Template_name=employedata.temp.temp_name):
            estimated_allowed = [i.estimated_allowed for i in
                      TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                                    Template_name=employedata.temp.temp_name)][0]
            estimated_allowed.update(request.data.get('estimated_allowed'))
            emp_estimated = [i.emp_estimated for i in
                      TaxDeclaration.objects.filter(fy=employedata.temp.fy, emp_code=employedata.emp_code,
                                                    Template_name=employedata.temp.temp_name)][0]
            emp_estimated.update(request.data.get('emp_estimated'))
        else:
            emp_estimated = request.data.get('emp_estimated')
            estimated_allowed = request.data.get('estimated_allowed')
        obj, create = TaxDeclaration.objects.update_or_create(fy=employedata.temp.fy,
                                                              emp_code=employedata.emp_code,
                                                              Template_name=employedata.temp.temp_name,
                                                              defaults={'estimated_allowed': estimated_allowed,
                                                                        'emp_estimated': emp_estimated})
        return Response('Submitted Sucessfully')