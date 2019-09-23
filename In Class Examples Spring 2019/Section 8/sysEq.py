import scipy.optimize as opt

def f(variables):

    (x, y) = variables

    first_eq = x + 2 * y + 4 
    second_eq = 2 * x + y + 3
    
    return  [first_eq, second_eq]

# use scipy.optimize.fsolve to solve n-equations with n-unknowns
(x, y) = opt.fsolve(f, (.01, .01))
print(x,y)

