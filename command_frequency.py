#!/usr/bin/env python
# -*- coding: utf-8 -*-

# process emacs's command frequency file.
# See: http://xahlee.org/emacs/command-frequency.html
# 2007-08
# Xah Lee

import re
import os
from unicodedata import *

FREQFILE = ["/Users/andrea/.emacs.frequencies"]

# raw data to be read in. Each element is of the form “command:count”
rawdata={}

# a list of commands that's considered “data entry” commands.
data_entry_cmd = ["self-insert-command", "newline"]

# a list of commands that are not counted
notcmd = ["mwheel-scroll", "nil"]

# commands sharing the same keystrokes.
# also, glyph alias for some commands
cmdgroup = {
"next-line":u"↓",
"dired-next-line":u"↓",
"next-history-element":u"↓",

"previous-line":u"↑",
"dired-previous-line":u"↑",
"previous-history-element":u"↑",

"delete-backward-char":u"⌫",
"backward-delete-char-untabify":u"⌫",
"python-backspace":u"⌫",
"cperl-electric-backspace":u"⌫",

"cua-scroll-up":u"▼",
"scroll-up":u"▼",

"scroll-down":u"▲",
"cua-scroll-down":u"▲",

"isearch-forward":u"isearch-→",
"isearch-repeat-forward":u"isearch-→",

"isearch-backward":u"isearch-←",
"isearch-repeat-backward":u"isearch-←",

"backward-char":u"←",
"forward-char":u"→",
"backward-word":u"←w",
"forward-word":u"→w",
"backward-sentence":u"←s",
"forward-sentence":u"→s",
"backward-paragraph":u"↑¶",
"forward-paragraph":u"↓¶",

"move-beginning-of-line":u"|←",
"move-end-of-line":u"→|",

"beginning-of-buffer":u"|◀",
"end-of-buffer":u"▶|",

"delete-char":u"⌦",
"kill-word":u"⌦w",
"backward-kill-word":u"⌫w",
"kill-line":u"⌦l",
"kill-sentence":u"⌦s",
"kill-ring-save":u"copy",
"kill-region":u"✂",
}

# read in each line, skip those starting with “;”
# put it into a rawdata hash
for item in FREQFILE:
     f=open(item,'r')
     lines = f.readlines()
     lines = filter(lambda x: x[0]!=";",lines)
     for li in lines:
          if li == "\n": continue
          parts=re.split(r'\t',li.rstrip(),re.U)
          cnt=int(parts[0])
          cmd=parts[1]
          if cmd in notcmd: continue
          #print cmd,cnt
          if cmdgroup.has_key(cmd): cmd=cmdgroup[cmd]
          if rawdata.has_key(cmd):
               rawdata[cmd] = rawdata[cmd] + cnt
          else:
              rawdata[cmd] = cnt

#for li in lines:print li.rstrip()

# total number of commands
total_cmds = reduce(lambda x,y: x+y,rawdata.values())

# total number of non-data-entry commands
total_nd_cmds = total_cmds
for cmd in data_entry_cmd:
     if rawdata.has_key(cmd):
          total_nd_cmds -= rawdata[cmd]

# cmdData is a list, where each element is of the form:
# [command name, frequency]
# this list form is easier for sorting
cmdData=[]
for cmd, cnt in rawdata.iteritems():
     cmdData.append([cmd,cnt])

cmdData.sort(key=lambda x:x[0]) # sort the cmd names
cmdData.sort(key=lambda x:x[1], reverse=True ) # sort by frequency

print (u'<p>Total number of command calls: %7s</p>' % (total_cmds)).encode('utf-8')
#print (u'<p>Total number of non-data-entry command calls: %7s</p>' % (total_nd_cmds)).encode('utf-8')
print (u'<p>Percent of non-data-entry command calls: %2.f%%</p>' % (float(total_nd_cmds)/total_cmds*100)).encode('utf-8')

print '<table border="1">'
print u'<tr><th>Command Name</th><th>Count</th><th>% total cmd call</th><th>% non-data-entry cmd call</th></tr>'
for el in cmdData:
     cmd=el[0]
     cnt=el[1]
     percT= float(cnt)/total_cmds*100
     percND= float(cnt)/total_nd_cmds*100
     if percND > 0.1:
          print (u'<tr><td class="l">%3s</td><td>%5d</td><td>%2.2f</td><td>%2.2f</td></tr>' % (cmd,cnt,percT,percND)).encode('utf-8')

print '</table>'
