import fileinput
import os

from enum import Enum
import shutil

from jinja2 import Template
from pydantic import BaseModel
import yaml

import pagekey_sitegen


class TemplateName(Enum):
    SPHINX = "sphinx"
    NEXT = "next"


class SiteConfig(BaseModel):

    @staticmethod
    def from_path(path: str):
        config_path = os.path.join(path, 'site.yaml')
        with open(config_path, 'r') as f:
            text_raw = f.read()
        parsed_config = yaml.safe_load(text_raw)
        site_config = SiteConfig(**parsed_config)
        return site_config

    project: str
    copyright: str
    author: str
    release: str
    package: str
    template: TemplateName


class SiteGenerator:
    def __init__(self, path: str):
        self.path = path
        self.config = SiteConfig.from_path(path)
        package_root = os.path.dirname(pagekey_sitegen.__file__)
        self.templates_dir = os.path.join(package_root, 'templates', self.config.template.value)
    def generate(self):
        # Get a fresh build dir
        self._setup_build_dir()

        # Walk directories to get file lists
        template_files = get_files_list(self.templates_dir)
        source_files = get_files_list(self.path)

        # Render templates
        for template in template_files:
            self._render_template(template)

        # Render source files
        for cur_file in source_files:
            self._render_source(cur_file)

        # Call whatever executable to generate the site
        if self.config.template == TemplateName.SPHINX:
            self._build_sphinx()
        elif self.config.template == TemplateName.NEXT:
            self._build_next()
    
    def _build_sphinx(self):
        os.chdir(f'build/{self.config.template.value}')
        os.system('make html')
        # Move the generated site to the top level of the build directory
        shutil.move('_build/html', '..')

    def _build_next(self):
        os.chdir(f'build/{self.config.template.value}')
        os.system('npm i')
        os.system('npm run build')
        os.system('npm run export')
        shutil.move('out', '../html')

    def _setup_build_dir(self):
        if os.path.exists('build'):
            shutil.rmtree('build')
        os.makedirs('build')

    def _render_template(self, filename: str):
        src_filename = filename
        relative_template_path = filename.replace(self.templates_dir + '/', '')
        dest_filename = os.path.join('build', self.config.template.value, relative_template_path)
        
        dest_dir = os.path.dirname(dest_filename)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        try:
            file_contents = get_file_as_string(src_filename)

            template = Template(file_contents)
            output_string = template.render(config=self.config)
            write_string_to_file(dest_filename, output_string)
        except Exception as e:
            print(f"Warning: Failed to parse template {src_filename}, copying instead")
            shutil.copy(src_filename, dest_filename)
    
    def _render_source(self, filename: str):
        dirname = os.path.dirname(filename)
        if len(dirname) < 1:
            # File is at the top-level of the repo - keep it simple
            dest_dir_relpath = os.path.join('build', self.config.template.value)
        else:
            # Handle nested files
            src_dir_relpath = os.path.relpath(os.path.dirname(filename))
            if self.config.template == TemplateName.SPHINX:
                dest_dir_relpath = os.path.join('build', self.config.template.value, src_dir_relpath)
            elif self.config.template == TemplateName.NEXT:
                # For Next, copy files into either src/pages or src/lib
                if src_dir_relpath.startswith('lib'):
                    dest_dir_relpath = os.path.join('build', self.config.template.value, 'src', src_dir_relpath)
                else:
                    dest_dir_relpath = os.path.join('build', self.config.template.value, 'src', 'pages', src_dir_relpath)
        
        # Create directories containing this file if not exists
        os.makedirs(dest_dir_relpath, exist_ok=True)
        # Copy the file over
        # TODO / NOTE: eventually this will do templating too
        shutil.copy(filename, dest_dir_relpath)
        if self.config.template == TemplateName.SPHINX:
            # Replace mermaid code blocks in md with sphinx-compatible ones
            dest_file = os.path.join(dest_dir_relpath, os.path.basename(filename))
            if dest_file.endswith('.md'):
                with fileinput.FileInput(dest_file, inplace=True, backup='.bak') as file:
                    for line in file:
                        print(line.replace('```mermaid', '```{mermaid}'), end='')


def get_files_list(path: str):
    """Walk directory and get all files recursively.
    
    Args:
      path: Directory path to walk.
    """
    result = []
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            cur_file_path = os.path.abspath(os.path.join(root, cur_file))
            result.append(cur_file_path)
    return result


def get_file_as_string(filename: str):
    with open(filename, 'r') as file:
        return file.read()


def write_string_to_file(filename: str, data: str):
    with open(filename, 'w') as file:
        file.write(data)
