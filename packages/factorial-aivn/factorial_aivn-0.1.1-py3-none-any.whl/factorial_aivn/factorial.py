def fact(n):
    """
    Tính giai thừa của một số nguyên dương n.

    Tham số:
    - n: Số nguyên dương.

    Trả về:
    - Giai thừa của n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result