This is the system developed for neo-natal baby unit to do sleep study. 

Run "GUI.py" to run the project. 

Due to size limitation, the model used for number recognition is not included. Download the model directly to this folder. The link is here:
https://drive.google.com/drive/folders/1cmEVIQFiDqzrqshG1CdM_YczeEhnvtoS?usp=sharing
You can only run the software after downloading the model.

If you are using mode 1, recognition, you can choose the file in the folder "Tables". 
If you are using mode 2, report generation, you need to use mode1 first to generate a csv file. Then choose the csv file and the corresponding oximetry data to get the report. 
If you are using mode 3, you need to choose the pdf or jpeg files as one input and the corresponding oximetry data to get the report. 

Four APIs are used in the project. Now this project is using my account. You can change to your account if you want to recognize more tables.

If error happens when recognizing, check if the APIs still work. If not, change the account.

********************
Folder Oximetry contains the sleep data collected from oximeter.

Folder Tables contains the raw observation chart.

AWSAPI.py, AzureAPI.py, GoogleAPI.py and iflytekAPI.py is to call the corresponding API.

convert.py is the file to divide the table.

Recognition_V2.py is the file to recognize the cells.

PDF2image.py is the file to transform the pdf file into jpg file.

rotate.py is the file to rotate the chart until it's correct.

OMR.py is the file to do optimal mark recognition.

number_recognition.py is the file to do handwritten digit recognition.

correction.py is the file to do the refinement.

DataProcessing.py is the file to do data filtering and generate the report.

GUI.py is the file to generate the GUI. You can also start the sofware by running the file.
