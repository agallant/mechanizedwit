# mechanizedwit
Because you're too busy to "socialize"
--------------------------------------

To install requirements (`easy_install` not `pip` due to [python-graph](https://code.google.com/p/python-graph/)):

    easy_install --user `cat requirements.txt`

Then it's just a matter of `python wit.py` and (after waiting on the [Hacker News API](https://github.com/HackerNews/API) for a bit) you'll get a generated comment based on the discussion in the currently most discussed HN story (out of the top 30).