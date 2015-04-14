def compute_deriv(poly):
#find a derivative
    deriv = []
    for expn, coef in enumerate(poly):
        if expn == 0:
            continue
        deriv.append(float(coef * expn))
    return tuple(deriv)
    
print compute_deriv((-13.39, 0.0, 17.5, 3.0, 1.0))
