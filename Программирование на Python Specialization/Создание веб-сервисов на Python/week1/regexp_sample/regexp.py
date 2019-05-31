def calculate(data, findall):
    matches = findall(r"([abc])([+-]?)=([abc])?([+-]?\d+)?")
    for a, sign, b, number in matches:
        right = data.get(b, 0) + int(number or 0)
        if sign == "-":
            data[a] -= right
        elif sign == "+":
            data[a] += right
        else:
            data[a] = right
    return data
