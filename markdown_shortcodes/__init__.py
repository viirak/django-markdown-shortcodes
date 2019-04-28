import re

from django.template.loader import render_to_string

# In the form [[command param param param]]
SHORTCODE_REGEX = re.compile(r'(\[\[([a-z-]+)(.*?)\]\])')

# getting key="value" format as parameters
SHORTCODE_PARAMETER_REGEX = re.compile(r"([a-z_]+)=\"(.+?)\"")  # key="value"

# Dictionary of shortcode functions
shortcodes = {}


def shortcode(func):
    """ A decorator function to define a shortcode """
    shortcodes[func.__name__] = func
    return func


@shortcode
def shortcode_vimeo(**kwargs):
    """ vimeo shortcode """
    return render_to_string("shortcodes/vimeo.html", {
        'id': kwargs.get("id"),
        'title': kwargs.get("title"),
        'alternate_uri': kwargs.get("alternate_uri")
    })


def expand_shortcodes(document):
    """ get custom shortcodes and its parameters from document """

    matches = re.findall(SHORTCODE_REGEX, document)
    for result in matches:
        sequence = result[0]
        shortcode_name = result[1].replace("-", "_")
        method_name = "shortcode_%s" % shortcode_name
        parameters_match = re.findall(SHORTCODE_PARAMETER_REGEX, result[2])
        parameters = dict(parameters_match)

        # If we have a method defined for the shortcode, call it.
        # Otherwise, ignore the shortcode string and move on.
        shortcode_method = shortcodes.get(method_name, None)
        if shortcode_method:
            print("-- Rendering shortcode {} with parameters {} \
                ".format(shortcode_name, parameters))
            html_string = shortcode_method(**parameters)
            document = document.replace(sequence, html_string)
        else:
            print("-- shortcode `%s` not found" % shortcode_name)

    return document
