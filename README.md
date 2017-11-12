-----

*"3:16 All scripture is given by a procedural argument to instantiate."*

[(kingjamesprogramming.tumblr.com)](http://kingjamesprogramming.tumblr.com/)

-----

# ChapterChainer

This script downloads serial web pages. It follows the *Next* or *Next Chapter* link of each page (no 'Table of Contents' page is required), does some formatting and cleanup of the retrieved html, and outputs all chapters to one large HTML file. 

ChapterChainer is heavily commented and uses descriptive variable names to make adding new serials fairly easy. Non-story pages (such as 'Author's Notes') can optionally be skipped or appended to the story.

Currently built-in serials are:

* Abelson, Sussman & Sussman: [*Structure and Interpretation of Computer 
Programs*](https://mitpress.mit.edu/sicp/full-text/book/book.html), 2nd edition ('SICP')
* Alexander, Scott: [*Unsong*](http://unsongbook.com/) (Author’s Notes optional, non-story announcements/greetings omitted)
* Walter: [*The Fifth Defiance*](https://thefifthdefiance.com/about/) ('T5D')
* Wildbow (John Charles McCrae):
  * [*Glow-worm*](https://parahumans.wordpress.com/2017/10/21/glowworm-p-1/) ('Glowo')
  * [*Pact*](https://pactwebserial.wordpress.com/)
  * [*Twig*](https://twigserial.wordpress.com/)
  * [*Ward*](https://www.parahumans.net/)
  * [*Worm*](https://parahumans.wordpress.com/)

### Required

Python 3,
[BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/Download), [lxml](https://pypi.python.org/pypi/lxml), [html5lib](https://github.com/html5lib/html5lib-python)

### Usage

Invoke the script with one of the titles, and one of the switches if applicable. Use the abbreviations where listed above. All arguments are *case sensitive*:

`ChapterChainer.py {Glowo, Pact, SICP, T5D, Twig, Unsong, Ward, Worm}`

Optional switches for Author's Notes and Postscript (currently for *'Unsong' only*): 

  `[--omit | --append | --chrono[logical]]`
 
 `--omit` skips these pages, `--append` collects and puts them after the story, the default `--chronological` (or `--chrono`) keeps them interspersed between chapters in order of publication.

Examples:

`ChapterChainer.py Unsong --omit` downloads Unsong without the non-story pages to the working directory.

`ChapterChainer.py Glowo` downloads 'Glow-worm' to the working directory. 

### Known Issues

Pages not published at the time of this script update may not be found if the 'Next' link has been changed. 

Links from a story to epilogue, afterword, author's blog, next story, etc. are not followed.

### Social and Legal

_Please donate to the authors for their writing!_ Using this script can deny them some needful income from advertising. Easy donation options are on their sites.
And you can _vote daily on topwebfiction.com_ if you enjoy reading.

* Glow-worm:
  * https://parahumans.wordpress.com/
  * (not listed in topwebfiction so far)
* Pact:
  * https://pactwebserial.wordpress.com/
  * http://topwebfiction.com/vote.php?for=pact
* Structure and Interpretation of Computer Programs:
  * ???
* The Fifth Defiance:
  * ???
  * http://topwebfiction.com/vote.php?for=the-fifth-defiance
* Twig:
  * https://twigserial.wordpress.com/
  * http://topwebfiction.com/vote.php?for=twig
* Unsong:
  * http://slatestarcodex.com/ (no own donation link for the serial)
  * http://topwebfiction.com/vote.php?for=unsong
* Ward:
  * https://www.parahumans.net/
  * (not listed in topwebfiction so far)
* Worm:
  * https://parahumans.wordpress.com/
  * http://topwebfiction.com/vote.php?for=worm

_This script must not be used to publish a serial without its author's permission._ (This would severely curtail their chances to sell the manuscript, and with no money to make they may give up writing for the web altogether. Also, few could afford the punitive damage for a lost film series deal of something big like 'Worm'. Sorry for the moralizing.) 

Enjoy reading!

### Credits

This project contains code originally (c) 2014 JordanSekky (https://github.com/JordanSekky/BookWorm).
