def add(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError('Both parameters must be numbers')
    return a + b

def subtract(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError('Both parameters must be numbers')
    return a - b

def multiply(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError('Both parameters must be numbers')
    return a * b

def divide(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError('Both parameters must be numbers')
    if b == 0:
        raise ValueError('Division by zero is not allowed')
    return a / b

def gcd(numbers):
    if not isinstance(numbers, list) or len(numbers) == 0:
        raise ValueError('Input must be a non-empty list')
    for num in numbers:
        if not isinstance(num, int) or num != int(num):
            raise ValueError('All elements of the list must be integers')

    def find_gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    result = numbers[0]
    for num in numbers[1:]:
        result = find_gcd(result, num)
        a = abs(result)
        b = abs(num)
        while b != 0:
            temp = b
            b = a % b
            a = temp
        result = a
        if result == 1:
            return 1
    return result

def decimal_to_percent(decimal):
    if not isinstance(decimal, (int, float)):
        raise ValueError('Input must be a number')
    return decimal * 100

def calculate_percentage(part, whole):
    if not isinstance(part, (int, float)) or not isinstance(whole, (int, float)):
        raise ValueError('Both parameters must be numbers')
    return (part / whole) * 100

def round_up(number):
    if not isinstance(number, (int, float)):
        raise ValueError('Input must be a number')
    return int(number + 0.5)

def bmi(weight, height):
    if not isinstance(weight, (int, float)) or not isinstance(height, (int, float)):
        raise ValueError('Both weight and height must be numbers')
    height_in_meters = height / 100
    return weight / (height_in_meters * height_in_meters)

def rounded_bmi(weight, height):
    if not isinstance(weight, (int, float)) or not isinstance(height, (int, float)):
        raise ValueError('Both weight and height must be numbers')
    height_in_meters = height / 100
    bmi_value = weight / (height_in_meters * height_in_meters)
    return round_up(bmi_value)