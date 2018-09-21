import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

# simple formatting
def formatting(cpi, emp, hmean):
  hmean.fillna(method='ffill', inplace=True)
  cpi['Time'] = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), cpi['Time']))
  emp['date'] = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), emp['date']))
  emp.set_index('date', inplace=True)
  hmean['date'] = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), hmean['date']))
  hmean.set_index('date', inplace=True)

  cpi.drop('Unnamed: 0', axis=1, inplace=True)
  cpi = cpi.rename(columns={'Time': 'date'})
  cpi.set_index('date',inplace=True)
  cpi = cpi.loc[emp.index.values]
  return cpi, emp, hmean

# make animation
def animate(data):
  cpi, emp, hmean = data
  job = emp.columns.values
  x = emp.index.values
  
# create the function that will do the plotting, where curr is the current frame
  def update(curr):
    if curr == (len(job)-1): 
      a.event_source.stop()
    plt.clf()
    plt.gcf().text(0.013, 0.75, 'Estimated Total Employment', fontsize=10, rotation='vertical', color='blue')
    plt.gcf().text(0.976, 0.7, 'Mean Hourly Wage / CPI', fontsize=10, rotation='vertical', color='red')

    ax = plt.gca()
    ax2 = ax.twinx()
    ax.tick_params(axis='y', which='major', labelsize=8)
    ax2.tick_params(axis='y', which='major', labelsize=8)

    ax.axis([datetime.datetime(1999,1,1,0,0),datetime.datetime(2018,1,1,0,0),min(emp[job[curr]])/1.1,1.1*max(emp[job[curr]])])
    ax.plot(x, emp[job[curr]], 'bo-')
    ax.set_xlabel('Time')
    ax.tick_params('y', colors='b')
    plt.gcf().text(0.2, 0.91, 'Occupation:        '+job[curr], ha='left')
    for item in ax.xaxis.get_ticklabels():
      item.set_rotation(45)

    ax2.plot(x, hmean[job[curr]]/cpi['Cpi'], 'ro-')
    ax2.tick_params('y', colors='r')

# save emp & h_mean variation of all occupations to animation
  fig = plt.figure(figsize=(7,5))
  fig.subplots_adjust(bottom=0.2, left = 0.125, right=0.875, top=0.9)
  return animation.FuncAnimation(fig, update, interval=700, save_count=21)

def main():
  try:
    cpi = pd.read_csv(sys.argv[1])
    emp = pd.read_csv(sys.argv[2]) 
    hmean = pd.read_csv(sys.argv[3]) 
  except:
    print('\033[1;31m\n Error: please provide 3 input files for CPI, Employment and h_mean \n\033[1;m')
    return
  data = formatting(cpi,emp,hmean)
  animate(data).save('animation.mp4', dpi=500)


if __name__ == "__main__":
  main()
