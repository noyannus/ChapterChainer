#!python3
# -*- coding: utf-8 -*-
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#   This script downloads serial web pages. It follows the 'Next' or 'Next    #
#   Chapter' link of each page (no 'Table of Contents' page is required),     #
#   does some formatting and cleanup of the retrieved html, and outputs all   #
#   chapters to one large HTML file.                                          #
#                                                                             #
#   ChapterChainer is heavily commented and uses descriptive variable names   #
#   to make adding new serials fairly easy. Non-story pages (such as          #
#   'Author's Notes') can optionally be skipped or appended to the story.     #
#                                                                             #
#                                                                             #
#   Currently built-in serials are:                                           #
#                                                                             #
#   Abelson, Sussman & Sussman  'Structure and Interpretation of Computer     #
#                               Programs', 2nd edition ('SICP')               #
#   Alexander, Scott           'Unsong' (Author’s Notes optional, non-story   #
#                                        announcements/greetings omitted)     #
#   Walter                     'The Fifth Defiance' ('T5D')                   #
#   Wildbow (John C. McCrae)   'Glow-worm' ('Glowo')                          #
#                              'Pact'                                         #
#                              'Twig'                                         #
#                              'Ward'                                         #
#                              'Worm'                                         #
#                                                                             #
#                                                                             #
#   Required:   Python 3, BeautifulSoup4, lxml, html5lib                      #
#                                                                             #
#                                                                             #
#   Usage:                                                                    #
#   Invoke the script with one of the titles, and one of the switches if      #
#   applicable. Use the abbreviations where listed above.                     #
#   All arguments are case sensitive:                                         #
#                                                                             #
#   python3 ChapterChainer.py {Glowo, Pact, SICP, T5D, Twig, Unsong,          #
#                              Ward, Worm}                                    #
#                                                                             #
#   Optional switches for Author's Notes and Postscript; currently only for   #
#   'Unsong':                                                                 #
#                                                                             #
#   [--omit | --append | --chrono[logical]]                                   #
#                                                                             #
#   '-omit' skips these pages, '--append' collects and puts them after the    #
#   story, the default '--chronological' (or '--chrono') keeps them           #
#   interspersed between chapters in order of publication.                    #
#                                                                             #
#   Examples:                                                                 #
#   'ChapterChainer.py Unsong --omit'                                         #
#   downloads 'Unsong' without the non-story pages to the working directory.  #
#   'ChapterChainer.py Glowo'                                                 #
#   downloads 'Glow-worm' to the working directory.                           #
#                                                                             #
#   Known Issues:                                                             #
#   Pages not published at the time of this script update may not be found    #
#   if the 'Next' link has been changed.                                      #
#   Links from a story to epilogue, afterword, author's blog, next story,     #
#   etc. are not followed.                                                    #
#                                                                             #
#                                                                             #
#   Social and Legal                                                          #
#   Please donate to the authors for their writing! Using this script can     #
#   deny them some needful income from advertising.                           #
#   Easy donation options are on their sites. As usually are options to       #
#   share, like, and comment (high added value from audience sometimes!)      #
#   And you can vote daily on topwebfiction.com if you enjoy reading.         #
#                                                                             #
#       Glow-worm: https://parahumans.wordpress.com/                          #
#                (not listed in topwebfiction so far)                         #
#       Pact:    https://pactwebserial.wordpress.com/                         #
#                http://topwebfiction.com/vote.php?for=pact                   #
#       Structure and Interpretation of Computer Programs: ???                #
#       The Fifth Defiance: ???                                               #
#                http://topwebfiction.com/vote.php?for=the-fifth-defiance     #
#       Twig:    https://twigserial.wordpress.com/                            #
#                http://topwebfiction.com/vote.php?for=twig                   #
#       Unsong:  Patreon link on http://slatestarcodex.com/                   #
#                http://topwebfiction.com/vote.php?for=unsong                 #
#       Ward:    https://www.parahumans.net/                                  #
#                (not listed in topwebfiction so far)                         #
#       Worm:    https://parahumans.wordpress.com/                            #
#                http://topwebfiction.com/vote.php?for=worm                   #
#                                                                             #
#                                                                             #
#   This script must not be used to publish a serial without its author's     #
#   permission. (This would severely curtail their chances to sell the        #
#   manuscript, and with no money to make we might lose them writing for the  #
#   web altogether. Also, few could afford the punitive damage for a lost     #
#   film series deal of something big like 'Worm'. Sorry for the              #
#   moralizing.) Enjoy reading!                                               #
#                                                                             #
#   ......................................................................    #
#                                                                             #
#   "3:16 All scripture is given by a procedural argument to instantiate."    #
#                                       (kingjamesprogramming.tumblr.com)     #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""


import os
import os.path
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request

import bs4
import html5lib  # is used, ignore code inspector's complaint
import lxml  # is used, ignore code inspector's complaint


def download_page(next_link, raw_html_file):
    """Download page to temporary file"""

    # Timing
    down_start_time = time.time()  # Start download time

    # Save retrieved html to temp file
    # (Keep the 'try..' and leave broad despite code inspector's complaint, in
    # case a connection needs debugging)
    try:
        # Spoof the User-Agent, in case Python is a blacklisted agent and
        # receives a 403. (Web search a list of valid user agents, pick one)
        request = urllib.request.Request(next_link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 \
            Safari/537.36'})
        with urllib.request.urlopen(request) as response:
            with open(raw_html_file, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
    except Exception as this_exception:  # debug info & exit
        print('\nCould not retrieve next page. Is this link broken?\n\'' +
              next_link + '\'\n\n')
        print(type(this_exception))
        print(this_exception)
        sys.exit()          # stop gracefully

    return str(time.time() - down_start_time)  # Download time


def find_next_link(soup):
    """Identify and return a link to the next page"""

    maybe_link = None

    # 'Pact', 'Twig', 'Unsong', 'Ward', 'Worm': various link texts
    if WHICH_SERIAL in ('Glowo', 'Pact', 'T5D', 'Twig', 'Unsong',
                        'Ward', 'Worm'):
        if soup.find('a', {'rel': 'next'}) is not None:  # find by 'rel'='next'
            maybe_link = soup.find('a', {'rel': 'next'})['href']
        else:  # find by link text
            this_re = re.compile(r'(Next)(( |0xC2A0|&nbsp;)+Chapter)?')
            if soup.find('a', text=this_re) is not None:
                maybe_link = soup.find('a', text=this_re)['href']

    # Only 'next' as link text
    if WHICH_SERIAL == 'SICP':
        if soup.find('a', text='next') is not None:
            maybe_link = soup.find('a', text='next')['href']
            # Make the relative 'SICP' links absolute
            maybe_link = REL_LINK_BASE + maybe_link

    # Store url if found, replace broken links
    if maybe_link is not None:
        next_link = urllib.parse.quote(maybe_link, safe='/:%')
    else:
        next_link = ''

#    To work around links that slip detection or are broken,
#    repeat for each link:
#    1. duplicate commented explanation and 'if' block below,
#    2. uncomment it, and
#    3. insert page of broken link, broken link url, working url.
#    The Twig 8.3 page below is a real world example.
#
#        # Broken URL in The_broken_links_page
#        if (next_link == 'Broken_link'):
#            next_link = 'Working_link'

    # Broken URL in Twig 8.3
    if next_link == ('//twigserial.wordpress.com/'
                     '2015/12/17/bleeding-edge-8-4/'):
        next_link = ('https://twigserial.wordpress.com/'
                     '2015/12/17/bleeding-edge-8-4/')

    return next_link


def get_wanted_content_tags(soup, chap_title_tag, chap_cont_tag):
    """Get tags that hold headline and wanted content"""

    # 'Glowo', 'Pact', 'T5D', 'Twig', 'Worm'
    if WHICH_SERIAL in ('Glowo', 'Pact', 'T5D', 'Twig', 'Ward', 'Worm'):
        chap_title_tag = soup.find('h1', {'class': 'entry-title'})
        chap_cont_tag = soup.find('div', {'class': 'entry-content'})

    # 'Unsong'
    if WHICH_SERIAL == 'Unsong':
        chap_title_tag = soup.find('h1', {'class': 'pjgm-posttitle'})
        chap_cont_tag = soup.find('div', {'class': 'pjgm-postcontent'})

    # 'SICP'
    if WHICH_SERIAL == 'SICP':
        # Get a headline: try first h1, then try h2, then leave None
        if soup.find('h1') is not None:
            chap_title_tag = soup.find('h1')
        elif soup.find('h2') is not None:
            chap_title_tag = soup.find('h2')

        chap_cont_tag = soup.find('body')

    return chap_title_tag, chap_cont_tag


def check_note(chap_title):
    """Check if downloaded page is a Notes page"""

    is_note = None

    # Check title for Notes page
    # 'Unsong'
    if WHICH_SERIAL == 'Unsong':
        this_re = re.compile(r'^(Author.s Note|Postscript)')
        is_note = this_re.search(chap_title)

    return is_note


def declutter_wildbow(chap_title_tag, chap_cont_tag):
    """Remove clutter from Wildbow's content, convert to strings"""

#    # Keep to identify unwanted content
#    if (chap_cont_tag.find_all('a')) is not None:
#        for i in(chap_cont_tag.find_all('a')):
#            print(i)

    # # Tags -- 'Pact' only
    if WHICH_SERIAL == 'Pact':
        # Advertisement
        for i in chap_cont_tag.find_all('div', {'class': 'wpcnt'}):
            i.decompose()
        for i in chap_cont_tag.find_all('style', {'type': 'text/css'}):
            i.decompose()
        # Unlinked link text
        for i in chap_cont_tag.find_all('strong', text='Last Chapter'):
            i.decompose()

    # # Tags -- 'Twig' only
    if WHICH_SERIAL == 'Twig':
        # Mysterious white dot
        for i in chap_cont_tag.find_all('span', {'style': 'color:#ffffff;'},
                                        {'text': '.'}
                                        ):
            i.decompose()

    # # Tags -- All: 'Glowo', 'Pact', 'Twig', 'Ward', 'Worm'
    # Navigation links
    this_re = re.compile(r'(\s|&nbsp;)*'
                         r'(Previous|Next|L?ast|About|'
                         r'( *The *)?End(\s*\(Afterword\))?)'
                         r'(\s|&nbsp;)*(Chapter)?'
                         r'(\s|&nbsp;)*'
                         )
    this_tag_list = [this_tag for this_tag in chap_cont_tag.find_all()
                     if this_re.match(this_tag.text)
                     and this_tag.name == 'a'
                     ]
    for this_tag in this_tag_list:
        this_tag.decompose()

    # Social web
    for i in chap_cont_tag.find_all('div', id='jp-post-flair'):
        i.decompose()

    # Tags except <br/> with no rendered text (they prevent decomposing -?)
    all_tags = chap_cont_tag.find_all()
    this_re = re.compile(r'^(\s|&nbsp;)*$')
    this_tag_list = [this_tag for this_tag in all_tags
                     if (this_re.match(this_tag.text) and
                         this_tag.name != 'br'
                         )]
    for this_tag in this_tag_list:
        this_tag.decompose()

    # Tags with only runs of of ≥40 spaces
    this_re = re.compile(r'^( |0xC2A0|&nbsp;){40,}$')
    for i in chap_cont_tag.find_all('p', text=this_re):
        i.decompose()

    # # HTML string
    # Tags to html string
    out_title = str(chap_title_tag)
    out_chap = str(chap_cont_tag)

    # Standardize several kinds of breaks to newline
    out_chap = '\n'.join(out_chap.splitlines())  # misses '0x2028' - bug?
    out_chap = out_chap.replace(u'\u2028', '\n')

    # Whitespace not before AND after tags that format rendered text
    this_re = re.compile(r'(\s|&nbsp;)'
                         r'(</?(b|i|em|del|strong|span)>)'
                         r'(\s|&nbsp;)'
                         )
    out_title = this_re.sub(r'\2 ', out_title)
    out_chap = this_re.sub(r'\2 ', out_chap)

    # Collapse 2 to 4 whitespace after punctuation, non-space entities,
    # tags that format rendered text
    this_re = re.compile(r'([,.;:!?&…’”a-zA-Z0-9]|'  # literals
                         r'(&.{3,10}(?!sp);)|'  # entities not '&…sp;'
                         r'(</?(b|i|em|del|strong|span)>))'  # tags
                         r'(\s|&nbsp;){2,4}'
                         )
    out_title = this_re.sub(r'\1 ', out_title)
    out_chap = this_re.sub(r'\1 ', out_chap)

    # No non-breaking space after punctuation, non-space entities
    this_re = re.compile(r'([,.;:!?&…’”a-zA-Z0-9]|'  # literals
                         r'(&.{3,10}(?!sp);))'  # entities not '&…sp;'
                         r'(0xC2A0|&nbsp;)'
                         )
    out_title = this_re.sub(r'\1 ', out_title)
    out_chap = this_re.sub(r'\1 ', out_chap)

    # Collapse multiple newlines and leading spaces (not really necessary…)
    this_re = re.compile(r'(\n{2,} *|\n +)')
    out_title = this_re.sub(r'\n', out_title)
    out_chap = this_re.sub(r'\n', out_chap)

    # # Special case 'Glow-worm': Unusual navigation lines
    if WHICH_SERIAL == 'Glowo':
        this_re = re.compile(r'>\n?(Last Chapter)?'
                             r'(\s|&nbsp;){40,}'
                             r'(Next Chapter)?\n?<')
        out_chap = this_re.sub(r'><', out_chap)

    return out_title, out_chap


def declutter_unsong(chap_title_tag, chap_cont_tag):
    """Remove clutter from Unsong content, convert to strings"""

    # Navigation links
    this_re = re.compile(r'(prev|next)')
    for i in chap_cont_tag.find_all('a', {'rel': this_re}):
        i.decompose()

    # Social web
    for i in chap_cont_tag.find_all(
            'div', {'class': 'sharedaddy sd-sharing-enabled'}):
        i.decompose()

    # Tags to html string
    out_title = str(chap_title_tag)
    out_chap = str(chap_cont_tag)

    # 'End of Book…' Season's greetings
    this_re = re.compile(r'(<hr/>\n<p></p><center><b>End of Book [^<]+)'
                         '<.+(</b></center>)', re.DOTALL
                         )
    out_chap = re.sub(this_re, r'\1\2', out_chap)

    # Author's Note announcements
    this_re = re.compile(  # find by '<hr/>\n<p> …'
        r'<hr/>\n<p>(<font size="1">|<i>)+.+'
        '(<a href="https?://unsongbook.com/authors-note-).+'
        '((</i>|</font>)+</p>|((<br/>\n.?)+</center>))', re.DOTALL
        )
    out_chap = re.sub(this_re, '', out_chap)

    this_re = re.compile(  # find by '<p>[ …' ;  '[^C]' b/c '[Content warning:'
        r'<p>(<font size="1">|<i>)+\[[^C].+'
        '(<a href="https?://unsongbook.com/authors-note-).+'
        '((</i>|</font>)+</p>|((<br/>\n.?)+</center>))', re.DOTALL
        )
    out_chap = re.sub(this_re, '', out_chap)

    this_re = re.compile(  # find by '<p></p><center>…'
        r'<p></p><center><br/>\n\.<br/>.+'
        '(<a href="https?://unsongbook.com/authors-note-).+'
        '((</i>|</font>)+</p>|((<br/>\n.?)+</center>))', re.DOTALL
        )
    out_chap = re.sub(this_re, '', out_chap)

    # Other announcements; not from Author's Notes
    this_re = re.compile(r'(<p>Further information will be posted .+ '
                         r'and with next week’s chapter\]</p>\n)|'
                         r'(<p>— 2 PM on Sunday April 17 at the CFAR.+ '
                         r'Stanford, time and exact location tbd</p>\n)|'
                         r'(<p><i>\[If you like this story, please <a .+'
                         r'spamming you with it every update\.\]</i></p>)|'
                         r'(<p><b>Thank you for reading '
                         r'<i>Unsong</i>\.</b></p>\n)|'
                         r'(<p>I have a few extra things I need to .+'
                         r'the box at the top right of the page\.</p>\n)|'
                         r'(<p>I have gotten some very vague express.+ '
                         r'thing, subscribe as mentioned above\.</p>\n)|'
                         r'(<p>Thanks also to everyone who attended .+'
                         r'ople who live there are very confused\.</p>\n)|'
                         r'(<p>Most of you probably know this, but I.+'
                         r'com/r/rational/.>r/rational</a>\.</p>\n)|'
                         r'(<hr/>\n<p>The final chapter will be posted next .+'
                         r'on the linked Facebook pages for details\.</p>)|'
                         r'(<p>There.s a video of me reading the final.+'
                         r'593197826365/.>here</a> \(thanks Ben.\)</p>\n)',
                         re.DOTALL
                         )
    out_chap = re.sub(this_re, '', out_chap)

    return out_title, out_chap


def declutter_t5d(chap_title_tag, chap_cont_tag):
    """Remove clutter from The Fifth Defiance content, convert to strings"""

    # Social web
    chap_cont_tag.find('div',
                       {'class': 'sharedaddy sd-sharing-enabled'}).decompose()
    chap_cont_tag.find('div',
                       {'class': 'sharedaddy sd-block sd-like '
                                 'jetpack-likes-widget-wrapper '
                                 'jetpack-likes-widget-unloaded'}).decompose()

    # Tags to html string
    out_title = str(chap_title_tag)
    out_chap = str(chap_cont_tag)

    # Collapse 2 to 4 whitespace after punctuation, non-space entities,
    # tags that format rendered text
    this_re = re.compile(r'([,.;:!?&…’”a-zA-Z0-9]|'  # literals
                         r'(&.{3,10}(?!sp);)|'  # entities not '&…sp;'
                         r'(</?(b|i|em|del|strong|span)>))'  # tags
                         r'(\s|&nbsp;){2,4}')
    out_title = this_re.sub(r'\1 ', out_title)
    out_chap = this_re.sub(r'\1 ', out_chap)

    # Whitespace not before AND after tags that format rendered text
    this_re = re.compile(r'(\s|&nbsp;)'
                         r'(</?(b|i|em|del|strong|span)>)'
                         r'(\s|&nbsp;)')
    out_title = this_re.sub(r'\2 ', out_title)
    out_chap = this_re.sub(r'\2 ', out_chap)

    # No space after opening quotes
    this_re = re.compile(r'(‘|“|&l[sd]quo;)(\s|&nbsp;)')
    out_title = this_re.sub(r'\1', out_title)
    out_chap = this_re.sub(r'\1', out_chap)

    return out_title, out_chap


def declutter_sicp(chap_cont_tag, next_link):
    """Remove clutter from SICP content, convert to strings"""

    # Navigation links
    for i in chap_cont_tag.find_all('div', {'class': 'navigation'}):
        i.decompose()

    # Point relative text links to within output file
    this_re = re.compile(r'^([^#]*)#(.+)$')
    for link_tag in chap_cont_tag.find_all('a', href=True):  # <a href…>
        if not link_tag.get('href').startswith('http'):  # relative
            link_tag['href'] = this_re.sub(r'#\2', link_tag['href'])

    # Make relative image sources absolute
    for link_tag in chap_cont_tag.find_all('img', src=True):  # <img src…>
        if not link_tag.get('src').startswith('http'):  # relative
            link_tag['src'] = REL_LINK_BASE + link_tag['src']

    # Tags to html string
    out_chap = str(chap_cont_tag)

    # No …</body><body>… at page borders
    if next_link != ('https://mitpress.mit.edu/'
                     'sicp/full-text/book/book.html'):
        out_chap = out_chap.replace('<body>', '')  # not first: no <body>
    if next_link != '':
        out_chap = out_chap.replace('</body>', '')  # not last: no </body>

    return out_chap


def process_page(next_link, page_count, write_to_file):
    """Download & process page, repeat until no next link"""

    chap_title_tag, chap_cont_tag = None, None
    out_title, out_chap = None, None
    prev_links = []

    while next_link != '':

        # Store link of this page for comparison
        prev_links.append(next_link)

        # Set temporary file for downloaded html
        raw_html_file = PAGE_TITLE + '-' + str(page_count) + '.html'

        # Download page, time of download
        down_time = download_page(next_link, raw_html_file)

        # Start processing time
        proc_start_time = time.time()

        # Open temporary file with Beautiful Soup to process html
        soup = bs4.BeautifulSoup(open(raw_html_file, encoding='utf-8'), PARS)

        # Get url of next chapter, keep last link
        next_link = find_next_link(soup)

        # Get tags holding headline and content
        (chap_title_tag, chap_cont_tag)\
            = get_wanted_content_tags(soup, chap_title_tag, chap_cont_tag)

        # Get page title and clean some multiple whitespace
        if chap_title_tag is not None:
            chap_title = ''.join(chap_title_tag.get_text())
            this_re = re.compile(r'(\s|&nbsp;)+')
            chap_title = this_re.sub(r' ', chap_title).strip()
        else:
            chap_title = '<No Page Headline>'

        # Check if Notes page
        if WHICH_SERIAL == 'Unsong':
            is_note = check_note(chap_title)  # is_note = False

        # Increment Chapter count
        page_count += 1

        # If Notes page to omit: skip processing and appending to output
        if GET_NOTES == 'omit' and is_note:

            # Delete chapter file
            os.remove(raw_html_file)

            # User feedback, incl. processing time
            trunc_title = ('<Skipping> ' + chap_title[:33] +
                           (chap_title[33:] and '…')  # 'and', not '+' ==> bool
                           )
            print('{: >5}   {: <45}   {:.5} sec.   {:.5} sec.'
                  .format(page_count, trunc_title[:45], str(down_time),
                          str(time.time() - proc_start_time)
                          )
                  )

        else:
            # Process page content, one def per html style
            if WHICH_SERIAL in ('Glowo', 'Pact', 'Twig', 'Ward', 'Worm'):
                # Remove clutter
                (out_title, out_chap) = declutter_wildbow(chap_title_tag,
                                                          chap_cont_tag)

            if WHICH_SERIAL == 'Unsong':
                # Remove clutter
                (out_title, out_chap) = declutter_unsong(chap_title_tag,
                                                         chap_cont_tag)

                # Write to story or notes file?
                if GET_NOTES == 'append' and is_note:
                    write_to_file = NOTES_FILE
                else:
                    write_to_file = PAGES_FILE

            if WHICH_SERIAL == 'T5D':
                # Remove clutter
                (out_title, out_chap) = declutter_t5d(chap_title_tag,
                                                      chap_cont_tag)

            if WHICH_SERIAL == 'SICP':
                # Remove clutter
                out_chap = declutter_sicp(chap_cont_tag, next_link)

            # Append chapter title and content strings to story or notes file
            with open(write_to_file, 'a', encoding='UTF8') as output:
                if TITLE_SEPARATE:
                    output.write(out_title)
                output.write(out_chap + '<p>&nbsp;</p>\n')  # Add blank line

            # Delete chapter file
            os.remove(raw_html_file)

            # User feedback, incl. processing time
            trunc_title = (chap_title[:44] + (chap_title[44:] and '…'))
            print('{: >5}   {: <45}   {:.5} sec.   {:.5} sec.'
                  .format(page_count, trunc_title[:45], str(down_time),
                          str(time.time() - proc_start_time))
                  )

        # if (page_count >= 4): next_link = ''  # Sample for testing

        # Don't follow to epilogue, afterword, author's blog, next story, etc.
        # Wildbow/WordPress:
        if WHICH_SERIAL in ('Glowo', 'Pact', 'Twig', 'Worm'):
            if next_link in ['https://pactwebserial.wordpress.com/'  # 'Pact'
                             '2015/03/10/rule-of-three/',
                             'https://wildbow.wordpress.com/'  # 'Twig'
                             '2017/10/17/an-end-to-the-twig-experiment/',
                             'https://parahumans.wordpress.com/'  # 'Worm'
                             '2015/03/10/moving-on/',
                             'https://parahumans.wordpress.com/'  # 'Glow-worm'
                             '2017/11/11/glow-worm-p-10-sequel-is-live/'
                             ]:
                next_link = ''

        # No circling back to visited pages
        if next_link in prev_links:
            next_link = ''

        time.sleep(WAIT_BETWEEN_REQUESTS)


def start_end_serial_download():
    """Prepare download, call downloading & processing, complete page"""

    # User feedback headline
    print('Downloading \'' + PAGE_TITLE + '\' to file \'' + PAGES_FILE +
          '\'...\nCount   Page Title' + ' ' * 37 + 'Downloading   Processing'
          )

    # Files to write; remove existing files
    if os.path.isfile(PAGES_FILE):
        os.remove(PAGES_FILE)

    if GET_NOTES == 'append':
        if os.path.isfile(NOTES_FILE):
            os.remove(NOTES_FILE)

    # Output file to append content
    write_to_file = PAGES_FILE

    # Write html opening
    with open(PAGES_FILE, 'a', encoding='UTF8') as output:
        output.write('<html>\n<head>\n<title>' + PAGE_TITLE +
                     '</title>\n<meta content=\'text/html; charset=UTF-8\' '
                     'http-equiv=\'Content-Type\'>\n</head>\n<body>\n')

    # Call download loop, beginning with first page
    process_page(FIRST_LINK, 0, write_to_file)  # initialize page_count

    # Append Notes and closing
    with open(PAGES_FILE, 'a', encoding='UTF8') as output:

        # Append Notes if exist
        if GET_NOTES == 'append' and os.path.isfile(NOTES_FILE):
            proc_time = time.time()  # Start processing time for appending
            for this_line in open(NOTES_FILE):  # only 1 line in memory
                output.write(this_line)
            # Delete chapter file
            os.remove(NOTES_FILE)
            # User feedback
            print(('{: >5}   {: <45}' + ' ' * 16 + '{:.5} sec.')
                  .format('—', '<Appending Notes to story>'[:45],
                          str(time.time() - proc_time)
                          )
                  )

        # HTML closing
        output.write('\n</body>\n</html>')

    # User feedback
    print('Serial \'' + PAGE_TITLE + '\' complete?\n'
          'Could not find a link to a \'Next\'/\'Next Chapter\' page, '
          'or stopped because link pointed to known non-story page (epilogue, '
          'afterword, author\'s blog, another story, sequel, …).\n'
          'Total time: {:.5} sec.'
          .format(time.time() - START_TIME) + '\n'  # total time
          )


if __name__ == '__main__':
    """Set serial-specific parameters, initialize variables."""

    """
    For a new serial download source:
    1. Add another 'elif'-block and set parameters:
     sys.argv[1]       Command line argument that determines serial to download
     GET_NOTES         Options for some serials
     PAGES_FILE        File name of resulting HTML file
     FIRST_LINK        URL of serial's first page
     REL_LINK_BASE     Path prefix to convert relative to absolute links
     TITLE_SEPARATE    Set to False if title and chapter are in the same tag
     WAIT_BETWEEN_REQUESTS      Time in seconds to wait between page downloads
     PARS              Parser used to find links, headlines, content
                       Available parsers, select one that works well:
                       • 'lxml' (fastest, lenient)
                       • 'html.parser' (decent speed, lenient, Python built-in)
                       • 'html5lib' (very slow, extremely lenient, parses pages
                                  like a web browser does, creates valid HTML5)
    
    2. Set other parameters in the if-branches in the script above:
     In find_next_link(), if required:
         A soup.find()     What defines a link to the next page
     In get_wanted_content_tags(), if required:
         chap_title_tag    What defines the tag holding the page headline
         chap_cont_tag     What defines the tag holding the page content
     Add a declutter_XXXXX(), 
         For any unwanted clutter to decompose and delete
    
    3. Add argument to all appropriate '(WHICH_SERIAL [in | ==]' conditions
    """

    # 'Glow-worm'
    if len(sys.argv) > 1 and sys.argv[1] == 'Glowo':
        PAGE_TITLE = 'Glow-worm'
        FIRST_LINK = 'https://parahumans.wordpress.com/2017/10/21/glowworm-p-1/'
        PARS = 'html5lib'  # the others don't handle this html style well

    # 'Pact'
    elif len(sys.argv) > 1 and sys.argv[1] == 'Pact':
        PAGE_TITLE = 'Pact'
        FIRST_LINK = 'http://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/'
        PARS = 'lxml'

    # 'SICP' (Structure and Interpretation of Computer Programs)
    elif len(sys.argv) > 1 and sys.argv[1] == 'SICP':
        PAGE_TITLE = 'Structure and Interpretation of Computer Programs'
        PAGES_FILE = 'StructInterprCompProg.html'
        FIRST_LINK = ('https://mitpress.mit.edu/'
                      'sicp/full-text/book/book.html')
        REL_LINK_BASE = 'https://mitpress.mit.edu/sicp/full-text/book/'
        TITLE_SEPARATE = False  # header and chapter are the same tag
        PARS = 'html5lib'  # the others don't handle this html style well

    # 'T5D'
    elif len(sys.argv) > 1 and sys.argv[1] == 'T5D':
        PAGE_TITLE = 'The Fifth Defiance'
        FIRST_LINK = 'https://thefifthdefiance.com/2015/11/02/introduction/'
        PARS = 'lxml'

    # 'Twig'
    elif len(sys.argv) > 1 and sys.argv[1] == 'Twig':
        PAGE_TITLE = 'Twig'
        FIRST_LINK = ('https://twigserial.wordpress.com/'
                      '2014/12/24/taking-root-1-1/')
        PARS = 'lxml'

    # 'Unsong'
    elif len(sys.argv) > 1 and sys.argv[1] == 'Unsong':
        PAGE_TITLE = 'Unsong'
        FIRST_LINK = 'https://unsongbook.com/prologue-2/'
        PARS = 'lxml'
        GET_NOTES = 'chrono'  # Default: chronological order w/story pages
        if len(sys.argv) == 3:
            if sys.argv[2] == '--omit' or sys.argv[2] is None:
                GET_NOTES = 'omit'  # None
                PAGES_FILE = PAGE_TITLE + '-Notes_omitted.html'
            if sys.argv[2] == '--append':
                GET_NOTES = 'append'  # Copy after story end
                PAGES_FILE = PAGE_TITLE + '-Notes_appended.html'
            if sys.argv[2] in ('--chronological', '--chrono'):
                GET_NOTES = 'chrono'
                PAGES_FILE = PAGE_TITLE + '.html'

    # 'Ward'
    elif len(sys.argv) > 1 and sys.argv[1] == 'Ward':
        PAGE_TITLE = 'Ward'
        FIRST_LINK = 'https://www.parahumans.net/2017/09/11/daybreak-1-1/'
        # •••••••••• might need html5lib depending on Ward's html •••••••••••
        PARS = 'lxml'

    # 'Worm'
    elif len(sys.argv) > 1 and sys.argv[1] == 'Worm':
        PAGE_TITLE = 'Worm'
        FIRST_LINK = 'https://parahumans.wordpress.com/2011/06/11/1-1/'
        PARS = 'lxml'

    # No correct arguments for serial selection were stated
    else:
        print('\nSerial to download not or incorrectly stated.\n'
              'Usage:\nChapterChainer.py {Glowo, Pact, SICP, T5D, Twig, '
              'Unsong [--append | --chrono[logical] | --omit], '
              'Ward, Worm}\n'
              )
        sys.exit()

    # Check for correct arguments for Unsong options
    if sys.argv[1] == 'Unsong':
        if len(sys.argv) == 2:
            print('\nDefaulting to --chronological\n')
        else:
            if sys.argv[2] not in \
                    ('--omit', '--append', '--chronological', '--chrono'):
                print('\nOptions for Notes pages incorrectly stated.\n'
                      'Usage:\nChapterChainer.py {Pact, SICP, T5D, Twig, '
                      'Unsong [--append | --chrono[logical] | --omit], '
                      'Ward, Worm}\n'
                      )
                sys.exit()

    # Constants not set before, including some defaults
    WHICH_SERIAL = sys.argv[1]
    if 'PAGES_FILE' not in locals():
        PAGES_FILE = PAGE_TITLE + '.html'
    if 'GET_NOTES' not in locals():
        GET_NOTES = ''
    if 'WAIT_BETWEEN_REQUESTS' not in locals():
        WAIT_BETWEEN_REQUESTS = 0
    if 'TITLE_SEPARATE' not in locals():
        TITLE_SEPARATE = True
    NOTES_FILE = PAGE_TITLE + '_temp.html'
    START_TIME = time.time()  # For total time

    start_end_serial_download()  # Start actual processing
