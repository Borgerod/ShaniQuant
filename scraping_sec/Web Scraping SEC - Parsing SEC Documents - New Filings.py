#!/usr/bin/env python
# coding: utf-8

# # Parsing SEC Documents - New Filings

# ## Introduction:
# In this notebook, we will go over how to parse SEC filing documents so you can extract different content from it and also logically organize the information. Making additional parsing more natural.
# 
# At this point, it's safe to say that there is a remarkable amount of data available to individuals who seek high-quality financial data across a multitude of companies. This data can be used in a range of activities, from competition analysis to sentiment analysis. All it requires the individual to do is define a company they want, filing that belongs to that company, and the file that contains the information.
# 
# Right now, we've defined a few ways to search for information depending on the type of search you want to conduct:
# 
# 1. **Broad Search:**
#     - You don't care what is returned, and you want all the filings for a given period. This search is best acheived by parsing the different index directories. These directories list all the filings made for a given period. While probably the most simple to wrap your head around, this returned the most significant amount of data. Making data management a priority.
# 2. **Company Specific Search:**
#     - You are looking for a specific company and all their filings. There are currently two ways of doing this, using the CIK method or EDGAR Search Method. If you used the CIK method, you followed a technique that was similar to the Broad search method. Instead of looking at a specific period, you provide the CIK number, which will take you to a directory that contains all the filings that the company has made. Inside each filing folder, you would find all the files for that particular filing. If you didn't know the CIK number, you looked it up and did the CIK method. If you didn't know the CIK number you leveraged the EDGAR Search Method. Using this strategy meant requesting a URL that would direct you to a table containing all the filings for that company. However, this method required us to make a more complex script that would parse XML strings, paginating if the company had multiple pages, and reconstructing links to other directories.
# 3. **Filing Specific Search:**
#     - Here you want only a specific filing for a particular company. Again this can be achieved either using the CIK Search Method or the EDGAR Search Method. It solely depends on whether you have the information upfront or not. The only additional piece of information you needed was the accession number.
# 4. **Criteria Specific Search:**
#     - Here you were looking for a filing that has specific criteria, like the form being a 10K, a particular SIC number, or a particular date. This could only be achieved using the EDGAR Search Method, where you built a URL that contains the criteria you were searching on. In this case, your search was relatively simple because you only provided one rule. This search returns either an HTML or XML version of the data, which you would then have to parse.
# 5. **Multi-Criteria Search:**
#     - This is similar to a form specific search, but instead of only having one criterion, you were searching on multiple criteria. The only difference here is you had to build and request a URL that contained multiple parameters. Once you got the data, it was parsed the same.
# 6. **Text Search:**
#     - This type of search was done if you wanted to search on information found in the HEADER file for each filing. This allowed us to do the most complex searches as we could use boolean operators, wildcards, stemming, the order of evaluation, and phrase searching. While a powerful tool that allowed your searches to become very customized, it did require a decent working knowledge of both the HEADER file and search functionality. This was challenging as documentation is limited, requiring a fair amount of experimentation.
# 
# Regardless of your particular search method, each can give you access to filings that match the criteria you specified. Once you've landed on the filing, you want to scrape. You can begin the process of extracting the information.
# 
# ## Libraries
# Surprisingly, we don't need that many libraries to scrape the SEC filing. In this particular tutorial, we will use the following libraries:
# 
# 1. BeautifulSoup - This will be used to parse the actual text file content.
# 2. Requests - This will be used to request the text file from the URL provided.
# 3. Unicodedata - The text that is sent back is messy and will need to be cleaned up. We can use unicodedata to do that.
# 4. Re - This is the RegEx library for python and will make looking for keywords smooth and quick.
# 
# Depending on your specific needs, you may need extra libraries but at this point, for simplicity, we will keep it to these four.

# In[ ]:


# import our libraries
import re
import requests
import unicodedata
from bs4 import BeautifulSoup


# ## Define Text Normalization Function
# The text is a mess, so we will need to normalize it. However, we can't rely on just the `unicodedata` library to help us. Some `windows_1252_characters` will provide some challenges. I found a solution on Stack Overflow that'll help us normalize the remaining portions of the data. All this function does is take a string, finds any qualifying matches, decodes those matches, and then replaces them in the string. In essence, it's just cleaning up the characters that weren't decoded by the unicodedata library.

# In[ ]:


def restore_windows_1252_characters(restore_string):
    """
        Replace C1 control characters in the Unicode string s by the
        characters at the corresponding code points in Windows-1252,
        where possible.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''
        
    return re.sub(r'[\u0080-\u0099]', to_windows_1252, restore_string)


# ## Grab the Document Content
# Let's grab the document first. In my case, I have a URL that'll direct me to a text file found on the SEC website. I take the URL, request the content using a `GET` request, store the response in a variable called `response`, and then pass through the content into our BeautifulSoup parser object. Make sure to specify the `lxml` parser.
# 
# ### Old Vs. New
# This is an excellent time to mention document structure and how structure changes depending on the filing's age. In newer filings, the HTML code is very well structured, meaning the tags are correct and allow us to go into extraordinary detail when we parse the info. In older filings, the HTML code is not well strucutred. To give you an idea of what you'll encounter, entire content will b stored in tags called `<PAGE>` and tables that don't have normal `td` and `tr` elements. This is just listing a few.
# 
# Unfortunately, the scraping strategy we leverage will depend on the age of the filing. Additionally, I can't say with confidence at what point in time a filing is considered "old" as I haven't explored enough filings to find a pattern. I'm assuming most of us don't need to go far back in time to collect data, so this series focuses on the "newer" filings. In other words, those filings that have will define HTML code inside the text file.
# 
# If you're curious as to what an example of an older and newer filing would look like, I've provided a link to two different text files for two separate filings. 
# 
# **Newer Filing:**
# 
# https://www.sec.gov/Archives/edgar/data/1166036/000110465904027382/0001104659-04-027382.txt
# 
# **Older Filing:**
# 
# https://www.sec.gov/Archives/edgar/data/1750/0000912057-94-002818.txt

# In[ ]:


# define the url to specific html_text file
new_html_text = r"https://www.sec.gov/Archives/edgar/data/1166036/000110465904027382/0001104659-04-027382.txt"

# grab the response
response = requests.get(new_html_text)

# pass it through the parser, in this case let's just use lxml because the tags seem to follow xml.
soup = BeautifulSoup(response.content, 'lxml')


# ## Defining Our Master Dictionary To House Filings
# Assuming you want to parse more than one filing, we will need to create a structure that allows for a natural hierarchy. This hierarchy will provide a defined path to each component of our filing, while still being flexible enough to grow as you need to add different pieces.
# 
# At the highest level, we have our `master_filings_dict`, which will contain all the filings we scrape. For this to work, we need a mechanism that provides a unique identifier to serve as our dictionary key. In this case, the `accession_number` will work perfectly as it's unique for every filing.
# 
# From here, we will have an `accession` dictionary, which will contain two parts:
# 
# 1. One for the SEC Header content, which is found at the top of every filing.
# 2. One for the filing documents, which will contain all the documents for a filing.
# 
# To be clear, a filing can contain multiple documents. For example, a filing can include a 10-K document and an exhibit document. You must remember this it will help you understand the upcoming sections.

# In[ ]:


# define a dictionary that will house all filings.
master_filings_dict = {}

# let's use the accession number as the key. This 
accession_number = '0001104659-04-027382'

# add a new level to our master_filing_dict, this will also be a dictionary.
master_filings_dict[accession_number] = {}

# this dictionary will contain two keys, the sec header content, and a documents key.
master_filings_dict[accession_number]['sec_header_content'] = {}
master_filings_dict[accession_number]['filing_documents'] = None


# ## Examing the SEC-Header Tag
# 
# Honestly, I would not want to scrape this poriton of the filing. The reason why is it's a bunch text that isn't strucutred well. Also you probably can get this information from somewhere else in the filing and have it be more structured. However, there may be some information in this part that people want. Here's a simple solution. Grab first, and parse later.

# In[ ]:


# grab the sec-header tag, so we can store it in the master filing dictionary.
sec_header_tag = soup.find('sec-header')

# store the tag in the dictionary just as is.
master_filings_dict[accession_number]['sec_header_content']['sec_header_code'] = sec_header_tag

# display the sec header tag, so you can see how it looks.
display(sec_header_tag)


# ## Parsing the documents
# 
# Now the fun part, grabbing all the documents. This isn't too bad, just do a find all with the `document` tag and loop through the results. However, I want to take some time and give you an idea of the natural structure of the text file.
# 
# At this point, we know that a filing contains two main elements:
# 
# 1. A header
# 2. A document collection.
# 
# We've seen from up above that the header while challenging to parse, contains more information like time of filing, company info, and more contextual data. Some of this data requires going through multiple levels to get it. For example, the company zip requires going into the header, then the filer, then the business address, and finally, you'll arrive at the company zip code.
# 
# The reason I mention this is because it helps you understand that some of the info exists deep in the document hierarchy. To get this info means traversing the hierarchy, in some cases, multiple times for each document in a filing. Continuing, a `document` has another hierarchy:
# 
# 1. type
# 2. sequence
# 3. filename
# 4. description
# 5. text
# 
# Additionally, the `text` tag contains all the HTML code for our document, which has its own structure that can change depending on the document you're looking at. The vital point to take away is that a hierarchy is there and can be beneficial for storage purposes and searching.
# 
# In the code I present below, I try to maintain the hierarchy as much as possible — no sense of wasting something that is already there. However, I do modify it in some instances to meet my requirements. For example, I break each document into pages and store those pages in a document dictionary. I also have search results stored at a page level and, in some cases, at a document level.
# 
# It's not to say that one is better than the other, but more to show that you can approach this task in multiple ways. The way you decide to go with will depend on the problem you're trying to solve.

# In[ ]:


# initalize the dictionary that will house all of our documents
master_document_dict = {}

# find all the documents in the filing.
for filing_document in soup.find_all('document'):
    
    # define the document type, found under the <type> tag, this will serve as our key for the dictionary.
    document_id = filing_document.type.find(text=True, recursive=False).strip()
    
    # here are the other parts if you want them.
    document_sequence = filing_document.sequence.find(text=True, recursive=False).strip()
    document_filename = filing_document.filename.find(text=True, recursive=False).strip()
    document_description = filing_document.description.find(text=True, recursive=False).strip()
    
    # initalize our document dictionary
    master_document_dict[document_id] = {}
    
    # add the different parts, we parsed up above.
    master_document_dict[document_id]['document_sequence'] = document_sequence
    master_document_dict[document_id]['document_filename'] = document_filename
    master_document_dict[document_id]['document_description'] = document_description
    
    # store the document itself, this portion extracts the HTML code. We will have to reparse it later.
    master_document_dict[document_id]['document_code'] = filing_document.extract()
    
    
    # grab the text portion of the document, this will be used to split the document into pages.
    filing_doc_text = filing_document.find('text').extract()

    
    # find all the thematic breaks, these help define page numbers and page breaks.
    all_thematic_breaks = filing_doc_text.find_all('hr',{'width':'100%'})
    
    
    '''
        THE FOLLOWING CODE IS OPTIONAL:
        -------------------------------
        
        This portion will demonstrate how to parse the page number from each "page". Now I would only do this if you
        want the ACTUAL page number on the document, if you don't need it then forget about it and just wait till the
        next seciton.
        
        Additionally, some of the documents appear not to have page numbers when they should so there is no guarantee
        that all the documents will be nice and organized.
    
    '''
    
    
    
    # grab all the page numbers, first one is usually blank
    all_page_numbers = [thematic_break.parent.parent.previous_sibling.previous_sibling.get_text(strip=True) 
                        for thematic_break in all_thematic_breaks]
    
    
    '''
    
        If the above list comprehension doesn't make sense to you, here is how it would look as a regular loop.
    
        # define a list to house all the page numbers
        all_page_numbers = []

        # loop throuhg all the thematic breaks.
        for thematic_break in all thematic_breaks:

           # this would grab the page number tag.
           page_number = thematic_break.parent.parent.previous_sibling.previous_sibling

           # this would grab the page number text
           page_number = page_number.get_text(strip=True)
           
           # store it in the list.
           all_page_numbers.append(page_number)

    '''
    
    # determine the number of pages, will be used for the upcoming if conditions.
    length_of_page_numbers = len(all_page_numbers)
    
    # as long as there are numbers to change then proceed.
    if length_of_page_numbers > 0:
        
        # grab the last number
        previous_number = all_page_numbers[-1]
        
        # initalize a new list
        all_page_numbers_cleaned = []
        
        # loop through the old list in reverse order.
        for number in reversed(all_page_numbers):
            
            # if it's blank proceed to cleaning.
            if number == '':
                
                # the tricky part, there are three scenarios.

                # the previous one we looped was 0 or 1.
                if previous_number == '1' or previous_number == '0':
                    
                    # in this case, it means this is a "new section", so restart at 0.
                    all_page_numbers_cleaned.append(str(0))
                    
                    # reset the page number and the previous number.
                    length_of_page_numbers = length_of_page_numbers - 1
                    previous_number = '0'
                
                # the previous one we looped it wasn't either of those.
                else:
                    
                    # if it was blank, take the current length, subtract 1, and add it to the list.
                    all_page_numbers_cleaned.append(str(length_of_page_numbers - 1))
                    
                    # reset the page number and the previous number.
                    length_of_page_numbers = length_of_page_numbers - 1
                    previous_number = number

            else:
                
                # add the number to the list.
                all_page_numbers_cleaned.append(number)
                
                # reset the page number and the previous number.
                length_of_page_numbers = length_of_page_numbers - 1
                previous_number = number
    else:
        
        # make sure that it has a page number even if there are none, just have it equal 0
        all_page_numbers_cleaned = ['0']
    
    # have the page numbers be the cleaned ones, in reversed order.
    all_page_numbers = list(reversed(all_page_numbers_cleaned))
    
    # store the page_numbers
    master_document_dict[document_id]['page_numbers'] = all_page_numbers
    
    
    '''
        -------------------------------
          THE OPTIONAL CODE HAS ENDED
        -------------------------------
    
        This next portion of code is really what made this all possible. Up above you saw I grabbed all the thematic
        breaks from our document because they sever as natural page breaks. Without those thematic breaks I'm not sure
        if this would be such an easy process. It's not to say we couldn't break it into pages, but I would bet the code
        would be more complex.
    
    '''
    
    
    # convert all thematic breaks to a string so it can be used for parsing
    all_thematic_breaks = [str(thematic_break) for thematic_break in all_thematic_breaks]
    
    # prep the document text for splitting, this means converting it to a string.
    filing_doc_string = str(filing_doc_text)

    
    # handle the case where there are thematic breaks.
    if len(all_thematic_breaks) > 0:
    
        # define the regex delimiter pattern, this would just be all of our thematic breaks.
        regex_delimiter_pattern = '|'.join(map(re.escape, all_thematic_breaks))

        # split the document along each thematic break.
        split_filing_string = re.split(regex_delimiter_pattern, filing_doc_string)

        # store the document itself
        master_document_dict[document_id]['pages_code'] = split_filing_string

    # handle the case where there are no thematic breaks.
    elif len(all_thematic_breaks) == 0:

        # handles so it will display correctly.
        split_filing_string = all_thematic_breaks
        
        # store the document as is, since there are no thematic breaks. In other words, no splitting.
        master_document_dict[document_id]['pages_code'] = [filing_doc_string]
    

    # display some information to the user.
    print('-'*80)
    print('The document {} was parsed.'.format(document_id))
    print('There was {} page(s) found.'.format(len(all_page_numbers)))
    print('There was {} thematic breaks(s) found.'.format(len(all_thematic_breaks)))
    

# store the documents in the master_filing_dictionary.
master_filings_dict[accession_number]['filing_documents'] = master_document_dict

print('-'*80)
print('All the documents for filing {} were parsed and stored.'.format(accession_number))


# ## Normalizing Text
# 
# Okay, so at this point, we are in pretty good shape. We have all the documents, they've been split into their pages and have been stored in the dictionary. From here, we can proceed to further data cleaning and transformation. Now, I will add a little bit of a disclosure. Technically, we could have done some of this cleaning up above, but for organizational purposes, I decided to loop through everything again and parse it that way.
# 
# This would increase the amount of time it will take to run your code, but it is easier to follow. I will provide a more "optimized" script that will do the cleaning up above and store that on GitHub. Another drawback to this method is that I pass through all the code for each page back through BeautifulSoup. The reason why is the tags have been slightly messed up during the extraction and have to be fixed. I haven't run into many hiccups with this, but there is no guarantee that this will be the case for every filing type.
# 
# You might be asking why I am doing this method if there are these drawbacks. Well, I find I have a little bit more control over the process when it comes to leveraging patterns in the HTML code. These patterns will help us to find section headers, titles, and other "meaningful" components of the page that will provide context as to what it contains. This will serve to be useful down the road when we want to look for particular parts of a paragraph.

# In[ ]:


# first grab all the documents
filing_documents = master_filings_dict[accession_number]['filing_documents']


# loop through each document
for document_id in filing_documents:
    
    # display some info to give status updates.
    print('-'*80)
    print('Pulling document {} for text normilzation.'.format(document))
    
    # grab all the pages for that document
    document_pages = filing_documents[document_id]['pages_code']
    
    # page length
    pages_length = len(filing_documents[document_id]['pages_code'])
    
    # initalize a dictionary that'll house our repaired html code for each page.
    repaired_pages = {}
    
    # initalize a dictionary that'll house all the normalized text.
    normalized_text = {}

    # loop through each page in that document.
    for index, page in enumerate(document_pages):
        
        # pass it through the parser. NOTE I AM USING THE HTML5 PARSER. YOU MUST USE THIS TO FIX BROKEN TAGS.
        page_soup = BeautifulSoup(page,'html5')
        
        # grab all the text, notice I go to the BODY tag to do this
        page_text = page_soup.html.body.get_text(' ',strip = True)
        
        # normalize the text, remove messy characters. Additionally, restore missing window characters.
        page_text_norm = restore_windows_1252_characters(unicodedata.normalize('NFKD', page_text)) 
        
        # Additional cleaning steps, removing double spaces, and new line breaks.
        page_text_norm = page_text_norm.replace('  ', ' ').replace('\n',' ')
                
        
        '''
            NOTES FROM UP ABOVE:
            --------------------
            
            Remember up above, where I had some optional code. Well, this is where we add page numbers. If you notice
            I simply take the index add 1 to it and with that we now have a page number. Now, this doesn't technically
            follow the sections in each document but I don't think most people will care. Also we will see that we can
            infer the sections from other parts.
        
        '''
        
        # define the page number.
        page_number = index + 1
        
        # add the normalized text to the list.
        normalized_text[page_number] = page_text_norm
        
        # add the repaired html to the list. Also now we have a page number as the key.
        repaired_pages[page_number] = page_soup
    
        # display a status to the user
        print('Page {} of {} from document {} has had their text normalized.'.format(index + 1, 
                                                                                     pages_length, 
                                                                                     document))

    # add the normalized text back to the document dictionary
    filing_documents[document_id]['pages_normalized_text'] = normalized_text
    
    # add the repaired html code back to the document dictionary
    filing_documents[document_id]['pages_code'] = repaired_pages
    
    # define the generated page numbers
    gen_page_numbers = list(repaired_pages.keys())
    
    # add the page numbers we have.
    filing_documents[document_id]['pages_numbers_generated'] = gen_page_numbers    
    
    # display a status to the user.
    print('All the pages from document {} have been normalized.'.format(document_id))
    


# ## Additional Scraping and Context Extraction
# 
# Alright, so now we are really in a good spot. From here on out, most of what we need to do will be relatively straight forward. By maintaining the natural hierarchy of the filing, and only expanding upon it when beneficial, we can now easily do further analysis of our data.
# 
# What I'll demonstrate next is how to get different parts of each page. Additionally, I'll show you strategies for helping to infer the "context" of each page. For example, is a page a signature page, an exhibit page, or a section page? This will help give you context and help you get to where you need to be when getting info.
# 
# Also, I'll demonstrate a strategy for how to search for keywords on each page.
# 
# Now, like I mentioned up above, this might not be the fastest way to do it, but I am trying to layout this information in a logical format that flows from section to section. I am not concerned about the speed at this point; I'm worried about you following the steps I'm doing to clean my data. I will be posting a more "optimized" script on GitHub in the future.
# 
# ## Defining Search Words
# 
# Part of the next section is helping you gain a contextual understanding of each page/document. For example, you might have the belief that certain words like `liability` are only found in pages that talk about debt. If that is the case, then we can define a list of words and see if they are found on any of the pages of our document. If they are, we can store the matches in our master dictionary.
# 
# With some background, let's define some words we might want to search for. Also, these are just guesses, and there is no guarantee that they will be the words we want. Unfortunately, you might have to read a few documents to determine the words that most appear in certain parts of the document.

# In[ ]:


search_dict = {
    
    # these could possibly be words that help us find pages that discuss financial statements.
    'financial_words':['liability', 'asset'],
    
    # these could possible be words that help us find sections that discuss administration topics.
    'admin_words':['administration', 'government']
}


# In[ ]:


# first grab all the documents
filing_documents = master_filings_dict[accession_number]['filing_documents']

# loop through each document
for document_id in filing_documents:
    
    
    ####################################
    # THIS WILL HANDLE THE WORD SEARCH #
    ####################################
    
    
    # let's grab the normalized text in this example, since it's cleaned and easier to search
    normalized_text_dict = filing_documents[document_id]['pages_normalized_text']  
            
    # initalize a dictionary to store all the tables we find.
    matching_words_dict = {}
    
    # define the number of pages
    page_length = len(normalized_text_dict)
    
    # loop through all the text
    for page_num in normalized_text_dict:
        
        # grab the actual text
        normalized_page_text = normalized_text_dict[page_num]
        
        # each page is going to be checked, so let's have another dictionary that'll house each pages result.
        matching_words_dict[page_num] = {}
        
        # loop through each word list in the search dictionary.
        for search_list in search_dict:
            
            # grab the list of words.
            list_of_words = search_dict[search_list]
            
            # lets see if any of the words are found
            matching_words = [word for word in list_of_words if word in normalized_page_text]
            
            '''
                Again, I know list comprehension might be hard to understand so I'll show you what the loop
                looks like.
                
                # initalize a list of matching words.
                matching_words = []
                
                # loop through the list of words.
                for word in list_of_words:
                
                    # check to see if it's in the text
                    if word in normalized_page_text:
                        
                        # if it is then add it to the list.
                        matching_words.append(word)
            '''
            
            # each page will have a set of results, list of words
            matching_words_dict[page_num][search_list] = {}
            
            # let's add the list of words we search to the matching words dictionary first.
            matching_words_dict[page_num][search_list]['list_of_words'] = list_of_words
            
            # next let's add the list of matchings words to the matching words dictionary.
            matching_words_dict[page_num][search_list]['matches'] = matching_words
            
        
        # display a status to the user.
        print('Page {} of {} from document {} has been searched.'.format(page_num, page_length, document_id))
    
    
    # display a status to the user.
    print('-'*80)    
    print('All the pages from document {} have been searched.'.format(document_id))    
    
    
    ####################################
    # THIS WILL HANDLE THE LINK SEARCH #
    ####################################
    
    
    # let's grab the all pages code.
    pages_dict = filing_documents[document_id]['pages_code']  
            
    # initalize a dictionary to store all the anchors we find.
    link_anchor_dict = {}
    
    # loop through each page
    for page_num in pages_dict:
        
        # grab the actual text
        page_code = pages_dict[page_num]
        
        # find all the anchors in the page, that have the attribute 'name'
        anchors_found = page_code.find_all('a',{'name':True})
        
        # number of anchors found
        num_found = len(anchors_found)
        
        # each page is going to be checked, so let's have another dictionary that'll house all the anchors found.
        link_anchor_dict[page_num]= {(anchor_id + 1): anchor for anchor_id, anchor in enumerate(anchors_found)}        
    
        # display a status to the user.
        print('Page {} of {} from document {} contained {} anchors with names.'.format(page_num, 
                                                                                       page_length, 
                                                                                       document_id, 
                                                                                       num_found))
    
    # display a status to the user.  
    print('All the pages from document {} have been scraped for anchors with names.'.format(document_id)) 
    print('-'*80)  
    
    
    #####################################
    # THIS WILL HANDLE THE TABLE SEARCH #
    #####################################
    
         
    # let's grab the all pages code.
    pages_dict = filing_documents[document_id]['pages_code']  
            
    # initalize a dictionary to store matching words.
    tables_dict = {}
    
    # loop through each page
    for page_num in pages_dict:
        
        # grab the actual text
        page_code = pages_dict[page_num]
        
        # find all the tables
        tables_found = page_code.find_all('table')
        
        # number of tables found
        num_found = len(tables_found)
        
        # each page is going to be checked, so let's have another dictionary that'll house all the tables found.
        tables_dict[page_num] = {(table_id + 1): table for table_id, table in enumerate(tables_found)}        
    
        # display a status to the user.
        print('Page {} of {} from document {} contained {} tables.'.format(page_num, page_length, document_id, num_found))
    
    # display a status to the user.  
    print('All the pages from document {} have been scraped for tables.'.format(document_id)) 
    print('-'*80)    
    
        
    # let's add the matching words dict to the document.
    filing_documents[document_id]['word_search'] = matching_words_dict  
    
    # let's add the matching tables dict to the document.
    filing_documents[document_id]['table_search'] = tables_dict
    
    # let's add the matching anchors dict to the document.
    filing_documents[document_id]['anchor_search'] = link_anchor_dict
    


# ## Scraping Tables
# 
# Now I know for some of you that you'll want to scrape the tables. I've provided a function you can use that will take your tables dictionary and parse each table to the best of its ability. Unfortuantely this might not return perfect results, but it's a good starting point for you to build off of.
# 
# One of the biggest challenges is that tables are formatted with blank rows and columns. Making it difficult to determine the "true" number of rows and columns.

# In[ ]:


def scrape_table_dictionary(table_dictionary):
    
    # initalize a new dicitonary that'll house all your results
    new_table_dictionary = {}
    
    if len(table_dictionary) != 0:

        # loop through the dictionary
        for table_id in table_dictionary:

            # grab the table
            table_html = table_dictionary[table_id]
            
            # grab all the rows.
            table_rows = table_html.find_all('tr')
            
            # parse the table, first loop through the rows, then each element, and then parse each element.
            parsed_table = [
                [element.get_text(strip=True) for element in row.find_all('td')]
                for row in table_rows
            ]
            
            # keep the original just to be safe.
            new_table_dictionary[table_id]['original_table'] = table_html
            
            # add the new parsed table.
            new_table_dictionary[table_id]['parsed_table'] = parsed_table
            
            # here some additional steps you can take to clean up the data - Removing '$'.
            parsed_table_cleaned = [
                [element for element in row if element != '$']
                for row in parsed_table
            ]
            
            # here some additional steps you can take to clean up the data - Removing Blanks.
            parsed_table_cleaned = [
                [element for element in row if element != None]
                for row in parsed_table_cleaned.
            ]

            
    else:
        
        # if there are no tables then just have the id equal NONE
        new_table_dictionary[1]['original_table'] = None
        new_table_dictionary[1]['parsed_table'] = None
        
    return new_table_dictionary


# ## Complex Searches
# 
# In some cases, what you're trying to do might require doing a very complex search. For example, we might want the text that is centered over the page. This will give us context as to what is on the page and provide us more details of its content. This would fall under a "complex search," and to do a complex search, we will need to define some extra strategies we can take to find different parts of the page.
# 
# The beautiful thing about BeautifulSoup is we can define functions where we set our criteria and then only return tags that match those criteria. Below I've provided some example "search functions" that will help you find precise portions of your page.
# 
# ### Search For Centered Headers

# In[ ]:


def search_for_centered_headers(tag):

    # easy way to end early is check if the 'align' keet is in attributes.
    if 'align' not in tag.attrs:
        return
    
    # define the criteria.
    criteria1 = tag.name == 'p'                # I want the tag to be name of 'p'
    criteria2 = tag.parent.name != 'td'        # I want the parent tag NOT to be named 'td'
    criteria3 = tag['align'] == 'center'       # I want the 'align' attribute to be labeled 'center'.
    
    # if it matches all the criteria then return the text.
    if criteria1 and criteria2 and criteria3:         
        return tag.get_text(strip = True)


# ### Search For Bolded Text

# In[ ]:


def search_for_bolded_tags(tag):
    
    # define the criteria.
    criteria1 = tag.name == 'b'                # I want the tag to be name of 'p'
    criteria2 = tag.parent.name != 'td'        # I want the parent tag NOT to be named 'td'
    
    # if it matches all the criteria then return the text.
    if criteria1 and criteria2:         
        return tag.get_text(strip = True).replace('\n',' ')    


# ### Using Custom Search Functions

# In[ ]:


# first grab all the documents
filing_documents = master_filings_dict[accession_number]['filing_documents']

# loop through each document
for document_id in filing_documents:   
    
    # let's grab the all pages code.
    pages_dict = filing_documents[document_id]['pages_code']  
            
    # initalize a dictionary to store all the anchors we find.
    centered_headers_dict = {}
    
    # loop through each page
    for page_num in pages_dict:
        
        # grab the actual text
        page_code = pages_dict[page_num]
        
        # find all the anchors in the page, that have the attribute 'name'
        centered_headers_found = page_code.find_all(search_for_centered_headers)
        
        # number of anchors found
        num_found = len(centered_headers_found)
   
        # display a status to the user.
        print('Page {} of {} from document {} contained {} centered headers.'.format(page_num, 
                                                                                     page_length, 
                                                                                     document_id, 
                                                                                     num_found))
    
    # display a status to the user.  
    print('All the pages from document {} have been scraped for centered headers.'.format(document_id)) 
    print('-'*80)  


# ## Closing Notes
# Alright at this point you understand the natural hierarchy of an SEC filing, can parse an SEC filing for it's different documents, can break those documents into pages, can normalize the text of each page, can conduct searches on those pages, can create dictionaries that follow that natural hierarchy, can parse HTML tables, and can build custom search functions.
# 
# If that sounds like a lot, it's because it is. There was a lot to this series, and it's just scratching the surface. I've seen individuals take this approach and expand on it to do a wide variety of tasks. However, what I hope this provides you is a foundation to build off of. The challenging thing about parsing documents is it's easy to get lost early on. My advice to you is to keep it simple, keep it organized, and keep it clean. Most importantly, keep it organized!
# 
# The easiest way to take a simple problem and make it a complex problem is not to keep the task organized. You might also be wondering where do you go from here. The simple answer is it's up to you, and it depends on what you're doing. In some cases, it might make sense to take your numeric data and some of your text data and store it in a database. In other cases, you might want to dump your results in a text file.
# 
# Your best bet is to define what you want to do with the data, as this will help you determine the best strategy for long-term storage. All in all, I hoped you found this tutorial useful, and more importantly, hopefully, it can help relieve/automate some of your workloads.
