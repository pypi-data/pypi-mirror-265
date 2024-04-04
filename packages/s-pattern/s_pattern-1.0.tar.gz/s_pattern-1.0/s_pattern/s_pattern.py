def find_pattern(z,q,y,p,n):
    x = q-z
    w = y-q
    m = p-y
    k = w-x
    h = m-w
    v = h-k
    a = v/6
    b = (k-12*a)/2
    c = x-7*a-3*b
    d = z-a-b-c
    n = a*n**3+b*n**2+c*n+d
    n_om = ("" if a == 0 else ("n^3" if a == 1 else f"{a}n^3"))+("" if a == 0 or b == 0 else " + ")+("" if b == 0 else ("n^2" if b == 1 else f"{b}n^2"))+("" if a == b == 0 or c == 0 else " + ")+("" if c == 0 else ("n" if c == 1 else f"{c}n"))+("" if a == b == c == 0 or d == 0 else " + ")+("" if d == 0 else ("1" if d == 1 else f"{d}"))
    return f'''n = {n}
n_om = {n_om}'''