from ..interface import Contract, ContractNotRespected
from ..syntax import add_contract, W, contract, O, Literal


class String(Contract):
    
    def __init__(self, length=None, where=None):
        Contract.__init__(self, where)
        self.length = length
        assert length is None or isinstance(length, Contract)
        
    def check_contract(self, context, value): 
        if not isinstance(value, str):
            error = 'Expected a str, got %r.' % value.__class__.__name__
            raise ContractNotRespected(contract=self, error=error,
                                       value=value, context=context)
       
        if self.length is not None:
            self.length._check_contract(context, len(value))
            
    def __repr__(self):
        return 'String(%r)' % self.length
    
    def __str__(self):
        s = 'str'
        if self.length is not None:
            s += '[%s]' % self.length
        return s
            
    @staticmethod
    def parse_action(s, loc, tokens): 
        where = W(s, loc)
        length = tokens.get('length', None)
        return String(length, where=where)
 

string_contract = (Literal('str') | Literal('string')) + O('[' + contract('length') + ']') 

add_contract(string_contract.setParseAction(String.parse_action))