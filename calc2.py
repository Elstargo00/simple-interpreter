# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, OP, EMP, EOF = 'INTEGER', 'OP', ' ', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type 
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        # .., 99, '+', or None
        self.value = value
        
    def __str__(self):
        """String representation of the class instance.
        
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()
    
class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text 
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None 
        
    def error(self):
        raise Exception('Error parsing input')
    
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        
        This method is responsible for breaking a sentence
        appart into tokens. One token at a time.
        """
        text = self.text 
        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        
        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]
        
        # if the character is a digit then convert it to
        # interger, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        if current_char == '+' or current_char == '-':
            token = Token(OP, current_char)
            self.pos += 1
            return token
        
        if current_char == ' ':
            token = Token(EMP, current_char)
            self.pos += 1
            return token
        
        self.error()
        
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception error
        if self.current_token.type == token_type:
            pass
        else: 
            self.error()
            
    def expr(self):
        """expr -> INTEGER1[INTEGER2] PLUS INTEGER1[INTEGER2]"""
        # set current token to the first token taken from the input
        self.item = []
        next_token_available = True

        while next_token_available:
            self.current_token = self.get_next_token()
            if self.current_token.type == INTEGER:
                self.eat(INTEGER)
                self.item.append(self.current_token)
            elif self.current_token.type == OP:
                self.eat(OP)
                self.item.append(self.current_token)
            elif self.current_token.type == EMP:
                self.eat(EMP)
                self.item.append(self.current_token)
            else:
                next_token_available = False
        
        str_rep = ''
        for i in range(len(self.item)):
            str_rep += str(self.item[i].value)
        str_rep1 = str_rep.split('+')
        str_rep2 = str_rep.split('-')
        if len(str_rep1) > len(str_rep2):
            result = sum([int(item) for item in str_rep.split('+')])
        else: 
            pre_result = [int(item) for item in str_rep.split('-')]
            result = pre_result[0] - pre_result[1] 
        return result
    
def main():
    while True:
        try: 
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
        
if __name__ == '__main__':
    main()