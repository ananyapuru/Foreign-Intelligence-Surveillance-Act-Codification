from flask import Flask, request, render_template
from selenium import webdriver
import time
import sys

 
app = Flask(__name__)  

TEXT_ONE = """begin_problem(FISA).

list_of_descriptions.
name({*FISA-Proj*}).
author({*Ananya Purushottam, Jad Bataha, Zayyan Naveed.*}).
status(unsatisfiable).
description({*Model FISA*}).
end_of_list.

list_of_symbols.
  functions[(F,0), (P,0), (device,0), (govt,0), (message,0), (US,0)].
  predicates[(consent,0), (sender,1), (receiver,1), (has,2), (EV,1), (send,3), (USP,1), (inUS,1), (REP,1), (WAR,1), (wire,1), (radio,1), (electronic,1), (mechanical,1), (intentional,1), (acquisition,3), (installed,1), (used,1), (comp_trespass,1), (target,1), (acquisition_loc,1), (acquisition_intentional,0)].
end_of_list.

list_of_formulae(axioms).

"""

TEXT_TWO = """

% (1) : acquisition(govt,message, device) ^ (electronic(device) v mechanical(device)) ^ (wire(message) v radio(message)) ^ (sender(P) v receiver(P)) ^ USP(P) ^ inUS(P) ^ target(P) ^ REP(P) --> EV(P)
formula(forall([X],forall([M], forall([D],
    implies(and(acquisition(govt,M,D), or(electronic(D), mechanical(D)), or(wire(M),radio(M)), or(sender(X),receiver(X)), USP(X), inUS(X), target(X), REP(X)), EV(X)))))).

% (1) : acquisition(govt,message, device) ^ (electronic(device) v mechanical(device)) ^ (wire(message) v radio(message)) ^ (sender(P) v receiver(P)) ^ USP(P) ^ inUS(P) ^ target(P) ^ REP(P) --> EV(P)
%formula(forall([X],forall([M], forall([D],
  %  implies(and(and(and(and(and(and(and(acquisition(govt,M,D), or(electronic(D), mechanical(D))), or(wire(M),radio(M))), or(sender(X),receiver(X))), USP(X)), inUS(X)), target(X)), REP(X)), EV(X)))))).

% (2) : acquisition(govt,message, device) ^ (electronic(device) v mechanical(device)) ^ wire(message) ^ (sender(P) v receiver(P)) ^ inUS(P) ^ not(consent) ^ inUS(acquisition(govt,M,D)) ^ not(comp_trespass(M)) --> EV(P)
formula(forall([X],forall([M], forall([D],
    implies(and(acquisition(govt,M,D), or(electronic(D), mechanical(D)), wire(M), or(sender(X),receiver(X)), inUS(X), not(consent), acquisition_loc(US), not(comp_trespass(M))), EV(X)))))).

% (3) : intentional(acquision(govt,message,device)) ^ (electronic(device) v mechanical(device)) ^ radio(message) ^ REP(P) ^ inUS(I) [sender] ^ inUS(J) [receiver]
formula(forall([X],forall([Y], forall([M], forall([D],
    implies(and(acquisition(govt,M,D), acquisition_intentional, or(electronic(D), mechanical(D)), radio(M), inUS(X), inUS(Y)), EV(X))))))).

% (4) : (installed(device) v used(device)) ^ (electronic(device) v mechanical(device)) ^ inUS(device) ^ not(or(wire(message), radio(message))) ^ REP(P) 
formula(forall([X], forall([M], forall([D],
    implies(and(or(installed(D), used(D)), or(electronic(D), mechanical(D)), inUS(D), not(or(wire(M), radio(M))), REP(X)), EV(X)))))).


end_of_list.

list_of_formulae(conjectures).

% person1 should be surveilled
formula(EV(P)).

% person2 should not be surveilled
%formula(not(EV(person2))).

end_of_list.
% this is a comment. We like comments ;-)
list_of_settings(SPASS).
{*
set_flag(PGiven,1).
set_flag(PProblem,0).
*}
end_of_list.

end_problem."""
 
@app.route('/', methods =["GET", "POST"])
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result', methods =["GET", "POST"])
def result():
      if request.method == "POST":
         # getting input with name = fname in HTML form
         acquisition = request.form.get("acquisition")
         selDeviceE = request.form.get("selDeviceE")
         selDeviceM = request.form.get("selDeviceM")
         wire = request.form.get("wire")
         radio = request.form.get("radio")
         sender = request.form.get("sender")
         receiver = request.form.get("receiver")
         usp = request.form.get("USP")
         inUSP = request.form.get("inUSP")
         Target = request.form.get("Target")
         rep = request.form.get("REP")
         Consent = request.form.get("Consent")
         Comp_Trespass = request.form.get("Comp_Trespass")
         Install = request.form.get("Install")
         Use = request.form.get("Use")
         intentional = request.form.get("intentional")
         inUSDevice = request.form.get("inUSDevice")

         data = TEXT_ONE + '\n' + acquisition + '\n' + selDeviceE + '\n' + selDeviceM + '\n' + wire + '\n' + radio + '\n' + sender + '\n' + receiver + '\n'
         data = data + usp + '\n' + inUSP + '\n' + Target + '\n' + rep + '\n' + Consent + '\n' + Comp_Trespass + '\n' + Install + '\n' 
         data = data + Use + '\n' + intentional + '\n' + inUSDevice + '\n' + TEXT_TWO

         chrome_options = webdriver. ChromeOptions()
         chrome_options. add_experimental_option("detach", True)
         chrome_options.add_argument("--incognito")
         web = webdriver.Chrome(chrome_options=chrome_options)
         web.get('https://webspass.spass-prover.org/index.html')

         time.sleep(2)

         inputtext = web.find_element("xpath", '//*[@id="mpiicontent"]/div/div[2]/div/div/form/div/textarea')
         inputtext.clear()
         inputtext.send_keys(data)

         submit = web.find_element("xpath", '//*[@id="mpiicontent"]/div/div[2]/div/div/form/input[2]')
         submit.click()

         return render_template("index.html")

      return render_template("index.html")

 
if __name__=='__main__':
   app.run(debug= True, port = 5001)