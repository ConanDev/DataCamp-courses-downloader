# DataCamp-courses-downloader
Provided with a DataCamp account, this python app automatically downloads course content which is tedious browsing the website/app. I can use this as a tool to get structured course content quickly for me to learn a certain topic.

#Actual Read-me
This app requires selenium python library installed, as well as Chrome webdriver. You can obviously change that.
To use this app, edit the config file and add your email and password for DataCamp.
You can either enter the course name you wish to download in the config file as well, or add it as an argument to main:
python app "course name" (which is obviously more practical)
In the DataCampCoursesAutomatic.py file, add the path to the webdriver in the body of the main function.
#General notes
Please feel free to edit this program as it can be easily improved by making sleeping time more efficient, and perhaps adding a GUI.
