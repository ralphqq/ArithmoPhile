import random

#some global constants
EASY = 0
MEDIUM = 1
HARD = 2

#operations
ALL = 0b1111
PLUS = 0b1000
MINUS = 0b0100
TIMES = 0b0010
DIVIDE = 0b0001


class Question(object):
    """This defines the attributes of arithmetic questions asked in the app."""

    def __init__(self, difficulty=EASY, operations=PLUS|MINUS):
        """Initializes the question object"""
        self.difficulty = difficulty
        self.operations = operations
    
    def GetQuestion(self):
        """Generates the operation and operands"""
        random.seed()
        signs = {PLUS: '+', MINUS: '-', TIMES: chr(215), DIVIDE: chr(247)}
        
        ops_a = random.choice(
            filter(lambda c:c!=0,
                   [self.operations & p for p in signs.keys() ])
        )
        
        x = y = ans = 0
        
        if ops_a == PLUS or ops_a == MINUS:
            interval = {EASY:(1, 10), MEDIUM:(10, 1000), HARD:(100, 10000)}
            x = random.randint(*interval[self.difficulty])
            y = random.randint(*interval[self.difficulty])
            
            if ops_a == PLUS:
                ans = x + y
            elif ops_a == MINUS:
            
                if x < y:
                    x, y = y, x
                
                ans = x - y
        else:
            
            if ops_a == TIMES:
                interval = {EASY:(1, 10), MEDIUM:(10, 100), HARD:(100, 1000)}
                x = random.randint(*interval[self.difficulty])
                y = random.randint(*interval[self.difficulty])
                ans = x * y
            elif ops_a == DIVIDE:
                interval = {EASY:(1, 10), MEDIUM:(10, 50), HARD:(100, 500)}
                x = random.randint(*interval[self.difficulty])
                y = random.randint(*interval[self.difficulty])
                x, y, ans = x * y, x, y
        
        return x, y, ans, signs[ops_a]
