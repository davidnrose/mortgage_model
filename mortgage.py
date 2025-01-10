class Mortgage:
    def __init__(self, P, d, r, n):
        self.principal = P  # total mortgage amount
        self.deposit = d  # deposit
        self.rate = r  # interest rate
        self.term = n  # number of years of the term

        # ---------------------------------------------
        # calculate monthly repayments for repayment mortgage plan
        # get monthly interest
        r = self.rate / 12

        # get length of term in months
        n = self.term * 12

        # get the loaned amount by subtracting deposit from the total borrowed money
        P = self.principal - self.deposit

        # calculate monthly repayment with annualised formulae
        R = (r + 1) ** n
        q = (r * R) / (R - 1)

        mrepay = round(P * q, 2)

        # assign to attribute
        self.repayment = mrepay

        # ---------------------------------------------
        # calculate monthly repayments for repayment mortgage plan
        total_interest = P * self.rate
        self.interest_only = round(total_interest / 12, 2)

        # ---------------------------------------------
        # calculate stamp duty land tax as attibute
        prop_value = self.principal
        if prop_value >= 1500000:
            tax_1 = (prop_value - 1500000) * 0.15
            tax_2 = 575000 * 0.13
            tax_3 = 675000 * 0.08
            tax_4 = 250000 * 0.03
        elif prop_value > 925001 and prop_value < 1500000:
            tax_1 = 0
            tax_2 = (prop_value - 925000) * 0.13
            tax_3 = 675000 * 0.08
            tax_4 = 250000 * 0.03
        elif prop_value > 250000 and prop_value < 925000:
            tax_1 = 0
            tax_2 = 0
            tax_3 = (prop_value - 250000) * 0.08
            tax_4 = 250000 * 0.3
        elif prop_value < 250000 and prop_value > 40000:
            tax_1 = 0
            tax_2 = 0
            tax_3 = 0
            tax_4 = prop_value * 0.3
        else:
            tax_1 = 0
            tax_2 = 0
            tax_3 = 0
            tax_4 = 0

        self.sdlt_btl = round(tax_1 + tax_2 + tax_3, 2)

        # ---------------------------------------------
        # calculate sdlt for residential property
        if prop_value >= 1500000:
            tax_1 = (prop_value - 1500000) * 0.12
            tax_2 = 575000 * 0.1
            tax_3 = 675000 * 0.05
        elif prop_value > 925001 and prop_value < 1500000:
            tax_1 = 0
            tax_2 = (prop_value - 925000) * 0.1
            tax_3 = 675000 * 0.05
        elif prop_value > 250000 and prop_value < 925000:
            tax_1 = 0
            tax_2 = 0
            tax_3 = (prop_value - 250000) * 0.05
        else:
            tax_1 = 0
            tax_2 = 0
            tax_3 = 0

        self.sdlt = round(tax_1 + tax_2 + tax_3, 2)

    # print all the info associated with the mortgage
    def info(self):
        print(f"Principal: {self.principal}")
        print(f"Deposit: {self.deposit}")
        print(f"Repayment: {self.repayment}")
        print(f"Interest only repayment: {self.interest_only}")
        print(f"Term (years): {self.term}")
        print(f"SDLT: {self.sdlt}")
        print(f"SDLT BTL: {self.sdlt_btl}")

    def calc_interest_paid(self, months):
        total_int_paid = 0
        capital = self.principal - self.deposit
        repayment = self.repayment
        for i in range(months):
            int_paid = (capital * self.rate) / 12
            cap_paid = self.repayment - int_paid
            capital -= cap_paid

            total_int_paid += int_paid

        return round(total_int_paid, 2)

    def calc_capital_paid(self, months):
        total_cap_paid = 0
        capital_remaining = self.principal - self.deposit
        repayment = self.repayment
        for i in range(months):
            int_paid = (capital_remaining * self.rate) / 12
            cap_paid = self.repayment - int_paid
            capital_remaining -= cap_paid

            total_cap_paid += cap_paid

        return round(total_cap_paid, 2)

    def rental_profit(self, months, rent, tax_rate=0.4, management=0.07):  # assume estate agent management fee of 7%
        total_income = months * rent
        total_repayments = mortgage.interest_only * months
        management_fee = total_income * management

        # get total interest paid in the period
        total_int = self.calc_interest(months)

        tax_credit = total_int * 0.2

        # get tax
        tax = (total_income - tax_credit - management_fee - (1000 * (months / 12))) * tax_rate  # assume running costs

        # get net profit after tax
        profit = total_income - total_repayments - tax - management_fee - self.sdlt_btl  # take off the SDLT as this is a cost at the start

        return round(profit, 2)

    def rental_profit_margin(self, months, rent, tax_rate=0.4):
        profit = self.rental_profit(months, rent, tax_rate)

        total_cost = (self.repayment * months) + (1000 * (months / 12))

        return round(profit / total_cost, 3)

    def estimate_rent(self):
        return round(self.principal * 0.007, 2)

    def calc_yield(self, rent):
        return (rent * 12) / self.principal

    def project_sale_price(self, annual_growth=0.015, years_held=15):
        return round(self.principal * (1 + annual_growth) ** years_held, 2)

    def estimate_cgt(self, sale_price, tax_rate="higher", sale_costs=7000):
        taxable = sale_price - self.principal - sale_costs - 3000  # capital gains allowance

        if tax_rate == "higher":
            cgt_rate = 0.24
        elif tax_rate == "basic":
            cgt_rate = 0.18

        return round(taxable * cgt_rate, 2)


def calc_prop_value(repay, d, r, n):
    rate = r / 12
    term = n * 12

    R = (rate + 1) ** term
    q = (rate * R) / (R - 1)

    P = repay / q

    P = P / (1 - d)

    return P

# project increase in asset value for x years with assumed annual percentage growth
def project_growth(value, ann_growth, years):
    res = round(value * (1 + ann_growth) ** years, 2)
    return res

# calculate time to save for a mortgage under conditions specified
def saving(mortgage, month_saving, savings_rate, house_price_growth=0.02, months=1, saved=0, deposit=0, deposit_perc=0.1):
    deposit_amount = list()
    annual_growth = house_price_growth
    if saved > deposit:
        return deposit

    else:
        saved += month_saving
        interest = saved * (savings_rate / 12)
        saved += interest

        house_value = mortgage.project_sale_price(annual_growth=annual_growth, years_held=months/12)
        deposit = house_value * deposit_perc
        print(deposit)
        deposit_amount.append(deposit)

        months += 1
        return saving(mortgage, month_saving=month_saving, savings_rate=savings_rate, months=months, saved=saved, deposit=deposit)