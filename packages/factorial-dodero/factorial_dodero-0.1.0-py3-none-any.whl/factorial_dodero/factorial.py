def fact(n):
    """
    Returns the factorial of a number
    :param n: the number to find the factorial
    :return: factorial of a number
    """
    if n < 0:
        raise ValueError("Factorial cannot be negative")
    elif n==0 or n==1:
        return 1
    else:
        return n*fact(n-1)