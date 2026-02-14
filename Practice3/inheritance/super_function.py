class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        parent_sound = super().speak()
        return parent_sound + " but louder"