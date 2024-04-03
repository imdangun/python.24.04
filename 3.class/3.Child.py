class Parent:
    def sing(self):
        print('la la.')

class Child(Parent):
    pass


boy = Child()
boy.sing()