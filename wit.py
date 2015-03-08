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
# TODO - graph idea for deeper model of text
#from pygraph.classes.graph import graph

def mimic(text):
  mimic_dict = {}
  for line in text:
    words = line.split()
    if len(words) > 1:
      for i, word in enumerate(words[:-1]):
        mimic_dict[word] = mimic_dict.get(word, []) + [words[i + 1]]
      # Use empty string as successor for last word
      mimic_dict[word[-1]] = mimic_dict.get(word[-1], []) + ['']
  return mimic_dict

def parrot(text, numchars):
  mimic_dict = mimic(text)
  res = ''
  current_word = sample([line.split()[0] for line in text], 1)[0]
  numchars -= len(current_word)
  while numchars > 0:
    res += current_word
    current_word = sample(mimic_dict.get(current_word, ['']), 1)[0]
    if current_word:
      numchars -= len(current_word)
    else:
      numchars = 0  # found no word, stop here
    if numchars > 0:
      res += ' '
      numchars -= 1
  return res

def main():
  hn = HackerNews()
  top_stories = [hn.item(top_story) for top_story in hn.top_stories()[:30]]
  # Currently just grabbing direct descendants, which may be more natural anyway
  most_discussed = max(top_stories,
                       key=lambda story:len(story.kids)
                       if hasattr(story, 'kids') else 0)
  comments = [hn.item(kid) for kid in most_discussed.kids]
  new_comment = parrot([comment.text for comment in comments
                        if hasattr(comment, 'text')], 117)
  # For now, just print the 'clever' comment
  if hasattr(most_discussed, 'title'):
    print most_discussed.title
  print new_comment

if __name__ == "__main__":
  main()
