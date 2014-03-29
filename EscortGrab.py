#!/usr/bin/env python

import urllib2
import lxml.html
from lxml import etree
from sys import argv, exit
import re
import os

# You need to specify the tag that the link is wrapped in, if no tag exists use
# body
# You need to specify the class name the link is wrapped in. If no class name
# exists, you will need to write a new scrapper
# You need to specify how the site moves from page to page. So for backpage,
# this is done by base_page?page=number
# So if we are looking for escorts, we move from page to page by doing the
# following
# http://newyork.backpage.com/FemaleEscorts/?page=1 <- first page
# http://newyork.backpage.com/FemaleEscorts/?page=2 <- second page
# base html is where to start scraping from.

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


def contents_grab(links, tag_list, attr_list, attr_name_list,
        post_process_funcs, post_process_args):
   data = []

   for i in xrange(len(post_process_funcs)):
       if post_process_funcs[i] == None:
           post_process_funcs[i] = lambda x, arglist: x

   extract_list = zip(tag_list, attr_list, attr_name_list, post_process_funcs,
           post_process_args)

   for link in links:
      link = str(link)
      to_lxml = lxml.html.fromstring(urllib2.urlopen(link).read())
      result = [ link ]
      for tag, attr, attr_name, func, func_args in extract_list:
          try:
            contents = to_lxml.xpath("//" + tag + "[@" + attr + "=\"" +
                    attr_name + "\"]")[0]
            result.append(func(etree.tostring(contents), func_args))
          except(IndexError):
              pass
      data.append(result)

   return data

def extractWithPattern(contents, listOfArguments):
    if len(listOfArguments) != 1:
        raise Exception
    contentsList = contents.split("\n")
    regex = listOfArguments[0]
    for line in contentsList:
        isMatch = regex.match(line.strip())
        if isMatch != None:
            target = isMatch.group(0)
            if len(target) > 0:
                return target
        else:
            return "No Match"

def main():
    result_filename = "contents.txt"
    locationMatch = re.compile('[a-z A-Z]+(, [a-z A-Z]+)+')
    ageMatch      = re.compile('Poster\'s age: [0-9]+')

    if len(argv) != 2:
        print "Missing arg"
        exit(0)

    links = link_grab("http://newyork.backpage.com/FemaleEscorts/",
            int(argv[1]), "div", "cat", "?page=")
    content_data = contents_grab(links,
            ["p", "div", "div"],
            ["class", "style", "class"],
            ["metaInfoDisplay", "padding-left:2em;", "postingBody"],
            [ extractWithPattern, extractWithPattern, None ],
            [ [ ageMatch ], [ locationMatch ], [] ])

    print_headers = os.path.exists(result_filename)

    with open(result_filename, "a") as f:
      if not print_headers:
        f.write("Link, Age, Location, Content\n")

      for result in content_data:
        for i in xrange(0, len(result)):
            print(i)
            if i == len(result) - 1:
                f.write(result[i] + "\n")
            else:
                f.write(result[i] + ",")
    print("{0} results found".format(len(content_data)))


if __name__ == "__main__":
    main()

