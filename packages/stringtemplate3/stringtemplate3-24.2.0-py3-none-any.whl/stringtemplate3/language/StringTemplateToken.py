from builtins import str
from stringtemplate3 import antlr


class StringTemplateToken(antlr.CommonToken):

    def __init__(self, a_type=0, text='', args=None):
        """
        Track any args for anonymous templates like
          <tokens,rules:{t,r | <t> then <r>}>
        The lexer in action.g returns a single token ANONYMOUS_TEMPLATE,
        and so I need to have it parse args in the lexer and make them
        available for when I build the anonymous template."""
        super(StringTemplateToken, self).__init__(type=a_type, text=text)
        self._args = [] if args is None else args

    def __str__(self):
        return super(StringTemplateToken, self).__str__() + \
            '; args=' + str(self._args)

    __repr__ = __str__

    @property
    def args(self):
        return self._args

