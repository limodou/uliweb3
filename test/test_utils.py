from uliweb.utils.textconvert import text2html


def test_textconvert():
    """
    >>> text2html("<span>test</span>")
    '&lt;span&gt;test&lt;/span&gt;'
"""
