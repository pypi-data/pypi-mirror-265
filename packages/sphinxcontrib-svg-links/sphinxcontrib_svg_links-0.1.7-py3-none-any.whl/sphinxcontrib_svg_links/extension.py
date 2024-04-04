from docutils import nodes
from docutils.parsers.rst.directives.images import Image, Figure

from docutils.parsers.rst.directives import unchanged

from sphinxcontrib_svg_links.writer import visit_image_html, depart_image_html


def setup(app):

    # add a new option *svglinks* to the *image* and *figure* directive
    Image.option_spec['svglinks'] = unchanged
    Figure.option_spec['svglinks'] = unchanged

    # override the html writer methods for the *image* nodes
    # to react on the svglinks option
    app.add_node(
        nodes.image,
        override=True,
        html=(visit_image_html, depart_image_html),
    )

    # Todo: Check if this is really true
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }