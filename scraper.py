# -*- coding: utf-8 -*-
import os
import csv
import pdb
import argparse
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Scrapes the Yoruba word list and saves results locally.')
	parser.add_argument('username', type=str, help="Your sketch.co.uk username")
	parser.add_argument('password', type=str, help="Your sketch.co.uk password")
	parser.add_argument('--min_freq', type=int, help="Only download words that show up min_freq times in the corpus", default=2)
	parser.add_argument('--output_filename', type=str, help="Basename of csv file to write to")

	args = parser.parse_args()

	urls = {
		'word_list_form': "https://the.sketchengine.co.uk/corpus/wordlist_form?corpname=preloaded/yorubawac15"
	}

	try:
		chromedriver_path = os.path.abspath("chromedriver")
		browser = webdriver.Chrome(executable_path=chromedriver_path)

		# Login - Please specify your credentials from command line args!
		browser.get(urls['word_list_form'])
		browser.find_element_by_id('id_username').send_keys(args.username)
		browser.find_element_by_id('id_password').send_keys(args.password)
		browser.find_element_by_xpath('//*[@id="in-body"]/form/fieldset/div/input[2]').submit()

		# pdb.set_trace()

		# Create word list with specified parameters
		freq_field = browser.find_element_by_xpath('//*[@id="wordlist_form"]/fieldset[1]/table/tbody/tr[2]/td[3]/input')
		freq_field.clear()
		freq_field.send_keys(args.min_freq)
		browser.find_element_by_xpath('//*[@id="wordlist_form"]/div/input').submit()

		# Copy all words
		output_path = args.output_filename if args.output_filename else 'output_{0}_freqs.csv'.format(args.min_freq)
		
		with open(output_path, 'w+') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['WORD', 'FREQUENCY'])

			while True:
				table = browser.find_element_by_xpath('//*[@id="content"]/table/tbody')
				for row in table.find_elements_by_tag_name('tr'):
					word = row.find_element_by_xpath('.//td[1]').text
					freq = row.find_element_by_xpath('.//td[2]/a').text
					freq = int(freq.replace(',', ''))
					print((word, freq))
					writer.writerow([word.encode('utf-8'), freq])

				try:
					browser.find_element_by_id('next2').click()
				except NoSuchElementException:
					break
	finally:
		pass
		# browser.quit()


