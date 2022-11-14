import json
import random
import re
import requests

from bs4 import BeautifulSoup
from math import ceil


def categories():
	cat_list = list()

	category_url = 'http://www.brainyquote.com/topics.html'
	html = requests.get(category_url)
	soup = BeautifulSoup(html.text, "html.parser")

	# Get all links with href matching the regex
	category = soup.find_all('a', {"href": re.compile("/topics/")})
	for name in category:
		cat_list.append(name.text.strip())

	return cat_list


def authors():
	aut_list = list()
	aut_list_html = list()

	author_url = 'http://www.brainyquote.com/authors.html'
	html = requests.get(author_url)
	soup = BeautifulSoup(html.text, "html.parser")

	# Get all links with href matching the regex
	author = soup.find_all('a', {"href": re.compile("/authors/")})
	for name in author:
		author_name = name.text.strip()
		if len(author_name) > 1 and "Authors" not in author_name and "More" not in author_name:
			aut_list.append(author_name)
			aut_name_html = author_name.replace(" ", "-").replace(".", "").lower()
			aut_list_html.append(aut_name_html)

	return aut_list, aut_list_html


def retrieve_quote_from_url(url_base, numberOfQuotes):
	quotes_list = list()

	url = url_base + ".html"
	html = requests.get(url)
	soup = BeautifulSoup(html.text, features="html.parser")

	# div id of the quotes are generated by position with the format:
	# "qpos_%page%_%element%"
	# where element <- [1, .. 26] and page <- [1..] with infinite scroll
	times = 1
	if numberOfQuotes > 26:
		# Scrolling is required as there are not enough quotes in the page
		times = ceil(numberOfQuotes / 26)
		print("Getting %d pages..." % times)

	x = y = n = 0
	while n < numberOfQuotes:
		y = (y % 26) + 1  # List starts at 1
		if y == 1:  # New Page must be loaded
			x += 1
			# We can get each page individually with "%category%_[1..]"
			url = url_base + "_" + str(x)
			html = requests.get(url)
			soup = BeautifulSoup(html.text, features="html.parser")

		divID = "pos_" + str(x) + "_" + str(y)
		find = soup.find("div", {"id": divID})
		if find is not None:
			quotes_list.append(find.text.replace('\n\n\n\n', '\n').strip())

		n += 1

	return quotes_list


def quotes_category(category, numberOfQuotes):
	url_base = "http://www.brainyquote.com/quotes/topics/" + category
	return retrieve_quote_from_url(url_base, numberOfQuotes)


def quotes_author(author, numberOfQuotes):
	url_base = "https://www.brainyquote.com/authors/" + author + "-quotes"
	return retrieve_quote_from_url(url_base, numberOfQuotes)


def get_random_quote(category=None):
	cats = categories()
	c_category = None
	if category:
		for cat in cats:
			if category.lower() in cat.lower():
				c_category = cat
	if not c_category:
		c_category = random.choice(cats)
	cit = quotes_category(c_category, 40)
	random_int = random.randrange(len(cit))
	return cit[random_int]


def get_random_quote_author(author=None):
	auts1, auts2 = authors()
	c_author = None
	if author:
		for index, aut in enumerate(auts1):
			if author.lower() in aut.lower():
				c_author = auts2[index]
	if not c_author:
		c_author = random.choice(auts2)
	cit = quotes_author(c_author, 40)
	random_int = random.randrange(len(cit))
	return cit[random_int]


if __name__ == "__main__":
	# Demo: Get 40 quotes of the category 'Amazing'
	# print("Category '%s'" % categories()[2])
	# demoResult = quotes_category(categories()[2], 40)
	# print("Got %d quotes" % len(demoResult))
	# if len(demoResult) > 0:
	# 	print("Example: %s" % demoResult[0])
	print("-----")
	print(get_random_quote())
	print("-----")
	print(get_random_quote_author())
	print("-----")
	print(get_random_quote_author("Peterson"))
	print("---")
	print(get_random_quote("robe"))


