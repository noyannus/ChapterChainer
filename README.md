-----

*"3:16 All scripture is given by a procedural argument to instantiate."*

[(kingjamesprogramming.tumblr.com)](http://kingjamesprogramming.tumblr.com/)

-----

# ChapterChainer

This script downloads serial web pages. It follows the *Next* or *Next Chapter* link of each page (no 'Table of Contents' page is required), does some formatting and cleanup of the retrieved html, and outputs all chapters to one large HTML file. 

ChapterChainer is heavily commented and uses descriptive variable names to make adding new serials fairly easy. Non-story pages (such as 'Author's Notes') can optionally be skipped or appended to the story.

### Currently built-in serials

* Abelson, Sussman & Sussman: [*Structure and Interpretation of Computer 
Programs*](https://mitpress.mit.edu/sicp/full-text/book/book.html), 2nd edition ('SICP')
* Alexander, Scott: [*Unsong*](http://unsongbook.com/) (Author’s Notes optional, non-story announcements/greetings omitted)
* Walter: [*The Fifth Defiance*](https://thefifthdefiance.com/about/) ('T5D')

### Required

Python 3,
[BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/Download), [lxml](https://pypi.python.org/pypi/lxml), [html5lib](https://github.com/html5lib/html5lib-python)

### Usage

`ChapterChainer.py Title [option] [URL]`

`ChapterChainer.py URL`

Invoke the script with one of the builtin titles (`SICP`, `T5D`, `Unsong`), 
one of the switches if applicable (see below), your start URL if you don't want to start at the serial's first page. 

Alternatively, just state the URL where you want to start downloading.

All arguments are case sensitive. 

Optional switches for pages not being part of the story (e.g., Author's 
Notes, Greetings, Postscript); currently only for 'Unsong':

`[--omit | --append | --chrono[logical]]`

`-omit` skips these pages, `--append` collects and puts them after the story, the default `--chronological` (or `--chrono`) keeps them interspersed between chapters in order of publication.

##### Example:

`ChapterChainer.py Unsong --omit` downloads Unsong without the non-story pages to the working directory.

### Known Issues

Pages not published at the time of this script update may not be found if the 'Next' link has been changed. Links from a story to epilogue, afterword, author's blog, next story, etc. are not followed.

### Social and Legal

_Please donate to the authors for their writing!_ Using this script can deny them some needful income from advertising. Easy donation options are usually on their sites.
And you can _vote daily on topwebfiction.com_ if you enjoy reading.

* Structure and Interpretation of Computer Programs:
 * ???
* The Fifth Defiance:
 * ???
 * http://topwebfiction.com/vote.php?for=the-fifth-defiance
* Unsong:
 * http://slatestarcodex.com/
 * http://topwebfiction.com/vote.php?for=unsong

**This script must not be used to publish or circulate a serial without its author's permission.** This would severely curtail their chances to sell the manuscript, and with no money to make they may give up writing for the web altogether. Also, few could afford the punitive damage for a lost film series deal. Sorry for the moralizing. Wildbow's works have been deleted from the built-in serials because [he does not endorse scraping](https://www.parahumans.net/f-a-q/).

### Credits

This project contains code originally (c) 2014 JordanSekky (https://github.com/JordanSekky/BookWorm).
