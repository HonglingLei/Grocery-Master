# Team Contacts
- Hongliang Liu: honglian@andrew.cmu.edu
- Jing Li: jingli4@andrew.cmu.edu
- Hongling Lei: hongling@andrew.cmu.edu
- Kura Aishwarya: akura@andrew.cmu.edu

Many thanks to all my amazing team members, especially Hongliang who contributed a lot to the coding part.

# Demo Links
We have recorded several videos to help people understand how Grocery Master works and why it matters. The first video is our pitch presentation where we explained the market and potential business value of our product. The second video is a detailed case demo, including some explanations about the code structure. The third video is a pure showcase of the program.
- [Pitch Presentation](https://www.youtube.com/watch?v=g1utgS0EcM0)
- [Detailed Demo](https://www.youtube.com/watch?v=RKH5n60_kZ4)
- [Pure Showcase](https://www.youtube.com/watch?v=k-xWSYLsQx4)

# Project Introduction
Our project Grocery Master is an application that makes grocery shopping more convenient and scientific for customers. Users can simply type the product name in the search bar, and GroceryMaster will display all available options, including brand name, ingredients and nutrition values, as well as their availability at nearby grocery stores. Grocery Master can also give customized product recommendations based on users’ health needs. For example, if you search for “apple juice” and click on “sugar”, GroceryMaster will return available apple juice options - ranked by sugar amount - at Trader Joe’s, Target, and Walmart.

# Instructions
## Run-time environment
To run this code, you have to install not only selenium, but also chromedriver.exe and chrome, on your computer as well.
This code will automatically detect if chromedriver.exe has been installed and check its version. If chromedriver has not been installed, the program will install it automatically, so usually you do not have to install it manually.
If you want, you can also get chromedrive.exe [here](https://chromedriver.chromium.org/downloads).
Unfortunately, this code will not work in the IOS system, because some packages we used are only available in Windows.

## How to run the code
We have provided you with a script version. To run this code, run the [main.py](https://github.com/HonglingLei/Grocery-Master/blob/main/main.py) script. A GUI interface will pop up and ask what product you would like to search for. You can also choose "turn on the browser", and a chrome browser will be opened when scraping the data, and you can watch how it scrapes. When the scraping process is finished, the button "output" table will become "finished". Click on that, and you will see a table containing nutrition information. If you click on the column names (they are actually buttons), and the table will be ranked accordingly in that dimension.
Output will be stored in a .csv file in the same package with main.py.

## Selenium instead of beautifulsoup
We didn't use beautifulsoup because our target websites hide their html code with javascript. Therefore, instead of bs, we chose selenium to handle this problem. Actually this is more challenging because the javascript is not static, and we used xpath to locate elements in web pages.

## Your input
Sometimes the websites do not have things you want. For example, we did not find doritos on Trader Joe's. Also, sometimes you will find ambiguity in certain cases. For example, if you look up apples on Target and Walmart, they will show you phones and laptops rather than the fruit. Besides, some food and beverages simply don't have the nutrition information on the websites.

## Anti-scraping
Walmart has an anti-scraping program, and sometimes it will throw a verification page to check if you are a robot. Sometimes it will keep asking if you are a robot again and again. We checked our code and there was no logic error, so we checked in the chrome deveploper mode and found that it was an anti-scraping problem. We have provided you with a demo of our pre-scraped data just in case live-scraping does not work.

## Tricks on anti-scraping
Sometimes Walmart will keep asking if you are a robot again and again. In this case, you can try the following steps:
1. Copy url of verification page;
2. Open another chrome browser (not new tab, new browser) manually;
3. Paste the url and verify there;
4. Restart our scraping script;
Usually it will work after all these steps.

## Limitations
We limited Target and Trader Joe's scraping to 3 times each because the scraping process is really slow. This means that we will only get 3 items from each website.
