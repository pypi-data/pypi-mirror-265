def calc():
    """ 
    Найпростіший калькулятор.
    Приймає до себе два числа та чотири операції:
    додавання, віднімання, множення та ділення.
    
    :param1: number1
    :param2: number2
    :param3: data

    Типи змінних:
    
    :type1: int
    :type2: int
    :type3: str
    
    """
 
    while True:
        number1 = int(input("Введіть перше число:"))
        number2 = int(input("Введіть друге число:"))
        choice = input('''+
-
*
/''')
        
        if choice == "+":
            print(number1 + number2)
        elif choice == "-":
            print(number1 - number2)
        elif choice == "*":
            print(number1 * number2)
        elif choice == "/" and number2 != 0:
            print(number1 / number2)
        else:
            print("Некорректний вибір операції")
    
calc()

