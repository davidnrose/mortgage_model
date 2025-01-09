

repay = 1216.57
rate = 0.0402 / 12
term = 25 * 12
d = 0.34


R = (rate + 1) ** term
q = (rate * R) / (R - 1)

res = repay / q



print(res)