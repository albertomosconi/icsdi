import icsdi

while True:
    text = input('icsdi > ')
    result, error = icsdi.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
