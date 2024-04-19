from enum import Enum
from dataclasses import dataclass


class TokenTypes(Enum):
    INTEGER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    EOF = 6


@dataclass
class Token:
    token_type: TokenTypes
    value: str | int


class Interpreter:
    def __init__(self, user_input) -> None:
        self.user_input = user_input
        self.pos = 0
        self.current_token = None
        self.current_char = self.user_input[self.pos]

    def is_end_of_file(self) -> Token:
        if self.pos >= len(self.user_input):
            return Token(TokenTypes.EOF, None)

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

    def get_token(self) -> Token:
        # lexical analyser
        # get token for each character
        """
        possible characters that need to be tokenised:
        * whitespace (method to skip this)
        * integer (must account for multiple digits)
        * all operation characters (should all be same implementation)
        * end of file (know when to stop analysis)
        """

        token = self.is_end_of_file()

        self.current_char = self.user_input[self.pos]

        self.skip_whitespace()

        if self.current_char.isdigit():
            return self.integer()

        if self.current_char == "+":
            self.pos += 1
            return Token(TokenTypes.PLUS, self.current_char)

        if token:
            return token
        else:
            raise Exception("Error parsing input")

    def parse(self) -> None:
        """
        parses the tokenised string - the main entry point of this class

        should recognise current token and build up a sequence
        should then interpret what to do with that sequence

        every time a token is read, call a method to get the next token
        i.e. build the tokenised input up as it is interpreted
        """

        self.current_token = self.get_token()

        if self.current_token.token_type == TokenTypes.EOF:
            return

        result = 0
        if self.current_token.token_type == TokenTypes.INTEGER:
            result = self.current_token.value
            self.current_token = self.get_token()

        if self.current_token.token_type == TokenTypes.PLUS:
            self.current_token = self.get_token()
            value = self.current_token.value
            result = result + value

        return result


def main() -> None:
    # should take an input with string and run it through an interpreter

    """
    interpreter should do the following:

    * lexer that converts stream of input in to tokens
    * parser that parses those tokens in to a structure
    * interpreter that generates results from stream

    a token data structure is required

    * use a @dataclass
    * token has a type and a value
    """

    while True:
        user_input = input("> ")
        if not user_input:
            continue
        interpreter = Interpreter(user_input)
        output = interpreter.parse()
        print(output)


if __name__ == "__main__":
    main()
