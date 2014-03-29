#!/usr/bin/env python

import urllib2
import lxml.html
from lxml import etree
from sys import argv

#You need to specify the tag that the link is wrapped in, if no tag exists use
#body
#You need to specify the class name the link is wrapped in.  If no class name
#exists, you will need to write a new scrapper
#You need to specify how the site moves from page to page.  So for backpage,
#this is done by base_page?page=number
#So if we are looking for escorts, we move from page to page by doing the
#following
#http://newyork.backpage.com/FemaleEscorts/?page=1 <- first page
#http://newyork.backpage.com/FemaleEscorts/?page=2 <- second page
#base html is where to start scraping from.

def link_grab(num_pages, tags, class_name, next_page, html_base):
    to_grab = []
    pages = []
    listing = []

    for i in xrange(num_pages):
        pages.append(next_page+str(i))

    to_grab.append(html_base)
    for i in xrange(num_pages):
        to_grab.append(html_base + next_page)

    for html in to_grab:
        url = urllib2.urlopen(html)
        to_text = url.read()
        to_lxml = lxml.html.fromstring(to_text)
        links = to_lxml.xpath('//' + tags + "[@class=\"" + class_name + "\"]/a")
        print(links)
        for i in links:
            listing.append(str(i.attrib['href']))

    return listing

def contents_grab(tag, class_name, links):
   content = []

   for i in links:
      to_text = urllib2.urlopen(str(i.strip("\n"))).read()
      to_lxml = lxml.html.fromstring(to_text)
      contents = to_lxml.xpath("//" + tag + "[@class='" + class_name + "']")
      contents = etree.tostring(contents[0])
      content.append([html, contents])

   with open("contents.txt", "a") as f:
      for i in content:
         f.write(i[0]+"\n")
         f.write(i[1]+"\n")

def main():
    if len(argv) != 2:
        print "Missing arg"
        exit(0)
    links = link_grab(int(argv[1]), "div", "cat", "?page=",
            "http://newyork.backpage.com/FemaleEscorts/")
    contents_grab("div", "postingBody", links)

if __name__ == "__main__":
    main()

