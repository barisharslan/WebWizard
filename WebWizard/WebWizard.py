import PySimpleGUI as sg
import filenamevalidation as fnv
import os
import subprocess
DETACHED_PROCESS = 0x00000008

# -------------- File Boilerplates ---------------------------
html_boiler = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
%s%s\t<title>%s</title>
</head>
<body>
  
</body>
</html>
"""

css_link = """\t<link rel="stylesheet" type="text/css" href="%s.css">\n"""
js_link = """\t<script type="text/javascript" src="%s.js"></script>\n"""

# -------------- MyFile Class --------------------------------
class MyFile:
  """File Object"""
  def __init__(self, file_name, directory, create_css, create_js, launch):
    self.file_name = file_name
    self.file_path = directory + "/" + file_name
    sg.Popup("file will be created at " + self.file_path)
    self.create_css = create_css
    self.create_js = create_js
    self.launch = launch

  def createCSS(self):
    fcss = open(self.file_path + ".css", "w+")
    fcss.close()

  def createJS(self):
    fjs = open(self.file_path + ".js", "w+")
    fjs.close()

  def createHTML(self):
    try:
      # check file destination
      if os.path.isfile(self.file_path + ".html"):
        # if file already exists, prompt user if they want to overwrite the file
        shouldOverwrite = sg.PopupOKCancel('File already exists. Okay to overwrite?')
        if shouldOverwrite == "Cancel":
          # user cancels overwrite request
          raise FileExistsError("File already exists and you requested not to overwrite. Try again.")
        elif shouldOverwrite == None:
          # user quits out of overwrite window
          raise RuntimeError("Quitting script...")
      # else create/overwrite file
      with open(self.file_path + ".html", "w+") as htmlFile:
        htmlFile.write(html_boiler % ((css_link % (self.file_name))*self.create_css, (js_link % (self.file_name))*self.create_js, self.file_name))
    except (FileNotFoundError, IOError):
      sg.Popup("The file could not be created. Please try again.")

  def launchFile(self, path_program):
    sg.Popup("Launching file...")
    if self.create_css:
      subprocess.Popen([path_program, self.file_path + ".css"],creationflags=DETACHED_PROCESS)
    if self.create_js:
      subprocess.Popen([path_program, self.file_path + ".js"],creationflags=DETACHED_PROCESS)
    subprocess.Popen([path_program, self.file_path + ".html"],creationflags=DETACHED_PROCESS)
  
  def createFile(self, path_program):
    # create html file at directory/file_name
    # sg.Popup("Creating HTML file named " + self.file_name + ".html")
    self.createHTML()
    if self.create_css:
      self.createCSS()
    if self.create_js:
      self.createJS()
    # if launch True, call launchFile function
    if self.launch:
      self.launchFile(path_program)





# -------------- Functions --------------------------------
def getLaunchApp():
  # creates text file with directory of user's launch program
  if os.path.isfile("launch.txt"):
    # if file already exists, prompt user if they want to overwrite the file                       
    shouldOverwrite = sg.PopupOKCancel('File already exists. Okay to overwrite?')
    if shouldOverwrite == "Cancel":
      # user cancels overwrite request
      raise FileExistsError("File already exists and you requested not to overwrite. Try again.")
  with open("launch.txt", "w+") as launch:
    launch.write(sg.PopupGetFile("Choose the program you want to use to launch the created files."))
    sg.Popup("Launch file successfully created.")
  

def checkLaunchApp():
  # makes sure directory to app is still valid, and app hasn't been 
  data = ""
  while not os.path.isfile(data):
    with open("launch.txt", "r") as f:
      data = f.read()
  # sg.Popup("Your launch program exists!")
  # then returns string of launch app's directory
  return data


# -------------- GUI Layout -------------------------------
sg.ChangeLookAndFeel('TealMono')
sg.SetOptions(element_padding=(1, 1), text_color="black")



layout =  [
          [sg.Text('WebWizard', size=(15, 1), font=('Fixedsys', 20),
                   justification='center')],
          [sg.Text('Name', size=(10, 1), font=('Fixedsys', 14),
                   justification='left'),
          sg.Input(size=(20, 1), key='fileName')],
          [sg.Text('Directory', size=(10, 1), font=('Fixedsys', 14),
                   justification='left'),
          sg.Input(size=(20, 2), key='folder'),
          sg.FolderBrowse()],
          [sg.Checkbox('Create and Link .css file', default=True, key='makeCss')],
          [sg.Checkbox('Create and Link .js file', default=True, key='makeJs')],
          [sg.Checkbox('Launch files upon creation', default=True, key='open')],
          [sg.CloseButton('Create', size=(15, 1), key='create'),
          sg.CloseButton('Cancel', key='cancel')]


]

# ------------- Main Loop ---------------------------------------
if not os.path.isfile("launch.txt"):
  # if launch file doesn't exist
  getLaunchApp()

path_to_program = checkLaunchApp()

window = sg.Window('Web Wizard', icon="icon.ico").Layout(layout)

while True:
  event, values = window.Read()
  temp_file_path = values['folder'] + "/" + values['fileName']
  if ((fnv.is_path_exists_or_creatable_portable(temp_file_path))):
    if event == 'create':
      myFile = MyFile(values['fileName'], values['folder'], values['makeCss'], values['makeJs'], values['open'])
      myFile.createFile(path_to_program)
      break
    elif event is None or event == 'cancel':
      break
  sg.Popup("Invalid file path, try again.")
  

window.Close()