#!python3
# -*- coding: utf-8 -*-
"""
Download serial web pages into one file.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#   This script downloads serial web pages into one html file.                #
#   Available serials are:                                                    #
#                                                                             #
#   Wildbow (John C. McCrae)   'Worm'                                         #
#                              'Pact'                                         #
#                              'Twig'                                         #
#   Scott Alexander            'Unsong' (Author’s Notes optional)             #
#                                                                             #
#   The script follows the 'Next' or 'Next Chapter' link of each page, does   #
#   some formatting and cleanup of the retrieved html, and outputs all        #
#   chapters to one large HTML file. No Table of Contents page is required.   #
#   Remarks not pertaining to the story (announcements/greetings/etc.) on     #
#   some story pages are omitted.                                             #
#   See code for how to add new serials or fix broken links.                  #
#                                                                             #
#       Required:   Python 3, BeautifulSoup4,                                 #
#       Optional:   lxml and html5lib for PARSer alternatives                 #
#                                                                             #
#   Usage:                                                                    #
#         python3 ChapterChainer.py [Pact | Twig | Worm | Unsong]             #
#   Unsong only: Option for Author's Notes and Postscript:                    #
#         [--omit | --append | --chrono[logical]]                             #
#         '--omit' skips these pages, '--append' puts them after the story,   #
#         and '--chronological' (or '--chrono') leaves them interspersed      #
#         between chapters in order of publication.                           #
#   Title argument is case sensitive.                                         #
#                                                                             #
#   Please donate to the authors for their writing! Using this script can     #
#   deny them some needful income from advertising.                           #
#   Easy donation options are on their sites.                                 #
#   And you can vote daily on topwebfiction.com if you enjoy reading.         #
#        Worm:    https://parahumans.wordpress.com/                           #
#                 http://topwebfiction.com/vote.php?for=worm                  #
#        Pact:    https://pactwebserial.wordpress.com/                        #
#                 http://topwebfiction.com/vote.php?for=pact                  #
#        Twig:    https://twigserial.wordpress.com/                           #
#                 http://topwebfiction.com/vote.php?for=twig                  #
#        Unsong:  Patreon link on http://slatestarcodex.com/                  #
#                 http://topwebfiction.com/vote.php?for=unsong                #
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

DEVELOPERS:
Some editors secretly replace the unicode non-breaking space (\xA0) with a
space. To check, let editor show 'Invisibles' (or 'Spaces' or 'Whitespace'):
If '( )' looks like '( )', you may have lost that character, which is used
in search or replace. (The script should have the capability to treat ' '
(space), ' ' ('\xA0'), and '&nbsp;' (html entity) differently because they
may be have been (ab)used for layout purposes in the serials to download.)
"""

import html
import os
import os.path
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request

import bs4


# import html5lib  # If lxml or html.parser set @ ('PARS = …') not working


def download_page(next_link, raw_html_file):
    """Download page to temporary file"""

    # Timing
    down_time = time.time()  # Start download time

    # Save retrieved html to temp file.
    # (Keep the 'try..' for debugging connections and leave broad despite
    # pylint complaining.)
    try:
        # Spoof the User-Agent, in case Python is a blacklisted agent
        # and receives a 403. Valid agents e.g. @
        # https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
        request = urllib.request.Request(next_link, data=None, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 \
            Safari/537.36'})
        with urllib.request.urlopen(request) as response:
            with open(raw_html_file, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
    except Exception as inst:
        print('\nCould not retrieve next page. Is this link broken?\n\'' +
              next_link + '\'\n\n')
        print(type(inst))   # exception instance
        print(inst.args)    # arguments stored in .args
        print(inst)         # __str__ allows args to be printed directly
        sys.exit()          # stop gracefully

    # Timing
    down_time = str(time.time() - down_time)  # Download time

    return down_time


def find_next_link(soup):
    """Return a link to the next page"""

    # 'Worm', 'Pact', 'Twig', 'Unsong'
    # (Keep 'if..' for later additions.)
    if PAGE_TITLE in ('Worm', 'Pact', 'Twig', 'Unsong'):
        if soup.find('a', {'rel': 'next'}) is not None:  # find by 'rel'='next'
            maybe_link = soup.find('a', {'rel': 'next'})['href']
        else:
            this_re = re.compile(r'(Next)(( |( )|&nbsp;)+Chapter)?')  # by Text
            if soup.find('a', text=this_re) is not None:  # ^^^^ ( ) is a \xA0
                maybe_link = soup.find('a', text=this_re)['href']
            else:
                maybe_link = None

    # Store url if found, replace broken links
    # noinspection PyUnboundLocalVariable
    if maybe_link is not None:
        # noinspection PyUnboundLocalVariable
        next_link = urllib.parse.quote(maybe_link, safe='/:%')

#    To work around links that have slipped detection or are broken,
#    repeat for each link:
#    1. duplicate commented explanation and 'if' block below,
#    2. uncomment it, and
#    3. insert page of broken link, broken link url, working url.
#    The Twig 8.3 page below is a real world example.
#
#       # Broken URL in The_broken_links_page
#       if (next_link == 'Broken_link'):
#           next_link = 'Working_link'

        # Broken URL in Twig 8.3
        if next_link == ('//twigserial.wordpress.com/'
                         '2015/12/17/bleeding-edge-8-4/'):
            next_link = ('https://twigserial.wordpress.com/'
                         '2015/12/17/bleeding-edge-8-4/')
    else:
        next_link = ''

    return next_link


def get_wanted_content_tags(soup):
    """Get tags that hold headline and wanted content"""

    # 'Worm', 'Pact', 'Twig'
    if PAGE_TITLE in ('Worm', 'Pact', 'Twig'):
        chap_title_tag = soup.find('h1', {'class': 'entry-title'})
        chap_cont_tag = soup.find('div', {'class': 'entry-content'})

    # 'Unsong'
    if PAGE_TITLE == 'Unsong':
        chap_title_tag = (soup.find('h1', {'class': 'pjgm-posttitle'}))
        chap_cont_tag = (soup.find('div', {'class': 'pjgm-postcontent'}))

    # noinspection PyUnboundLocalVariable
    return chap_title_tag, chap_cont_tag


def check_note(chap_title):
    """Check if downloaded page is a Notes page"""

    # Check title for Notes page
    this_re = re.compile(r'^(Author.s Note|Postscript)')  # Unsong
    is_note = this_re.search(chap_title)

    return is_note


def declutter_wildbow(chap_title_tag, chap_cont_tag):
    """Remove clutter in wanted tags of Wildbow's pages, convert to strings"""

#    # Keep to identify unwanted content
#    if (chap_cont_tag.find_all('a')) is not None:
#        for i in(chap_cont_tag.find_all('a')):
#            print(i)

    # 'Pact'
    if PAGE_TITLE == 'Pact':
        # Advertisement
        for i in chap_cont_tag.find_all('div', {'class': 'wpcnt'}):
            i.decompose()
        for i in chap_cont_tag.find_all('style', {'type': 'text/css'}):
            i.decompose()
        # Unlinked link text
        for i in chap_cont_tag.find_all('strong', text='Last Chapter'):
            i.decompose()

    # 'Twig'
    if PAGE_TITLE == 'Twig':
        # Mysterious white dot
        for i in chap_cont_tag.find_all('span', {'style': 'color:#ffffff;'},
                                        {'text': '.'}
                                        ):
            i.decompose()

    # 'Worm', 'Pact', 'Twig'
    if PAGE_TITLE in ('Worm', 'Pact', 'Twig'):

        # Navigation links
        this_re = re.compile(r'(\s|( )|&nbsp;)*(Previous|Next|L?ast|About|'
                             r'( *The *)?End(\s*\(Afterword\))?)'
                             r'(\s|( )|&nbsp;)*(Chapter)?(\s|( )|&nbsp;)*'
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
        this_re = re.compile(r'^(\s|( )|&nbsp;)*$')  # ( ) is a \xA0
        #  '( )' aka '\xA0' breaks this
        this_tag_list = [this_tag for this_tag in all_tags
                         if (this_re.match(this_tag.text) and
                             this_tag.name != 'br'
                             )]
        for this_tag in this_tag_list:
            this_tag.decompose()

        # Tags to string
        out_title = html.unescape(str(chap_title_tag))
        out_chap = html.unescape(str(chap_cont_tag))

        # Standardize several kinds of breaks to newline
        out_chap = '\n'.join(out_chap.splitlines())

        # Collapse 2 or 3 spaces after punctuation, some visible entities, or
        # rendering formatting tags
        # noinspection Annotator  -- Pycharm Inspect Code: ignore
        this_re = re.compile(r'([,\.;\:\!\?…’”a-zA-Z0-9]|'  # literals
                             r'(&.?[^s][^p];){3,10};|'  # entities
                             r'(</?(b|i|em|del|strong|span)>))'  # tags
                             r'(\s|( )|&nbsp;){2,3}'  # ( ) is a \xA0
                             )
        out_title = this_re.sub(r'\1 ', out_title)
        out_chap = this_re.sub(r'\1 ', out_chap)

        # No space/newline before AND after certain tags
        this_re = re.compile(r'(\s|( )|&nbsp;)'  # ( ) is a \xA0
                             r'(</?(b|i|em|del|strong|span)>)'
                             r'(\s|( )|&nbsp;)'  # ( ) is a \xA0
                             )
        out_title = this_re.sub(r'\3 ', out_title)
        out_chap = this_re.sub(r'\3 ', out_chap)

    # Un-tag 'Worm' story text in '< >'
    if PAGE_TITLE == 'Worm':
        tags_to_ident = ([('<Walk!>', '&lt;Walk!&gt;'),
                          ('<Walk or->', '&lt;Walk or-&gt;'),
                          ('<Faster!>', '&lt;Faster!&gt;'),
                          ('<Wal-', '&lt;Wal-'),
                          ('-k!>', '-k!&gt;')
                          ])
        for from_tag, to_ident in tags_to_ident:
            # noinspection PyUnboundLocalVariable
            out_chap = out_chap.replace(from_tag, to_ident)

    # noinspection PyUnboundLocalVariable
    return out_title, out_chap


def declutter_unsong(chap_title_tag, chap_cont_tag):
    """Remove clutter in wanted tags of Unsong pages, convert to strings"""

#    # Keep to identify unwanted content
#    if (chap_cont_tag.find_all('a')) is not None:
#        for i in(chap_cont_tag.find_all('a')):
#            print(i)

    # Navigation links
    this_re = re.compile(r'(prev|next)')
    for i in chap_cont_tag.find_all('a', {'rel': this_re}):
        i.decompose()

    # Social web
    for i in chap_cont_tag.find_all(
            'div', {'class': 'sharedaddy sd-sharing-enabled'}):
        i.decompose()

    # Tags to string
    out_title = str(chap_title_tag)
    out_chap = str(chap_cont_tag)

    # 'End of Book…' Season's greetings
    this_re = re.compile(r'(<hr/>\n<p></p><center><b>End of Book [^<]+)'
                         '<.+(</b></center>)', re.DOTALL
                         )
    out_chap = re.sub(this_re, r'\1\2', out_chap)

    # Author's Note announcements
    this_re = re.compile(  # '<hr/>\n<p> …'
        r'<hr/>\n<p>(<font size="1">|<i>)+.+'
        '(<a href="https?://unsongbook.com/authors-note-).+'
        '((</i>|</font>)+</p>|((<br/>\n.?)+</center>))', re.DOTALL
    )
    out_chap = re.sub(this_re, '', out_chap)

    this_re = re.compile(  # '<p>[ …' ;  '[^C]' b/c '[Content warning:…'
        r'<p>(<font size="1">|<i>)+\[[^C].+'
        '(<a href="https?://unsongbook.com/authors-note-).+'
        '((</i>|</font>)+</p>|((<br/>\n.?)+</center>))', re.DOTALL
    )
    out_chap = re.sub(this_re, '', out_chap)

    this_re = re.compile(  # '<p></p><center>…'
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
                         r'593197826365/.>here</a> \(thanks Ben.\)</p>\n)'
                         , re.DOTALL
                         )
    out_chap = re.sub(this_re, '', out_chap)

    return out_title, out_chap


def process_page(next_link, page_count, write_to_file):
    """Download & process page, repeat until no next link"""

    while next_link != '':

        # Set temporary file for downloaded html
        raw_html_file = PAGE_TITLE + '-' + str(page_count) + '.html'

        # #### Downloading page ####
        down_time = download_page(next_link, raw_html_file)

        # Start processing time
        proc_time = time.time()

        # Open temporary file with Beautiful Soup to process html.
        soup = bs4.BeautifulSoup(open(raw_html_file, encoding='utf-8'), PARS)

        # Get url of next chapter
        next_link = find_next_link(soup)

        # Get tags holding headline and content
        (chap_title_tag, chap_cont_tag) = get_wanted_content_tags(soup)

        # Get page title
        chap_title = chap_title_tag.get_text()

        # Check if Notes page
        is_note = check_note(chap_title)

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
                          str(time.time() - proc_time)
                          )
                  )

        else:
            # Process page content, one def per html style
            if PAGE_TITLE in ('Worm', 'Pact', 'Twig'):
                # Remove clutter
                (out_title, out_chap) = declutter_wildbow(chap_title_tag,
                                                          chap_cont_tag)

            if PAGE_TITLE == 'Unsong':
                # Remove clutter
                (out_title, out_chap) = declutter_unsong(chap_title_tag,
                                                         chap_cont_tag)

                # Write to story or notes file?
                if GET_NOTES == 'append' and is_note:
                    write_to_file = NOTES_FILE
                else:
                    write_to_file = PAGES_FILE

            # Append chapter title and content strings to story or notes file
            with open(write_to_file, 'a', encoding='UTF8') as output:
                # noinspection PyUnboundLocalVariable
                output.write(out_title)
                # noinspection PyUnboundLocalVariable
                output.write(out_chap)

            # Delete chapter file
            os.remove(raw_html_file)

            # User feedback, incl. processing time
            trunc_title = (chap_title[:44] + (chap_title[44:] and '…'))
            print('{: >5}   {: <45}   {:.5} sec.   {:.5} sec.'
                  .format(page_count, trunc_title[:45], str(down_time),
                          str(time.time() - proc_time))
                  )

        # if (page_count >= 2): next_link = ''  # Sample for testing
        time.sleep(WAIT_BETWEEN_REQUESTS)


def start_end_serial_download():
    """Prepare download, call downloading & processing, complete page"""

    # User feedback headline
    print('Downloading \'' + PAGE_TITLE + '\' to file \'' + PAGES_FILE
          + '\'...\nCount   Page Title                                     '
          'Downloading   Processing'
          )

    # Files to write; don't append to existing files
    if os.path.isfile(PAGES_FILE):
        os.remove(PAGES_FILE)

    if GET_NOTES == 'append':
        if os.path.isfile(NOTES_FILE):
            os.remove(NOTES_FILE)

    # Initial file to append content
    write_to_file = PAGES_FILE

    # Write html opening
    with open(PAGES_FILE, 'a', encoding='UTF8') as output:
        output.write('<html>\n<head>\n<title>' + PAGE_TITLE +
                     '</title>\n<meta content=\'text/html; charset=UTF-8\' '
                     'http-equiv=\'Content-Type\'>\n</head>\n<body>\n')

    # #### Call recursive download on first chapter ####
    process_page(FIRST_LINK, 0, write_to_file)  # zero page_count

    # Append Notes and closing
    with open(PAGES_FILE, 'a', encoding='UTF8') as output:
        # Append Notes if exist; large Notes file might need too much memory
        if GET_NOTES == 'append' and os.path.isfile(NOTES_FILE):
            print('app+  notes+')
            proc_time = time.time()  # Start processing time for appending
            output.write(open(NOTES_FILE, 'r').read())  # all in memory
            # Delete chapter file
            os.remove(NOTES_FILE)
            # User feedback
            print('{: >5}   {: <45}                {:.5} sec.'
                  .format('—', '<Appending Notes to story>'[:45],
                          str(time.time() - proc_time)
                          )
                  )
        # HTML closing
        output.write('\n</body>\n</html>')
    # User feedback
    print('Could not find a link to a \'Next\'/\'Next Chapter\' page.\n'
          '  Serial \'' + PAGE_TITLE + '\' complete?\n'
          '  Total time: {:.5} sec.'
          .format(time.time() - START_TIME) + '\n'  # total time
          )


if __name__ == '__main__':
    """Set serial-specific parameters, initialize variables."""

# For a new serial download source:
# 1. Add another 'if'-block and set parameters:
# sys.argv[1]    Command line argument that determines serial to download
# GET_NOTES      Options for some serials
# PAGE_TITLE     Script argument determining serial to download
# PAGES_FILE     File name of resulting HTML file
# FIRST_LINK     URL of serial's first page
# WAIT_BETWEEN_REQUESTS Time in seconds to wait between page downloads
# PARS           Parser used to find links, headlines, content
#   Available parsers, select one that works well:
#       'lxml' (fastest, lenient)
#       'html.parser' (decent speed, lenient, Python built-in)
#       'html5lib' (very slow, extremely lenient, parses pages the same way
#                   a web browser does, creates valid HTML5)
# print          A motto (if you like)
#
# 2. Set other parameters in the if-branches above:
# Parameters that define a link to the next page
# soup_headline  defines the page headline
# soup_content   Tag that defines the page content
# Unwanted clutter to decompose
#
# 3. Add argument to all appropriate '(PAGE_TITLE in ...' conditions

    if len(sys.argv) > 1 and sys.argv[1] == 'Worm':
        PAGE_TITLE = sys.argv[1]
        PAGES_FILE = PAGE_TITLE + '.html'
        FIRST_LINK = 'https://parahumans.wordpress.com/2011/06/11/1-1/'
#        WAIT_BETWEEN_REQUESTS = 0
        PARS = 'lxml'
        print('\n\n                 "'
              'the sword devoureth one as well as modify them,'
              '\n                  '
              'because it allows us to ignore'
              '\n                  '
              'the details of the query-system implementation.'
              '"\n                                '
              '(kingjamesprogramming.tumblr.com)\n'
              )

    if len(sys.argv) > 1 and sys.argv[1] == 'Pact':
        PAGE_TITLE = sys.argv[1]
        PAGES_FILE = PAGE_TITLE + '.html'
        FIRST_LINK = 'http://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/'
#        WAIT_BETWEEN_REQUESTS = 0
        PARS = 'lxml'
        print('\n\n               "'
              'Suppose we are modeling incomplete knowledge about'
              '\n                '
              'the world of our forefathers, but this one brought'
              '\n                '
              'the horror right into our own daily life!'
              '"\n                                 '
              '(kingjamesprogramming.tumblr.com)\n'
              )

    if len(sys.argv) > 1 and sys.argv[1] == 'Twig':
        PAGE_TITLE = sys.argv[1]
        PAGES_FILE = PAGE_TITLE + '.html'
        FIRST_LINK = ('https://twigserial.wordpress.com/'
                      '2014/12/24/taking-root-1-1/')
#        WAIT_BETWEEN_REQUESTS = 0
        PARS = 'lxml'

    if len(sys.argv) > 1 and sys.argv[1] == 'Unsong':
        PAGE_TITLE = sys.argv[1]
        PAGES_FILE = PAGE_TITLE + '.html'
        FIRST_LINK = 'https://unsongbook.com/prologue-2/'
#        WAIT_BETWEEN_REQUESTS = 0
        PARS = 'lxml'
        GET_NOTES = 'chrono'  # Default
        if len(sys.argv) == 3:
            if sys.argv[2] not in ('--omit', '--append', '--chronological',
                                   '--chrono'
                                   ):
                print('\nOptions for Unsong incorrectly stated.\n'
                      'Usage: python3 Book_worm.py Unsong '
                      '[--omit|--append|--chrono[logical]]\n'
                      )
                sys.exit()
            if sys.argv[2] == '--omit' or sys.argv[2] is None:
                GET_NOTES = 'omit'  # None
                PAGES_FILE = PAGE_TITLE + '-Notes_omitted.html'
            if sys.argv[2] == '--append':
                GET_NOTES = 'append'  # Copy after story end
                PAGES_FILE = PAGE_TITLE + '-Notes_appended.html'
            if sys.argv[2] in ('--chronological', '--chrono'):
                GET_NOTES = 'chrono'  # In chronological order w/story pages
                PAGES_FILE = PAGE_TITLE + '.html'
        print('\n\n       "he instructed about the song, because he was '
              'basically insane."\n                                     '
              '(kingjamesprogramming.tumblr.com)\n'
              )

    # Check for correct argument (serial, options)
    if len(sys.argv) <= 1 or (sys.argv[1]
                              not in ('Worm', 'Pact', 'Twig', 'Unsong')):
        print('\n_serial to download not or incorrectly stated.\n'
              'Usage: python3 Book_worm.py [Pact|Twig|Worm|Unsong]\n'
              )
        sys.exit()

    START_TIME = time.time()  # For total time

    # Not set constants
    if 'GET_NOTES' not in locals():
        GET_NOTES = ''
    if 'WAIT_BETWEEN_REQUESTS' not in locals():
        WAIT_BETWEEN_REQUESTS = 0

    # noinspection PyUnboundLocalVariable
    NOTES_FILE = PAGE_TITLE + '_temp.html'

    start_end_serial_download()
