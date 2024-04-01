#!/opt/local/bin/python

import base
from base import rightdown


class Token(base.Thing):
  ''' base class for everything that ends up in the parse tree '''

  tokentype         = None
  text              = None      # narrative content from the document
  text_after_inline = False     # does this token allow .text after inline parsing?
  inline            = False     # is this token inline content or block content?

  def __init__(self, **kwargs):
    base.utils.SetAttrs(self, **kwargs)

  def __str__(self):
    return self.text or ''

  @property
  def debug(self):
    ''' optionally return a string of text for debugging purposes '''
    return self.text and self.text.lstrip().split('\n', 1)[0].rstrip()

  @property
  def debug_sep(self):
    ''' separator character for debug output '''
    if self.empty:
      return '-'
    return ':'

  @property
  def empty(self):
    return not self.text

  def PrintOpen(self, printer, first, last):
    ''' return an Imprint or list of Imprints for this token's open text '''

  def PrintClose(self, printer, first, last):
    ''' return an Imprint or list of Imprints for this token's close text '''

  def Validate(self):
    ''' test our structure for flaws; raise on finding any '''
    if not any(self.tokentype in x for x in (rightdown.enums.LineTypes, rightdown.enums.BlockTypes, rightdown.enums.SnipTypes)):
      raise rightdown.errors.BadTokenType(self.tokentype)
    if self.text and not self.text_after_inline:
      raise rightdown.errors.LingeringText(self, self.debug)


###
## Lines and Snips are only ever leaves of the tree
#


class Line(Token):
  ''' an unparsed line of input '''

  original          = None      # str
  trimmed           = None      # str, with whitespace cleaned up
  mergable          = None      # trimmed, but with a \n at the end if a force-break has been requested
  metadata          = None      # dict
  leading_space     = 0

  def __str__(self):
    s               = self.original or ''
    maxwidth        = rightdown.printers.DebugPrinter.truncate_width
    if len(s) > maxwidth:
      s             = s[:maxwidth-1] + '…'
    return s

  @property
  def debug(self):
    return self.original

  @property
  def empty(self):
    return not self.trimmed



class Snip(Token):
  ''' a fully-parsed snip of inert text '''

  text_after_inline = True
  inline            = True

  def __init__(self, tokentype, **kwargs):
    self.tokentype  = tokentype
    base.utils.SetAttrs(self, **kwargs)

  def ProcessText(self, parser, parenttext=None):
    return

  def ToString(self, printer):
    # this is called by text blocks to make a complete string of our contents

    if self.tokentype == rightdown.enums.SNIPTYPE_COMMENT and not printer.pass_comments:
      return ''
    if self.tokentype == rightdown.enums.SNIPTYPE_HTML and not printer.pass_html:
      return ''
    if self.tokentype == rightdown.enums.SNIPTYPE_TEMPLATE and not printer.pass_templates:
      return ''

    if self.tokentype == rightdown.enums.SNIPTYPE_CODE:
      return self.ToCodeString(printer)

    return self.text

  def PrintOpen(self, printer, first, last):
    # the only sniptype this is called on is plain snips, because they are the only snips
    # that don't live under a text block, and text always mutes through the end of itself
    return Imprint(rightdown.enums.IMPRINT_NARRATIVE, self.text, inline=self.inline)

  def ToCodeString(self, printer):
    results         = ''
    if printer.markup:
      results       += '<code>'
    if printer.formatting:
      results       += '`'
    results         += self.text
    if printer.formatting:
      results       += '`'
    if printer.markup:
      results       += '</code>'
    return results

  def Validate(self):
    super().Validate()
    if self.text:
      if SpecialCharGen.HasAnySpecialChars(self.text):
        raise rightdown.errors.SnipSubbedChars(self.text)


###
## Block is the structural, branch-nodes of the token tree
#


class Block(Token):
  ''' branch nodes in the token tree '''

  children          = None      # the "parse tree" is here
  metadata          = None      # structured data we found while parsing

  @property
  def empty(self):
    return not self.children and not self.text

  ###
  ## tree mechanics
  #

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children   = self.children or []
    self.metadata   = self.metadata or {}
    self.text       = self.text     or None

  def __iter__(self):
    ''' serializes the token tree '''
    yield self
    for thing in self.children:
      if isinstance(thing, Block):
        for subthing in thing:
          yield subthing
      else:
        yield thing

  def Walk(self, fxn0, fxn1=None, depth=0, first=None, last=None):
    ''' calls fxn(token, depth) for each token in the tree in serial order.
        fxn0 is called before descending into a token's children, fxn1 after.
        the return value of each fxn is accumulated into a list, which is returned
    '''
    if not fxn0 and not fxn1:
      return

    results         = []

    if fxn0:
      self._UpdateWalkResults(results, fxn0(self, depth, first, last))

    thinglist       = self.children or []
    for i in range(len(thinglist)):
      thing         = thinglist[i]
      ifirst        = i == 0
      ilast         = i == len(thinglist)-1
      if isinstance(thing, Block):
        self._UpdateWalkResults(results, thing.Walk(fxn0, fxn1, depth+1, ifirst, ilast))
      else:
        if fxn0:
          self._UpdateWalkResults(results, fxn0(thing, depth+1, ifirst, ilast))
        if fxn1:
          self._UpdateWalkResults(results, fxn1(thing, depth+1, ifirst, ilast))

    if fxn1:
      self._UpdateWalkResults(results, fxn1(self, depth, first, last))

    return results

  def _UpdateWalkResults(self, results, newresults):
    if isinstance(newresults, list) or isinstance(newresults, tuple):
      results.extend(newresults)
    elif newresults is not None:
      results.append(newresults)

  def All(self, tokentype):
    ''' returns all the tokens in the tree that match the tokentype or tokentypes given '''
    if not tokentype:
      return list(self)
    if isinstance(tokentype, str):
      tokentypes    = set([tokentype])
    else:
      tokentypes    = set(tokentype)
    return [x for x in self if x.tokentype in tokentypes]

  ###
  ## parsing
  #

  digested          = False     # has DigestLines been called?
  processed         = False     # has ProcessText been called?

  def DigestLines(self, parser):
    ''' during early stage parsing, our children are Lines.  when this method is done, our children should be
        only Blocks, but not yet Text blocks.  any text we hold should be loaded into self.text instead
    '''
    if self.digested:
      raise rightdown.errors.DoubleDigest(self)
    self.digested   = True
    for child in self.children:
      if isinstance(child, Block) and not child.digested:
        child.DigestLines(parser)
      if hasattr(child, 'metadata') and child.metadata:
        self.metadata.update(child.metadata)

  def ProcessText(self, parser, parenttext=None):
    ''' if we have a self.text, make a Text block and prepend it to our children '''
    if self.processed:
      raise rightdown.errors.DoubleProcess(self)
    self.processed  = True

    if self.text:
      unless        = parenttext and parenttext.subdict
      cleantext     = SpecialCharGen.WipeSpecialChars(self.text, parser.barf_char, parser._TriggerBarf, unless)
      textblock     = parser.textmaker(cleantext, parenttext)
      self.children = [textblock] + self.children
      self.text     = None

    textblock       = parenttext
    for child in self.children:
      if isinstance(child, rightdown.blocks.Text):
        textblock   = child
      if isinstance(child, Block) and not child.processed:
        child.ProcessText(parser, parenttext=textblock)

  def Validate(self):
    ''' verify our final child list makes sense '''
    super().Validate()
    for child in self.children:
      # no longer should have any lines in the parse tree
      if child.tokentype in rightdown.enums.LineTypes:
        raise rightdown.errors.InvalidChild(child)
      child.Validate()


class VerbatimBlock(Block):
  ''' shared implementation for block classes that just verbatim quote the lines they're given '''

  indent            = 0
  fence             = False
  sniptype          = None

  def DigestLines(self, parser):
    lines           = [x for x in list(self) if isinstance(x, Line)]
    self.children   = []
    if not lines:
      super().DigestLines(parser)
      return
    if len(lines) >= 2:
      if lines[0].tokentype == rightdown.enums.LINETYPE_FENCE and lines[-1].tokentype == rightdown.enums.LINETYPE_FENCE:
        self.fence  = True
        lines       = lines[1:-1]
    if lines:
      self.indent   = min(x.leading_space for x in lines)
    self.text       = '\n'.join(x.original[self.indent:].rstrip() for x in lines)
    super().DigestLines(parser)

  def ProcessText(self, parser, parenttext=None):
    if self.text:
      self.children = [Snip(self.sniptype, text=self.text)]
      self.text     = None
    super().ProcessText(parser, parenttext=parenttext)


###
## a helper for making token patterns and inline tokens
#


class SpecialCharGen(base.utils.Counter):
  ''' for inline tokenizing, tokens we substitute into strings need to be something we can differentiate
      from the original string.  to this end, we generate single-character strings, drawn from the unicode
      range reserved for "private use"

      this is used in two forms:  first, patterns.py defines the 'co-mingles' which use symbols from our
      range.  second, each Text block has an instance of this that's used to populate keys for its
      substitution dictionary
  '''

  UNICODE_USER_MIN  = 0xE000
  UNICODE_USER_MAX  = 0xF8FF

  def __init__(self, start=UNICODE_USER_MIN):
    super().__init__(start=start)

  def __call__(self):
    ''' returns the next special char in order '''
    x               = super().__call__()
    if x > self.UNICODE_USER_MAX:
      # if this error is hit, it means we've exhausted all 6400 characters in the two-byte unicode
      # private use range.  we might consider upgrading to a 3-byte range (U+F0000..U+FFFFF), but
      # we might ask instead what we're doing that's so inefficient we need so many tags at once?
      raise rightdown.errors.UnicodeRangeOverflow
    return chr(x)

  def AsInt(self):
    x               = super().__call__()
    if x > self.UNICODE_USER_MAX:
      raise rightdown.errors.UnicodeRangeOverflow
    return x

  @classmethod
  def HasAnySpecialChars(klass, s):
    return s and any(c >= chr(klass.UNICODE_USER_MIN) and c <= chr(klass.UNICODE_USER_MAX) for c in s)

  @classmethod
  def WipeSpecialChars(klass, s, replacer, trigger, unless=None):
    def Fix(c):
      if c >= chr(klass.UNICODE_USER_MIN) and c <= chr(klass.UNICODE_USER_MAX):
        if not unless or c not in unless:
          trigger()
          return replacer
      return c
    results         = ''.join(Fix(c) for c in s)
    return results



###
## also not a token, but what tokens serialize to during printing
#


class Imprint(base.Thing):
  ''' printing means serializing a token tree into a list of Imprints '''

  def __init__(self, imprinttype, text=None, inline=False, depth=0):
    self.imprinttype  = imprinttype
    self.text         = text
    self.inline       = inline
    self.depth        = depth

  def __str__(self):
    return self.ConsoleStr()

  @property
  def debug(self):
    typename        = self.imprinttype and self.imprinttype.name or base.utils.ClassName(self)
    text            = ''
    if self.text:
      inline        = (self.inline and rightdown.enums.CHAR_BI_ARROW or ' ') + ' '
      text          = inline + self.ConsoleStr()
    if text:
      return base.utils.PadString(typename + ':', rightdown.printers.DebugPrinter.token_width) + text
    return typename

  def ConsoleStr(self):
    s               = self.text or ''
    cut             = s.strip().split('\n')[0].strip()
    maxwidth        = rightdown.printers.DebugPrinter.truncate_width
    if cut != s.strip():
      s             = cut[:maxwidth-1] + '…'
    elif len(s) > maxwidth:
      s             = s[:maxwidth-1] + '…'
    return s and ("'" + s + "'") or ''
