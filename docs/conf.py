# -*- coding: utf-8 -*-

# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'rst2pdf.pdfbuilder',
    ]

templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
project = u'nmadb-academics'
copyright = u'2012, Vytautas Astrauskas'
version = '0.1'
release = '0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

today_fmt = '%Y-%m-%d'
exclude_patterns = ['build']
add_function_parentheses = True
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

html_theme = 'default'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as 
# html_title.
#html_short_title = None

html_static_path = []
html_last_updated_fmt = '%Y-%m-%d'
html_use_smartypants = True

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'namedoc'


# -- Options for LaTeX output ---------------------------------------------

latex_paper_size = 'a4'
latex_font_size = '10pt'
latex_documents = [
  (
      'index', 'main.tex',
      u'\\nmadb-academics Documentation', u'\\Vytautas Astrauskas', 'manual'
      ),
  ]

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        'index', 'main',
        u'nmadb-academics Documentation', [u'Vytautas Astrauskas'], 1,
        ),
    ]


# Example configuration for intersphinx: refer to the Python standard 
# library.
intersphinx_mapping = {'http://docs.python.org/': None}

# -- Options for PDF output ---------------------------------------------

# Manual can be found at 
# http://lateral.netmanagers.com.ar/static/manual.pdf.
# Available options listed at page 42.

pdf_documents = [
    (
        'index', u'main',
        u'nmadb-academics Documentation', u'Vytautas Astrauskas'
        ),
    ]
pdf_stylesheets = ['sphinx', 'kerning', 'a4']
#pdf_language = 'lt'
pdf_break_level = 0
pdf_breakside = 'any'
pdf_inline_footnotes = True
pdf_verbosity = 0
#pdf_use_index = False
#pdf_use_modindex = False
pdf_use_coverpage = True
