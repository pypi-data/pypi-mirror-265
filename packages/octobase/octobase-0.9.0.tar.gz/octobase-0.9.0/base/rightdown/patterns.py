#!/opt/local/bin/python

import base

from base                 import rightdown
from base.regexp          import *
from base.rightdown.enums import *


###
## Line patterns
#


LINE_PATTERNS       = (
    (LINETYPE_HARD_BREAK,        '---\s*$'),
    (LINETYPE_SOFT_BREAK,        '\.\s?\.\s?\.\s*$'),
    (LINETYPE_BLANK,             '\.\s*$'),
    (LINETYPE_FENCE,             '```'),

    (LINETYPE_COMMENT_LINE,      '//'),
    (LINETYPE_COMMENT_LINE,      '/\*.*\*/\s*$'),    # must come before COMMENT_STARTs and _ENDs
    (LINETYPE_COMMENT_LINE,      '<!--.*-->\s*$'),   # must come before COMMENT_STARTs and _ENDs
    (LINETYPE_COMMENT_START,     '/\*'),
    (LINETYPE_COMMENT_START,     '<!--'),
    (LINETYPE_COMMENT_END,       '.*\*/\s*$'),
    (LINETYPE_COMMENT_END,       '.*-->\s*$'),

    (LINETYPE_HEADER,            '#'),
    (LINETYPE_QUOTE,             '>'),
    (LINETYPE_VALUE,             ':'),
    (LINETYPE_TABLE,             '.*\|.+\|'),
    (LINETYPE_LIST_BULLET,       '[-+\*]' + Group(Or('$', '\s+[^\s]'))),
    (LINETYPE_LIST_NUMBER,       '\d+\.' + Group(Or('$', '\s+[^\s]'))),
    (LINETYPE_LIST_ALPHA,        '[a-zA-Z]\.' + Group(Or('$', '\s+[^\s]'))),
    (LINETYPE_SLUG,              '[a-z0-9_]+$'),
    (LINETYPE_ATTRIBUTE,         '[a-z0-9_]+:'),
)

LINE_PATTERNS_NO_COMMENT  = [
    (x,y) for x,y in LINE_PATTERNS if not x in (LINETYPE_COMMENT_LINE, LINETYPE_COMMENT_START, LINETYPE_COMMENT_END)]


###
## Block patterns
#


ANYTOKEN            = Group('\w\w\w,')
ANYINDENT           = Group(Or(LINETYPE_INDENTED_CODE, LINETYPE_ALMOST_INDENTED))
FRAGBREAK           = Group(Or(LINETYPE_HARD_BREAK, BLOCKTYPE_FRAGMENT, '$'), GROUPTYPE_LOOK_AHEAD)
BLOCKSTART          = Group(Or('^', LINETYPE_EMPTY))
BLOCKBREAK          = Group(Or(LINETYPE_EMPTY, '$'), GROUPTYPE_LOOK_AHEAD)


# this matches against the entire block of metadata at the top of a fragment
METADATA_PATTERN    = LINETYPE_HARD_BREAK + Capture(
    Group(Or(
        LINETYPE_SLUG, LINETYPE_ATTRIBUTE, LINETYPE_VALUE, LINETYPE_INDENTED_CODE, LINETYPE_ALMOST_INDENTED
    )) + '*?'
) + LINETYPE_SOFT_BREAK


# these are used to break a document into the highest level blocks
FRAGMENT_PATTERNS   = (
    (BLOCKTYPE_COMMENT,     GROUPERMODE_SEARCH,   (
        LINETYPE_COMMENT_LINE
    )),
    (BLOCKTYPE_COMMENT,     GROUPERMODE_SEARCH,   (
        LINETYPE_COMMENT_START + ANYTOKEN + '*?' + LINETYPE_COMMENT_END
    )),
    (BLOCKTYPE_CODE,        GROUPERMODE_SEARCH,   (
        LINETYPE_FENCE + ANYTOKEN + '*?' + LINETYPE_FENCE
    )),
    (BLOCKTYPE_CODE,        GROUPERMODE_SEARCH,   (
        Group(LINETYPE_EMPTY, GROUPTYPE_LOOK_BEHIND) +
        LINETYPE_INDENTED_CODE +
        Group(Or(LINETYPE_INDENTED_CODE, LINETYPE_EMPTY)) + '*' +
        Group(Or(LINETYPE_EMPTY, LINETYPE_HARD_BREAK, BLOCKTYPE_FRAGMENT, '$'), GROUPTYPE_LOOK_AHEAD)
    )),
    (BLOCKTYPE_FRAGMENT,    GROUPERMODE_SEARCH,   (
        ANYTOKEN + '+?' + FRAGBREAK
    )),
)


# these are the patterns for the items inside the metadata block
FIELDLIST_PATTERNS  = (
    (BLOCKTYPE_FIELD,       GROUPERMODE_SEARCH,   (
        LINETYPE_ATTRIBUTE + ANYINDENT + '*'
    )),
    (BLOCKTYPE_MULTIFIELD,  GROUPERMODE_SEARCH,   (
        LINETYPE_SLUG + Group(LINETYPE_VALUE) + '*'
    )),
)


# these are the patterns for the types of blocks that make up the general flow of content
CONTENT_PATTERNS    = (
    (BLOCKTYPE_HEADING,     GROUPERMODE_SEARCH,   (
        LINETYPE_HEADER
    )),
    (BLOCKTYPE_SOFT_BREAK,  GROUPERMODE_SEARCH,   (
        Group(LINETYPE_SOFT_BREAK) + '+' + BLOCKBREAK
    )),
    (BLOCKTYPE_BLANK,       GROUPERMODE_SEARCH,   (
        Group(LINETYPE_BLANK) + '+' + BLOCKBREAK
    )),
    (BLOCKTYPE_QUOTE,       GROUPERMODE_SEARCH,   (
        LINETYPE_QUOTE + Group(ANYTOKEN) + '*?' + BLOCKBREAK
    )),
    (BLOCKTYPE_TABLE,       GROUPERMODE_SEARCH,   (
        Group(LINETYPE_TABLE) + '+' + BLOCKBREAK
    )),
    (BLOCKTYPE_LIST,        GROUPERMODE_SEARCH,   (
        Group(Or(
            LINETYPE_LIST_BULLET, LINETYPE_LIST_NUMBER, LINETYPE_LIST_ALPHA
        )) + Group(Or(
            LINETYPE_LIST_BULLET, LINETYPE_LIST_NUMBER, LINETYPE_LIST_ALPHA,
            LINETYPE_INDENTED_CODE, LINETYPE_ALMOST_INDENTED
        )) + '*' + BLOCKBREAK
    )),
    (BLOCKTYPE_FIELD,       GROUPERMODE_SEARCH,   (
        BLOCKSTART + Capture(
            LINETYPE_ATTRIBUTE + ANYINDENT + '*'
        ) + BLOCKBREAK
    )),
    (BLOCKTYPE_MULTIFIELD,  GROUPERMODE_SEARCH,   (
        BLOCKSTART + Capture(LINETYPE_SLUG + Group(LINETYPE_VALUE) + '+') + BLOCKBREAK
    )),
)


###
## Text patterns
#

## pattern building helpers

SPACE0              = Group(Or('^', r'[^\w]'))
SPACE1              = Group(Or(r'[^\w]', '$'))
NOTSPACE            = r'[^\s]'

LA_SPACE1           = Group(SPACE1, grouptype=GROUPTYPE_LOOK_AHEAD)
LB_NOTSPACE         = Group(NOTSPACE, grouptype=GROUPTYPE_LOOK_BEHIND)

TEXT_SUB_DECORATORS = {
    SUBMODE_ALL:      lambda x: Capture(x),
    SUBMODE_SOLO:     lambda x: SPACE0 + Capture(x) + SPACE1,
    SUBMODE_OPEN:     lambda x: SPACE0 + Capture(x),
    SUBMODE_CLOSE:    lambda x: Capture(x) + SPACE1,
    SUBMODE_NOTOPEN:  lambda x: NOTSPACE + Capture(x)

}


## simple text substitutions

HTML_TH             = '<sup><u>th</u></sup>'
HTML_ST             = '<sup><u>st</u></sup>'
HTML_ND             = '<sup><u>nd</u></sup>'
HTML_RD             = '<sup><u>rd</u></sup>'

SIMPLE_PATTERN_NBSP = (r'\\ ', CHAR_NO_BREAK_SPACE)

# tuples are:  (pattern, naked, text, html)
#   if html is missing, naked will be used
#   if text is missing, pattern will be used
TEXT_SUBSTITUTIONS  = {
    SUBMODE_ALL:    (
        SIMPLE_PATTERN_NBSP,
        ('\n',                  '\n',                   '\n',             '<br>'),
        (r'\.\.\.',             CHAR_ELLIPSIS,          '...'),
        ('<-->',                CHAR_BI_ARROW),
        ('-->',                 CHAR_RIGHT_ARROW),
        ('<--',                 CHAR_LEFT_ARROW),
        ('---',                 CHAR_EMDASH),
        ('--',                  CHAR_ENDASH),
        (r'\+/-',               CHAR_PLUS_MINUS),
        ('=/=',                 CHAR_NOT_EQUAL),
        ('~=',                  CHAR_ALMOST_EQUAL),
    ),
    SUBMODE_SOLO:   (
        ('1/2',                 CHAR_ONE_HALF),
        ('1/3',                 CHAR_ONE_THIRD),
        ('2/3',                 CHAR_TWO_THIRDS),
        ('1/4',                 CHAR_ONE_QUARTER),
        ('3/4',                 CHAR_THREE_QUARTERS),
        ('1/5',                 CHAR_ONE_FIFTH),
        ('2/5',                 CHAR_TWO_FIFTHS),
        ('3/5',                 CHAR_THREE_FIFTHS),
        ('4/5',                 CHAR_FOUR_FIFTHS),
        ('1/6',                 CHAR_ONE_SIXTH),
        ('5/6',                 CHAR_FIVE_SIXTHS),
        ('1/8',                 CHAR_ONE_EIGHTH),
        ('3/8',                 CHAR_THREE_EIGHTHS),
        ('5/8',                 CHAR_FIVE_EIGTHS),
        ('7/8',                 CHAR_SEVEN_EIGHTS),
        (r'\(c\)',              CHAR_COPYRIGHT,         '(c)'),           # xyzzy: revisit
        (r'\(tm\)',             CHAR_TRADEMARK,         '(tm)'),
        (r'\(r\)',              CHAR_REGISTERED,        '(r)'),
        ( '0' + Capture('st'),  HTML_ST),
    ),
    SUBMODE_OPEN:   (
        ("'",                   CHAR_LEFT_TICK),
        ('"',                   CHAR_LEFT_QUOTE),
    ),
    SUBMODE_CLOSE:  (
        ('11' + Capture('th'),  'th',                   'th',             HTML_TH),
        ('12' + Capture('th'),  'th',                   'th',             HTML_TH),
        ('13' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '0' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '1' + Capture('st'),  'st',                   'st',             HTML_ST),
        ( '2' + Capture('nd'),  'nd',                   'nd',             HTML_ND),
        ( '3' + Capture('rd'),  'rd',                   'rd',             HTML_RD),
        ( '4' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '5' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '6' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '7' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '8' + Capture('th'),  'th',                   'th',             HTML_TH),
        ( '9' + Capture('th'),  'th',                   'th',             HTML_TH),
    ),
    SUBMODE_NOTOPEN:  (
        ("'",           CHAR_RIGHT_TICK),
        ('"',           CHAR_RIGHT_QUOTE),
    ),
}

## these patterns identify range-based parts of text

IMAGE               = Capture('!?', name='image')
FLAGS               = Capture('.*?', name='flags')
TITLE               = Capture('.*?', name='text')
URL                 = Capture('.*?', name='url')
PROTOCOL            = Capture(Or('https?:/', 'mailto:'), name='protocol')

CODE_SNIP_PATTERN   = '`' + Capture('.*?', name='text') + '`'

HTMLATTR0           = '\\s*\\w+\\s*' + Optional('=' + '\\s*".*?"')
HTMLATTR1           = '\\s*\\w+\\s*' + Optional('=' + "\\s*'.*?'")
HTMLTAGOPEN         = '<\\w+' + Group(Or(HTMLATTR0, HTMLATTR1)) + '*\\s*/?>'
HTMLTAGCLOSE        = '</\\w+\s*>'
HTMLTAGCOMMENT      = '<!.*?>'


TEXTBLOCK_PATTERNS  = (
    (BLOCKTYPE_LINK,            IMAGE + r'\[\[' + FLAGS + r'\]\]\(' + URL + r'\)'),
    (BLOCKTYPE_LINK,            IMAGE + r'\['   + TITLE +   r'\]\(' + URL + r'\)'),
    (BLOCKTYPE_LINK,            IMAGE + r'\[\(' + URL   + r'\)\]'),
    (BLOCKTYPE_LINK,            PROTOCOL + URL + SPACE1),
    (SNIPTYPE_ICON,             r'\(\(' + Capture('\w+\s?' + Group('\w+')) + '\)\)'),
    (SNIPTYPE_TEMPLATE,         Capture(r'{%.*?%}', name='text')),
    (SNIPTYPE_TEMPLATE,         Capture(r'{{.*?}}', name='text')),
    (SNIPTYPE_COMMENT,          Capture(r'{#.*?#}', name='text')),
    (SNIPTYPE_HTML,             Capture(HTMLTAGOPEN, name='text')),
    (SNIPTYPE_HTML,             Capture(HTMLTAGCLOSE, name='text')),
    (SNIPTYPE_COMMENT,          Capture(HTMLTAGCOMMENT, name='text')),
    (BLOCKTYPE_SUBSCRIPT,       LB_NOTSPACE + '~' + r'\(' + Capture('.*?', name='text') + r'\)' + LA_SPACE1),
    (BLOCKTYPE_SUPERSCRIPT,     LB_NOTSPACE + '\\^' + r'\(' + Capture('.*?', name='text') + r'\)' + LA_SPACE1),
    (BLOCKTYPE_SUPERSCRIPT,     LB_NOTSPACE + '\\^' + Capture(r'.+?', name='text') + LA_SPACE1),
    # *DISABLED BY INTENTION*
    #   because mid-word strikethrough is more useful
    # (BLOCKTYPE_SUBSCRIPT,     NOTSPACE + '~' + Capture(r'\w+', name='sub') + SPACE),
)

## these patterns relate to the formatting symbols we see co-mingled with each other

comingle_char_gen   = rightdown.tokens.SpecialCharGen()
base.Enum.Define(('COMINGLE', 'CoMingles'), (
    {'name': 'Push Left',     'pattern': TEXT_SUB_DECORATORS[SUBMODE_SOLO](Or(r'^<-', r'<-$')), 'tag': comingle_char_gen()},
    {'name': 'Push Right',    'pattern': TEXT_SUB_DECORATORS[SUBMODE_SOLO](Or(r'^->', r'->$')), 'tag': comingle_char_gen()},
    {'name': 'Strike',        'pattern': TEXT_SUB_DECORATORS[SUBMODE_ALL]  ('~'),               'tag': comingle_char_gen()},
    {'name': 'Under Up',      'pattern': TEXT_SUB_DECORATORS[SUBMODE_OPEN] ('_'),               'tag': comingle_char_gen()},
    {'name': 'Under Down',    'pattern': TEXT_SUB_DECORATORS[SUBMODE_CLOSE]('_'),               'tag': comingle_char_gen()},
    {'name': 'Light Up',      'pattern': TEXT_SUB_DECORATORS[SUBMODE_OPEN] ('='),               'tag': comingle_char_gen()},
    {'name': 'Light Down',    'pattern': TEXT_SUB_DECORATORS[SUBMODE_CLOSE]('='),               'tag': comingle_char_gen()},
    {'name': 'Star 3 Up',     'pattern': TEXT_SUB_DECORATORS[SUBMODE_OPEN] (r'\*\*\*'),         'tag': comingle_char_gen()},
    {'name': 'Star 3 Down',   'pattern': TEXT_SUB_DECORATORS[SUBMODE_CLOSE](r'\*\*\*'),         'tag': comingle_char_gen()},
    {'name': 'Star 2 Up',     'pattern': TEXT_SUB_DECORATORS[SUBMODE_OPEN] (r'\*\*'),           'tag': comingle_char_gen()},
    {'name': 'Star 2 Down',   'pattern': TEXT_SUB_DECORATORS[SUBMODE_CLOSE](r'\*\*'),           'tag': comingle_char_gen()},
    {'name': 'Star 1 Up',     'pattern': TEXT_SUB_DECORATORS[SUBMODE_OPEN] (r'\*'),             'tag': comingle_char_gen()},
    {'name': 'Star 1 Down',   'pattern': TEXT_SUB_DECORATORS[SUBMODE_CLOSE](r'\*'),             'tag': comingle_char_gen()},
))
FIRST_SPECIAL_CHAR  = comingle_char_gen.AsInt()
