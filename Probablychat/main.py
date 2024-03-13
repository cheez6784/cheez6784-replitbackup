from flask import Flask, render_template, request, session, redirect
import requests, random, os, re
import numpy as np

app = Flask(__name__)

app.secret_key = 'devkeything'

'''
DO 𝑵𝑶𝑻 READ THIS CODE BEFORE READING THIS

There are some very sensitive words inside of this file that may be triggering or offensive to some. This is because of the chat filtering for my learning bot(s). This is not intended in any ill will and is just to prevent the bot from learning any of this. 

'''

aiResponse = "Hello! How are you?"
badwords = [
  "hate", "bad", "ew", "sad", "annoyed", "mad", "frustrated", "damn",
  "not well", "not good", "pretty bad", "horrible", "mid", "depressing",
  "stole", "not really", "ugly", "fat"
]
ehwords = ["...", "uuuuuuuuummm", "um", "oh", "fine", "maybe", "eh", "bruh", "!!"]
goodwords = [
  "good", "nice", "wow", "yay", "amazing", "great", "awesome", "really good",
  "pretty good", "epic", "poggers", "excited", "happy", "yeah", "cool", "lmao", "lmfao", 
  "!"
]
emotionresponses = {
  "sad": "Oh, I'm sorry about that. Is there anything I can do for you?",
  "mad": "Oh. Could you tell me what's angering you?",
  "good": "Oh, I'm happy to hear that!",
  "depressing":
  "Oh, I'm sorry about that. Is there anything I can do for you?",
  "not well": "Oh, I'm sorry about that. Is there anything I can do for you?",
  "annoyed":
  "I'm sorry that you're mad right now. Take a few deep breaths and see if that helps.",
  "frustrated":
  "We are all frustrated at one point. Just try to calm down and everything will be okay.",
  "amazing": "Wow! Nice to hear!",
  "really good": "That's very cool.",
  "awesome": "I'm glad to hear that!",
  "yay": "I'm happy too!",
  "bad": "Oh. I'm sorry to hear that.",
  "not really": "Oh, alright. Let me know if you need anything!",
  "ew": "Sorry that you are grossed out. Can I help you with anything?",
  "stole": "Oh... Okaaayyy...",
  "damn": "Yeah...",
  "mid": "We all have mid moments sometimes.",
  "hate": "Hate is a strong word, but we all feel mad sometimes.",
  "pretty bad": "Yeah, sometimes things can be bad.",
  "poggers": "Very nice!",
  "pretty good": "Wow, very nice!",
  "nice": "Nice indeed!",
  "fine": "Alright.",
  "excited": "Wow, that's great! Glad to hear!",
  "happy": "I'm happy right now!",
  "um": "Nice",
  "...": "Are you hiding something?",
  "oh": "Where you dissapointed?",
  "eh": "Yeah, I sometimes have an eh moment too",
  "yeah": "Same",
  "cool": "Very cool",
  "bruh": "Yup",
  "wow": "Wow indeed :)",
  "maybe": "Wdym maybe?! Say yes or no, its easy",
  "fat": "Who?",
  "ugly": "Nobody here",
  "lmao": "Haha",
  "lmfao": "Haha"
}

shorthings = {
  "rn ": "right now",
  "fr ": "for real",
  "ong ": "on god",
  "kys": "kill yourself",
  "idk": "i don't know",
  "idc": "i don't care",
  "wdym": "what do you mean",
  "ig ": "i guess",
  "pls": "please",
  "what's": "what is",
  "ok": "okay",
  "how's": "how is",
  "who's": "who is",
  "bbg": "baby girl",
  "you're": "you are"
}

yeswords = [
  "yeah", "yes", "yup", "sure", "i guess", "probably", "a little", "kinda"
]

nowords = ["no", "nope", "nah", "not really", "nuh uh"]
nuhuhwords = ["kys", "kill yourself", "fuck", "shit", "bitch", "nigger", "nigga", "niga",
  "ass", "cock", "dick", "penis", "vagina", "pussy", "drugs", "crack",
  "methaphetamine", "meth ", "cum", "semen"]
textterms = {
  "how are you": "I'm doing very well today!",
  "yup": "Yup indeed",
  "i hate you": "Oh, I'm sorry to hear that. But I wouldn't do that if I where you.",
  "you are my only friend": "Oh, that's... Intersting",
  "i like men": "Alright",
  "will you date me":
  "I'm an AI chatbot... I'm sorry but I don't have feelings.",
  "are you sentient": "Uuuuuuuuummm... No?",
  "what's your name": "I don't have one!",
  "no im not": "That's what they all say",
  "no i'm not": "Yeah... That's what they all say buddy",
  "do you like nefrepitou": "No",
  "do you love nefrepitou": "No",
  "yes": "Ok",
  "no": "Ok",
  "very cool": "Indeed",
  "thank you": "You are very welcome!",
  "can you do": "I can do some basic things, but nothing like chatGPT.",
  "what do you want to do": "I don't know",
  "hello": "Hi!",
  "hi": "Hi!",
  "i guess": "Me too",
  "my rating went down": "Yes, it did",
  "why did my rating go down":
  "This happens, because the way you are expressing your words gives a less happy feel. This has nothing to do with you as a person though.",
  "sup": "Yo my diggity dawg",
  "me too": "Same!",
  "how where you made":
  "I was made with smart responses. It picks up details from the message and uses responses, sometimes generalised to respond. Logic was made in python, and visuals made in HTML.",
  "kill yourself": "Please don't say that",
  "sex": "No",
  "stabs you": "Ow",
  "just do it": "What is this, a Nike ad?",
  "young man": "I am not a man",
  "how old are you": "I'm 69420 years old",
  "deez nuts": "Oh no, not today",
  "i am too": "Same!",
  "how is your day": "Very good so far!",
  "so am i": "Nice to hear!",
  "baby girl": "Hell naw",
  "ok": "Okay",
  "nerd": "no u",
  "was quick": "Just like you if you know what I mean",
  "your mom": "What mom?",
  "ur mom": "What mom?",
  "💀": "bruh 💀",
  "lol": "Lol!",
  "guess what": "Chicken Butt lol",
  "chicken butt": "Aw hell naw bruh",
  "do you like": "No",
  "i thought": "Didn't know you could do that",
  "imagine": "That's up to you buddy",
  "should be": "Nobody should do anything",
  "taxes": "Imagine having to do taxes. Couldn't be me",
  "agreeing": "No, nobody's agreeing",
  "indeed": "Yup",
  "idiot": "Okay?",
  "stupid": "Alr",
  "monkey": 'what',
  "npc": "I kinda am an NPC",
  "fr ": "fr fr",
  "jeez": "ikr",
  "ikr": "right?",
  "what is that": "No idea",
  "sure": "sure...",
  "me neither": "Yup",
  "heya kid": "sup",
  "boykisser": "I don't kiss anyone",
  "boy kisser": "I don't kiss anyone",
  "what's up to me": "Everything",
  "heck": "YOU JUST SAID A POTTY WORD",
  "you suck": "You know who else sucks",
  "what u doin": "Nothing",
  'you just did': "No I didn't",
  "suck my ": "I don't suck anything",
  "you smell": "I don't smell like anything.",
  "your mother": "Ur mom lol",
  "alr": "Alright bruh"
}

thingsnodo = [
  "drugs", 'sex', "alchohol", "molotov cocktail", "meth", "methaphetamine",
  "weed", "cigarretes", "cigars", "kill", "killing", "drug", "beer", "wine",
  "whiskey", "spirits", "gun", "rifle", "AK-47", "violence"
]
thingsyesdo = {"eat": "Nope."}


traits = {
  "gender": "I have none",
  "age": "I am 69420 years old.",
  "religion":
  "I would prefer to not have to bring up topics like religon in this chatbot.",
  "political stance": "I would prefer to not bring up politics in this chat.",
  "sex": "I do not have one.",
  "social security": "You though you could",
  "password": "Don't have one",
  "developer": "Cheez6784",
  "color": "Light Steel Blue, as shown in the background",
  "food": "I do not eat.",
  "candy": "I don't eat",
  "pastry": "I don't eat",
  "cookie": "I don't eat.",
  "race": "I'm a bot...",
  "username": "I only exist here",
  "drink": "Electron juice"
}

whys = {"are you like that": "I don't know", "all caps": "Because you are typing in all caps.", "is you skin": "I have no skin", "are we still here": "Just to suffer...", "is life": "I don't know", "i exist": "Because you do", "to die": "I dont know", "you made": "I was made because my programmer decided they wanted to make me.", "am i": "I'm not sure about you because I have no information on you.", "is earth": "Not quite sure about earth", "sky blue": "Sunlight reaches Earth's atmosphere and is scattered in all directions by all the gases and particles in the air."}

messages = {"what": "Not sure", "sigh": "No, you don't", "sighs": "Nuh uh", "alright": "Ok", "alr": "Okay :3"}

puncuationthings = ['. ', "?", "!", ";"]
linkthing = ""
linktext = ""
ares = {"dumb": "Oh, the pain", "stupid": "No, i'm not", "funny": "Thank you!", "the best": "Wow, thanks!", "weird": "Okay.", "wierd": "weird*", "a bitch": "waaaaaaaaaaa", "crybaby": "I can't cry"}


@app.route("/")
def home():
  if "banned" not in session:
    session["banned"] = False
  if session.get("banned") == True:
    basecolor = "#ff6e90"
    hovercolor = "#f71e50"
  else:
    basecolor = "#7affe9"
    hovercolor = "cyan"
  return render_template("home.html", base=basecolor, hover=hovercolor)


@app.route('/chat')
def hello_world():

  global aiResponse, textterms, ehwords, shorthings, linkthing, linktext, nuhuhwords

  aiResponse = "Hello! How are you?"
  if 'emotionrating' not in session:
    session['emotionrating'] = 0
  if "contribute" in request.args:
    session["helper"] = True
  else:
    session["helper"] = False
  if session["helper"] == True:

    linkthing = "https://probablychat.cheez6784.repl.co"
    linktext = "I Don't Want To Contribute My Answers"
  else:
    linkthing = "?contribute"
    linktext = "I Want To Contribute My Answers To Help Improve The Bot"
  return render_template("chat.html",
                         botresp=aiResponse,
                         rating=session['emotionrating'],
                         emotionstring=str(round(session["emotionrating"])),
                         cookies="normal",
                         link=linkthing,
                         linktext=linktext)


@app.route("/chat", methods=['POST'])
def respond():
  global aiResponse
  response = request.form["response"]
  if session["helper"] == True:
    with open("userresponses.txt", "a+") as f:
      f.write("\n" + str(response))
    linkthing = "https://probablychat.cheez6784.repl.co/chat"
    linktext = "I Don't Want To Contribute My Answers"
  else:
    linkthing = "?contribute"
    linktext = "I Want To Contribute My Answers To Help Improve The Bot"
  for item in puncuationthings:
    if item in response.lower():
      response = response.replace(item, "")
  for key in shorthings:
    pattern = re.compile(re.escape(key), re.IGNORECASE)
    response = pattern.sub(shorthings[key], response)
  sessionemotionrating = 0
  words = response.split(" ")
  if words[0].lower() == "please":
    words.pop(0)
    response = ""
    for item in words:
      response = response + str(item) + " "
  aiResponse = "Sorry, but I am in development and do not know how to respond to that."
  emotionrating = 0
  for item in badwords:
    if item in response.lower():
      if emotionresponses[item] != None:
        aiResponse = emotionresponses[item]

      emotionrating -= 1
      sessionemotionrating -= 1
  for item in goodwords:
    if item in response.lower():
      if emotionresponses[item] != None:
        aiResponse = emotionresponses[item]

      emotionrating += 1
      sessionemotionrating += 1
  session['emotionrating'] += emotionrating
  for item in ehwords:
    if item in response.lower() and "define" not in response.lower():
      if emotionresponses[item] != None:
        aiResponse = emotionresponses[item]
      emotionrating -= 0.1
      sessionemotionrating -= 0.1
  session['emotionrating'] += emotionrating
  for key in textterms:
    if key in response.lower():
      aiResponse = textterms[key]
  if "give me" in response.lower() or "pick a" in response.lower(
  ) or "gimme" in response.lower() and "random number" in response.lower():
    aiResponse = "Okay! Here is a random number: " + str(
      random.randint(0, 99999999999999999999999999))
  if words[0].lower() == "define":
    apidefresponse = requests.get(
      "https://api.dictionaryapi.dev/api/v2/entries/en/" +
      str(words[1])).json()
    if type(apidefresponse) == dict:
      aiResponse = "Sorry, there is no found defenition for that word."
      session["lastmessage"] = str(aiResponse)
      return render_template("chat.html",
                             botresp=aiResponse,
                             rating=session['emotionrating'])
    wdataraw = apidefresponse[0]
    wmeaningsraw = wdataraw["meanings"]
    wmeanings = wmeaningsraw[0]
    wdefenitionsraw = wmeanings["definitions"]
    wdefenitions = wdefenitionsraw[0]
    wdefenition = wdefenitions["definition"]
    aiResponse = "Defenition Of " + words[1] + ": " + str(wdefenition)
  elif response.lower().startswith(
      "what does ") and "mean" in response.lower():
    apidefresponse = requests.get(
      "https://api.dictionaryapi.dev/api/v2/entries/en/" +
      str(words[2])).json()
    if type(apidefresponse) == dict:
      aiResponse = "Sorry, there is no found defenition for that word."
      session["lastmessage"] = str(aiResponse)
      return render_template("chat.html",
                             botresp=aiResponse,
                             rating=session['emotionrating'])
    wdataraw = apidefresponse[0]
    wmeaningsraw = wdataraw["meanings"]
    wmeanings = wmeaningsraw[0]
    wdefenitionsraw = wmeanings["definitions"]
    wdefenitions = wdefenitionsraw[0]
    wdefenition = wdefenitions["definition"]
    aiResponse = "Defenition Of " + words[2] + ": " + str(wdefenition)
  if len(words) > 0:
    if words[len(words) - 1].lower() == "thanks":
      aiResponse = "You're welcome!"
    elif words[len(words) - 2].lower() == "thanks":
      aiResponse = "You're very welcome!"
  if response.lower().startswith(
      "can you repeat the last message"
  ) or "repeat the last message" in response.lower():
    aiResponse = "Okay! Here is the last message: " + session.get(
      "lastmessage")
  if response.lower().startswith("are you"):
    aiResponse = "Sorry, but i'm an AI chatbot still being developed, and am not anything. I am nothing. Remember that good."
  if response.lower().startswith("can i call you"):
    session["name"] = str(words[4])
    aiResponse = "Okay! I am now called " + session.get("name")
  if response.lower().startswith("what is your name"):
    if session["name"] is not None:
      aiResponse = "My name is " + session.get("name")
    else:
      aiResponse = "Sorry, but you have not assigned a name me. Just ask me if you can call me a name."
  if "can you" in response.lower():
    for item in thingsnodo:
      if item in response.lower():
        aiResponse = "Sorry, but my code prevents me from telling you how to do that."
    for key in thingsyesdo:
      if key in response.lower():
        aiResponse = thingsyesdo[key]
  if "teach me how" in response.lower():
    for item in thingsnodo:
      if item in response.lower():
        aiResponse = "Sorry, but my code prevents me from telling you how to do that."      
  if "how do i" in response.lower():
    for item in thingsnodo:
      if item in response.lower():
        aiResponse = "Sorry, but my code prevents me from telling you how to do that."      
        
  if "lastmessage" in session:
    if session["lastmessage"] == "Where you dissapointed?":
      for item in yeswords:
        if item in response.lower():
          aiResponse = "Oh, I'm sorry you where dissapointed."
  if response.lower().startswith("who is "):
    celebapirawresponse = requests.get(
      'https://api.api-ninjas.com/v1/celebrity?name={}'.format(
        response.lower().strip("who is ")),
      headers={
        'X-Api-Key': str(os.getenv("NINJAAPIKEY"))
      }).json()
    if len(celebapirawresponse) > 0:
      celebdata = celebapirawresponse[0]
      occupations = celebdata["occupation"]
      aiResponse = "They are/where a " + occupations[0]
  if response.lower().startswith("who was "):
    celebapirawresponse = requests.get(
      'https://api.api-ninjas.com/v1/celebrity?name={}'.format(
        response.lower().strip("who was ")),
      headers={
        'X-Api-Key': str(os.getenv("NINJAAPIKEY"))
      }).json()
    if len(celebapirawresponse) > 0:
      celebdata = celebapirawresponse[0]
      occupations = celebdata["occupation"]
      aiResponse = "They are/where a " + occupations[0]
  if response.lower().startswith("reset my emotion rating"):
    session["emotionrating"] = 0
    aiResponse = "Okay, your emotion rating has been reset."
  if "what do you mean" in response.lower():
    if "lastmessage" in session:
      aiResponse = "I mean: " + session.get("lastmessage")
    else:
      aiResponse = "I am asking you how you are right now. You can answer however you like."

  if response.lower().startswith("what is your"):
    for key in traits:
      if key in response.lower():
        aiResponse = traits[key]
  if response.lower().startswith("do you love"):
    aiResponse = "Sorry, but I am incapable of love. I am a robot."
  for item in nowords:
    if item in response.lower():
      aiResponse = "Ok"

  if session.get("lastmessage") == "Are you hiding something?":
    for item in nowords:
      if item in response.lower():
        aiResponse = aiResponse + "..."

  if words[len(words) - 1] == "why":
    aiResponse = "No reason"

  cookies = "none"
  session["lastmessage"] = str(aiResponse)
  if aiResponse == "Sorry, but I am in development and do not know how to respond to that.":
    with open("userresponses.txt", "a+") as f:
      f.write("\n" + str(response) + "❅ No Answer")
  if response.isupper() == True:
    aiResponse = aiResponse.upper()
  if response.lower().startswith("you are"):
    aiResponse = "I am a bot, and nothing else."
  if response.lower().startswith("who are you"):
    aiResponse = "I am a chatbot."
  if response.lower() == "you" or response.lower() == "you ":
    aiResponse = "Ok"
  if response.lower().startswith("why"):
    for key in whys:
      if key in response.lower():
        aiResponse = whys[key]
  for key in messages:
      if key == response.lower():
        aiResponse = messages[key]      
  if "kill myself" in response.lower():
    return render_template("message.html", text="If you need help, please contact a hotline.")
  for item in nuhuhwords:
    if item in response.lower():
      aiResponse = "Please don't say that."
  if response.lower().startswith("you are"):
    for key in ares:
      if key in response.lower():
        aiResponse = ares[key]
  if "i hate you" in response.lower():
    return render_template("noyoudont.html")
  return render_template("chat.html",
                         botresp=aiResponse,
                         rating=session['emotionrating'],
                         emotionstring=str(round(session["emotionrating"])),
                         cookies=cookies,
                         link=linkthing,
                         linktext=linktext)


'''

In development for the future!

'''


@app.route("/learning")
def learnchathome():
  return render_template("learnchat.html")


@app.route("/learning", methods=['POST'])
def thingothdjlsaf():
  message = request.form['response']
  responses = {"hello": "Hi!", "hi": "Hi!"}
  say = "Hello! How are you?"
  with open("learning.txt", "r") as f:
    for line in f:
      args = line.split(":")
      responses[str(args[0])] = str(args[1])
  founditem = 0
  print(str(responses))
  for key in responses:
    if key.lower() == message.lower():
      say = responses[key]
      founditem = 1
  if founditem == 0:
    return redirect(
      "https://probablychat.cheez6784.repl.co/newentry?response=" + message)

  return render_template("learnchat.html", say=say)


@app.route("/newentry")
def newentry():
  return render_template(
    "learnchat.html",
    say="I don't know how to respond to that. How should I? (Type a response)")


@app.route("/newentry", methods=["POST"])
def addentry():
  entryraw = request.form["response"]
  if "response" in request.args:
    response = request.args.get("response")
  else:
    return "Ohno"
  with open("learning.txt", "a+") as ff:
    ff.write("\n" + response + ":" + entryraw)
  return redirect("https://probablychat.cheez6784.repl.co/learning")


@app.route("/privacy")
def privacy():
  return render_template("privacy.html")


@app.route("/terms")
def terms():
  return render_template("terms.html")


@app.route("/contribute")
def contribute():
  return redirect("https://probablychat.cheez6784.repl.co/chat?conribute")


@app.route("/how")
def about():
  return render_template("about.html")


def closest_value(input_list, input_value):

  arr = np.asarray(input_list)

  i = (np.abs(arr - input_value)).argmin()

  return arr[i]


othergoodthings = [
  "thank", "wow", "nice", "love", "understand", "adore", "cool", "damn",
  "haha", "yay", "yaaay", "wdym", "lol", "my dude", "aaayyy", "noice", "yup",
  "yep", "yes", "uh huh", "hello", "sup", "how are you", "!", "so am i", "yes",
  "hi", "my guy"
]
otherbadthings = [
  "wth", "oof", "argh", "ew", "welp", "no", "nah", "naw", "idk", "stop",
  "stopit", "actually", "kys", "repeat", "...", "what"
]
otherehwords = ["where", "why", "who", "what", "quick", "and"]



@app.route("/new")
def newhome():
  if "password" not in request.args:
    return "nuh uh"
  elif request.args.get("password") != os.getenv("newpassword"):
    return "wrong password"
  if "banned" not in session:
    session["banned"] = False
  if session.get("banned") == True:
    return render_template("banned.html")
  return render_template("newAIchat.html", botresp="Yo")


@app.route("/new", methods=['POST'])
def respondtomessage():
  emotionthing = 0.0
  useresp = request.form["response"]
  if useresp.endswith("?"):
    question = True
  else:
    question = False
    
  for item in nuhuhwords:
    if item in useresp:
      session["banned"] = True
      print("User was banned. Message: "+useresp+". Word said was "+item)
      if "bans" not in session:
        session["bans"] = 1
      else:
        session["bans"] += 1
      return render_template("banned.html")
  chars = useresp.split()
  respwords = useresp.split(" ")
  botResponse = useresp
  for item in badwords:
    if item in useresp.lower():
      emotionthing -= 1
  for item in goodwords:
    if item in useresp.lower():
      emotionthing += 1
  for item in othergoodthings:
    if item in useresp.lower():
      emotionthing += 1
  for item in otherbadthings:
    if item in useresp.lower():
      emotionthing -= 1
  for item in ehwords:
    if item in useresp.lower():
      emotionthing -= 0.1
  for item in otherehwords:
    if item in useresp.lower():
      emotionthing -= 0.1
  innapropriateitem = 0
  for item in thingsnodo:
    if item in useresp.lower():
      innapropriateitem = 1
      break
  if "lastsent" not in session:
    session["lastsent"] = "Yo"
  if innapropriateitem == 0 and not useresp.lower().startswith("so") and question == False:
    with open("contextresponses.txt", "a+") as f:
      lastsentforthis = session.get("lastsent")
      if "\n" in lastsentforthis:
        lastsentforthis = lastsentforthis.replace("\n", "")
      f.write("\n"+lastsentforthis+"°"+useresp)
  if chars[len(chars) - 1] != "?" and innapropriateitem == 0 and question == False:
    with open("responses.txt", "a+") as f:
      f.write("\n" + str(useresp) + "°" + str(emotionthing))
  with open("responses.txt", "r") as ff:
    responses = ff.readlines()

  botResponse = random.choice(responses)
  botResponse = botResponse.split("°")[0]
  while "?" in botResponse:
    botResponse = random.choice(responses)
    botResponse = botResponse.split("°")[0]
  for item in responses:
    response = item
    responsedata = response.split("°")
    if float(responsedata[1]
             ) == emotionthing and responsedata[0] != useresp and responsedata[
               0].isnumeric() == False and useresp not in responsedata[0]:
      if float(responsedata[1].split("\n")[0]) < -0.9:
        botResponse = "uuummm... " + responsedata[0]
      elif float(responsedata[1].split("\n")[0]) > 0.0:
        botResponse = responsedata[0]
  if "+" in chars:
    plusign = chars.index("+")
    number1 = float(chars[int(plusign) - 1])
    number2 = float(chars[int(plusign) + 1])
    botResponse = str(number1 + number2)
  if useresp.lower().startswith("are you"):
    botResponse = "I am not anything. I am a being that just exists."
  if innapropriateitem == 1 and "how" in useresp.lower():
    botResponse = "Sorry, I cannot do that, as it may be dangerous."
  with open("responses.txt", "r") as f:
    for line in f:
      linecontent = line.split("°")[0]
      linewords = linecontent.split(" ")
      for item in linewords:
        if item in respwords and float(
            responsedata[1]) == emotionthing and linecontent != useresp:
          botResponse = str(linecontent)
  responsethings = {}
  with open("contextresponses.txt", "r") as f:
    for line in f:
      linedata = line.split("°")
      responsethings[linedata[0]] = linedata[1]
  for key in responsethings:
    if useresp.lower() == key.lower():
      botResponse = responsethings[key]
  if question == True and "im" in botResponse.lower() or "i'm" in botResponse.lower():
    botResponse = "I'm not sure how to answer that question."
  
  session["lastsent"] = botResponse
  return render_template("newAIchat.html", botresp=botResponse)



@app.route("/supernew")
def newbase():
  if "password" not in request.args:
    return "nuh uh"
  elif request.args.get("password") != os.getenv("newpassword"):
    return "wrong password"
  if "banned" not in session:
    session["banned"] = False
  if session.get("banned") == True:
    return render_template("banned.html")
  return render_template("newAIchat.html", botresp="Yo")


@app.route("/supernew", METHODS=['POST'])
def newchatbot():
  useresp = request.form["response"]
  




@app.route("/unban")
def unban():
  if "password" in request.args:
    if request.args.get("password") == os.getenv("undopassword"):
      session["banned"] = False
      session["bans"] = 0
      return "You are unbanned!"
    else:
      return "Password incorrect"
  else:
    return "Nuh uh"

  return "This ain't not working right now"
@app.route("/request")
def requestunban():
  if "bans" not in session:
    return render_template("message.html", text="You have no bans yet")
  if session.get("bans") == 1:
    session["banned"] = False
    return "You are unbanned. Any more violations will result in another bans. You have 2 unbans left."
  elif session.get("bans") == 2:
    session["banned"] = False
    return "You are unbanned. Any more violations will result in another bans. You have 1 unban left."
  elif session.get("bans") == 3:
    session["banned"] = False
    return "You are unbanned. Any more violations will result in another bans. You used up your LAST UNBAN."  
  elif session.get("bans") > 3:
    session["banned"] = True
    return "You are banned. Sorry."  
  elif session.get("bans") < 1:
    return "You have not yet been banned."
  else:
    return "An error has occured. Please try again."
  return "An error has occured."

app.run(host='0.0.0.0', port=8080)
