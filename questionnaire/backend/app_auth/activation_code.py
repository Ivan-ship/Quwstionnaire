import random

#Генерируем случайный код
def generate_activation_code(length = 6):
    return "".join(str(random.randint(0, 9)) for _ in range(length))


activation_code = generate_activation_code()
