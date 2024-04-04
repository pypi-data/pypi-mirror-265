import logging
import os
import posixpath
import urllib

from docutils import nodes
from sphinx.util.images import get_image_size

from sphinx.locale import __
from sphinx.writers.html5 import multiply_length, HTML5Translator

from sphinxcontrib_svg_links.svg import patch_svg

logger = logging.getLogger(__name__)


def visit_image_html(self, node: nodes.Node):
    olduri = node['uri']
    # rewrite the URI if the environment knows about it
    if olduri in self.builder.images:
        node['uri'] = posixpath.join(self.builder.imgpath,
                                     urllib.parse.quote(self.builder.images[olduri]))

    if 'scale' in node:
        # Try to figure out image height and width.  Docutils does that too,
        # but it tries the final file name, which does not necessarily exist
        # yet at the time the HTML file is written.
        if not ('width' in node and 'height' in node):
            size = get_image_size(os.path.join(self.builder.srcdir, olduri))
            if size is None:
                logger.warning(
                    __('Could not obtain image size. :scale: option is ignored.'),
                    location=node,
                )
            else:
                if 'width' not in node:
                    node['width'] = str(size[0])
                if 'height' not in node:
                    node['height'] = str(size[1])

    uri = node['uri']
    if uri.lower().endswith(('svg', 'svgz')):
        atts = {'src': uri}
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'scale' in node:
            if 'width' in atts:
                atts['width'] = multiply_length(atts['width'], node['scale'])
            if 'height' in atts:
                atts['height'] = multiply_length(atts['height'], node['scale'])
        atts['alt'] = node.get('alt', uri)
        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']

        # This is due to svg-links
        if 'svglinks' in node.attributes and node.attributes['svglinks'] \
                or 'svglinks' in node.parent.attributes and node.parent.attributes['svglinks']:
            patched_SVG_path = patch_svg(node, self)
            atts['data'] = patched_SVG_path
            del atts['src']
            atts['type'] = 'image/svg+xml'
            atts['target'] ="_parent"
            self.body.append(self.starttag(node, 'object', '', **atts))
            self.body.append('</object>')

        else:
            # thi sis the original behavior
            self.body.append(self.emptytag(node, 'img', '', **atts))
        return

    super(HTML5Translator, self).visit_image(node)


def depart_image_html(self, node: nodes.Node):
    pass
