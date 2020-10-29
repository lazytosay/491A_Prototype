# 491A_Prototype


##Before getting started
1. reference: https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
2. difference: I used pipenv for the virtual environment not the one he used, everything else are basically the same
3. requirements:
        install node.js, yarn, python3.7.6, pipenv (pip3 install pipenv)
     

##to get started:
1. base folder is 491A_Prototype/front_end/
2.go to base folder
3. first you need to start the backend
4. in console, type: yarn start-api
5. open another console, second step is to start the front-end
6. go to base folder
7. in console, type: yarn start
8. leave the two consoles running
9. a page should pop-out after you start the front-end
10. you should see the time is updating on the bottom of the page
11. if you start front-end before back-end, you should refresh the webpage for the front-end to reconfig with the backend


##install libraries for python virtual environemnt
1. base folder is 491A_Prototype/front_end/
2. it should not happen unless the file that stores all the libraries "Pipfile" is not working correctly
3. go to base folder, type: pipenv shell to enter the virtual environment
4. inside the virtual environment, type: pipenv install -r requirements.txt    to install all the dependencies provided in the requirements.txt file
5. (optional) if you want to share the libraries you installed, type: pipenv lock -r > requirements.txt, 
you can generate the requirement document others can install



##problem regarding the pipenv "command not found" in mac
1. (magacula) https://www.youtube.com/watch?v=K2fNEoZfuy8
2. (magacula) https://medium.com/@jayden.chua/virtual-environments-pip-and-pipenv-on-macos-8f3178b13b75


##problem regarding yarn start
1. try: "npm install" before you run "yarn start"
2. or try: "yarn isntall" before you run "yarn start"


##could not locate a Flask application
1. check if the file ".flaskenv" exist in the base folder
2. if ".flaskenv" does not exist, contact someone to config the project correctly, or download the latest changes
3. if ".flaskenv" file exist, please install the "python-dotenv" under the 
virtual environment
