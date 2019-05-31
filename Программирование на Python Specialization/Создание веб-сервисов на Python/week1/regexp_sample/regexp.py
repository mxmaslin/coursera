def calculate(data, findall):
    matches = findall(r"([abc])([+-])?=([abc])?([+-]?\d+)?")  # Если придумать хорошую регулярку, будет просто
    for a, sign, b, number in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        right = data.get(b, 0) + int(number or 0)
        if sign == "-":
            data[a] -= right
        elif sign == "+":
            data[a] += right
        else:
            data[a] = right

    return data
