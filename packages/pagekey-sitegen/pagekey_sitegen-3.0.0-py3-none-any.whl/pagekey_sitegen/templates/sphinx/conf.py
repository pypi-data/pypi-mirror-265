"""Template for Sphinx configuration file."""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '{{ config.project }}'
copyright = '2024, {{ config.author }}'
author = '{{ config.author }}'
release = '{{ config.release }}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'autoapi.extension',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

html_title = "{{ config.name }}"

# Add '.md' to source_suffix
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

autoapi_dirs = [
    '{{ config.package }}'
]
