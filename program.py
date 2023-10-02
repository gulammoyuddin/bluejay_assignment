# -*- coding: utf-8 -*-

import pandas as pd # we are using pandas framework to analyse the given data file

def cons(df): #this function takes a dataframe as an input and returns true if it finds the seven consecutive dates inside it
  gk=df['Time'] #first we extract the starting time of shifts
  gk.index=range(0,gk.size)
  #this are  timestamps for further comparitions
  day=pd.Timedelta('1d') 
  zer=pd.Timedelta('0d')
  #we initialized a list and a variable which we will be using in the algorithm
  x=0
  lt=[] 
  lt.append(gk[0])
  """
  we loop through whole series of shift`s start timing and add the dates to lists which are consecutive in nature 
  if we get a non-consecutive date we check if lists contains 7 or more consecutive dates if yes we return true 
  else clear the list and move further until whole series is processed 
  """
  for i in range(1,gk.size):
    if(gk[i].date()-lt[x].date()==day):
      lt.append(gk[i])
      x=x+1# to update the latest consecutive date in the list for further comparisions
    else:
      if(gk[i].date()-lt[x].date()!=zer):
        if(len(lt)>=7):
          return True
        else:
          lt.clear()
          lt.append(gk[i])
          x=0# to reset the list
  if(len(lt)>=7):# to check after the loop if we have 7 or more consecutive dates or not
    return True
  return False

def shif(df): #this function takes a dataframe as an input and returns true if it finds in between shift time between 1 and 10 hours 
  #first we extract shifts starting and ending times
  gk1=df['Time']
  gk2=df['Time Out']
  gk1.index=range(0,gk1.size)
  gk2.index=range(0,gk2.size)
  #we loop through all the rows 
  for i in range(1,gk1.size):
    # to calculate time(in minutes) in between two shifts as substracting shifts ending time from starting time of next shift
    ts=(gk1[i]-gk2[i-1]).total_seconds()/60
    if (ts>=60 and ts<600):#checking whether time we calculated before is between 1 hour to 10 hours or not
      return True
  return False

def frsh(df): #this function takes a dataframe as an input and returns true if it finds any shift hours greater than 14 hours
  #first we extract shifts starting and ending times
  gk1=df['Time']
  gk2=df['Time Out']
  gk1.index=range(0,gk1.size)
  gk2.index=range(0,gk2.size)
  # we loop through all the rows
  for i in range(0,gk1.size):
    # we calculate total time of the shift (in minutes) by substracting starting time from ending time of a shift 
    ts=(gk2[i]-gk1[i]).total_seconds()/60
    if(ts>840):# checking whether time calculated previously is greater than 14 hours as 14 multiplied by 60 gives 840
      return True
  return False

df=pd.read_excel('Assignment_Timecard.xlsx') # we make a pandas dataframe by reading the file
name=df['Employee Name'] 
name=name.drop_duplicates(keep='first') # we extracted the names of employees from the raw data
name.index=range(0,name.size)
df=df.groupby('Employee Name') # we grouped all the data with same name togethere for ease of analysis
#initializing lists to store the results
ts1=[]
ts2=[]
ts3=[]
"""
the loop below iterates through all the groups we made before by name and based on the 
output of the functions it saves the relevent data (basically employee name and position id)
"""
for i in range(0,name.size):
  bk=df.get_group(name[i])
  if(cons(bk)):
    ts1.append((name[i],bk['Position ID'].iloc[0]))
  if(shif(bk)):
    ts2.append((name[i],bk['Position ID'].iloc[0]))
  if(frsh(bk)):
    ts3.append((name[i],bk['Position ID'].iloc[0]))

#Below block of code simply writes the results to a text file


with open('output.txt','w') as file:
  file.write('Employees who worked for 7 consecutive days are:\n')
  file.write('\n')
  for k in ts1:
    file.write(k[0]+' '+k[1]+'\n')
  file.write('\n')
  file.write('\n')
  file.write('Employees who have less than 10 hour but greater than 1 hour of time between shifts are:\n')
  file.write('\n')
  for k in ts2:
    file.write(k[0]+' '+k[1]+'\n')
  file.write('\n')
  file.write('\n')
  file.write('Employees who have worked for more than 14 hours in a single shift are:\n')
  file.write('\n')
  for k in ts3:
    file.write(k[0]+' '+k[1]+'\n')