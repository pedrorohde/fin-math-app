

rate_conversion_exponent = {
    'd':360.,
    'wkd':252.,
    'm':12.,
    'bim':6.,
    'q':4.,
    'sem':2.,
    'y':1.
}

def rate_conversion(rate, from, to):
    return rate**(rate_conversion_exponent[from]/rate_conversion_exponent[to])