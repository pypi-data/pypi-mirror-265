## **BIA (IA)**, your **IA powered vocal assistant**. 

## Pitch:
-  **BIA** is an **IA powered vocal assistant**. BIA brings all in one ChatGPT, 
voice command, YouTube, Netflix, TV, Radio and web navigation. 
- **BIA** is multi language and can interact via the voice or command line. Can run 
on any laptop, and even on a Raspberry.
- Extra cool functionality, **BIA** also provides IA to the educational **Otto robot**.
- Historically, **Otto** is a world-wide known open source robot used for 
educational and fun purpose. **BIA** brings **Otto** to the next 
level. Yes, you can now have a conversation 
with the robot, execute dynamic actions (danse, walk, make sounds, and so on). 
- A **double layer IA mechanism** provide fast and accurate answers : one layer powered 
by OpenAI, and a second layer processed by a native AI manages the cache and the 
smart actions (complex requests), ensuring better and faster answers.

## Basic usage of BIA, **app mode** :
- Create a shortcut on your desktop. The shortcut should link to :
	./deploy/run.sh

- The Bia app will open, just push the button and ask a question. Bia will answer ... Enjoy :)

Note : the **UI** parameter under the **[main]** section is the default one : "app" 

## Lazy usage of BIA, **voice mode** :
- Open a terminal, then type : 

	./deploy/run.sh
	or : python3 main.py

- Ask a question. Bia will answer ... Enjoy :)

Note : the **UI** parameter under the **[main]** section must be set to "voice" 

## Advanced usage of BIA, **command line mode** :
- Open a terminal, then type : 

	python3 ./main.py -help
	python3 ./main.py -update
	python3 ./main.py -version
	python3 ./main.py "what can I do a friday afternoon in Paris?"

- Bia will answer ... Enjoy :)

## Developer usage of BIA, **keyboard mode** :
- Open a terminal, then type : 

	./deploy/run.sh
	or : python3 main.py

- Write a question. Bia will answer ... Enjoy :)

Note : the **UI** parameter under the **[main]** section must be set to "keyboard" 

## Example of some prompt :
- Quelle est la capitale de la France?
- How are you today?

## Advanced prompts :
- I do not like this answer => a negative prompt will decrease the scoring of the latest answer, it will go down in the cache
- I like this answer very much => a positive prompt will increase the scoring of the latest answer, it will stays up in the cache

## Skills. The special prompts are the following :
- **arduino** : ask the otto robot to do something => Example : Arduino dance the salsa
- **camera** : take a picture => Example : Camera now
- **macro** : save the last command as a keyword => Example : Macro salsa
- **netflix** : run netflix and search for a movie => Example : Netflix breaking bad
- **python** : run a combination of prompts => Example : Python if the capital of France is Paris then Arduino walk one meter
- **radio** : open the web radio site and search for a station => Example : Radio deutschlandfunk
- **tv** : open molotov tv => Example : TV m6
- **web** : open a website => Example : Web google.com
- **youtube** : open youtube and search for some => Example : Youtube dire straits

## Required hardware:
- Developed under MacOS Catalina version 10.15.7 and Python version 3.8
- Tested under Raspberry OS and Python version 3.9
- Headphone and microphone
- (optional) Arduino
- (optional) Raspberry PI
- (optional) Otto robot

## How to install on MacOS : 
 1. Copy the content of the Bia folder to /home/<<your user>>/Bia
 2. Download the nltk ressources :

 	pip install nltk
 	python3
 	>>import nltk
 	>>nltk.download('punkt')
 	>>nltk.download('vader_lexicon')
 	
 3. Download and install homebrew-4.2.4.pkg
	Install one by one the libraries : 

	pip install openai
	pip install websockets
	pip install argostranslate
	pip install py3langid
	pip install pyautogui 
	pip install pyaudio
	pip install speechrecognition
	pip install pyttsx3
 	pip install parrot
	pip install opencv-python --verbose
	pip install customtkinter
	pip install pyduinocli      
	
	Install arduino-cli
	curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

	Install the languages :
	argospm install translate-de_en
	argospm install translate-en_de
	etc with all the languages needed
	
## How to install on Raspberry OS : 
 1. Copy the content of the Bia folder to /home/<<your user>>/Bia
 2. Download the nltk ressources :

	pip install nltk
 	python3
 	>>import nltk
 	>>nltk.download('punkt')
 	>>nltk.download('vader_lexicon')
 	
 3. Install one by one the libraries : 

	sudo apt-get install libjpeg8-dev
 	sudo apt install espeak
	sudo apt install python3-opencv
	sudo apt-get install flac

 	pip install openai
 	pip install websockets
 	pip install argostranslate
 	pip install py3langid
 	pip install pyautogui 
 	pip install pyaudio
 	pip install speechrecognition
 	pip install pyttsx3
 	pip install parrot
	pip install customtkinter
	pip install pyduinocli      
	
	Install arduino-cli
	curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
	
	Install the languages :
	argospm install translate-de_en
	argospm install translate-en_de
	etc with all the languages needed
	
	Check the microphone configuration : https://www.pofilo.fr/post/2018/12/16-mic-raspberry-pi/
 
## Parameters to be checked and changed in the file config.cfg : 
- Mandatory, **api_key** parameter under the **[openAI]** section : put your own key
- **OS** parameter under the **[main]** section, the possible values are :
	"raspberry" for Raspberry OS, "macos" for MacOSX  
- **UI** parameter under the **[main]** section, the possible values are :
	
	"keyboard" (keyboard/command line mode) 
	"voice" (voice mode) 
	"app" for (app/gui mode)  

- Optional, parameters under the **[arduino]** section
- Others parameters are self explanatory

## Advanced tips, logs : 
- Bia will **log into a file** when run with the command "./deploy/run.sh"
- If run with the command "python3 main.py", the logs will be displayed in the terminal window of the command 
- The log files are stored under the folder ./data/logs
- The log level can be changed with the **level** parameter under the **[logging]** section. The values can be INFO, ERROR, DEBUG

## Advanced tips, maintenance : 
- Run from time to time the command "python3 main.py -update
- This option will update the grandma table with the paraphrase of the prompts, this will improve the cache functionality

## Nicolas Christophe (nicolas.christophe@gmail.com)

## Versions:
- v1.0 02.01.2023 Creation

