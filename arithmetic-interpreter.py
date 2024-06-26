from enum import Enum
from dataclasses import dataclass


class TokenTypes(Enum):
    INTEGER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    EOF = 6
    LPAREN = 7
    RPAREN = 8


@dataclass
class Token:
    token_type: TokenTypes
    value: str | int


class Lexer:
    def __init__(self, user_input) -> None:
        self.user_input = user_input
        self.pos = 0
        self.current_char = self.user_input[self.pos]

    def move_forward(self) -> None:
        self.pos += 1
        if not self.pos >= len(self.user_input):
            self.current_char = self.user_input[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.move_forward()

    def integer(self) -> Token:
        integer_value = ""
        while self.current_char is not None and self.current_char.isdigit():
            integer_value += self.current_char
            self.move_forward()
        return Token(TokenTypes.INTEGER, int(integer_value))

    def is_end_of_file(self) -> Token:
        if self.pos >= len(self.user_input):
            return Token(TokenTypes.EOF, None)

    def get_token(self) -> Token:
        # lexical analyser
        # get token for each character

        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char.isdigit():
                return self.integer()

            operations = {
                "+": TokenTypes.PLUS,
                "-": TokenTypes.MINUS,
                "*": TokenTypes.MULTIPLY,
                "/": TokenTypes.DIVIDE,
                "(": TokenTypes.LPAREN,
                ")": TokenTypes.RPAREN,
            }

            if self.current_char in operations:
                token_value = self.current_char
                self.move_forward()
                return Token(operations[token_value], token_value)

        token = self.is_end_of_file()

        if token:
            return token
        else:
            raise Exception("Error parsing input: get_token()")


class Interpreter:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

    def eat(self, *args):
        if self.current_token.token_type in args:
            self.current_token = self.lexer.get_token()
        else:
            raise Exception("Error parsing input: eat()")

    def factor(self) -> str | int:
        token = self.current_token
        if token.token_type == TokenTypes.INTEGER:
            self.eat(TokenTypes.INTEGER)
            return token.value
        elif token.token_type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            result = self.expr()
            self.eat(TokenTypes.RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.current_token.token_type in (TokenTypes.MULTIPLY, TokenTypes.DIVIDE):
            token = self.current_token
            if token.token_type == TokenTypes.MULTIPLY:
                self.eat(TokenTypes.MULTIPLY)
                result = result * self.factor()
            elif token.token_type == TokenTypes.DIVIDE:
                self.eat(TokenTypes.DIVIDE)
                result = result / self.factor()

        return result

    def expr(self) -> int:
        result = self.term()

        if self.current_token.token_type == TokenTypes.EOF:
            return

        while self.current_token.token_type in (TokenTypes.PLUS, TokenTypes.MINUS):
            token = self.current_token
            if token.token_type == TokenTypes.PLUS:
                self.eat(TokenTypes.PLUS)
                result = result + self.term()
            elif token.token_type == TokenTypes.MINUS:
                self.eat(TokenTypes.MINUS)
                result = result - self.term()

        return result


def main() -> None:
    """
    interpreter should do the following:

    * lexer that converts stream of input in to tokens
    * parser that parses those tokens in to a structure
    * interpreter that generates results from stream

    the basic arithmetic would be based on the following grammar:

    expr: factor((MULTIPLY|DIVIDE|PLUS|MINUS)factor)*
    factor: INTEGER

    to account for levels of precedence and associativity with different operators:

    For each level of precedence define a non-terminal. The body of a production
    for the non-terminal should contain arithmetic operators from that level and
    non-terminals for the next higher level of precedence.

    Create an additional non-terminal factor for basic units of expression, in our case,
    integers. The general rule is that if you have N levels of precedence, you
    will need N + 1 non-terminals in total: one non-terminal for each level plus
    one non-terminal for basic units of expression.

    therefore:

    expr: term((PLUS|MINUS)term)*
    term: factor((MULTIPLY|DIVIDE)factor)*
    factor: INTEGER

    plus and minus have lower precedence than multiply and divide
    e.g. 7 + 5 * 2 executed as 7 + (5 * 2)

    to include parantheses the factor production can be modified like so:

    factor: INTEGER | LPAREN expr RPAREN
    it then becomes recursive to evaluate the expressions inside parantheses
    """

    while True:
        user_input = input("> ")
        if not user_input:
            continue
        lexer = Lexer(user_input)
        interpreter = Interpreter(lexer)
        output = interpreter.expr()
        print(output)


if __name__ == "__main__":
    main()
