def check_string(s):
    # Состояния для 010 (ищем подстроку)
    # 0: старт, 1: '0', 2: '01', 3: '010' (успех)
    a = 0 
    
    # Состояния для 101 (избегаем подстроку)
    # 0: старт, 1: '1', 2: '10', 3: '101' (провал/trap)
    b = 0
    
    found_010 = False

    for char in s:
        # Логика автомата А (ищем 010)
        if a < 3:
            if char == '0':
                a = 1 if a == 0 or a == 2 else 1
                if a == 2: # если были в '01' и пришел '0'
                    a = 3
                    found_010 = True
            elif char == '1':
                a = 2 if a == 1 else 0

        # Логика автомата B (избегаем 101)
        if char == '1':
            if b == 0: b = 1
            elif b == 1: b = 1
            elif b == 2: b = 3 # Ловушка! Нашли 101
        else: # char == '0'
            if b == 0: b = 0
            elif b == 1: b = 2
            elif b == 2: b = 0
            
        if b == 3: # Если попали в ловушку 101
            return False

    return found_010

# Тесты
test_strings = ["010", "00100", "0101", "111010", "0100011"]
for ts in test_strings:
    print(f"Строка {ts}: {'✅ Подходит' if check_string(ts) else '❌ Не подходит'}")