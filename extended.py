# Token types
#
# EOF (end-of-files) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        """String representation of the class instance.
        
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
        
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        
    def error(self):
        raise Exception('Invalid character')
        
    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
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
                
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
                
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
                
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
                
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
                
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
                
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
                
            self.error()
            
        return Token(EOF, None)

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    
class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
  """Represents a 'BEGIN ... END' block"""
  def __init__(self):
    self.children = []

class Assign(AST):
  def __init__(self, left, op, right)
  self.left = left
  self.token = self.op = op
  self.right = right

class Var(AST):
  """The Var node is constructed out of ID token."""
  def __init__(self, token):
    self.token = token
    self.value = token.value

class NoOp(AST):
  pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
            
    def error(self):
        raise Exception('Invalid syntax')
            
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
           self.current_token = self.lexer.get_next_token()
        else:
           self.error()

    def program(self):
      """program : compound_statement DOT"""
      node = self.compound_statement()
      self.eat(DOT)
      return node

    def compound_statement(self)
      """compound_statement: BEGIN statement_list END
      """
      self.eat(BEGIN)
      nodes = self.statement_list()
      self.eat(END)

      root = Compound()
      for node in nodes:
          root.children.append(node)

    def statement_list(self):
      """
      statement_list : statement
                     | statement SEMI statement_list
      """
      node = self.statement()

      results = [node]

      while self.current_token.type == SEMI:
        self.eat(SEMI)
        results.append(self.statement())

      if self.current_token.type == ID:
        self.error()

      return results

    def statement(self):
      """
      statement : compound_statement
                | assignment_statement
                | empty
      """
      if self.current_token.type == BEGIN:
        node = self.compound_statement()
      elif self.current_token.type == ID:
        node = self.compound_statement()
      else:
        node = self.empty()
      return node

    def assignment_statement(self):
      """
      assignment_statement : variable ASSIGN expr
      """
      left = self.variable()
      token = self.current_token
      self.eat(ASSIGN)
      right = self.expr()
      node = Assign(left, token, right)
      return node

    def variable(self):
      """
      variable : ID
      """
      node = Var(self.current_token)
      self.eat(ID)
      return node

    def empty(self):
      """An empty production"""
      return NoOp()
  
    def factor(self):
        """factor: PLUS factor
                 | MINUS factor
                 | INTEGER
                 | LPAREN expr RPAREN
                 | variable
        """
        token = self.current_token
        if token.type == PLUS:
          self.eat(PLUS)
          node = UnaryOp(token, self.factor())
            return node
          ...
        else:
          node = self.variable()
          return node
                
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
            
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
                
            node = BinOp(left=node, op=token, right=self.factor())
            
        return node
            
    def expr(self):
        """
        expr    : term ((PLUS | MINUS) term)*
        term    : factor ((MUL | DIV) factor)*
        factor  : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()
            
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            
            node = BinOp(left=node, op=token, right=self.term())
                    
        return node
        
    def parse(self):
        node = self.program()
      if self.current_token.type != EOF:
        self.error

      return node

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
        
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_Num(self, node):
        return node.value
        
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
        
def main():
    while True:
        try:
            try:
                text = raw_input('spi> ')
            except NameError: # Python3
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue
        
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
                
if __name__ == '__main__':
    main()
