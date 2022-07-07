from returns.result import Result, Failure, Success

def safe_div(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Failure("do not divide by zero!")
    return Success(a/b)

x = safe_div(10,0)

match x:
    case Success(a):
        print(a)
    case Failure(message):
        pass
