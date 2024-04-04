import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from sphinx.locale import __

logger = logging.getLogger(__name__)


SVGLINKS_PREFIX = "svglink://"

ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

def patch_svg(node, writer):
    """
    SVG elements should link to sphinx content. This is done by cluing pseudo URIs to
    the SVG elements.

        <a xlink:href="svglink://#other-reference-label">
            <ellipse cx="235" cy="220" rx="40" ry="40" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)"
                     pointer-events="all"/>
        </a>

    In this example the ellipse links to the pseudo URI "svglink://#other-reference-label" which represents
    the target label "#other-reference-label". The target "#other-reference-label" should
    be defined elsewhere e.g. it may link to a chapter_

        .. _other-reference-label:

        This is a chapter
        -----------------

    Each pseudo URI has to start with "svglink://".
    THe linking can be done comfortably by using draw.io or inkscape or any other capable SVG editor.

    This routine patches the SVG file so that the pseudo URIs are replaced by the
    correct relative URIs to the target referenced.

    :param node: The current node that is rendered
    :param writer: The writer to which renders the node
    :return: the relative path to the patched SVG file
    """

    # Get the SVG file path
    # The current base dir is the parent of the current file
    current_doc_dir = Path(writer.builder.current_docname).parent
    # and the original_uri or candidates attribute of the node gives us the relative SVG file path
    if 'original_uri' in node.attributes:
        svg_file_path = current_doc_dir / Path(node.attributes['original_uri'])
    elif 'candidates' in node.attributes:
        svg_file_path = Path(node.attributes['candidates']['*'])
    else:
        pass
        # ToDo error handling
    # Parse the SVG file
    with open(svg_file_path, "rb") as f:
        etree = ET.parse(f)

    root = etree.getroot()

    # Iterate over all hrefs in the SVG file
    for child in root.findall(".//*[@xlink:href]", namespaces={'xlink': 'http://www.w3.org/1999/xlink'}):
        # Get the pseudo URI. Yes, the namespace has to be so written into the argument.
        speudo_URI = child.attrib['{http://www.w3.org/1999/xlink}href']
        if not speudo_URI.startswith(SVGLINKS_PREFIX):
            continue
        # cut the reference part from the pseudo URI
        reference = speudo_URI[len(SVGLINKS_PREFIX):]
        # Strip '#' to get the reference label
        if reference.startswith('#'):
            reference = reference[1:]
        # lookup the reference via the labels dict
        labels = writer.builder.env.domains['std'].labels
        if reference in labels:
            ref_tupel = labels[reference]
            # local link or link to file in same directory
            if len(ref_tupel) == 3:
                new_reference = ref_tupel[0] + '.html' + '#' + ref_tupel[1]
            else:
                # Link to file in other directory needs a path
                new_reference = '/'.join(ref_tupel[:-3]) + ref_tupel[-3] + '.html' + '#' + ref_tupel[-2]
            # Replace the link to the pseudo URI with the new reference
            child.attrib['{http://www.w3.org/1999/xlink}href'] = '../' + new_reference
            # Tell the browser to measure the relative paths from the parent of the embedded SVG object.
            child.attrib['target'] = '_parent'
        else:
            logger.warning(
                __(f'  Cannot find anchor for svglink reference: "{reference}". Please check your anchors!'),
            )

    # Determine the new location in the filesystem for the patched SVG file in the "build" dir.
    # ToDo: Catch file name collisions [SVG image is embedded twice]
    # ToDo: better file naming convention
    # ToDo: prevent copying the original file
    if 'original_uri' in node.attributes:
        svg_file_name = Path(node.attributes['original_uri']).name
    elif 'candidates' in node.attributes:
        svg_file_name = Path(node.attributes['candidates']['*']).name
    else:
        pass
        # ToDo error handling

    new_svg_file_path = Path(writer.builder.outdir) / writer.builder.imagedir / (svg_file_name + '1.svg')

    # check if *build/_images* exists and if not create it:
    if not new_svg_file_path.exists():
        new_svg_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the SVG file
    with open(new_svg_file_path, "wb") as f:
        etree.write(f)

    # Return the relative URI for the SVG <object> to find its data
    return Path(writer.builder.imgpath) / (svg_file_name + '1.svg')
