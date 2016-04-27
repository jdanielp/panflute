# ---------------------------
# Imports
# ---------------------------
from collections import OrderedDict


# ---------------------------
# Special Root Class
# ---------------------------

class Doc(object):
    # We don't have slots, so you can e.g. add backmatter as an element
    # (sort of like a global variable)

    def __init__(self, metadata, items, format):
        assert type(metadata) == OrderedDict, type(metadata)
        self.metadata = metadata
        self.items = items
        self.format = format  # Output format

    def get_metadata(self, request, default):
        """Easy requests to nested metadata with default values

        Examples:
        >>> show_frame = doc.get_metadata('format.show-frame', False)
        >>> stata_path = doc.get_metadata('stata.path', default_path())
        """

        keys = request.split('.')
        meta = self.metadata
        for key in keys:
            if key not in meta:
                return default
            else:
                meta = meta[key]
        return meta


# ---------------------------
# Metaclasses
# ---------------------------

class Element(object):
    pass


class Inline(Element):
    pass


class Block(Element):
    pass


# ---------------------------
# Classes - Null
# ---------------------------

class Null(Block):
    """Nothing

     Block Null()"""

    __slots__ = []

    def encode_content(self):
        return []


class Space(Inline):
    """Inter-word space

     Inline Space()"""

    __slots__ = []

    def __repr__(self):
        return 'Space'

    def encode_content(self):
        return []


class HorizontalRule(Block):
    """Horizontal rule

     Block HorizontalRule()"""

    __slots__ = []

    def encode_content(self):
        return []


class SoftBreak(Inline):
    """Soft line break

     Inline SoftBreak()"""

    __slots__ = []

    def encode_content(self):
        return []


class LineBreak(Inline):
    """Hard line break

     Inline LineBreak()"""

    __slots__ = []

    def encode_content(self):
        return []


# ---------------------------
# Classes - Simple Containers
# ---------------------------

class Plain(Block):
    """Plain text, not a paragraph

     Block Plain(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Plain({})'.format(','.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class Para(Block):
    """Paragraph

     Block Para(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Para({})'.format(' '.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class BlockQuote(Block):
    """Block quote (list of blocks)

     Block BlockQuote(items=[Block])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=True)

    def encode_content(self):
        return encode_items(self)


class Emph(Inline):
    """Emphasized text (list of inlines)

     Inline Emph(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Emph({})'.format(' '.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class Strong(Inline):
    """Strongly emphasized text (list of inlines)

     Inline Strong(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Strong({})'.format(' '.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class Strikeout(Inline):
    """Strikeout text (list of inlines)

     Inline Strikeout(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Strikeout({})'.format(' '.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class Superscript(Inline):
    """Superscripted text (list of inlines)

     Inline Superscript(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def encode_content(self):
        return encode_items(self)


class Subscript(Inline):
    """Subscripted text (list of inlines)

     Inline Subscript(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def encode_content(self):
        return encode_items(self)


class SmallCaps(Inline):
    """Small caps text (list of inlines)

     Inline SmallCaps(items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def encode_content(self):
        return encode_items(self)


class Note(Inline):
    """Footnote or endnote

     Inline Note(items=[Block])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=True)

    def encode_content(self):
        return encode_items(self)


# ---------------------------
# Classes - Complex Containers
# ---------------------------

class Header(Block):
    """Header - level (integer) and text (inlines)

     Block Header(level=Int ica=Attr items=[Inline])"""

    __slots__ = ['level', 'items', 'identifier', 'classes', 'attributes']

    def __init__(self, *args, level=1, identifier='', classes=None,
                 attributes=None):
        self.level = validate(level, group=(1, 2, 3, 4, 5, 6))
        init_ica(self, identifier, classes, attributes)
        self.items = init_items(type(self), args, has_blocks=False)

    def encode_content(self):
        ica = encode_ica(self)
        items = encode_items(self)
        return [self.level, ica, items]


class Div(Block):
    """Generic block container with attributes

     Block Div(ica=Attr items=[Block])"""

    __slots__ = ['items', 'identifier', 'classes', 'attributes']

    def __init__(self, *args, identifier='', classes=None, attributes=None):
        init_ica(self, identifier, classes, attributes)
        self.items = init_items(type(self), args, has_blocks=True)

    def encode_content(self):
        ica = encode_ica(self)
        items = encode_items(self)
        return [ica, items]


class Span(Inline):
    """Generic inline container with attributes

     Inline Span(ica=Attr items=[Inline])"""

    __slots__ = ['items', 'identifier', 'classes', 'attributes']

    def __init__(self, *args, identifier='', classes=None, attributes=None):
        init_ica(self, identifier, classes, attributes)
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        _id = 'id={}'.format(self.identifier) if self.identifier else ''
        _cl = 'classes={}'.format(repr(self.classes)) if self.classes else ''
        _at = 'classes={}'.format(repr(self.attributes)) if self.attributes else ''
        ica = ''.join(';'+ x for x in [_id, _cl, _at] if x)
        return 'Span({}{})'.format(' '.join(repr(x) for x in self.items), ica)

    def encode_content(self):
        ica = encode_ica(self)
        items = encode_items(self)
        return [ica, items]


class Quoted(Inline):
    """Quoted text (list of inlines)

     Inline Quoted(quote_type=QuoteType items=[Inline])"""

    __slots__ = ['quote_type', 'items']

    def __init__(self, *args, quote_type='DoubleQuote'):
        self.quote_type = validate(quote_type, group=QUOTE_TYPES)
        self.items = init_items(type(self), args, has_blocks=False)

    def encode_content(self):
        quote_type = encode_dict(self.quote_type, [])
        items = encode_items(self)
        return [quote_type, items]


class Cite(Inline):
    """Cite (list of inlines)

     Inline Cite(citations=[Citation] items=[Inline])"""

    __slots__ = ['items', 'citations']

    def __init__(self, *args, citations):
        self.citations = [Citation(**dict(c)) for c in citations]
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'Cite(...)'

    def encode_content(self):
        citations = [x.encode_content() for x in self.citations]
        items = encode_items(self)
        return [citations, items]


class Citation(Element):
    __slots__ = ['citationHash', 'citationId', 'citationMode',
                 'citationNoteNum', 'citationPrefix', 'citationSuffix']

    def __init__(self, citationHash, citationId, citationMode,
                 citationNoteNum, citationPrefix, citationSuffix):
        self.citationHash = citationHash  # ??
        self.citationId = citationId  # the bibtex keyword
        self.citationMode = validate(citationMode, group=CITATION_MODE)
        self.citationNoteNum = citationNoteNum  # ??
        self.citationPrefix = init_items(citationPrefix, has_blocks=False)
        self.citationSuffix = init_items(citationSuffix, has_blocks=False)

    def encode_content(self):
        content = []
        content.append(['citationSuffix',
                       [to_json(x) for x in self.citationSuffix]])
        content.append(['citationNoteNum', self.citationNoteNum])
        content.append(['citationMode', encode_dict(self.citationMode, [])])
        content.append(['citationPrefix',
                       [to_json(x) for x in self.citationPrefix]])
        content.append(['citationId', self.citationId])
        content.append(['citationHash', self.citationHash])
        return OrderedDict(content)


class Link(Inline):
    """Hyperlink: alt text (list of inlines), target

     Inline Link(ica=Attr items=[Inline] [url=String title=String])"""

    __slots__ = ['items', 'url', 'title', 'identifier', 'classes',
                 'attributes']

    def __init__(self, *args, url, title, identifier='', classes=None,
                 attributes=None):
        self.items = init_items(type(self), args, has_blocks=False)
        init_ut(self, url, title)
        init_ica(self, identifier, classes, attributes)

    def encode_content(self):
        ica = encode_ica(self)
        items = encode_items(self)
        ut = [self.url, self.title]
        content = [ica, items, ut]
        return content


class Image(Inline):
    """Image: alt text (list of inlines), target

     Inline Image(ica=Attr items=[Inline] ut=Target)"""

    __slots__ = ['items', 'url', 'title', 'identifier', 'classes',
                 'attributes']

    def __init__(self, *args, url, title, identifier='', classes=None,
                 attributes=None):
        self.items = init_items(type(self), args, has_blocks=False)
        init_ut(self, url, title)
        init_ica(self, identifier, classes, attributes)

    def encode_content(self):
        ica = encode_ica(self)
        items = encode_items(self)
        ut = [self.url, self.title]
        return [ica, items, ut]


# ---------------------------
# Classes - Text
# ---------------------------

class Str(Inline):
    """Text (string)

     Inline Str(text=String)"""

    __slots__ = ['text']

    def __init__(self, text):
        self.text = validate(text, instance=str)

    def __repr__(self):
        return 'Str({})'.format(self.text)

    def encode_content(self):
        return self.text


class CodeBlock(Block):
    """Code block (literal) with attributes

     Block CodeBlock(ica=Attr text=String)"""

    __slots__ = ['text', 'identifier', 'classes', 'attributes']

    def __init__(self, text, identifier='', classes=None, attributes=None):
        self.text = validate(text, instance=str)
        init_ica(self, identifier, classes, attributes)

    def encode_content(self):
        return [encode_ica(self), self.text]


class RawBlock(Block):
    """Raw block

     Block RawBlock(format=Format text=String)"""

    __slots__ = ['text', 'format']

    def __init__(self, text, format):
        self.text = validate(text, instance=str)
        self.format = validate(format, group=RAW_FORMATS)

    def encode_content(self):
        return [self.format, self.text]


class Code(Inline):
    """Inline code (literal)

     Inline Code(ica=Attr text=String)"""

    __slots__ = ['text', 'identifier', 'classes', 'attributes']

    def __init__(self, text, identifier='', classes=None, attributes=None):
        self.text = validate(text, instance=str)
        init_ica(self, identifier, classes, attributes)

    def encode_content(self):
        ica = encode_ica(self)
        return [ica, self.text]


class Math(Inline):
    """TeX math (literal)

     Inline Math(text=String format=MathType)"""

    __slots__ = ['format', 'text']

    def __init__(self, text, format):
        self.text = validate(text, instance=str)
        self.format = validate(format, group=MATH_FORMATS)

    def encode_content(self):
        format = encode_dict(self.format, [])
        return [format, self.text]


class RawInline(Inline):
    """Raw inline

     Inline RawInline(format=Format text=String)"""

    __slots__ = ['text', 'format']

    def __init__(self, text, format):
        self.text = validate(text, instance=str)
        self.format = validate(format, group=RAW_FORMATS)

    def encode_content(self):
        return [self.format, self.text]


# ---------------------------
# Classes - Misc
# ---------------------------

class BulletList(Block):
    """Bullet list (list of items, each a list of blocks)

     Block BulletList(items=[[Block]])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=True, depth=2)

    def encode_content(self):
        return encode_items(self)


class OrderedList(Block):
    """Ordered list (attributes and a list of items, each a list of blocks)

     Block OrderedList(ssd=ListAttributes items=[[Block]])"""

    __slots__ = ['items', 'start', 'style', 'delimiter']

    def __init__(self, *args, start=1, style='Decimal', delimiter='Period'):
        self.items = init_items(type(self), args, has_blocks=True, depth=2)
        init_ssd(self, start, style, delimiter)

    def encode_content(self):
        ssd = [self.start, encode_dict(self.style, []),
               encode_dict(self.delimiter, [])]
        items = encode_items(self)
        return [ssd, items]


class DefinitionList(Block):
    """Definition list Each list item is a pair consisting of a term
    (a list of inlines) and one or more definitions (each a list of blocks)

     Block DefinitionList(items=[([Inline],[[Block]])])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = [(init_items(k, has_blocks=False),
                       init_items(v, has_blocks=True, depth=2))
                      for k, v in args]

    def encode_content(self):
        return encode_items(self)


class Table(Block):
    """Table, with caption, column alignments (required), relative column
    widths (0 = default), column headers (each a list of blocks),
    and rows (each a list of lists of blocks)

     Block Table(caption=[Inline] alignment=[Alignment] width=[Double]
     header=[[Block]] items=[[[Block]]])"""

    __slots__ = ['items', 'header', 'caption', 'alignment', 'width', 'rows',
                 'cols']

    def __init__(self, *args, header=None, caption=None, alignment=None,
                 width=None):
        self.items = init_items(type(self), args, has_blocks=True, depth=3)
        self.rows = len(self.items)
        self.cols = len(self.items[0])

        self.header = init_items(header, has_blocks=True, depth=2)
        assert len(header) == self.cols

        self.caption = init_items(caption, has_blocks=False)

        self.alignment = ['AlignDefault'] * len(self.items[0]) \
            if alignment is None else alignment
        assert all(item in TABLE_ALIGNMENT for item in alignment)

        self.width = [0.0] * len(self.items[0]) if width is None else width
        assert all(item >= 0 for item in width)

    def encode_content(self):
        caption = [to_json(x) for x in self.caption]
        alignment = [encode_dict(x, []) for x in self.alignment]
        header = [[to_json(x) for x in cell] for cell in self.header]
        items = encode_items(self)
        content = [caption, alignment, self.width, header, items]
        return content

        return OrderedDict((k, metawalk(v)) for k, v in self.items.items())


def metawalk(e):
    t = type(e)
    assert t in (str, list, bool, MetaInlines, MetaBlocks, OrderedDict), t

    if t == str:
        return e
    elif t == MetaInlines:
        return to_json(e)
    elif t == MetaBlocks:
        return to_json(e)
    elif t == list:
        return encode_dict('MetaList', [metawalk(ee) for ee in e])
    elif t == OrderedDict:
        return encode_dict('MetaMap', OrderedDict((k, metawalk(v))
                                                  for k, v in e.items()))
    elif t == bool:
        return encode_dict('MetaBool', e)


class MetaInlines(Element):
    """MetaInlines

     MetaValue MetaInlines (items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=False)

    def __repr__(self):
        return 'MetaInlines({})'.format(','.join(repr(x) for x in self.items))

    def encode_content(self):
        return encode_items(self)


class MetaBlocks(Element):
    """MetaBlocks

     MetaValue MetaBlocks (items=[Inline])"""

    __slots__ = ['items']

    def __init__(self, *args):
        self.items = init_items(type(self), args, has_blocks=True)

    def encode_content(self):
        return encode_items(self)


# ---------------------------
# Constants
# ---------------------------

LIST_NUMBER_STYLES = {
    'DefaultStyle', 'Example', 'Decimal', 'LowerRoman',
    'UpperRoman', 'LowerAlpha', 'UpperAlpha'
}

LIST_NUMBER_DELIMITERS = {'DefaultDelim', 'Period', 'OneParen', 'TwoParens'}

TABLE_ALIGNMENT = {'AlignLeft', 'AlignRight', 'AlignCenter', 'AlignDefault'}

QUOTE_TYPES = {'SingleQuote', 'DoubleQuote'}

CITATION_MODE = {'AuthorInText', 'SuppressAuthor', 'NormalCitation'}

MATH_FORMATS = {'DisplayMath', 'InlineMath'}

RAW_FORMATS = {'html', 'tex', 'latex'}

SPECIAL_ELEMENTS = LIST_NUMBER_STYLES | LIST_NUMBER_DELIMITERS | \
    MATH_FORMATS | TABLE_ALIGNMENT | QUOTE_TYPES | CITATION_MODE

# ---------------------------
# Aux Functions - Initialize
# ---------------------------

def validate(x, group=None, instance=None):
    if group is not None:
        assert x in group, x
    else:
        assert isinstance(x, instance), x
    return x


def init_items(obj, args, has_blocks, depth=1):
    assert depth in (1, 2, 3)
    if depth == 1:
        ans = [validate_item(x, has_blocks, obj) for x in args]
    elif depth == 2:
        ans = [[validate_item(x, has_blocks, obj) for x in y] for y in args]
    else:
        ans = [[[validate_item(x, has_blocks, obj) for x in y] for y in z] 
               for z in args]
    return ans


def validate_item(x, has_blocks, obj):
    def error_message(x):
        expected = 'Block' if has_blocks else 'Inline'
        root_name = obj.__name__
        child_name = type(x).__name__
        err = '{}() element must contain {}s but received a {}()\n---\n{}\n---'
        return err.format(root_name, expected, child_name, repr(x))

    x = x() if callable(x) else x
    assert isinstance(x, Block if has_blocks else Inline), error_message(x)
    return x


def init_ica(self, identifier, classes, attributes):
    self.identifier = identifier
    self.classes = classes if classes else []
    self.attributes = attributes if attributes else OrderedDict()
    assert isinstance(self.identifier, str)
    assert isinstance(self.attributes, dict)
    assert all(isinstance(cl, str) for cl in self.classes)


def init_ssd(self, start, style, delimiter):
    self.start = start
    self.style = style
    self.delimiter = delimiter

    assert (self.start == int(self.start)) and (0 <= self.start)
    assert self.style in LIST_NUMBER_STYLES, self.style
    assert self.delimiter in LIST_NUMBER_DELIMITERS, self.delimiter


def init_ut(self, url, title):
    self.url = validate(url, instance=str)
    self.title = validate(title, instance=str)

# ---------------------------
# Main JSON Functions
# ---------------------------

def to_json(element):
    tag = type(element)
    if tag == Doc:
        meta = element.metadata.items()
        meta = OrderedDict((k, metawalk(v)) for k, v in meta)
        return [{'unMeta': meta}, element.items]
    else:
        return encode_dict(tag.__name__, element.encode_content())


def from_json(data):

    # Empty metadata
    if data == []:
        return data

    # Odd cases
    if data[0][0] != 't':
        tag = data[0][0]

        if tag == 'unMeta':
            assert len(data) == 1
            c = data[0][1]
            c = OrderedDict(c)
            return c
        else:
            return data

    # Standard cases
    assert data[1][0] == 'c'
    tag = data[0][1]
    c = data[1][1]

    if tag == 'Null':
        return Null()
    elif tag == 'Space':
        return Space()
    elif tag == 'HorizontalRule':
        return HorizontalRule()
    elif tag == 'SoftBreak':
        return SoftBreak()
    elif tag == 'LineBreak':
        return LineBreak()

    elif tag == 'Plain':
        return Plain(*c)
    elif tag == 'Para':
        return Para(*c)
    elif tag == 'BlockQuote':
        return BlockQuote(*c)
    elif tag == 'Emph':
        return Emph(*c)
    elif tag == 'Strong':
        return Strong(*c)
    elif tag == 'Strikeout':
        return Strikeout(*c)
    elif tag == 'Superscript':
        return Superscript(*c)
    elif tag == 'Subscript':
        return Subscript(*c)
    elif tag == 'SmallCaps':
        return SmallCaps(*c)
    elif tag == 'Note':
        return Note(*c)

    elif tag == 'Header':
        return Header(*c[2], level=c[0], identifier=c[1][0], classes=c[1][1],
                      attributes=c[1][2])
    elif tag == 'Div':
        return Div(*c[1], identifier=c[0][0], classes=c[0][1],
                   attributes=c[0][2])
    elif tag == 'Span':
        return Span(*c[1], identifier=c[0][0], classes=c[0][1],
                    attributes=c[0][2])
    elif tag == 'Quoted':
        return Quoted(*c[1], quote_type=c[0])
    elif tag == 'Cite':
        return Cite(*c[1], citations=c[0])
    elif tag == 'Link':
        return Link(*c[1], url=c[2][0], title=c[2][1], identifier=c[0][0],
                    classes=c[0][1], attributes=c[0][2])
    elif tag == 'Image':
        return Image(*c[1], url=c[2][0], title=c[2][1], identifier=c[0][0],
                     classes=c[0][1], attributes=c[0][2])

    elif tag == 'Str':
        return Str(c)
    elif tag == 'CodeBlock':
        return CodeBlock(text=c[1], identifier=c[0][0],
                         classes=c[0][1], attributes=c[0][2])
    elif tag == 'RawBlock':
        return RawBlock(text=c[1], format=c[0])
    elif tag == 'Code':
        return Code(text=c[1], identifier=c[0][0],
                    classes=c[0][1], attributes=c[0][2])
    elif tag == 'Math':
        return Math(text=c[1], format=c[0])
    elif tag == 'RawInline':
        return RawInline(text=c[1], format=c[0])

    elif tag == 'BulletList':
        return BulletList(*c)
    elif tag == 'OrderedList':
        return OrderedList(*c[1], start=c[0][0],
                           style=c[0][1], delimiter=c[0][2])
    elif tag == 'DefinitionList':
        return DefinitionList(*c)
    elif tag == 'Table':
        return Table(*c[4], caption=c[0], alignment=c[1], width=c[2],
                     header=c[3])

    elif tag == 'MetaList':
        return c
    elif tag == 'MetaMap':
        return OrderedDict(c)
    elif tag == 'MetaInlines':
        return MetaInlines(*c)
    elif tag == 'MetaBlocks':
        return MetaBlocks(*c)
    elif tag == 'MetaString':
        return c
    elif tag == 'MetaBool':
        assert c in {True, False}, c
        return c

    elif tag in SPECIAL_ELEMENTS:
        return tag

    else:
        print('-- UNKNOWN TAG')
        print(type(tag))
        print(tag)
        print(c)
        print('--')
        raise Exception('unknown tag ' + tag)


# ---------------------------
# Aux JSON Functions
# ---------------------------

def encode_dict(tag, content):
    return OrderedDict((("t", tag), ("c", content)))


def encode_items(self):
    tag = type(self).__name__
    if tag in ('BulletList', 'OrderedList'):
        return [[to_json(x) for x in row] for row in self.items]
    elif tag == 'DefinitionList':
        return [[[to_json(x) for x in k], [[to_json(x) for x in y]
                for y in v]] for (k, v) in self.items]
    elif tag == 'Table':
        return [[[to_json(x) for x in cell] for cell in row]
                for row in self.items]
    else:
        return [to_json(x) for x in self.items]


def encode_ica(self):
    return [self.identifier, self.classes, list(self.attributes.items())]


def encode_list(items):
    return [x.to_json() for x in items]


def decode_ica(self, attr):
    if attr is None:
        attr = ["", [], []]  # ID, classes, attribute pairs
    self.identifier, self.classes, attributes = attr
    self.attributes = dict(attributes)
