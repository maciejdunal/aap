# Napisz klasę, która będzie implementować generator kolejnych n potęg liczby a.
# Użyj metod magicznych __iter__() i __next__(). Liczby n i a powinny być
# parametrami wejściowymi generatora.

class Generator:
    def __init__(self, base, exponent_count):
        self.base = base
        self.exponent_count = exponent_count
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.exponent_count:
            result = self.base ** self.current
            self.current += 1
            return result
        raise StopIteration

# Przykład użycia:
power_gen = Generator(2, 5)
for power in power_gen:
    print(power)

