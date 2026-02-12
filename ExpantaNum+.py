import math
#--Edtiable things--
decimals = 16 # How many decimals (duh). Max 16
max_suffix = 63 # At how much 10^x it goes from being suffix to scientific. Example: 1e1,000 -> e1K
FirstOnes = ["", "U", "D", "T", "Qd", "Qn", "Sx", "Sp", "Oc", "No"]
SecondOnes = ["", "De", "Vt", "Tg", "qg", "Qg", "sg", "Sg", "Og", "Ng"]
ThirdOnes = ["", "Ce", "Du", "Tr", "Qa", "Qi", "Se", "Si", "Ot", "Ni"]
MultOnes = [
    "", "Mi", "Mc", "Na", "Pi", "Fm", "At", "Zp", "Yc", "Xo", "Ve", "Me", "Due", 
    "Tre", "Te", "Pt", "He", "Hp", "Oct", "En", "Ic", "Mei", "Dui", "Tri", "Teti", 
    "Pti", "Hei", "Hp", "Oci", "Eni", "Tra", "TeC", "MTc", "DTc", "TrTc", "TeTc", 
    "PeTc", "HTc", "HpT", "OcT", "EnT", "TetC", "MTetc", "DTetc", "TrTetc", "TeTetc", 
    "PeTetc", "HTetc", "HpTetc", "OcTetc", "EnTetc", "PcT", "MPcT", "DPcT", "TPCt", 
    "TePCt", "PePCt", "HePCt", "HpPct", "OcPct", "EnPct", "HCt", "MHcT", "DHcT", 
    "THCt", "TeHCt", "PeHCt", "HeHCt", "HpHct", "OcHct", "EnHct", "HpCt", "MHpcT", 
    "DHpcT", "THpCt", "TeHpCt", "PeHpCt", "HeHpCt", "HpHpct", "OcHpct", "EnHpct", 
    "OCt", "MOcT", "DOcT", "TOCt", "TeOCt", "PeOCt", "HeOCt", "HpOct", "OcOct", 
    "EnOct", "Ent", "MEnT", "DEnT", "TEnt", "TeEnt", "PeEnt", "HeEnt", "HpEnt", 
    "OcEnt", "EnEnt", "Hect", "MeHect"
]
#--End of editable things--
MAX_SAFE_INT = 2**53 - 1
MAX_LOGP1_REPEATS = 48
LOG5E = 0.6213349345596118
_log10 = math.log10
precise_arrow = False # Would not recommend turning this to True
arrow_precision = 44 # Would nto recommend changing this
grahams_number = [[0, 3638334640023.7783, 7625597484984, 0, 1], 0, 63, 0] # This variable is unused and is only here just to show how much the grahams number is
def correct(x):
    if isinstance(x, (int, float)): return correct([0 if x >= 0 else 1, abs(x)])

    if isinstance(x, str):
        try: return correct(float(x))
        except: pass
        s = x.strip()
        s = s.replace("1e", "e")
        if s.startswith("E") or s.startswith("-E"): return from_hyper_e(s)
        if any(c in "}^)e" for c in s): return fromstring(s)
        raise NotImplementedError("Can't convert the string you input")
        return fromformat(s)

    if isinstance(x, list):
        try: x[0][0]
        except: x = [x] + [0, 0, 0]
        if len(x) == 3: x.append(0)
        arr = x[0]
        arr = arr[:]
        if not arr: return [[0, 0], 0, 0, 0]
        if len(arr) == 1: return [0 if arr[0] >= 0 else 1, abs(arr[0])]
        if arr[0] not in (0, 1): raise ValueError(f"First element must be 0 (positive) or 1 (negative) (array:{arr})")

        for i in range(1, len(arr)):
            if isinstance(arr[i], str):
                try: arr[i] = float(arr[i])
                except ValueError: raise ValueError(f"Element at index {i} must be a number (array:{arr})")
            elif not isinstance(arr[i], (int, float)): raise ValueError(f"Element at index {i} must be a number (array:{arr})")
            if arr[i] < 0: raise ValueError(f"Element at index {i} must be positive (array:{arr})")
        while len(arr) > 4 and arr[-1] == 0: arr.pop(-1)
        
        changed = True
        while changed:
            changed = False
            for i in range(len(arr)-1, 0, -1):
                if arr[i] > MAX_SAFE_INT:
                    L = _log10(arr[i])
                    if i == 1:
                        arr[1] = L
                        if len(arr) > 2: arr[2] += 1
                        else: arr.append(1)
                    else:
                        arr[1] = L
                        for j in range(2, i): arr[j] = 1
                        if i == 2: arr[2] = 1
                        else: arr[i] = 0
                        if i == len(arr) - 1: arr.append(1)
                        else: arr[i+1] += 1
                    changed = True
                    break

        for i in range(1, len(arr)):
            if isinstance(arr[i], float) and arr[i] <= MAX_SAFE_INT and arr[i].is_integer(): arr[i] = int(arr[i])

        while len(arr) >= 3 and arr[2] >= 1 and arr[1] <= _log10(MAX_SAFE_INT):
            collapsed_val = 10 ** arr[1]
            if arr[2] == 1:
                if len(arr) == 3: arr = [arr[0], collapsed_val]
                else: arr = [arr[0], collapsed_val, 0] + arr[3:]
            else: arr = [arr[0], collapsed_val, arr[2]-1] + arr[3:]

        if len(arr) > 3 and arr[2] == 0:
            z = 0
            i = 2
            while i < len(arr) and arr[i] == 0:
                z += 1
                i += 1
            if i == len(arr): arr.append(1)
            if arr[i] == 0: arr[i] = 0
            else: arr[i] -= 1
            num_eight = 1 if z == 2 else z
            a1 = arr[1]
            if isinstance(a1, float) and a1.is_integer(): a1 = a1
            mid = [8] * num_eight
            arr = arr[:2] + mid + arr[i:]
        if x[1] > MAX_SAFE_INT:
            arr = [0, _log10(x[1]), 1]
            x[1] = 0
            x[2] += 1
        if x[2] != 0 and len(arr) == 2: raise ValueError("If layer is more than 0 and array is less than 2^53-1 its undefined")
        return [arr] + x[1:]
    raise TypeError("Unsupported type for correct")
def polarize(array, smallTop=False):
    pairs = correct(array)[0][1:]
    bottom = pairs[0]
    top = 0
    height = 0
    if len(pairs) <= 1:
        if smallTop:
            while bottom >= 10:
                bottom = _log10(bottom)
                top += 1
                height = 1
    else:
        elem = 1
        top = pairs[1]
        height = 1
        while (bottom >= 10) or (elem < len(pairs)) or (smallTop and top >= 10):
            if bottom >= 10:
                if height == 1:
                    bottom = _log10(bottom)
                    if bottom >= 10:
                        bottom = _log10(bottom)
                        top += 1
                elif height < MAX_LOGP1_REPEATS:
                    if bottom >= 1e10: bottom = _log10(_log10(_log10(bottom))) + 2
                    else: bottom = _log10(_log10(bottom)) + 1
                    for _i in range(2, height):
                        bottom = _log10(bottom) + 1
                else: bottom = 1
                top += 1
            else:
                if elem == len(pairs) - 1 and elem == height and not (smallTop and top >= 10): break
                bottom = _log10(bottom) + top
                height += 1
                if elem < len(pairs) and height > elem: elem += 1
                if elem < len(pairs):
                    if height == elem: top = pairs[elem] + 1
                    elif bottom < 10:
                        diff = elem - height
                        if diff < MAX_LOGP1_REPEATS:
                            for _ in range(diff):
                                bottom = _log10(bottom) + 1
                        else: bottom = 1
                        top = pairs[elem] + 1
                    else: top = 1
                else: top = 1
    return {"bottom": bottom, "top": top, "height": height}
def set_to_zero(x, y):
    x[y] = 0
    return x
def array_search(x, y):
    if len(x) <= y: return 0
    return x[y]
def comma_format(num, precision=0):
    a = correct(num)[0]
    if len(a) == 2:
        val = a[1]
        if precision == 0: return f"{int(round(val)):,}"
        else: return f"{val:,.{precision}f}"
    return str(a)

def regular_format(num, precision):
    a = correct(num)[0]
    if len(a) == 2:
        val = a[1]
        if precision == 0: return f"{int(val):,}"
        else: return f"{val:.{precision}f}"
    return str(a)

def compare(a, b):
    A = correct(a)
    B = correct(b)
    lenA = len(A)
    lenB = len(B)
    if lenA>lenB: return 1
    if lenB>lenA: return -1
    for i in range(len(A) - 1, 0, -1):
        if A[i] != B[i]:
            return 1 if A[i] > B[i] else -1
    A = A[0]
    B = B[0]
    if A[0] != B[0]: return -1 if A[0] == 1 else 1
    sign = -1 if A[0] == 1 else 1
    lenA = len(A)
    lenB = len(B)
    A_layer = lenA - 2 if lenA > 2 else 0
    B_layer = lenB - 2 if lenB > 2 else 0
    if A_layer != B_layer: return sign * (1 if A_layer > B_layer else -1)
    min_len = min(lenA, lenB)
    for i in range(1, min_len + 1):
        Ai = A[-i]
        Bi = B[-i]
        if Ai != Bi: return sign * (1 if Ai > Bi else -1)
    if lenA != lenB: return sign * (1 if lenA > lenB else -1)
    return 0

def lt(a, b): return compare(a, b) == -1
def gt(a, b): return compare(a, b) == 1
def eq(a, b): return compare(a, b) == 0
def lte(a, b): return compare(a, b) != 1
def gte(a, b): return compare(a, b) != -1
def maximum(a, b):
    if gte(a,b): return correct(a)
    else: return correct(b)

def minimum(a, b):
    if lte(a,b): return correct(a)
    else: return correct(b)

def neg(x):
    x = correct(x)
    return [[1-x[0][0]] + x[0][1:]] + x[1:]

def tofloat(a):
    a = correct(a)
    if a[0][0] == 1:
        if gt(neg(a), [[0, 308.25, 1], 0, 0, 0]): return None
    if gt(a, [[0, 308.25, 1], 0, 0, 0]): return None
    a = a[0]
    val = a[1]
    if len(a) == 3: val = 10**val
    return float(-val) if a[0] == 1 else float(val)

def tofloat2(a):
    a = correct(a)
    if a[1] != 0 or a[2] != 0 or a[3] != 0: return None
    if len(a)>4: return a
    a = a[0]
    if not len(a) == 2: return None
    return -a[1] if a[0] == 1 else a[1]

def _is_int_like(x):
    v = tofloat(x)
    return v is not None and abs(v - round(v)) < 1e-12

def _lambertw_float(r, tol=1e-12, max_iter=100):
    if not math.isfinite(r): raise ValueError("lambertw: non-finite input")
    if r < -0.3678794411714423: raise ValueError("lambertw is unimplemented for results less than -1/e on the principal branch")
    if r == 0: return 0
    if r == 1: return 0.5671432904097839
    t = 0 if r < 10 else (math.log(r) - math.log(math.log(r)))
    for _ in range(max_iter):
        n = (r * math.exp(-t) + t*t) / (t + 1)
        if abs(n - t) < tol * max(1, abs(n)): return n
        t = n
    raise RuntimeError(f"lambertw: iteration failed to converge: {r}")

def lambertw(x):
    X = correct(x)
    if X[1] != 0 or X[2] != 0 or X[3] != 0: return X
    if len(X)>4: return X
    x = x[0]
    if lt(X, [1, 0.3678794411714423]): raise ValueError("lambertw is unimplemented for results less than -1/e on the principal branch")
    if eq(X, 0): return [[0, 0], 0, 0, 0]
    if eq(X, 1): return [[0, 0.5671432904097839], 0, 0, 0]
    r = tofloat(X)
    if r is not None: return correct(_lambertw_float(r))
    L1 = ln(X)
    L2 = ln(L1)
    approx = add(subtract(L1, L2), divide(L2, L1))
    return correct(approx)

def log(x):
    arr = correct(x)
    if arr[0][0] == 1: raise ValueError("Can't log a negative")
    if arr[1] != 0 or arr[2] != 0 or arr[3] != 0: return arr
    if len(arr)>4: return arr
    arr = arr[0]
    len_arr = len(arr)
    if len_arr == 2: return correct(_log10(arr[1]))
    if len_arr == 3: return correct([[0, arr[1], arr[2] - 1], 0, 0, 0])
    if len_arr > 3: return [arr, 0, 0, 0]
    return [arr, 0, 0, 0]

def slog(x):
    arr = correct(x)
    if arr[1] != 0 or arr[2] != 0 or arr[3] != 0: return arr
    if len(arr)>4: return arr
    arr = arr[0]
    if arr[0] == 1: raise ValueError("Can't slog a negative")
    if lte(arr, 10): return correct(_log10(arr[1]))
    if lte(arr, [[0, 10000000000], 0, 0]): return correct(_log10(tofloat(log(arr))) + 1)
    len_arr = len(arr)
    if len_arr < 3: return correct(_log10(tofloat(log(log(arr)))) + 2)
    if len_arr == 3: return correct(tofloat(slog(arr[:2])) + arr[2])
    if len_arr == 4: return correct(0, arr[1:3] + [arr[4] - 1])
    return [arr, 0, 0]
def hyper_log(x, k):
    k = tofloat2(k)
    x = correct(x)
    if k == None: raise NotImplementedError("Hyper_log logs layer is not implemented for layers being more than 2^53-1")
    if x[2] != 0 or x[3] != 0: return x
    if k > 20:
        layers = 0
        if x[1] != 0: layers = x[1]
        else: layers = len(x[0])
        if layers >= k: return x
        return [[0, 1], 0, 0]
    x = x[0]
    if not _is_int_like(k) or tofloat(k) < 0: raise ValueError("hyper_log height must be a non-negative integer-like value")
    if k < 1: raise ValueError("k must be >= 1")
    if x[0] == 1: raise ValueError("Can't hyper_log a negative")
    if lte(x, 10): return correct(_log10(x[1]))
    if k == 1: return log(x)
    arr_len = len(x)
    pol = polarize(x, True)
    start = _log10(pol['bottom']) + pol['top']
    for i in range(k-pol["height"]-1): start = _log10(start)+1
    if arr_len == (k + 1): return correct(tofloat(hyper_log(x[:k], k)) + x[k])
    if arr_len == (k + 2): return correct([0] + x[1:(k + 1)] + [x[k + 1] - 1])
    if arr_len > (k + 2): return x
    return correct(start)
def abs_val(x): 
    x=correct(x)
    after = x[1:]
    x=x[0]
    return correct([[0] + x[1:]]+after)

def addlayer(x, layers=1,_add=0):
    arr = correct(x)
    if arr[1] != 0 or arr[2] != 0 or arr[3] != 0:
        if arr[0][0] == 1: return [[0, 0], 0, 0, 0]
        return arr
    arr = arr[0]
    len_arr = len(arr)
    arr0=arr[0]
    if arr0 == 1 and len_arr == 2: return correct([0, 10**(-(arr[1]+_add))])
    if arr0 == 1 and gt(abs_val(x), [[0, 308, 1], 0, 0, 0]): return [[0, 0], 0, 0, 0]
    if len_arr == 2: return correct([[0, arr[1], 1], 0, 0, 0])
    if len_arr == 3: return correct([[0, arr[1], arr[2] + layers], 0, 0, 0])
    if len_arr > 3: return [arr, 0, 0, 0]
    return arr

def add(a, b):
    a, b = correct(a), correct(b)
    if a[1] != 0 or a[2] != 0 or a[3] != 0: return maximum(a,b)
    if b[1] != 0 or b[2] != 0 or b[3] != 0: return maximum(a,b)
    if len(b)>4: return maximum(a,b)
    if len(a)>4: return maximum(a,b)
    a = a[0]
    b = b[0]
    if gt(a, [[0, MAX_SAFE_INT, 1], 0, 0, 0]) or gt(b, [[0, MAX_SAFE_INT, 1], 0, 0, 0]): return maximum(a,b)
    if a[0] == 1 and b[0] == 1: return neg(add(neg(a),neg(b)))
    if a[0] == 1 and b[0] == 0: return subtract(b, neg(a))
    if a[0] == 0 and b[0] == 1: return subtract(a, neg(b))
    len_a = len(a)
    len_b = len(b)
    if len_a == 3 or len_b == 3:
        if (len_a > 2 and a[2] > 1) or (len_b > 2 and b[2] > 1): return maximum(a, b)
    if len_a == 2 and len_b == 2: return correct([0, tofloat(a) + tofloat(b)])
    loga = tofloat(log(maximum(a,[[0,1], 0, 0])))
    logb = tofloat(log(b))
    M = max(loga, logb)
    m = min(loga, logb)
    return addlayer(M + tofloat(log(1 + 10**(m - M))))

def subtract(a,b):
    a, b = correct(a), correct(b)
    if eq(a,b) and a[0] == b[0]: return [[0, 0], 0, 0, 0]
    if gt(a, [[0, MAX_SAFE_INT, 1], 0, 0, 0]) or gt(b, [[0, MAX_SAFE_INT, 1], 0, 0, 0]):
        if gt(b,a): return neg(b)
        if gt(a,b): return a
    a = a[0]
    b = b[0]
    if eq(a,b): return neg(add(abs_val(a),abs_val(b)))
    if a[0] == 1 and b[0] == 1: return neg(subtract(abs_val(b), abs_val(a)))
    if a[0] == 1 and b[0] == 0: return neg(addlayer(tofloat(log(abs_val(a))) + tofloat(log(1 + tofloat(addlayer(tofloat(log(b)) - tofloat(log(abs_val(a)))))))))
    if a[0] == 0 and b[0] == 1: return add(a, abs_val(b))
    if lt(a,b):
        if a[0] == 0 and b[0] == 0: return neg(addlayer(tofloat(log(a)) + tofloat(log(abs_val(1 - tofloat(addlayer(tofloat(log(b)) - tofloat(log(a)))))))))
    if a[0] == 0 and b[0] == 0: return addlayer(tofloat(log(a)) + tofloat(log(1 - tofloat(addlayer(tofloat(log(b)) - tofloat(log(a)))))))

def multiply(a, b):
    a = correct(a)
    b = correct(b)
    if a[1] != 0 or a[2] != 0 or a[3] != 0: return maximum(a,b)
    if b[1] != 0 or b[2] != 0 or b[3] != 0: return maximum(a,b)
    if len(b)>4: return maximum(a,b)
    if len(a)>4: return maximum(a,b)
    a = a[0]
    b = b[0]
    result_sign = a[0] ^ b[0]
    if gt(a, [[0, 1000, 2], 0, 0, 0]) or gt(b, [[0, 1000, 2], 0, 0, 0]): return maximum(a,b)
    if len(a) == 2 and len(b) == 2:
        val = (a[1] if a[0] == 0 else -a[1]) * (b[1] if b[0] == 0 else -b[1])
        return correct([0 if val >= 0 else 1, abs(val)])
    result = addlayer(add(log(a), log(b)))
    return result if result_sign == 0 else neg(result)

def divide(a, b):
    a = correct(a)
    b = correct(b)
    if eq(b, [[0, 0], 0, 0, 0]): raise ZeroDivisionError("Can't divide with 0")
    if gt(maximum(a,b), [[0, MAX_SAFE_INT, 2], 0, 0, 0]): return a if gt(a,b) else 0
    a = a[0]
    b = b[0]
    if a[0] ^ b[0] == 1: return neg(divide(abs_val(a), abs_val(b)))
    if len(b) == 2 and len(a) == 2: return correct([0, tofloat(a) / tofloat(b)])
    if eq(log(a), [[0, 0], 0, 0, 0]): return addlayer(subtract(a, log(b)), _add=1)
    result = subtract(log(a), log(b))
    return addlayer(result)

def power(a, b):
    a = correct(a)
    b = correct(b)
    if b[0][0] == 1:
        if b[1] != 0 or b[2] != 0 or b[3] != 0: return [[0], 0, 0, 0]
        if len(b)>4: return [[0], 0, 0, 0]
        if a[1] != 0 or a[2] != 0 or a[3] != 0: return maximum(a,b)
        if len(a)>4: return maximum(a,b)
    if a[1] != 0 or a[2] != 0 or a[3] != 0: return maximum(a,b)
    if b[1] != 0 or b[2] != 0 or b[3] != 0: return maximum(a,b)
    if len(b)>4: return maximum(a,b)
    if len(a)>4: return maximum(a,b)
    a = a[0]
    b = b[0]
    if b[0] == 1 and a[0] == 0: return divide(1, power(a,neg(b)))
    if b[0] == 1 and a[0] == 1: return divide(1, power(neg(a),neg(b)))
    if a[0] == 1: return addlayer(multiply(log(neg(a)), b))
    return addlayer(multiply(log(a), b))

def factorial(n):
    n= correct(n)
    if n[0][0] == 1: raise ValueError("Can't factorial a negative")
    if n[1] != 0 or n[2] != 0 or n[3] != 0: return n
    return gamma(add(n, 1))

def floor(x):
    x = correct(x)
    if x[1] != 0 or x[2] != 0 or x[3] !=0: return x
    x = x[0]
    if len(x) == 2: return correct(str(int(x[1])).strip("+"))
    else: return x

def ceil(x):
    x = correct(x)
    if x[1] != 0 or x[2] != 0 or x[3] != 0: return x
    x = x[0]
    if len(x) == 2: return correct(str(math.ceil(x[1])).strip("+"))
    else: return x

def gamma(x):
    x = correct(x)
    if x[0][0] == 1: raise ValueError("Can't factorial a negative")
    if x[1] != 0 or x[2] != 0 or x[3] != 0: return x
    if len(x)>4: return x
    x0 = x[0]
    if gt(x0, [0, 15.954589770191003, 1]): return exp(x)
    if gte(x0, MAX_SAFE_INT): return exp(multiply(x0, subtract(ln(x0), 1)))
    n = tofloat2(x0)
    if n <= 171: return correct(math.gamma(n))
    t = n - 1
    l = 0.9189385332046727  # 0.5*ln(2π)
    l += (t + 0.5) * math.log(t)
    l -= t
    n2 = t * t
    np = t
    l += 1 / (12 * np)
    np *= n2
    l -= 1 / (360 * np)
    np *= n2
    l += 1 / (1260 * np)
    np *= n2
    l -= 1 / (1680 * np)
    return exp(correct(l))
def tetration(a, r, do=False):
    a = correct(a)
    r = correct(r)
    if a[1] != 0 or a[2] != 0 or a[3] != 0: return maximum(a,r)
    if len(a)>4: maximum(a,r)
    if r[1] != 0 or r[2] != 0 or r[3] != 0: return maximum(a,r)
    if len(r)>4: maximum(a,r)
    a = a[0]
    r = r[0]
    if lte(r, [[1, 2], 0, 0, 0]): raise ValueError("tetr(a, r): undefined for r <= -2 on the principal branch")

    if eq(a, [[0, 0], 0, 0, 0]):
        if eq(r, [[0, 0], 0, 0, 0]): raise ValueError("0^^0 is undefined")
        if _is_int_like(r): return correct(0 if int(tofloat(r)) % 2 == 0 else 1)
        raise ValueError("tetr(0, r) with non-integer r is not supported")

    if eq(a, 1):
        if eq(r, [[1, 1], 0, 0, 0]): raise ValueError("1^^(-1) is undefined")
        return [[0, 1], 0, 0, 0]
    if gt(r,[0,1,1,MAX_SAFE_INT]) or gt(a,[0, 1,1,1,MAX_SAFE_INT]): return maximum(a,r)
    if gte(r,MAX_SAFE_INT) and lte(r,[0, 1,MAX_SAFE_INT]):
        if do == True: return add(slog(a)[0], r)[0] + [1]
        return correct(add(slog(a)[0], r)[0] + [1])
    if gt(r,[0, 1,MAX_SAFE_INT]) or gt(a,[0, 1,1,MAX_SAFE_INT]):
        q = r[:3] + [(r[3] + 1)]
        return maximum(q,a)
    if eq(r, -1): return [[0, 0], 0, 0, 0]
    if eq(r, 0): return [[0, 1], 0, 0, 0]
    if eq(r, 1): return a
    if eq(r, 2): return power(a, a)
    if lt(a, 1.444667861009766):
        n = neg(ln(a))
        return divide(lambertw(n), n)
    s = tofloat(r)
    if s is None:
        try:
            if lt(a, 1.444667861009766):
                n = neg(ln(a))
                return divide(lambertw(n), n)
        except Exception:
            pass
        raise ValueError("tetr(a, r): r is too large for iterative evaluation in this simplified implementation")
    x1 = tofloat(a)
    if x1 == None:
        y_floor = int(s)
        frac = s-y_floor
        return addlayer(multiply(power(a, frac), log(a)),y_floor)
    y_floor = int(s)
    frac = s-y_floor
    end = math.exp(frac * math.log(x1)) if frac != 0 else 1.0
    skip = 0
    try:
        while y_floor > 0 and skip != 1000:
            end = x1**end
            y_floor -= 1
            skip += 1
    except OverflowError: end *= _log10(x1)
    if do == True: return correct([0, end, y_floor])[0]
    return correct([0, end, y_floor])
def _arrow(t, r, n, a_arg=0, prec=precise_arrow, done=False):
    r = tofloat2(r)
    t = correct(t)
    n = correct(n)
    if eq(r, 0): return multiply(t, n)
    if eq(r, 1): return power(t, n)
    if eq(r, 2): return tetration(t, n, do=True)
    if eq(t,2) and eq(n,2): return [[0, 4], 0, 0, 0]
    if eq(t, 143): t = 143.0000000000001 # If i dont do this the code never stops
    s = tofloat2(n)
    s_t = tofloat2(t)
    if prec == False and s != None and lt(n,2) and s_t != None and done == False:
        amount = 0
        while amount < r and s <= 2:
            amount += 1
            s = s_t ** (s - 1)
        return _arrow(s_t,r-amount,s, prec=False, done=True)
    if prec == False and r > arrow_precision:
        arrow_amount = _arrow(t,arrow_precision,n, a_arg, True, done=True)
        if eq(n,2): return [0, 10000000000] + [8] * (r-arrow_precision) + arrow_amount[-(arrow_precision):]
        return [0, 10000000000] + [8] * (r-arrow_precision) + arrow_amount[-(arrow_precision-1):]
    if gt(maximum(t, n), [0, 9007199254740991] + [8] * (r-1)): return maximum(t, n)
    if gt(t, [0, 9007199254740991] + [8] * (r-2)) or s is None:
        if gt(t, [0, 9007199254740991] + [8] * (r-2)):
            a = t.copy()
            a = a[:r]
        elif gt(t, [0, 9007199254740991] + [8] * (r-3)): a = t[r-1]
        else: a = [0, 0]
        j = add(a, n)[0]
        while len(j) <= r: j.append(0)
        j[r] += 1
        return j
    if r == 3 and gt(t, [0, MAX_SAFE_INT, 2]): return t[0] + [1]
    if s is None:
        arr_n = correct(n)[0]
        target_len = r + 2
        arr_res = arr_n + [0] * (target_len - len(arr_n))
        arr_res[-1] += 1
        return correct(arr_res)
    thr_r = [0, MAX_SAFE_INT, 1]
    if gte(t, thr_r) or (tofloat2(n) is None and gt(n, [0, MAX_SAFE_INT])): return maximum(t, n)
    u = int(s)
    frac = s - u
    if frac > 1e-15: i = _arrow(t, r - 1, frac, a_arg + 1, False, done=True)
    else:
        i = t
        if u > 0: u -= 1
    fcount = 0
    limit = thr_r
    while u != 0 and lt(i, limit) and fcount < 100:
        if u > 0:
            i = _arrow(t, r - 1, i, a_arg + 1, done=True)
            u -= 1
        else: break
        fcount += 1
    try:
        if len(i) >= r:
            idx = r
            if idx < len(i): i[idx] = i[idx] + u
            else:
                i = i + [0] * (idx - len(i) + 1)
                i[idx] = i[idx] + u
            return i
    except Exception: pass
    return i

def arrow(base, arrows, n, a_arg=0, prec=precise_arrow):
    q = correct(arrows)
    base_float = tofloat2(base)
    n_float = tofloat2(n)
    t = correct(base)
    n_corr = correct(n)
    if t[3] != 0 or q[3] != 0 or n_corr[3] != 0: return maximum(t, maximum(q, n_corr))
    if lte(n_corr, [[0, 1], 0, 0, 0]): return pow(base, n)
    if gt(q, [[0, 20], 0, 0, 0]):
        if base_float == None or n_float == None:
            return maximum(maximum(t, n_corr), arrow(10, q, 10))
    if gt(maximum(n_corr, t), [0, 16, 1] + [0] * 17 + [1]): return maximum(n_corr, t)
    if gt(q, MAX_SAFE_INT):
        return [q[0], q[1], q[2]+1, 0]
    if lt(q, [[0, 0], 0, 0]): raise ValueError("n must be >= 0")
    arro = 100
    if lt(base, 3.1): base = 3.1
    if lt(base, 4): arro = 295
    elif lt(base, 5): arro = 132
    elif lt(base, 7): arro = 100
    if gt(q, arro):
        r = tofloat2(q)
        result = [0, 0, 0]
        amount = 0
        s_t = tofloat2(base)
        if n_float == None: s = n
        else: s = n_float
        while amount < r and s <= 2 and n_float !=None and s_t != None:
            amount += 1
            s = s_t ** (s - 1)
        result[1] = r-amount
        result[0] = _arrow(base, arro, n)
        return result
    r_float = tofloat2(q)
    if r_float != None: 
        if _is_int_like(r_float) == False: raise("Arrows must be an integer")
        q = r_float
    res = _arrow(t, q, n_corr, a_arg, prec)
    return correct(res)
def expansion(a, b):
    a, b = correct(a), correct(b)
    float_b = tofloat2(b)
    if a[0][0] == 1 or b[0][0] == 1: raise ValueError("Expansion undefined for negative numbers")
    if eq(b, 0): raise ValueError("2nd expansion number can't be 0")
    if eq(a, 1): return [[0, 1], 0, 0, 0]
    if eq(a, 2): return [[0, 4], 0, 0, 0]
    if eq(a, 0): return [[0, 0], 0, 0, 0]
    if float_b == None: return [b[0]] + b[1:3] + [b[3]+1]
    b=float_b
    if _is_int_like(b) != True: raise ValueError("2nd expansion number must be an integer")
    b = int(b)
    if lt(a, MAX_SAFE_INT):
        if _is_int_like(a) != True: raise ValueError("1st expansion number must be an integer")
    if b == 1: return a
    if b == 2:
        if eq(a,2): return [[0, 4], 0, 0, 0]
    result = [0, 0, int(b-2), 0]
    if gt(a, MAX_SAFE_INT): result[2] += 1+a[2]
    result[:2] = arrow(a, a, a)[:2]
    return result
def multiexpansion(a,b):
    a, b = correct(a), tofloat(b)
    if a[0][0] == 1 or b < 0: raise ValueError("Multi-expansion undefined for negative numbers")
    if b == 0: raise ValueError("2nd multi-expansion number can't be 0")
    if eq(a, 1): return [[0, 1], 0, 0, 0]
    if eq(a, 2): return [[0, 4], 0, 0, 0]
    if eq(a, 0): return [[0, 0], 0, 0, 0]
    if _is_int_like(b) != True: raise ValueError("2nd expansion number must be an integer")
    b = int(b)
    if lt(a, MAX_SAFE_INT):
        if _is_int_like(a) != True: raise ValueError("1st expansion number must be an integer")
    if b == 1: return a
    if b == 2:
        if eq(a,2): return [[0, 4], 0, 0, 0]
    result = [0, 0, 0, int(b-2)]
    if gt(a, MAX_SAFE_INT): result[3] += 1+a[3]
    result[:3] = expansion(a,a)[:3]
    return result
def expansionarrow(a,b, c):
    a, b, c = correct(a), tofloat(b), int(tofloat2(c))
    if c == None: raise OverflowError("expansion arrows amount is too high")
    if c == 1: return expansion(a,b)
    if c == 2: return multiexpansion(a,b)
    if a[0][0] == 1 or b < 0: raise ValueError("expansionarrow undefined for negative numbers")
    if b == 0: raise ValueError("2nd multi-expansion number can't be 0")
    if eq(a, 1): return [[0, 1], 0, 0, 0]
    if eq(a, 2): return [[0, 4], 0, 0, 0]
    if eq(a, 0): return [[0, 0], 0, 0, 0]
    if _is_int_like(b) != True: raise ValueError("2nd expansion number must be an integer")
    b = int(b)
    if lt(a, MAX_SAFE_INT):
        if _is_int_like(a) != True: raise ValueError("1st expansion number must be an integer")
    if b == 1: return a
    if b == 2:
        if eq(a,2): return [[0, 4], 0, 0, 0]
    result = [int(b-2)]*(c+2)
    if gt(a, MAX_SAFE_INT): result[c+1] += 1+a[c+1]
    result[:2] = arrow(a,a,a)[:2]
    return result
def logbase(a,b):
    if lte(b, [[0, 1], 0, 0, 0]): raise ValueError("LogBase undefined for bases under or equal to 1")
    return divide(log(a),log(b))
def ln(a): return multiply(log(a),2.302585092994046) # log10(a)/log10(e) or log10(a)*(1/log10(e))
def sqrt(a): return root(a,2)
def root(a,b): 
    if lt(b,[[0, 0], 0, 0, 0]): raise ValueError("Can't root a negative")
    if gt(b,[[0, 0], 0, 0, 0]) and lt(b,[[0, 1], 0, 0, 0]): return power(a,divide(1,b))
    if eq(b, [[0, 0], 0, 0, 0]): raise ValueError("Root of 0 is undefined")
    return addlayer(divide(log(a),b))
def exp(x): return power(2.718281828459045, x)
def format(num, decimals=decimals, small=False):
    precision2 = max(5, decimals)
    precision3 = max(4, decimals)
    precision4 = max(6, decimals)
    num_correct = correct(num)
    n = num_correct[0]
    if len(n) == 2 and abs(n[1]) < 1e-308 and num_correct[1] != 0 and num_correct[2] != 0: return f"{0:.{decimals}f}"
    if n[0] == 1: return "-" + format(neg(num_correct), decimals)
    if lt(num_correct, 0.0001):
        inv = 1/tofloat(n)
        return "1/" + format(inv, decimals)
    elif lt(num_correct, 1): return regular_format(n, decimals + (2 if small else 0))
    elif lt(num_correct, 1000): return regular_format(n, decimals)
    elif lt(num_correct, MAX_SAFE_INT): return comma_format(n)
    elif lt(num_correct, [0, 10000000000, 3]):
        bottom = array_search(n, 1)
        rep = array_search(n, 2) - 1
        if bottom >= 1e9:
            bottom = _log10(bottom)
            rep += 1
        m = 10 ** (bottom - int(bottom))
        e = int(bottom)
        p = precision2 if bottom < 1_000_000 else 2
        return ("e" * int(rep)) + regular_format([0, m], p) + "e" + comma_format(e)
    pol = polarize(n)
    if lt(num_correct, [0, 10000000000, 999998]): return regular_format([0, pol['bottom']], precision3) + "F" + comma_format(pol['top'])
    elif lt(num_correct, [0, 10000000000, 8, 3]):
        rep = array_search(n, 3)
        if rep >= 1:
            n_arr = set_to_zero(n, 3)
            return ("F" * int(rep)) + format(n_arr, decimals)
        n_val = array_search(n, 2) + 1
        if gte(num_correct, [0, 10, n_val]):
            n_val += 1
        return "F" + format(n_val, decimals)
    elif lt(num_correct, [0, 10000000000, 8, 999998]): return regular_format([0, pol['bottom']], precision3) + "G" + comma_format(pol['top'])
    elif lt(num_correct, [0, 10000000000, 8, 8, 3]):
        rep = array_search(n, 4)
        if rep >= 1:
            n_arr = set_to_zero(n, 4)
            return ("G" * int(rep)) + format(n_arr, decimals)
        n_val = array_search(n, 3) + 1
        if gte(num_correct, [0, 10, 0, n_val]):
            n_val += 1
        return "G" + format(n_val, decimals)
    elif lt(num_correct, [0, 10000000000, 8, 8, 999998]): return regular_format([0, pol['bottom']], precision3) + "H" + comma_format(pol['top'])
    elif lt(num_correct, [0, 10000000000, 8, 8, 8, 3]):
        rep = array_search(n, 5)
        if rep >= 1:
            n_arr = set_to_zero(n, 5)
            return ("H" * int(rep)) + format(n_arr, decimals)
        n_val = array_search(n, 4) + 1
        if gte(num_correct, [0, 10, 0, 0, n_val]):
            n_val += 1
        return "H" + format(n_val, decimals)
    elif len(num_correct)>4:
        pol = polarize([0, 10000000000]+num_correct[2:], True)
        val = _log10(pol["bottom"]) + pol["top"]
        return regular_format(val,16) + "M" + comma_format(pol["height"]-1)
    elif num_correct[3] > MAX_SAFE_INT: return "L" + format(num_correct[3])
    elif num_correct[3] != 0 and num_correct[3] < 4: return "K" * num_correct[3] + format(num_correct[:3] + [0])
    elif num_correct[3] != 0 and num_correct[3] >= 4:
        pol = polarize(n, True)
        if lt(n, [0, 10000000000, 8]): return format(1+_log10(_log10(pol["bottom"])+pol["top"]), precision4) + "L" + comma_format(num_correct[3]+1)
        if lt(n, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return format(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E, precision4) + "L" + comma_format(num_correct[3]+1)
        else:
            if num_correct[1] == 0: num_correct[1] = len(n)-1
            nextToTopJ = num_correct[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return format(1+ _log10(_log10(bottom)+top),precision4) + "L" + comma_format(num_correct[3]+2)
    elif num_correct[2] > MAX_SAFE_INT: return "K" + format(num_correct[2])
    elif num_correct[2] != 0 and num_correct[2] < 4: return "J" * num_correct[2] + format(num_correct[:2] + [0])
    elif num_correct[2] != 0 and num_correct[2] >= 4:
        pol = polarize(n, True)
        if lt(n, [0, 10000000000, 8]): return format(1+_log10(_log10(pol["bottom"])+pol["top"]), precision4) + "K" + comma_format(num_correct[2]+1)
        if lt(n, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return format(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E, precision4) + "K" + comma_format(num_correct[2]+1)
        else:
            if num_correct[1] == 0: num_correct[1] = len(n)-1
            nextToTopJ = num_correct[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return format(1+ _log10(_log10(bottom)+top),precision4) + "K" + comma_format(num_correct[2]+2)
    elif num_correct[1] != 0:
        pol = polarize(n, True)
        val = _log10(pol['bottom']) + pol['top']
        j = num_correct[1]
        if j > 1e9: j = format(j, 6)
        else: j = comma_format(j)
        return regular_format([0, val], precision4) + "J" + j
    else:
        pol = polarize(n, True)
        val = _log10(pol['bottom']) + pol['top']
        return regular_format([0, val], precision4) + "J" + comma_format(pol['height'])
def hyper_e(x, use_sign=True):
    arr = correct(x)
    sign = "-E" if arr[0][0] == 1 else "E"
    if use_sign == False: sign = ""
    if arr[1] == 0: arr[1] = len(arr[0])
    # FOR NUMBERS ABOVE 10{2^53-1}10 MAY BE INACCURATE
    if len(x)>4: raise NotImplementedError("Hyper_e for numbers above 10{{1}}9007199254740991 is not implemented")
    if arr[3] != 0: raise NotImplementedError("Hyper_e for numbers above 10{{1}}9007199254740991 is not implemented")
    if arr[2] != 0: return sign + "10##" + str(len(arr[0])-1) + "#" + str(arr[2]+1)
    if arr[1] >= 10: return sign + "10000000000" + "#" + str(arr[0][-1]) + "##" + str(arr[1]-1)
    arr = arr[0]
    if len(arr) > 3:
        after = [v + 1 for v in arr[3:]]
        arr = arr[:3] + after
    return sign + "#".join(map(str, arr[1:]))
def string(arr, top=True):
    arr = correct(arr)
    sign = "-" if arr[0][0] == 1 and top else ""
    if arr[3] != 0:
        if arr[3] >=5: return "K^" + str(float(arr[3])) + " " + string(arr[:3] + [0])
        return "K" * arr[2] + string(arr[:3] + [0])
    if arr[2] != 0:
        if arr[2] >=5: return "J^" + str(float(arr[2])) + " " + string(arr[:2] + [0])
        return "J" * arr[2] + string(arr[:2] + [0])
    if arr[1] != 0:
        result = ""
        amount = 1
        for i in range(len(arr[0])-9, len(arr[0])):
            result += "(10{" + str(arr[1]-amount) + "})^" + str(arr[0][-amount]) + " "
            amount += 1
        return result +"10000000000"
    arr = arr[0]
    if len(arr) == 2: return f"{sign}{arr[1]}"
    e_count = arr[2]
    if e_count <= 7: inner = f"{'e'*e_count}{arr[1]}"
    else: inner = f"(10^)^{e_count} {arr[1]}"
    for d in range(3, len(arr)):
        n = arr[d]
        if n == 0: continue
        layer_depth = d - 1
        if layer_depth <= 3:
            arrows = "^" * layer_depth
            arrow_str = f"10{arrows}"
        else: arrow_str = f"10{{{layer_depth}}}"
        if n < 2: inner = f"{arrow_str}{inner}"
        else: inner = f"({arrow_str})^{n} {inner}"
    return sign + inner
def _suffix(x, suffix_decimals=decimals):
    x = correct(x)[0]
    if x[0] == 1: return "-" + _suffix([0] + x[1:])
    if len(x) == 3 and x[2] == 2 and x[1] < 308.2547155599167: x = [0, 10**x[1], x[2]-1]
    if len(x) > 2 and x[2] > 2 or _log10(x[1]) >= 308.2547155599167: return x
    if len(x) == 2:
        num_val = x[1]
        if num_val < 1000: 
            val = round(num_val, suffix_decimals)
            return str(int(val) if val == int(val) else val)
        exponent = int(_log10(num_val))
        mantissa = num_val / (10 ** exponent)
        SNumber = exponent
        SNumber1 = mantissa
    elif len(x) == 3:
        SNumber = x[1]
        SNumber1 = 1

    leftover = SNumber % 3
    SNumber = int(SNumber / 3) - 1

    def format_with_suffix(val, suffix):
        val_rounded = round(val, suffix_decimals)
        if val_rounded >= 1000:
            val_rounded /= 1000
            next_suffix = {"K": "M", "M": "B", "B": "T"}.get(suffix, "")
            suffix = next_suffix
        return str(int(val_rounded) if val_rounded == int(val_rounded) else val_rounded) + suffix

    base_num = SNumber1 * (10 ** leftover)

    if SNumber <= -1: return str(int(round(base_num, suffix_decimals))) if base_num == int(base_num) else str(round(base_num, suffix_decimals))
    elif SNumber == 0: return format_with_suffix(base_num, "K")
    elif SNumber == 1: return format_with_suffix(base_num, "M")
    elif SNumber == 2: return format_with_suffix(base_num, "B")

    txt = ""
    def suffixpart(n):
        nonlocal txt
        Hundreds = int(n / 100)
        n = n % 100
        Tens = int(n / 10)
        Ones = n % 10
        txt += FirstOnes[Ones]
        txt += SecondOnes[Tens]
        txt += ThirdOnes[Hundreds]

    def suffixpart2(n):
        nonlocal txt
        if n > 0: n += 1
        if n > 1000: n = n % 1000
        Hundreds = int(n / 100)
        n = n % 100
        Tens = int(n / 10)
        Ones = n % 10
        txt += FirstOnes[Ones]
        txt += SecondOnes[Tens]
        txt += ThirdOnes[Hundreds]

    if SNumber < 1000:
        suffixpart(SNumber)
        return format_with_suffix(base_num, "") + txt

    for i in range(len(MultOnes)-1, -1, -1):
        power_val = 10 ** (i * 3)
        if SNumber >= power_val:
            part_val = int(SNumber / power_val)
            suffixpart2(part_val - 1)
            txt += MultOnes[i]
            SNumber = SNumber % power_val
    return format_with_suffix(base_num, "") + txt

def suffix(num, small=False):
    precision2 = max(5, decimals)
    precision3 = max(4, decimals)
    precision4 = max(6, decimals)
    num_correct = correct(num)
    if len(num_correct)>4: raise NotImplementedError("Format not implemented for inputted number")
    n = num_correct[0]
    if len(n) == 2 and abs(n[1]) < 1e-308 and num_correct[1] != 0 and num_correct[2] != 0: return f"{0:.{decimals}f}"
    if n[0] == 1: return "-" + suffix(neg(num_correct), decimals)
    if lt(num_correct, 0.0001):
        inv = 1/tofloat(n)
        return "1/" + _suffix(inv)
    elif lt(num_correct, 1): return regular_format(n, decimals + (2 if small else 0))
    elif lt(num_correct, 1000): return regular_format(n, decimals)
    elif lt(num_correct, MAX_SAFE_INT): return _suffix(n)
    elif lt(num_correct, [0, max_suffix, 1]): return _suffix(n)
    elif lt(num_correct, [0, max_suffix, 2]):
        bottom = n[1]
        rep = n[2] - 1
        if bottom >= 1e9:
            bottom = _log10(bottom)
            rep += 1
        m = 10 ** (bottom - int(bottom))
        e = int(bottom)
        p = precision2
        return regular_format([0, m], p) + "e" + _suffix(e)
    elif lt(num_correct, [0, max_suffix, 3]):
        bottom = n[1]
        rep = n[2] - 1
        if bottom >= 1e9:
            bottom = _log10(bottom)
            rep += 1
        m = 10 ** (bottom - int(bottom))
        e = int(bottom)
        p = precision2
        return "e" + regular_format([0, m], p) + "e" + _suffix(e)
    elif lt(num_correct, [0, 10000000000, 3]):
        bottom = n[1]
        rep = n[2] - 1
        if bottom >= 1e9:
            bottom = _log10(bottom)
            rep += 1
        m = 10 ** (bottom - int(bottom))
        e = int(bottom)
        p = precision2
        return "ee" + regular_format([0, m], p) + "e" + _suffix(e)
    pol = polarize(n)
    if lt(num_correct, [0, 10000000000, 999998]): return regular_format([0, pol['bottom']], precision3) + "F" + _suffix(pol['top'], 0)
    elif lt(num_correct, [0, 10000000000, 8, 3]):
        rep = array_search(n, 3)
        if rep >= 1:
            n_arr = set_to_zero(n, 3)
            return ("F" * int(rep)) + suffix(n_arr, decimals)
        n_val = n[2] + 1
        if gte(num_correct, [0, 10, n_val]):
            n_val += 1
        return "F" + suffix(n_val, decimals)
    elif lt(num_correct, [0, 10000000000, 8, 999998]): return regular_format([0, pol['bottom']], precision3) + "G" + _suffix(pol['top'], 0)
    elif lt(num_correct, [0, 10000000000, 8, 8, 3]):
        rep = array_search(n, 4)
        if rep >= 1:
            n_arr = set_to_zero(n, 4)
            return ("G" * int(rep)) + suffix(n_arr, decimals)
        n_val = n[3] + 1
        if gte(num_correct, [0, 10, 0, n_val]):
            n_val += 1
        return "G" + suffix(n_val, decimals)
    elif lt(num_correct, [0, 10000000000, 8, 8, 999998]): return regular_format([0, pol['bottom']], precision3) + "H" + _suffix(pol['top'], 0)
    elif lt(num_correct, [0, 10000000000, 8, 8, 8, 3]):
        rep = array_search(n, 5)
        if rep >= 1:
            n_arr = set_to_zero(n, 5)
            return ("H" * int(rep)) + suffix(n_arr, decimals)
        n_val = n[4] + 1
        if gte(num_correct, [0, 10, 0, 0, n_val]):
            n_val += 1
        return "H" + suffix(n_val, decimals)
    elif num_correct[3] > MAX_SAFE_INT: return "L" + suffix(num_correct[3])
    elif num_correct[3] != 0 and num_correct[3] < 4: return "K" * num_correct[3] + suffix(num_correct[:3] + [0])
    elif num_correct[3] != 0 and num_correct[3] >= 4:
        pol = polarize(n, True)
        if lt(n, [0, 10000000000, 8]): return suffix(1+_log10(_log10(pol["bottom"])+pol["top"]), precision4) + "L" + suffix(num_correct[3]+1)
        if lt(n, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return suffix(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E, precision4) + "L" + suffix(num_correct[3]+1)
        else:
            if num_correct[1] == 0: num_correct[1] = len(n)-1
            nextToTopJ = num_correct[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return suffix(1+ _log10(_log10(bottom)+top),precision4) + "L" + suffix(num_correct[3]+2)
    elif num_correct[2] > MAX_SAFE_INT: return "K" + suffix(num_correct[2])
    elif num_correct[2] != 0 and num_correct[2] < 4: return "J" * num_correct[2] + suffix(num_correct[:2] + [0])
    elif num_correct[2] != 0 and num_correct[2] >= 4:
        pol = polarize(n, True)
        if lt(n, [0, 10000000000, 8]): return suffix(1+_log10(_log10(pol["bottom"])+pol["top"]), precision4) + "K" + suffix(num_correct[2]+1)
        if lt(n, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return suffix(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E, precision4) + "K" + suffix(num_correct[2]+1)
        else:
            if num_correct[1] == 0: num_correct[1] = len(n)-1
            nextToTopJ = num_correct[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return suffix(1+ _log10(_log10(bottom)+top),precision4) + "K" + suffix(num_correct[2]+2)
    elif num_correct[1] != 0:
        pol = polarize(n, True)
        val = _log10(pol['bottom']) + pol['top']
        j = num_correct[1]
        if j > 1e9: j = suffix(j, 6)
        else: j = suffix(j)
        return regular_format([0, val], precision4) + "J" + j
    else:
        pol = polarize(n, True)
        val = _log10(pol['bottom']) + pol['top']
        return regular_format([0, val], precision4) + "J" + suffix(pol['height'])
def arrow_format(x):
    x = correct(x)
    x0 = x[0]
    if len(x)>4: raise NotImplementedError("Format not implemented for inputted number")
    if x[3] != 0:
        if x[3] > MAX_SAFE_INT: return "10{{2}}" + str(float(x[3]))
        if x[3] < 4: return "10{{1}}" * x[3] + arrow_format(x[:3] + [0])
        pol = polarize(x0, True)
        if lt(x0, [0, 10000000000, 8]): return "10{{2}}" + format(x[3]+1+_log10(1+_log10(_log10(pol["bottom"])+pol["top"])))
        if lt(x0, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return "10{{2}}" + comma_format(x[3]+1+_log10(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E), 16)
        else:
            if x[1] == 0: x[1] = len(x0)-1
            nextToTopJ = x[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return "10{{2}}" + comma_format(x[3]+2 + _log10(1+_log10(_log10(bottom)+top)), 16)
    if x[2] != 0:
        if x[2] > MAX_SAFE_INT: return "10{{1}}" + str(float(x[2]))
        if x[2] < 4: return "10{10}" * x[2] + arrow_format(x[:2] + [0])
        pol = polarize(x0, True)
        if lt(x0, [0, 10000000000, 8]): return "10{{2}}" + format(x[2]+1+_log10(1+_log10(_log10(pol["bottom"])+pol["top"])))
        if lt(x0, [0, 10000000000, 8, 8, 8, 8, 8, 8, 8, 8, 8]): return "10{{2}}" + comma_format(x[2]+1+_log10(pol["height"] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E), 16)
        else:
            if x[1] == 0: x[1] = len(x0)-1
            nextToTopJ = x[1] + math.log((_log10(pol["bottom"]) + pol["top"]) / 2) * LOG5E
            if nextToTopJ >= 1e10: bottom = _log10(_log10(nextToTopJ))
            else: bottom = _log10(nextToTopJ)
            if nextToTopJ >= 1e10: top = 2
            else: top = 1
        return "10{{1}}" + comma_format(x[2]+2 + _log10(1+_log10(_log10(bottom)+top)), 16)
    if x[1] != 0:
        pol = polarize(x0, True)
        val = _log10(pol['bottom']) + pol['top']
        j = x[1]
        if j > 1e9: j = comma_format(j, 6)
        else: j = comma_format(j)
        return "10{" + str(j) + "}" + comma_format(val, 16)
    else:
        if lt(x0, 1e9): return format(x0)
        pol = polarize(x0)
        arrow = pol['height']+1
        if arrow > 7: return "10{" + str(arrow) + "}" + str(_log10(pol['bottom']) + pol['top'])
        return "10" + "^"*arrow + str(format(_log10(pol['bottom']) + pol['top']))
def from_hyper_e(x):
    if "##" in x: raise NotImplementedError("If you are trying to convert a hyper_e and it has ## in it, then it's not implemented yet.")
    if not x.lstrip('-').startswith('E'): raise ValueError("Not a hyper_e string")
    sign = int(x.startswith('-'))
    nums = [int(n) for n in x.lstrip('-E').replace('#', ',').split(',')]
    if len(nums) > 3: nums[2:] = [v - 1 for v in nums[2:]]
    return correct([sign] + nums)
def count_repeating(s, target=None):
    if not s: return 0
    if target is None: target = s[0]
    count = 0
    for ch in s:
        if ch == target: count += 1
        else: break
    return count
# Sniffed breaking bad money making stuff a bit too much to code and in the result got this code. Oh and spent ~3h for this trash
def fromstring(x, done=False):
    if x.startswith("K^"):
        x = x.strip("K^")
        return fromstring(x.split(" ", 1)[1])[:3] + [float(x.split(" ", 1)[0])]
    if x.startswith("K"): return fromstring(x.strip("K"))[:3] + [count_repeating(x)]
    if x.startswith("J^"):
        x = x.strip("J^")
        return fromstring(x.split(" ", 1)[1])[:2] + [float(x.split(" ", 1)[0])]
    if x.startswith("J"): return fromstring(x.strip("J"))[:2] + [count_repeating(x)]
    if x.startswith("(10"):
        size = x.strip("(10")
        size = count_repeating(size)
    if x.startswith("(10{"):
        size = x.strip("(10{")
        after = size.split("})^", 1)[0]
        size = int(after.split(None, 1)[0])
        if size > 10 and done==False:
            result = fromstring(x, done=True)
            return [result[0], size+1, result[2]]
    if x.startswith("10{"):
        size = x.strip("10").strip("{")
        before, after = size.split("}", 1)
        size = int(before)
    if x.startswith("10^"):
        size = x.strip("10")
        size = count_repeating(size)
    if x.startswith("e"): size = 1
    array = [0] * (size+3)
    if x.startswith("-"): 
        array[0] = 1
        x = x.strip("-")
    def logic(x, amount=size+1, gap=0):
        try:  array[1] = float(x)
        except: pass
        if x.startswith("(10^"):
            x2 = x.strip("(10")
            count = count_repeating(x2)
            after = x.split(")^", 1)[1]
            num = after.split(None, 1)[0]
            array[count + 1] = int(num)
            before, after = x.split(" ", 1)
            x = after
            logic(x, amount-1)
        if x.startswith("10^"):
           lst = list(x)
           x =  x.strip("10")
           count = count_repeating(x)
           array[count +1] = 1
           x= "".join(lst[2+count:])
           logic(x, amount-1)
        if x.startswith("(10{"):
            x = x.strip("(10{")
            before, after = x.split("})^", 1)
            num = after.split(None, 1)[0]
            if gap == 0: array[amount] = int(num)
            else: array[amount-(gap-int(before))+1] = int(num)
            gap = before
            before, after = x.split(" ", 1)
            x = after
            logic(x, amount-1, gap=int(before.split("})^")[0]))
        if x.startswith("10{"):
            x = x.removeprefix("10{")
            before, after = x.split("}", 1)
            array[int(before) + 1] = 1
            x = after
            logic(x, amount-1)
        if x.startswith("e"):
            e = count_repeating(x)
            array[2] = e
            array[1] = float(x[x.rfind('e')+1:])
    logic(x)
    if array[1] == 0: array[1] = 10000000000
    return correct(array)
def pentation(a,b): return arrow(a,3,b)
def hexation(a,b): return arrow(a,4,b)
def heptation(a,b): return arrow(a,5,b)
def octation(a,b): return arrow(a,6,b)
def nonation(a,b): return arrow(a,7,b)
def decation(a,b): return arrow(a,8,b)
def plog(x): return hyper_log(x, 3)
def hlog(x): return hyper_log(x, 4)
# Short names
def hept(a,b): return heptation(a,b)
def hex(a,b): return hexation(a,b)
def pent(a,b): return pentation(a,b)
def tetr(a,b): return tetration(a,b)
def pow(a,b): return power(a,b)
def sub(a,b): return subtract(a,b)
def div(a,b): return divide(a,b)
def mul(a,b): return multiply(a,b)
def fact(a): return factorial(a)
