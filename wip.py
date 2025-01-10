import numpy as np

import mortgage as mt

mortgage = mt.Mortgage(200000, 200000 * 0.1, 0.0405, 25)

res = mt.saving(mortgage, 200, 0.035, house_price_growth=0.1)

from math import floor

print(res)

# test price growth functionality
print(mortgage.project_sale_price(0.03, 25))

import numpy as np
test_range = np.arange(0.0, 0.11, 0.01)

#for t in test_range:
#    res = mortgage.project_sale_price(t, years_held=25)
#    print(res)

for t in test_range:
    res = saving(mortgage, 400, 0.02, house_price_growth=t)
    print(res)