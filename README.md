# Overview of the Project

This is a lightweight GUI-based application for merging (**at most 20**) PDF files and generating a consolidated output PDF file.

#### The Underlying Motivation

Although there are multiple great pdf merging websites like [ILovePdf](https://www.ilovepdf.com/merge_pdf), [SmallPdf](https://smallpdf.com/merge-pdf) etc., irrespective of all the privacy and security claims, there is a slight chance that the server might store your PDFs. If those PDF files contain any Personally Identifiable Information (PII) of yours, then third parties may become aware of it which is not desirable. Hence, a small lightweight GUI-based application to allow you to perform the PDF merging locally on your system without requiring any internet access.

# Usage

Two ways how a user can use this app are as follows:

1) Install the external Python modules from the [requirements.txt](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/blob/master/requirements.txt) file using:
```bash
pip install -r requirements.txt
```
Then, navigate to [root](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger) of the project and execute the application using:
```bash
python app.py
```

2) We also have an executable file generated using *auto-py-to-exe* and *pyinstaller* in [app/](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/tree/master/app). Just execute the [app.exe](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/blob/master/app/app.exe) and the application will start and the GUI will open.

## About the GUI

1) Upon start

![upon_opening](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/blob/master/readme_images/upon_opening.png)

2) After uploading some files

![after_uploading](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/blob/master/readme_images/after_uploading.png)

3) Click on a file to select it. Rearrange the order of the uploaded files by dragging-and-dropping. Click on **Remove File** to remove the selected file from the GUI.

![file_removal](https://github.com/Prateek-Banerjee/On-Prem_PDF_Merger/blob/master/readme_images/removing_file.png)

4) Toggle theme by switching between light and dark mode.