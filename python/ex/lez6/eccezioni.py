f=lambda a,b: a//b

class TuaMammaErrore(Exception):
    pass

try:
    c=f(4,1)
except (ZeroDivisionError,IndentationError) as err:
    print(str(err.args)+" errore!")
else:
    print('Risultato ',c)
print('FINEE')
x=2
assert x>10, "ics minore di undici"
raise IsADirectoryError('Unexpected end of JSON input')