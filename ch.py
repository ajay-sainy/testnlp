import sys
import nltk
from nltk import word_tokenize,Text,pos_tag,RegexpParser,tree

import speech_recognition as sr
import pyttsx

engine = pyttsx.init()
	
welcome_message = "Hi, I am waiting for your command, sir"
thanks_exit = "You said thanks, I say bye bye"
no_command = "You didn't say anything, I am going. Bye."
to_many_numbers = "Don't overwhelm me with numbers. I can handle only two"
to_less_numbers = "I didn't receive command. Please try again"
unknown_task = "I can handle only basic maths tasks"
waiting_msg = 'Waiting for a command.'

def speak(text):
	engine.say(text)
	engine.runAndWait()

# obtain audio from the microphone
def getCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		#print("Waiting for your command, sir...")		
		speak(waiting_msg)
		r.energy_threshold = 300	
		audio = r.listen(source)
		#print("I am Working...dont disturb")
		engine.say('I got it. Let me check.')
		engine.runAndWait()

	# recognize speech using Google Speech Recognition
	try:		
		return r.recognize_google(audio,language="en-IN")		
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
		return None
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
		return None

possible_tasks = {'add','subtract','divide','multiply'}	
tasks = set()
numbers = []
def traverse(t):	
	try:
		t.label()
	except AttributeError:
		print(t[0]+" "+t[1])
		if('VB' in t[1]):
			tasks.add(t[0])			
		elif ('CD' in t[1]):
			numbers.append(t[0])
	else:
        # Now we know that t.node is defined
		for child in t:			
			traverse(child)

def add(num1,num2):	
	result = 'The sum is '+str(int(num1)+int(num2))
	engine.say(result)	
	engine.runAndWait()
def sub(num1,num2):	
	result = 'The difference is '+str(int(num1)-int(num2))
	engine.say(result)
	engine.runAndWait()
def mul(num1,num2):	
	result = 'The Multiplication is '+str(int(num1)*int(num2))
	engine.say(result)
	engine.runAndWait()
def div(num1,num2):	
	result = 'The division is '+str(int(num1)/int(num2))
	engine.say(result)
	engine.runAndWait()
	
def process_command(command):
	try:        
		words = word_tokenize(command)
		tagged = pos_tag(words)
		chunkGram = r"""
					Tasks: {<VB.?>}
					Numbers:{<CD>}
					"""
		chunkParser = RegexpParser(chunkGram)
		chunked = chunkParser.parse(tagged)	
		
		traverse(chunked)				
		#chunked.draw()

		if(len(numbers)>2):
			speak(to_many_numbers)
			return
		elif(len(numbers)<2):
			speak(to_less_numbers)
			return
		if(possible_tasks.isdisjoint(tasks) ):
			speak(unknown_task)
			return
			
		if('add' in tasks):
			add(numbers[0],numbers[1])
		elif('subtract' in tasks):
			sub(numbers[0],numbers[1])
		elif('multiply' in tasks):
			mul(numbers[0],numbers[1])
		elif('divide' in tasks):
			div(numbers[0],numbers[1])

	except Exception as e:
		print(str(e))


def execute():	
	while(True):
		tasks.clear();
		del numbers[:]
		command = getCommand()
		if(command in ['thanx','thank u']):
			#print('Ok, Bye...')	
			speak(thanks_exit)
			break
		elif(command is None):
			#print('You dont want to talk. I am going.')
			speak(no_command)
			break;
		process_command(command)
	
execute()
