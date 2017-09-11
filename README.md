ChapterChainer
====

This script downloads serial web pages into one html file.
Available serials are:

* Wildbow (John C. McCrae):
  * [*Worm*](https://parahumans.wordpress.com/)
  * [*Pact*](https://pactwebserial.wordpress.com/)
  * [*Twig*](https://twigserial.wordpress.com/) (as published so far)
* Scott Alexander: [*Unsong*](http://unsongbook.com/) (Author’s Notes optional)

The script follows the *Next* or *Next Chapter* link of each page, does some formatting and cleanup of the retrieved html, and outputs all chapters to one large HTML file. No Table of Contents page is required. 

Non-story remarks (announcements/greetings/etc.) on some story pages are omitted. 

See code for how to add new serials or fix broken links. 

Required
----

Python 3,
[BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/Download)

Optional
----
Alternatives to built-in html parser:

[lxml](https://pypi.python.org/pypi/lxml), [html5lib](https://github.com/html5lib/html5lib-python)

Usage
-----

`python3 ChapterChainer.py [Pact|Twig|Worm|Unsong]`

Unsong only: Optional switches for Author's Notes and Postscript:

`[--omit | --append | --chrono[logical]]`

`omit` skips these pages, `append` puts them after the story, and `chronological` (or `chrono`) leaves them interspersed between chapters in order of publication. 

The title argument is case sensitive.

Known Issues
-----
Pages not published at the time of this script update may not be found if the Next link has been changed.

Social and Legal
----
Please donate to the authors for their writing! Using this script can deny them some needful income from advertising. Easy donation options are on their sites.
And you can vote daily on topwebfiction.com if you enjoy reading.

* Worm:
  * https://parahumans.wordpress.com/
  * http://topwebfiction.com/vote.php?for=worm
* Pact:
  * https://pactwebserial.wordpress.com/
  * http://topwebfiction.com/vote.php?for=pact
* Twig:
  * https://twigserial.wordpress.com/
  * http://topwebfiction.com/vote.php?for=twig
* Unsong:
  * Patreon link on http://slatestarcodex.com/
  * http://topwebfiction.com/vote.php?for=unsong

This script must not be used to publish a serial without its author's permission. (This would severely curtail their chances to sell the manuscript, and with no money to make they may give up writing for the web altogether. Also, few could afford the punitive damage for a lost film series deal of something big like 'Worm'. Sorry for the moralizing.) Enjoy reading!

Credits
-----
This project contains code originally (c) 2014 JordanSekky (https://github.com/JordanSekky/BookWorm).

____

*"3:16 All scripture is given by a procedural argument to instantiate."*
*[(kingjamesprogramming.tumblr.com)](http://kingjamesprogramming.tumblr.com/)*
