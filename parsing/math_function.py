import numpy as np

# x^3(21x^2-5.2)+3


class MathFunction:
    def __init__(self, exp):
        self._func_pipe = []
        self._operation_map = {"+": {"func": self.add, "precedence": 2, "associativity_right": False},
                               "-": {"func": self.sub, "precedence": 2, "associativity_right": False},
                               "*": {"func": self.times, "precedence": 3, "associativity_right": False},
                               "/": {"func": self.times, "precedence": 3, "associativity_right": False},
                               "^": {"func": self.power, "precedence": 4, "associativity_right": True},
                               "(": {"func": None, "precedence": 0, "associativity_right": False},
                               ")": {"func": None, "precedence": 0, "associativity_right": False}}

        self._polish_exp = []   # ["4", "3", "2", "+", "*"]
        self.operands_queue = []
        self.operations_stack = []
        self.exp = exp

        # INIT
        self.__to_polish_notation()
        print(self._polish_exp)

    def __call__(self, x):
        stack = []

        for c in self._polish_exp:
            if self.__is_operation(c):
                op2 = stack.pop()
                op1 = stack.pop()

                res = self._operation_map[c]["func"](float(op1), float(op2))
                stack.append(res)
            else:
                if self.__is_digit(c):
                    stack.append(c)
                else:
                    stack.append(x)
        return stack.pop()

    def __to_polish_notation(self):     # Shunting Yard Algorithm
        for c in self.exp:
            if self.__is_operation(c):
                if c == ")":
                    head = self.operations_stack.pop()

                    while head != "(":
                        self.operands_queue.append(head)
                        head = self.operations_stack.pop()

                elif c == "(":
                    self.operations_stack.append(c)

                elif self.__higher_precedence(self.__stack_head(), c):

                    while self.__higher_precedence(self.__stack_head(), c):
                        op = self.operations_stack.pop()
                        self.operands_queue.append(op)

                    self.operations_stack.append(c)

                else:
                    self.operations_stack.append(c)
            else:
                self.operands_queue.append(c)

        self.operations_stack.reverse()  # reverse bc pop operation stack and push to operands
        self._polish_exp = self.operands_queue + self.operations_stack

    def __stack_head(self):
        try:
            return self.operations_stack[-1]
        except IndexError:
            return None

    def __higher_precedence(self, stack_head, op):
        if stack_head is not None:
            return self._operation_map[stack_head]["precedence"] > self._operation_map[op]["precedence"]
        return False

    def __is_operation(self, char):
        return char in self._operation_map.keys()

    def __is_digit(self, char):
        try:
            float(char)
            return True
        except ValueError:
            return False

    def table(self, x_range: list):
        y_range = []
        x_range[1] += x_range[2]     # + step to get exact the defined range
        x_range = np.arange(*x_range)

        for x in x_range:
            y_range.append(self(x))

        return list(x_range), y_range

    @staticmethod
    def add(num1, num2):
        return num1 + num2

    @staticmethod
    def sub(num1, num2):
        return num1 - num2

    @staticmethod
    def times(num1, num2):
        return num1 * num2

    @staticmethod
    def divide(num1, num2):
        return num1 / num2

    @staticmethod
    def power(base, pot):
        return base ** pot


if __name__ == "__main__":
    exp = "0.1 * x ^ 4 - x ^ 2"   # = 9,6
    mf = MathFunction(exp.split(" "))

    # x^2 + 4

    print(mf(-4))
