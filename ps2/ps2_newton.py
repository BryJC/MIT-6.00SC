tries = 1
#setup global variable to count recursion loops

def compute_root(poly, x_0, epsilon):
#use Newton's method to find roots of a polynomial
    attempt = evaluate_poly(poly, x_0)
    global tries
    if abs(attempt) <= epsilon:
        return (x_0, tries)
    else:
        tries += 1
        x_1 = x_0 - (attempt / evaluate_poly(compute_deriv(poly), x_0))
        return compute_root(poly, x_1, epsilon)   

def evaluate_poly(poly, x):
#evaluate a polynomial
    total = 0
    for expn, coef in enumerate(poly):
        total += coef * (x**expn)
    return float(total)
    
def compute_deriv(poly):
#find a derivative
    deriv = []
    for expn, coef in enumerate(poly):
        if expn == 0:
            continue
        deriv.append(float(coef * expn))
    return tuple(deriv)

print compute_root((-13.39, 0.0, 17.5, 3.0, 1.0), 0.1, 0.0001)
