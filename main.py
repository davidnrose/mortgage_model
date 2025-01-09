
# import mortgage scripts
import mortgage as mt

mortgage = mt.Mortgage(350000, 120000, 0.0402, 25)
print(mortgage.repayment)

print(mt.calc_prop_value(1216.57, 0.343, 0.0402, 25))

print(mt.project_growth(200000, 0.02, 10))

# test mortgage
mortgage = mt.Mortgage(250000, 250000*0.1, 0.045, 25)
print(mt.saving(mortgage, 300, 0.035))