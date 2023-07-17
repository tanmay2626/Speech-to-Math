
#---------------------------------------Importing modules---------------------------------------------------#

import speech_recognition as sr
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox

import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
import threading

#---------------------------------------window formation---------------------------------------------------#

main_application = tk.Tk()
main_application.geometry("1200x600")
main_application.title("Mathematical Term and Word Recognizer")
style = ttk.Style()

main_menu = tk.Menu()
#---------------------------------------creating label---------------------------------------------------#

tool_bar_label = ttk.Label(main_application)
tool_bar_label.pack(side=tk.TOP,fill=tk.X)

#========================<Normal Specch Recognition system>=======================>

def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        text_editor.insert(tk.END,"Listening...")
        audio = r.listen(source)
        text_editor.delete(1.0,tk.END)

        try:
            speech = r.recognize_google(audio)
            text_editor.insert(tk.END,speech)
                
            
        except Exception as e:
            print("Error: " + str(e))


#========================<Math Specch Recognition system>=======================>

def math():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        text_editor.insert(tk.END, "Listening...")  # display "Listening" in text editor
        L = text_editor.get(1.0, "end")
        audio = r.listen(source)
        text_editor.delete("1.0", tk.END)
        text_editor.insert(tk.END, L.replace("Listening...", ""))  # remove "Listening" in text editor

        try:
            speech = r.recognize_google(audio)
            SUP = {ord(c): ord(t) for c, t in zip(u"0123456789abcdefghijklmnopqrstuvwxyz+-", u"⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ⁺⁻")}  # zip of superscript
            SUB = {ord(c): ord(t) for c, t in zip(u"0123456789aehijklmnoprstuvx", u"₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")}  # zip of subscript

            optr = []  # define empty list

            def power():
                power = []
                for n, i in enumerate(optr):
                    if i == 'power' or i == 'raise':
                        power.append(n)
                        optr[n] = ''
                for x in power:
                    for n, i in enumerate(optr[x:]):
                        if i == 'stop':
                            optr[n + x] = ''
                            break
                        for j in range(x + 1, n + x + 1):
                            optr[j] = optr[j].translate(SUP)
                eq = ''.join(optr)
                text_editor.insert(tk.END, eq)

            def bracket():
                bracket = []
                for n, i in enumerate(optr):
                    if i == "bracket":
                        bracket.append(n)
                        optr[n] = "("
                for x in bracket:
                    for n, i in enumerate(optr[x:]):
                        if i == "stop":
                            optr[n + x] = ")"
                eq = ''.join(optr)
                text_editor.insert(tk.END, eq)

            def bracketPower():
                PowBrack = []
                for n, i in enumerate(optr):
                    if i == 'bracket':
                        optr[n] = '('
                    elif i == "stop":
                        optr[n] = ")"
                    elif i == 'power' or i == 'raise':
                        optr[n] = ''
                        PowBrack.append(n)
                for x in PowBrack:
                    for n, i in enumerate(optr[x:]):
                        if i == ')':
                            optr[n + x] = ''
                            break
                        for j in range(x + 1, n + x + + 1):
                         optr[j] = optr[j].translate(SUP)
                eq = ''.join(optr)
                text_editor.insert(tk.END, eq)

            def replace_pi():
                for n, i in enumerate(optr):
                  if (i == 'pi' or i == 'fi' or i == 'bye'):
                   optr[n] = 'π'


            stop_words = set(stopwords.words('english'))

            word_data = speech
            word_data = word_data.lower()
            wnltk_tokens = nltk.word_tokenize(word_data)

            stop_words = set(stopwords.words('english')) 
            stop_words = set(stopwords.words('english')) - set(['y', 'a', 'd', 'into'])
            word_tokens = wnltk_tokens

            filtered_sentence = [w for w in word_tokens if not w in stop_words]

            filtered = []
            for w in word_tokens:
                if w not in stop_words:
                    filtered.append(w)

            for n, i in enumerate(filtered):
                if i == "(":
                    filtered[n] = "bracket"
                elif i == ")":
                    filtered[n] = "bracket"
                elif i == "pi":
                    filtered[n] = "π"

            for op in filtered:
                si = op.replace('plus', '+').replace('add', '+').replace('multiply', 'x').replace('into', 'x').replace(
                    'minus', '-').replace('integration', '\u222B').replace('factorial', '\u0021').replace('squared',
                                                                                                          '\u00b2').replace(
                    'square', '\u00b2').replace('equal', '=').replace('equals', '=').replace('cube', '\u00b3').replace(
                    '+', '+').replace('-', '-').replace('zero', '0').replace('one', '1').replace('two', '2').replace(
                    'three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven',
                                                                                                        '7').replace(
                    'eight', '8').replace('nine', '9').replace('theta', '\u03B8').replace('10', 'tan').replace('[',
                                                                                                                '\u00b2(').replace(
                    ']'.replace('/', '÷'), 'stop')
                optr.append(si)

            if 'pi' in optr:
                replace_pi()

            if 'raise' in optr and not 'bracket' in optr or 'power' in optr and not 'bracket' in optr:
                power()
            elif 'bracket' in optr and not 'raise' in optr and not 'power' in optr:
                bracket()
            elif 'bracket' and 'power' or 'raise' in optr:
                bracketPower()
            else:
                eq = ''.join(optr)
                text_editor.insert(tk.END, eq)

        except Exception as e:
            print("Error: " + str(e))


#---------------------------------------New File---------------------------------------------------#
def new_file(event=None):
   global text_url
   text_url = ""
   text_editor.delete(1.0,tk.END)

new_icon = tk.PhotoImage(file = "icon/new.png")
new_icon = new_icon.subsample(12, 12) 
new_button=Button(tool_bar_label,image=new_icon,bd=0,command=lambda:threading.Thread(target=new_file).start(),activebackground = '#c1bfbf',overrelief = 'groove')
new_button.grid(row=0,column=1,padx=5,pady=5)
  
#---------------------------------------Math button---------------------------------------#

speech_icon = tk.PhotoImage(file = "icon/speech.png")
speech_icon = speech_icon.subsample(12, 12) 
speech_button=Button(tool_bar_label,image=speech_icon,bd=0,command=lambda:threading.Thread(target=math).start(),activebackground = '#c1bfbf',overrelief = 'groove')
speech_button.grid(row=0,column=2,padx=5,pady=5)

#---------------------------------------textBOX---------------------------------------#
text_editor=tk.Text(main_application,undo=True)
text_editor.config(wrap="word",relief=tk.FLAT)

scroll_bar=tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

#---------------------------------------End of Code---------------------------------------#

main_application.config(menu=main_menu)


main_application.mainloop()
#---------------------------------------End of window---------------------------------------#