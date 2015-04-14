def evaluate_poly(poly, x):
#evaluate a polynomial
    total = 0
    for expn, coef in enumerate(poly):
        total += coef * (x**expn)
    return float(total)
    
print evaluate_poly((0.0, 0.0, 5.0, 9.3, 7.0), -13)         
