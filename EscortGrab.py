#!/usr/bin/env python

import urllib2
import lxml.html
from lxml import etree
from sys import argv, exit
import os

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

def link_grab(html_base, num_pages, tags, class_name, next_page):
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
        for i in links:
            listing.append(str(i.attrib['href']))

    return listing


def contents_grab(links, tag_list, attr_list, attr_name_list, post_process_funcs):
   content = []

   for i in xrange(len(post_process_funcs)):
       if post_process_funcs[i] == None:
           post_process_funcs[i] = lambda x: x

   extract_list = zip(tag_list, attr_list, attr_name_list, post_process_funcs)

   for link in links:
      link = str(link)
      to_lxml = lxml.html.fromstring(urllib2.urlopen(link).read())
      result = [ link ]
      for tag, attr, attr_name, func in extract_list:
          contents = to_lxml.xpath("//" + tag + "[@" + attr + "=\"" + attr_name
                  + "\"]")[0]
          result.append(func(etree.tostring(contents)))
      content.append(result)
      print(type(content))

   return contents


def main():
    result_filename = "contents.txt"

    if len(argv) != 2:
        print "Missing arg"
        exit(0)

    links = link_grab("http://newyork.backpage.com/FemaleEscorts/",
            int(argv[1]), "div", "cat", "?page=")
    content_data = contents_grab(links,
            ["p", "div", "div"],
            ["class", "style", "class"],
            ["metaInfoDisplay", "padding-left:2em;", "postingBody"],
            #[ post_process_location, post_process_age, post_process_body ])
            [ None, None, None ])

    print_headers = os.path.exists(result_filename)
    
    with open(result_filename, "a") as f:
      if print_headers:
        f.write("Link, Location, Age, Content\n")

      for result in content_data:
        for i in xrange(0, len(result) - 1):
            print(type(result[i]))
            if i == len(result) - 1:
                f.write(result[i] + "\n")
            else:
                f.write(result[i] + ",")


if __name__ == "__main__":
    main()

