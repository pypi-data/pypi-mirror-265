class ExampleClass:
    def __init__(self):
        self.name = "ExampleClass"
        self.age = 20

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_name_and_age(self):
        return self.name, self.age

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_name_and_age(self, name, age):
        self.name = name
        self.age = age


if __name__ == "__main__":
    example = ExampleClass()
    print(example.get_name())
    print(example.get_age())
    print(example.get_name_and_age())
    example.set_name("NewName")
    example.set_age(25)
    print(example.get_name())
    print(example.get_age())
    example.set_name_and_age("NewName", 25)
    print(example.get_name_and_age())
