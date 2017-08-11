# Dependencies: BeautifulSoup(bs), request,lxml
import bs4 as bs,urllib.request,csv
# Initializing List variable which stores company details.
company_details=[]
# Header for CSV file.
company_details.append(['Company Name', 'Address', 'Phone No', 'Mobile No','Website'])
# The website has the category list which has several company details listed under that category.
# As we are considering strictly Agriculture businesses.
# http://www.businesslist.com.ng/category/agriculture/ is the link for all the agriculture businesses
# The problem with the website is that they block you IP if we try to scrape it. So after few request it will block your IP address.
# As each page has only 20 records so we need to iterate to all the pages to get 1000 records.
# Using this 20 records we can get the link of the company page on this website which has the require content
# Like, Company Name, Address, Phone No, Mobile No, Website. They do not have any email Address information.
for page_no in range(1,57):
    # Just to show on which page we're on
    print(page_no)
    try:
        # Make first request to get the list of first 20 records from the given link using urllib request
        web_page_request = urllib.request.urlopen('http://www.businesslist.com.ng/category/agriculture/'+str(page_no)).read()
        # convert the response into BeautifulSoup object with lxml library
        soup_web_page = bs.BeautifulSoup(web_page_request,'lxml')
        # Print the header
        header = str(soup_web_page.h1.string)
        print(header)
        # If header is not 'Agriculture in Nigeria' that means you're IP has been suspended / blocked
        if header.find("Agriculture in Nigeria") != -1:
            # Find all the divs which has the attribute class as links.
            # It has the links to contact information page
            for get_links in soup_web_page.findAll('div', attrs={'class':'links'}):
                # Initializing the company info variable where we will store company information and then append it to company_details
                company_info = []
                # request to get the page of particular company
                company_info_request = urllib.request.urlopen('http://www.businesslist.com.ng'+get_links.a.get('href'))
                # convert response to BeautifulSoup object
                soup_company_info = bs.BeautifulSoup(company_info_request,'lxml')
                # Get the name of the company from the header.
                company_info.append(soup_company_info.h1.text)
                # Get all the divs which has the atrribute class as info.
                for get_info in soup_company_info.findAll('div', attrs={'class':'info'})[:5]:
                    # The div contains two div. Second div has the value.
                    get_contact_info = get_info.findAll('div')
                    if len(get_contact_info) > 1:
                        # append it to company info
                        company_info.append(get_contact_info[1].text)
                # append all the company information to company_details list
                company_details.append(company_info)
        else:
            # if you're IP is blocked or suspended then exit the loop.
            print("You're blocked!!!")
            break
    except:
        pass
# Finally store the list of companies into .csv file.
with open('company_details.csv', 'a') as company_details_files:
    # Open company_details.csv
    w = csv.writer(company_details_files, lineterminator='\n')
    # Append list into CSV file.
    w.writerows(company_details)
    print('List of companies saved to file.csv')
