class MyClass:
    f"This is an f-string {1+1}"
    pass

print(f"MyClass.__doc__ is: {MyClass.__doc__}")

class MyClass2:
    "{escaped_instruction}"
    pass
print(f"MyClass2.__doc__ is: {MyClass2.__doc__}")
