

period_keys = ['d','wkd','m','bim','q','sem','y']

_rate_conversion_exponent = {
    'd':360.0,
    'wkd':252.0,
    'm':12.0,
    'bim':6.0,
    'q':4.0,
    'sem':2.0,
    'y':1.0}


def rate_conversion(rate, base, to):
    return rate**(_rate_conversion_exponent[base]/_rate_conversion_exponent[to])


_period_singular = {
    'd':"dia",
    'wkd':"dia útil",
    'm':"mês",
    'bim':"bimestre",
    'q':"trimestre",
    'sem':"semestre",
    'y':"ano"
}

_period_plural = {
    'd':"dias",
    'wkd':"dias úteis",
    'm':"meses",
    'bim':"bimestres",
    'q':"trimestres",
    'sem':"semestres",
    'y':"anos"
}


def format_period(number):
    if number == "singular":
        def fun(option):
            return _period_singular[option]
    elif number == "plural":
        def fun(option):
            return _period_plural[option]
    return fun