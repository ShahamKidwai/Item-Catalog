  ### What's Included:
 
  **Database_Setup.py:**                           This is a python file includes database tables, and configuration and mapper code. 
  
  
  **LotsOfItems.py:**
  This file contains sample data to populate the database tables and display the information when the user goes to a homepage.
  
  **Project.py:**
  This is a python file that contains server side code, this is a file used to run the application it uses python flask framework to render the page and store information from the user in the database, this file has the code for CRUD(Create, Read and Update) operations to make the page more interactive. 
  
 ### How to populate the Database:
 Open Git Bash a Command line utility then Navigate to the directory where the project files are stored and the vagrant file is stored, in this case it is `c/fullstack/vagrant` then bring the vagrant machine up using the command `vagrant up` the ssh into it using `vagrant ssh` then change the directory to vagrant using the command `cd /vagrant` then navigate to the project directory, in this case is catalog using the command `cd catalog` once in this directory, go ahead and execute the file LotsOfItems.py using the command 
 `python LotsOfItems.py` this will populate the database with sample data. 
 
 ### How to Run this App:
 Open Git Bash a Command line utility then Navigate to the directory where the project files are stored and the vagrant file is stored, in this case it is `c/fullstack/vagrant` then bring the vagrant machine up using the command `vagrant up` the ssh into it using `vagrant ssh` then change the directory to vagrant using the command `cd /vagrant` then navigate to the project directory, in this case is catalog using the command `cd catalog` once in this directory, go ahead and execute the file Project.py using the command  `python Project.py`, after executing this command your app will run in localhost: 5000, the url http://localhost:5000/ will direct the user to the home page that display the item categories. 
 
 
###  Creating, Editing and Deleting Data in the App
The Homepage displays a list of categories, and clicking on each category displays the items for that category. Clicking the Item displays the item description. If the user is not logged in he cannot create category, add items in that category and update the item description. When the user is logged in, he create new category, add items to that category and update and delete the item description, **..Please Note only the creator of the item category can create update and delete items in that category and item description**.  
 
### JSON Request
This App does provide the data in JSON format to allow external api servers to use the data from this application. To request a data in this application in JSON format, please go to url: `/JSON/ ` this would list all the categories in the database with their respective IDs and it would also provide data for all the items within each category including their ids. To get information about particular item in a specific  category then go to the following URL:

`/category/<x>/<y>/JSON`

replace x and y with the category name and item name, for example: `/category/Soccer/Shinguards/JSON`
 
 
 
  
  
  
  
  
  
  
  
