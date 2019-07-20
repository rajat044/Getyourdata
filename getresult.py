import requests, bs4
import re as reg
import pandas as pd

def data():
  total_theory = []
  sessional = []
  total_practical = []
  names = []
  percentage = []
  enrollment_no = []
  roll_no = []
  t_back = []
  roll  = range(10, 150)
  
  for i in roll:
    if i <=99:
      re = requests.get('http://result.bteupexam.in/year/result.aspx?Roll_no=E16120330000' + str(i))
      soup = bs4.BeautifulSoup(re.text, 'lxml')
      marks = soup.select('.printtext')
      
    else:
      re = requests.get('http://result.bteupexam.in/year/result.aspx?Roll_no=E1612033000' + str(i))
      soup = bs4.BeautifulSoup(re.text, 'lxml')
      marks = soup.select('.printtext')

    if len(marks) == 0:
      continue 
      
    elif marks[3].text != '\xa0 [930] [ELECTRONICS ENGINEERING] 05 Semster \r\n                                ':
      continue
    
    else:
      raw_na = marks[4].text
      
      if reg.search(r"([A-Z])+(\s)([A-Z]+)(\s)([A-Z]+)", raw_na):
        na = reg.search(r"([A-Z])+(\s)([A-Z]+)(\s)([A-Z]+)", raw_na)
        names.append(na.group())
                
      elif  reg.search(r"([A-Z]+(\s)([A-Z]+))", raw_na):
        na = reg.search(r"([A-Z]+(\s)([A-Z]+))", raw_na)
        names.append(na.group())
      
      elif reg.search(r"([A-Z]+)", raw_na):
        na = reg.search(r"([A-Z]+)", raw_na)
        names.append(na.group())
             
      raw_enro = marks[6].text
      enro = reg.search(r"(E)([0-9]+)", raw_enro)
      enrollment_no.append(enro.group())

       #It finds the sum of numbers
      ts = 0
      for i in range(10, 65, 5):
        ts += int(marks[i].text)
      
      gs = 0
      for i in range(12, 67, 5):
        gs += int(marks[i].text)
      
      
      percentage.append(round((gs/ts) * 100, 2))
      
      #Total number in theory
      total_theory.append(gs)
      
      #Total number in sessionals
      sessional.append(int(marks[52].text))
      
      #Total number in practical     
      tp = 0
      for i in range(32, 52, 5): 
        tp += int(marks[i].text)
        
      total_practical.append(tp)

      back = []
      for i in range(12, 27, 5):
        get_m = int(marks[i].text)
        if get_m < 17:
          back.append(marks[i-3].text)
      if len(back) == 0:
        a = []
      else:
        a = back[:]

      t_back.append(a)
 # return (t_back)

  return (names, enrollment_no, percentage, t_back, total_theory, sessional, total_practical)

   

def k_group():
  total_theory = []
  sessional = []
  total_practical = []
  names = []
  percentage = []
  enrollment_no = []
  roll_no = []
  t_back = []
  roll  = range(0, 20)
  
  for i in roll:
    re = requests.get('http://result.bteupexam.in/year/result.aspx?Roll_no=E171203800000' + str(i))
    soup = bs4.BeautifulSoup(re.text, 'lxml')
    marks = soup.select('.printtext')
      

    if len(marks) == 0:
      continue 
    
    else:
      raw_na = marks[4].text
      
      if reg.search(r"([A-Z])+(\s)([A-Z]+)(\s)([A-Z]+)", raw_na):
        na = reg.search(r"([A-Z])+(\s)([A-Z]+)(\s)([A-Z]+)", raw_na)
        names.append(na.group())
                
      elif  reg.search(r"([A-Z]+(\s)([A-Z]+))", raw_na):
        na = reg.search(r"([A-Z]+(\s)([A-Z]+))", raw_na)
        names.append(na.group())
      
      elif reg.search(r"([A-Z]+)", raw_na):
        na = reg.search(r"([A-Z]+)", raw_na)
        names.append(na.group())
             
      raw_enro = marks[6].text
      enro = reg.search(r"(E)([0-9]+)", raw_enro)
      enrollment_no.append(enro.group())

       #It finds the sum of  numbers
      ts = 0
      for i in range(10, 65, 5):
        ts += int(marks[i].text)
      
      gs = 0
      for i in range(12, 67, 5):
        gs += int(marks[i].text)
      
      
      percentage.append(round((gs/ts) * 100, 2))
      
      #Total number in theory
      total_theory.append(gs)
      
      #Total number in sessionals
      sessional.append(int(marks[52].text))
      
      #Total number in practical     
      tp = 0
      for i in range(32, 52, 5): 
        tp += int(marks[i].text)
        
      total_practical.append(tp)
      

      back = []
      for i in range(12, 27, 5):
        get_m = int(marks[i].text)
        if get_m < 17:
          back.append(marks[i-3].text)
      if len(back) == 0:
        a = []
      else:
        a = back[:]

      t_back.append(a)
 # return (t_back)

  return (names, enrollment_no, percentage, t_back, total_theory, sessional, total_practical)


names, enrollment_no, percentage, no_back, theory, sessional, practical = data()
dataframe = {"Enrollment":enrollment_no, "Name":names, "Total of Theory":theory, "Sessional":sessional, "Total of Practicals":practical, "Percentage":percentage, "Back":no_back}
df = pd.DataFrame(dataframe) 
a = [len(i) for i in df.Back]
df['NO_of_backs'] = pd.Series(a)

names_k, enrollment_no_k, percentage_k, no_back_k, theory_k, sessional_k, practical_k  = k_group()
dataframe_k = {"Enrollment":enrollment_no_k, "Name":names_k, "Total of Theory":theory_k, "Sessional":sessional_k, "Total of Practicals":practical_k, "Percentage":percentage_k, "Back":no_back_k}
dfk = pd.DataFrame(dataframe_k)       
a = [len(i) for i in dfk.Back]
dfk['NO_of_backs'] = pd.Series(a)

df1 = df.append(dfk, ignore_index = True, sort = False)

df1.to_csv('result.csv')
