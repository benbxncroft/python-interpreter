# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "EOF",
)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Error parsing input")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            operations = {
                "+": Token(PLUS, "+"),
                "-": Token(MINUS, "-"),
                "*": Token(MULTIPLY, "*"),
                "/": Token(DIVIDE, "/"),
            }

            if self.current_char in operations:
                token = operations[self.current_char]
                self.advance()
                return token

            self.error()

        return Token(EOF, None)

    def eat(self, *args):
        # compare current token type with given token(s)
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type in args:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.get_next_token()
        result = self.term()

        def f(x, value):
            return {
                PLUS: result + value,
                MINUS: result - value,
                MULTIPLY: result * value,
                DIVIDE: result / value,
            }[x]

        while self.current_token.type in (PLUS, MINUS, MULTIPLY, DIVIDE):
            token = self.current_token
            self.eat(token.type)
            result = f(token.type, self.term())

        return result


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
