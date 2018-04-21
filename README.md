# 507final

Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

The data for this project is sourced from the American Research Center in Egypt website (arce.org) 

No API key is needed for arce.org, but a key will be needed to use the google maps API. Follow this link: (https://developers.google.com/maps/documentation/javascript/get-api-key) to create an API key and copy/paste your key in the googlekey python file provided. You may also want to review instructions for using plotly here: https://plot.ly/python/getting-started/





Any other information needed to run the program (e.g., pointer to getting started info for plotly)
Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
Brief user guide, including how to run the program and how to choose presentation options.

This project allows users to enter a year into the command prompt and see a map of certain, but not all, institutions that recieved funding for projects in that year in the United States from the Antiquities Endowment Fund. The structure of the code starts by crawling the arce AEF Projects page and caching the data from each of 12 pages that list projects funded for a specific year, using the get_aef_data function. Another function takes one year and parses the data from the cache for that year and cleans/formats it into a list of strings (get_projname). Every other string is a project name and every other string is the project director name and institution. Some of the pages that were crawled had completely different html structures, so the get_projname function accomodates different structures depending on the year that is entered. Once the list of strings is formatted correctly it is put into a dictionary where the year is the key and the value is the list of strings. The key value pairs are then put into tuples. The insert project data function takes these tuples and sorts out which strings are project names and which strings are project directors and inserts this information intot a database. Since the structure of the html pages were different, the data scraped was also different depending on which page it was retrieved from. Some pages had enbedded code to differentiate which strings were project names and which were directors, and some did not. For those that did not, I added my own identifiers and found ways to sort the strings in the insert_proj_data function. Other functions include the institutions function which sorts out the project host institution name from the director string and appends certain institutions (ones that have keywords such as university or museum, with some exceptions) to a list. This list is then drawn on from the plot_institutions function which searches each institution on the google maps api, finds its coordinates, and then plots it on a plotly map.  

To run the program, make sure you have modules/packages from the requirements.txt installed and your google api key pasted into the google key file.You should then be able to run the final507proj.py file and enter a year into the command line.

