def priceFormulaValidator(value):
    value = value.replace(' ','')
    err_val = []
    for i in value and i not in 'x/*+-.0123456789':
        err_val.append(i)
    if len(err_val) > 0:
        raise exceptions.ValidationError(f'Формула имеет не допустимые значения: {str(err_val)}')
    x = 1
    try: eval(value)
    except: raise exceptions.ValidationError(f'Формула не валидна')