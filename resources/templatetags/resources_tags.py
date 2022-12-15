import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def highlight_query(text, query):
    """ Function to highlight the query substring within the text string.
        'Highlight' means to wrap the query substring with a span tag that
        includes the CSS class 'highlight_query'.
        """

    # It is necessary to escape the text and query strings to avoid erroneous
    # highlighting in the case of strings that include ampersands, angle
    # brackets, and other chars that might be interpreted as html.
    # (See the below comment regarding why the same name is used for the 'text'
    # string.)
    text = escape(text)
    escaped_query = escape(query)

    matches = re.finditer(escaped_query, text, re.IGNORECASE)

    # In the for loop below, it is necessary to distinguish between the text
    # string in the first loop and that in the second and subsequent loops.
    # This would necessitate an additional if condition and more code.
    # Using the same name for the 'text' string avoids this and keeps the code
    # cleaner and simpler (except for the extra comment...).
    if matches:
        matches_reversed = reversed(list(matches))
        for m in matches_reversed:
            text = text[:m.end()] + '</span>' + text[m.end():]
            text = text[:m.start()] + '<span class="highlight_query">' + text[m.start():]
        return mark_safe(text)

    return text
