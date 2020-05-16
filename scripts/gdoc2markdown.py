"""
Custom script to convert a Google Doc to a Markdown file for publishing to a
Jekyll post. I download and unzip an HTML file of my Google Doc and feed the 
path into the arguments of this script. The script converts the given HTML file
from Google Docs into a single-file HTML document with images embedded as 
base64 encoded images. The script also changes some of the HTML DOM to aid with
formatting of the post. Very custom!
"""

from bs4 import BeautifulSoup
from os.path import basename, splitext
import sys
import base64
import os
import re


def main():
    if len(sys.argv) != 3:
        print(help())
        return

    _, html_path, markdown_path = sys.argv

    enclosing_folder = os.path.dirname(html_path)

    with open(html_path, mode='r') as html_file:
        html = html_file.read()

    soup = BeautifulSoup(html, features='html.parser')

    for img in soup.findAll('img'):
        local_img_path = os.path.join(enclosing_folder, img['src'])

        _, img_extension = os.path.splitext(local_img_path)
        img_extension = img_extension[1:]  # remove dot (".")

        with open(local_img_path, mode='rb') as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        
        img_data = f'data:image/{img_extension};base64,{encoded_string}'

        img['src'] = img_data
    
    # Remove classes from the <body> tag as it interferes with existing styling
    soup.body['class'] = ''

    # Add float-right class to tags in Table of Contents
    for a in soup.findAll('a'):
        if 'href' in a.attrs \
            and re.search(r'#h\.[a-z0-9]+', a['href']) \
            and re.search(r'[0-9]+', a.text):
            parent = a.find_parent()
            if 'class' in parent.attrs:
                parent.attrs['class'].append('float-right')
    
    # Include content after this indicator
    jekyll_start = list(soup(text='!jekyll::start'))
    
    if not jekyll_start:
        print('html file must have text literal !jekyll::start')
        return
    
    start_tag = jekyll_start[0]
    while start_tag.name != 'p':
        start_tag = start_tag.parent
    
    body_after_start = start_tag.find_next_siblings()
    body_after_start_html_str = ''.join(tag.prettify() for tag in body_after_start if tag)

    inline_img_html_string = soup.head.prettify() + '\n' + body_after_start_html_str
    
    markdown_front_matter = get_front_matter(markdown_path)

    if not markdown_front_matter:
        print('no matches in markdown front matter')
        return

    with open(markdown_path, mode='w+') as markdown_file:
        markdown_file.write(markdown_front_matter + '\n' + inline_img_html_string)

def get_front_matter(markdown_path):
    reading_front_matter = False
    front_matter_lines = []
    with open(markdown_path, mode='r') as markdown_file:
        for line in markdown_file:
            triple_dash_found = line.find('---') > -1
        
            if not reading_front_matter and triple_dash_found:
                reading_front_matter = True
            
            elif reading_front_matter and triple_dash_found:
                break

            elif reading_front_matter:
                front_matter_lines.append(line)
    
    return '---\n' + ''.join(front_matter_lines) + '---\n'

def help():
    return """
    python3 gdoc2markdown.py <input html file> <output markdown file>
        input html file: path to the HTML file in the unzipped Google Doc
        output markdown file: path to write markdown contents to
    """

if __name__ == "__main__":
    main()
