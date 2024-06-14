
# list comprehension
num1 = [1, 2, 3, 4, 5]
double1 = [num * 2 for num in num1]
print(double1)

double2 = [num for num in num1 if num % 2 == 0]
double3 = [2, 4]
print(double2 == double3)  # True
print(double2 is double3)  # False (different memory reference)


# destructuring
x, y = (5, 11)
stud = {"rob": 23, "adam": 42}
stud2 = {**stud, "cyndy": 12}
print(stud2)

for z, w in stud.items():
    print(z, " ", w)

person1 = ("bob", 32, "mechanics")
name, _, prof = person1  # _ means ignore

head, *tail = [1, 2, 3, 4, 5]

print(head)  # 1
print(tail)  # [2, 3, 4, 5]

head, *tail = [1, 2, 3, 4, 5]

print(head)  # 1
print(tail)  # [2, 3, 4, 5]

head, *middle, tail = [1, 2, 3, 4, 5]

print(head)    # 1
print(middle)  # [2, 3, 4]
print(tail)    # 5


# Lambda
seq1 = [1, 3, 5, 7, 9]
double4 = [(lambda l1: l1 * 2)(seq) for seq in seq1]
double5 = list(map(lambda l1: l1 * 2, seq1))
print('lambda', double4, double5)

# dictionary comprehension
stud3 = {**stud2, "anthony": 0}
stud_mapping = {user+'-key': user for user in stud3}
print(stud_mapping)


# class composition
class Shelf:
    def __init__(self, *books):
        self.books = books

    def __str__(self):
        return f"Shelf have {len(self.books)} books"


class Book:
    def __init__(self, book_name):
        self.name = book_name

    def __str__(self):
        return f"Name of book = {self.name} "


book1 = Book('HP')
book2 = Book('CS')
bookshelf = Shelf(book1, book2)
print(bookshelf.books[1])  # as tuples
print(book1)


# typing
from typing import List


def avg_sequence(sequence: List) -> float:
    return sum(sequence) / len(sequence)


avg_sequence([2, 3, 4])

