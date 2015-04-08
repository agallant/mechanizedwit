#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       wit.py
#      
#       Copyright 2014 www.soycode.com
#      
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#      
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#      
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from random import sample
from hackernews import HackerNews
from chatterbot import ChatBot


class HackerInsight:
  """Generates Markov-style comments based on HN discussion."""
  def __init__(self):
    self.hn = HackerNews()
    self.stories = []
    self.comments = []
    self.mimic_dict = {}
    self.processed_comments = 0

  def get_new_comments(self):
    """Pull fresh most-discussed story and get comments from it."""
    top_stories = [self.hn.item(top_story) for top_story
                   in self.hn.top_stories()[:30]  # makes frontpage only
                   if top_story not in [story.id for story in self.stories]]
    # Currently just grabbing direct descendants, which may be more natural anyway
    self.stories.append(max(top_stories,
                            key=lambda story:len(story.kids)
                            if hasattr(story, 'kids') else 0))
    comments = [self.hn.item(kid) for kid in self.stories[-1].kids]
    # Extending means past comments will be remembered/combined - revisit
    self.comments.extend([comment.text for comment in comments
                          if hasattr(comment, 'text')])

  def build_mimic_dict(self):
    """Take a list of strings and return Markov state dict word->word list."""
    for line in self.comments[self.processed_comments:]:
      words = line.split()
      if len(words) > 1:
        for i, word in enumerate(words[:-1]):
          self.mimic_dict[word] = self.mimic_dict.get(word, []) + [words[i + 1]]
        # Use empty string as successor for last word
        self.mimic_dict[word[-1]] = self.mimic_dict.get(word[-1], []) + ['']
    self.processed_comments = len(self.comments)

  def generate_comment(self, numchars=117):
    """Generate a comment from Markov states, default Tweet+link length."""
    res = ''
    # Randomly sample first word from all comments first words, then grow
    current_word = sample([line.split()[0] for line in self.comments], 1)[0]
    numchars -= len(current_word)
    while numchars > 0:
      res += current_word
      current_word = sample(self.mimic_dict.get(current_word, ['']), 1)[0]
      if current_word:
        numchars -= len(current_word)
      else:
        numchars = 0  # found no word, stop here
      if numchars > 0:
        res += ' '
        numchars -= 1
    return res


class BackTalker:
  """Use ChatBot to remember replies and generate new ones."""
  def __init__(self):
    self.chatbot = ChatBot()
    # TODO: decide how to train, e.g. from tweets/CleverBot/etc.


def main():
  # For now, just make and run a single time
  hi = HackerInsight()
  hi.get_new_comments()
  hi.build_mimic_dict()
  # Just print out basic story info and a comment
  print(hi.stories[-1].title)
  print(hi.stories[-1].id)
  print(hi.stories[-1].url)
  print(hi.generate_comment())
  # And run another story to make sure it's next-most discussed
  hi.get_new_comments()
  hi.build_mimic_dict()
  print(hi.stories[-1].title)
  print(hi.stories[-1].id)
  print(hi.stories[-1].url)
  print(hi.generate_comment())


if __name__ == "__main__":
  main()
