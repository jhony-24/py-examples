import subprocess
from time import sleep
from numpy import number
import termcolor
import os
from gtts import gTTS
import pyttsx3
from prettytable import PrettyTable
from progress.bar import Bar

subprocess.call("",shell=True)

languages = {
  "addQuestion": {
    "question": "Pregunta:",
    "answer": "Respuesta:"
  },
  "question": "Pregunta",
  "askTotalOfQuestions": "Cuánta información deseas agregar? ingresa un número:",
  "processing": "Estamos procesando tu información...",
  "newAudio": "Audio creado",
  "welcome" : {
    "intro": "Ingresar tu pregunta y respuesta",
    "leave": "Gracias por tus preguntas y respuestas"
  }
}

class Speaker:
   def __init__(self):
    pass

   def say(self,content: str) -> None:
     pyttsx3.speak(content) 

class Writer:
   def __init__(self):
    pass

   def ask(self,content: str):
      data = input(termcolor.colored(f"{content} ","cyan"))
      return data

   def print(self,content: str):
      print(termcolor.colored(f"{content} ","green"))

class QuestionBuilder:
    def __init__(self,speaker: Speaker, writter: Writer,introductionTitle: str,leaveTitle: str):
      self.speaker = speaker
      self.writter = writter
      self.introductionTitle = introductionTitle
      self.leaveTitle = leaveTitle
      self.questions = []

    def intro(self):
      self.speaker.say(self.introductionTitle)

    def leave(self):
      self.speaker.say(self.leaveTitle)

    def addQuestion(self):
      self.writter.print(self.introductionTitle)
      self.speaker.say(languages["addQuestion"]["question"])
      question = self.writter.ask(languages["addQuestion"]["question"])
      self.speaker.say(languages["addQuestion"]["answer"])
      answer = self.writter.ask(languages["addQuestion"]["answer"])
      self.questions.append({ "question": question, "answer": answer })
    
    def getQuestions(self):
      return self.questions

class CreateAudio:
  def __init__(self):
    pass
  
  def filename(self):
    return "audio.mp3"  

  def export(self, content : str) -> None:
    filename = self.filename()
    if os.path.exists(filename):
      os.remove(filename)
    data = gTTS(content,lang="es")
    data.save(filename)
    os.system(f"start {filename}")


class CreateMultipleQuestions:
  def __init__(self, speaker: Speaker, writter: Writer, builder: QuestionBuilder, totalQuestions: number):
    self.builder = builder
    self.speaker = speaker
    self.writter = writter
    self.totalQuestions = totalQuestions
  
  def create(self):
    for i in range(self.totalQuestions):
      self.builder.addQuestion()
  
  def askTotalOfQuestions(self):
    self.speaker.say(languages["askTotalOfQuestions"])
    self.totalQuestions = int(self.writter.ask(languages["askTotalOfQuestions"]))
    self.writter.print("")



def showTableOfQuestionsAndAnswers(data):
  dataTable = PrettyTable()
  dataTable.field_names = [ 
    languages["addQuestion"]["question"],
    languages["addQuestion"]["answer"]
  ]
  for item in data:
    dataTable.add_row([ item["question"], item["answer"] ])
  print()
  print(termcolor.colored(dataTable,"magenta"))
  

def createAudioFromQuestionsAndAnswers(createAudio: CreateAudio, speaker: Speaker,writter: Writer, data):
  message = languages["processing"]
  speaker.say(message)
  content = ""
  bar = Bar(languages["processing"], max=len(data))
  for index, item in enumerate(data):
    content += f"{languages['question']} {index + 1}: {item['question']} . {item['answer']} ."
    sleep(.5)
    bar.next()
  bar.finish()
  createAudio.export(content)
  speaker.say(languages["newAudio"])




speaker = Speaker()
writter = Writer()
createAudio = CreateAudio()

questionBuilder = QuestionBuilder(
  speaker = speaker,
  writter = writter,
  introductionTitle = languages["welcome"]["intro"],
  leaveTitle = languages["welcome"]["leave"]
)

createMultipleQuestions = CreateMultipleQuestions(
  speaker = speaker,
  writter = writter,
  builder= questionBuilder, 
  totalQuestions = 1
)

questionBuilder.intro()

createMultipleQuestions.askTotalOfQuestions()

createMultipleQuestions.create()

showTableOfQuestionsAndAnswers(data = questionBuilder.getQuestions())

questionBuilder.leave()

createAudioFromQuestionsAndAnswers(
  createAudio,
  speaker,
  writter,
  questionBuilder.getQuestions()
)

