# Scrape Discussion Script

## Introduction

The purpose of this script is to provide an easy way for instructors to track each of their student's discussion posts (both comments and replies) from every discussion topic in Canvas, without having to do it manually through the Canvas Interface.

## Main Features
- Creates an HTML File for every student in the class
- Each student's HTML files lists all their posts on each of the discussion topic in their course
- Each post contains the discussion topic in which the post is from, the date the post was made, and the post text.
-  There is also a quick summary at the top of each HTML file, in case instructor only cares about the number of posts made by the student.

## Requirements
- Python 3
- A Canvas API Token 
- The base URL "https://canvas.ubc.ca" or the testing instance "https://ubc.test.instructure.com."
- The course ID of the course. For example: https://ubc.instructure.com/courses/29 (the Course ID of this course is 29)

## How to get a Canvas API token
1. Log-in to canvas.ubc.ca
2. Click on "Account" on the left hand Global Navigation menu
3. Click on "Settings" 

![settings](https://github.com/jguarin16/screenshots/blob/master/account_settings.png)

4. Scroll to the very bottom of the page, then click on the ![new_access_token](https://github.com/jguarin16/screenshots/blob/master/access_token_button.png) button
5. Provide a purpose under the "Purpose feed", then click on "Generate Token"

![access-token-window](https://github.com/jguarin16/screenshots/blob/master/access_token_window.png)

6. Copy and Paste the token provided to you onto a secure/encrypted text file in your local machine. Once you close this window, you will not be able to access the token again, so please be careful where you save your text file.

![access-token-details](https://github.com/jguarin16/screenshots/blob/master/save_token.png)

## How to run the script (MAC Only)
1. Open the "main_app.py" with your python 3 IDLE
2. Click on "Run" then Run Module (the shortcut key for this is the F5 key)
3. If it ran successfully, a window will open:

![scrape-discussions-window](https://github.com/jguarin16/screenshots/blob/master/scrape_diss_window.png)

If you encounter any errors, please contact arts.helpdesk@ubc.ca

4. In this window, enter the course ID, the base URL (in the requirements section), and your Canvas API token
5. Click on Ok
6. Wait until the message below the "Ok" and "Cancel" says "Done"
7. The HTML files will be in a folder in the same directory as the script, titled with the course you extracted the discussions from

## How to run the script (can for Windows)
Open the the main_app.exe file, folow steps 4-7 from the steps above.
