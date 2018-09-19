from IPython.display import display_html

def display_side_by_side(*args):
    " display dataframes side-by-side"
    html_str=''
    for df in args:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)


def mydisplay(dfs, names=[]):
    " display dataframes side-by-side, with specified df names displayed"
    html_str = ''
    if names:
        html_str += '<tr>' + 
                    ''.join(f'<td style="text-align:center">{name}</td>' for name in names) + 
                    '</tr>'
    html_str += '<tr>' + 
                ''.join(f'<td style="vertical-align:top"> df.to_html(index=False)}</td>' 
                         for df in dfs) + 
                '</tr>'
    html_str = f'<table>{html_str}</table>'
    html_str = html_str.replace('table','table style="display:inline"')
    display_html(html_str, raw=True)
    
## A useful method for creating T.o.C. 
## Place anchor tag on line above heading (so heading is visible after clicking)
## Produces clickable references in any MarkDown editor.

# Table of contents
1. [Introduction](#introduction)
2. [Some paragraph](#paragraph1)
    1. [Sub paragraph](#subparagraph1)
3. [Another paragraph](#paragraph2)

## This is the introduction <a name="introduction"></a>
Some introduction text, formatted in heading 2 style

## Some paragraph <a name="paragraph1"></a>
The first paragraph text

### Sub paragraph <a name="subparagraph1"></a>
This is a sub paragraph, formatted in heading 3 style

## Another paragraph <a name="paragraph2"></a>
The second paragraph text