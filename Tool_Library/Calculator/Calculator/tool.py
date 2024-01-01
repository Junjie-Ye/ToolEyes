from operator import pow, truediv, mul, add, sub
import wolframalpha
import requests


def calculator(input_query: str):
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '^': pow
    }
    try:
        input_query = input_query.replace(' ', '')
        if input_query.isdigit():
            return float(input_query)
        for c in operators.keys():
            left, operator, right = input_query.partition(c)
            if operator in operators:
                return round(operators[operator](calculator(left), calculator(right)), 2)
    except:
        return "The input query is not a methematical expression."


def wolfram_alpha_calculator(input_query: str, api_key: str = ''):
    wolfram_client = wolframalpha.Client(api_key)
    res = wolfram_client.query(input_query)
    # assumption = next(res.pods).text
    answer = next(res.results).text
    try:
        return round(float(answer), 2)
    except:
        return "The input query is not for calculating."


def newton_calculator(operation: str, expression: str):
    operation = operation.lower()
    expression = expression.replace('+', '%2B')
    url = f'https://newton.now.sh/api/v2/{operation}/{expression}'

    response = requests.get(url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


if __name__ == '__main__':
    # print(calculator('4 * 6+2^ 5/ 3-1'))
    # print(wolfram_alpha_calculator('What is 2^3 +3 -(2-3)?'))
    # print(wolfram_alpha_calculator('Waht is two plus three minus thirteen?'))
    print(newton_calculator('log', '2|8'))
