import copy

import pandas as pd
import csv
from reportlab.pdfbase import pdfmetrics  # register the font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image
from reportlab.lib.pagesizes import letter  # (8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors  # color
from reportlab.graphics.charts.barcharts import VerticalBarChart  # chart
from reportlab.graphics.charts.legends import Legend  # legend
from reportlab.graphics.shapes import Drawing  # draw tools
from reportlab.lib.units import cm

import re
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
matplotlib.use('TkAgg')

def read_table(filepath1, filepath2):
    #filepath1 = 'Oximetry/'+
    data = pd.read_csv(filepath1, skiprows=85)
    print(data.shape[0])
    log_1 = pd.read_csv(filepath2, nrows=8)
    list_index = [i.start()for i in re.finditer("/",filepath2)]
    filename = filepath2[list_index[-1]+1:filepath2.find(".")]
    log_1.columns = ['head', 'data']
    total_time = []
    start_time = log_1.iloc[5, 1]
    end_time = log_1.iloc[6, 1]
    start_time = datetime.datetime.strptime(start_time, "%H%M")
    end_time = datetime.datetime.strptime(end_time, "%H%M")
    if end_time.hour <= 10:
        end_time = end_time + datetime.timedelta(days=1)
    total_record_time = end_time - start_time
    total_time.append(start_time)
    total_time.append(end_time)
    print(total_time)
    log_2 = pd.read_csv(filepath2, skiprows=9)
    print(log_1)
    print(log_2)
    data.columns = ['time', 'Saturation', 'Pulse', 'code']
    print(data)
    awake_time = cal_time(log_2)
    time_low_confidence, time_awake, time_outbound, data, data_original = delete(data, start_time, end_time, awake_time)
    total_sleep_time = data.shape[0] * 2
    total_sleep_time = datetime.timedelta(seconds=total_sleep_time)
    print(total_record_time, total_sleep_time)
    sat, pul, loc, sat_perception, pul_max_10, pul_min_10 = get_point(data)
    Saturation(data_original, data, time_low_confidence, time_outbound, time_awake)
    Pulse(data_original, data, time_low_confidence, time_outbound, time_awake)
    generate_report(total_record_time, total_sleep_time, sat, pul, loc, sat_perception, pul_max_10, pul_min_10,filename)
    return filename+'_report.pdf'

# calculate the awake time
def cal_time(log_2):
    awake_time = []
    SAstatus = log_2.iloc[0, 1:]
    Alltime = log_2.columns[1:]
    Allfeed = log_2.iloc[3, 1:]
    for time, status, feed in zip(Alltime, SAstatus, Allfeed):
        print(time)
        if status == 'awake':
            if time == '2400':
                time = '0000'
            time = datetime.datetime.strptime(time, "%H%M")
            if time.hour <= 10:
                time = time + datetime.timedelta(days=1)
            time_e = time + datetime.timedelta(minutes=15)
            # for the lines go with feed time
            if feed != ' ':
                time_a = ""
                for number in feed:
                    if '0' <= number <= '9':
                        time_a = time_a + number
                s_time = time_a[:4]
                e_time = time_a[-4:]
                s_time = datetime.datetime.strptime(s_time, '%H%M')
                e_time = datetime.datetime.strptime(e_time, '%H%M')
                if e_time < s_time:
                    e_time = e_time + datetime.timedelta(days=1)
                e_time = e_time + datetime.timedelta(minutes=10)
                if s_time <= time <= e_time:
                    awake_time.append([s_time, e_time])
                else:
                    awake_time.append([s_time, e_time])
                    awake_time.append([time, time_e])
            else:
                awake_time.append([time, time_e])
    print(awake_time)
    return awake_time

# delete the noise and awake data
def delete(data, start_time, end_time, awake_time):
    for time, index in zip(data.time, data.index):
        time_a = datetime.datetime.strptime(time, '%H:%M:%S')
        if time_a.hour <= 10:
            time_a = time_a + datetime.timedelta(days=1)
        # print(time_a)
        if time_a < start_time or time_a > end_time:
            data.drop(index=[index], inplace=True)
    data_original = copy.copy(data)
    print(data_original)
    time_awake = []
    for time, index in zip(data.time, data.index):
        time_a = datetime.datetime.strptime(time, '%H:%M:%S')
        if time_a.hour <= 10:
            time_a = time_a + datetime.timedelta(days=1)
        for awake in awake_time:
            if awake[0] <= time_a <= awake[1]:
                try:
                    data.drop(index=[index], inplace=True)
                except Exception as e:
                    continue
                time_awake.append(time)
    time_low_confidence = []
    time_outbound = []

    for code, index, saturation, pulse, time in zip(data.code, data.index, data.Saturation, data.Pulse, data.time):
        if '43' in code:
            # print(code)
            # print(index)
            time_low_confidence.append(time)
            data.drop(index=[index], inplace=True)
        elif saturation > 100 or saturation < 0:
            # print(saturation)
            # print(index)
            time_outbound.append(time)
            data.drop(index=[index], inplace=True)
        elif pulse > 500:
            # print(pulse)
            # print(index)
            time_outbound.append(time)
            data.drop(index=[index], inplace=True)
    print(data)
    return time_low_confidence, time_awake, time_outbound, data, data_original

# calculate the numerical measures
def get_point(data):
    spo2_mean = data['Saturation'].mean()
    spo2_min = data['Saturation'].min()
    spo2_min_loc = []
    spo2_median = data['Saturation'].median()
    spo2_mode = float(data['Saturation'].mode())
    spo2_std = data['Saturation'].std()
    for i, time in zip(data['Saturation'], data["time"]):
        if i == spo2_min:
            spo2_min_loc.append(time)
    print(spo2_min, spo2_min_loc)
    pulse_mean = data['Pulse'].mean()
    pulse_min = data['Pulse'].min()
    pulse_min_loc = []
    pulse_median = data['Pulse'].median()
    pulse_mode = float(data['Pulse'].mode())
    pulse_std = data['Pulse'].std()
    for i, time in zip(data['Pulse'], data["time"]):
        if i == pulse_min:
            pulse_min_loc.append(time)
    print(pulse_min, pulse_min_loc)
    # get the perception of the saturation
    sat_perception = []
    sat_limit = 100
    while sat_limit > 80:
        sat_limit = sat_limit - 2
        time_counter = 0
        for sat, time in zip(data['Saturation'], data['time']):
            if sat <= sat_limit:
                time_counter += 1
        total_time = datetime.timedelta(seconds=(time_counter * 2))
        perception = 100 * time_counter / data.shape[0]
        if perception == 0.0:
            perception = '0%'
        else:
            perception = f'%.2f%%' % perception
        sat_perception.append([sat_limit, total_time, perception])
    # generate the max and min 10 data points of pulse
    Ten_max = data.nlargest(10, 'Pulse', keep='first')
    Ten_min = data.nsmallest(10, 'Pulse', keep='first')
    pul_max_10 = []
    pul_min_10 = []
    print(Ten_max)
    print(Ten_min)
    for time, pulse in zip(Ten_max['time'], Ten_max['Pulse']):
        pul_max_10.append([pulse, time])
    for time, pulse in zip(Ten_min['time'], Ten_min['Pulse']):
        pul_min_10.append([pulse, time])
    spo2 = []
    pulse = []
    loc = []
    spo2.extend([spo2_mean, spo2_mode, spo2_median, spo2_std, spo2_min])
    pulse.extend([pulse_mean, pulse_mode, pulse_median, pulse_std, pulse_min])
    loc.extend([spo2_min_loc, pulse_min_loc])
    print(spo2, pulse, loc, sat_perception)
    print(sat_perception[0][1])
    return spo2, pulse, loc, sat_perception, pul_max_10, pul_min_10

# Plot the oxygen saturation
def Saturation(data_original, data, time_low_confidence, time_outbound, time_awake):
    x = []
    y = []
    y2 = []
    y3 = []
    y4 = []
    # print(data_original)
    for i, time, index in zip(data_original['Saturation'], data_original['time'], data_original.index):
        # print(time)
        # y.append(i)
        x.append(time)
        counter_2 = False
        counter_3 = False
        counter_4 = False
        for awake in time_awake:
            # print(awake)
            if time == awake:
                y2.append(i)
                counter_2 = True
        for out in time_outbound:
            if time == out:
                y3.append(i)
                counter_3 = True
        for con in time_low_confidence:
            if con == time:
                y4.append(i)
                counter_4 = True
        if counter_2 == False:
            y2.append(np.NAN)
        if counter_3 == False:
            y3.append(np.NAN)
        if counter_4 == False:
            y4.append(np.NAN)
        if counter_2 == False and counter_3 == False and counter_4 == False:
            y.append(i)
        else:
            y.append(np.NAN)
    # print(x)
    # print(y)
    fig = plt.figure(figsize=(12, 9))
    plt.subplot(211)
    plt.ylim(75, 105)
    plt.xlim(0, data_original.shape[0])
    plt.yticks(np.arange(70, 110, step=10))
    plt.plot(x, y, label='Sleep data')
    plt.plot(x, y2, label='awake data')
    plt.plot(x, y3, label='out of bounds')
    plt.plot(x, y4, label='low confidence')
    plt.title("All Saturation data")
    plt.legend()
    plt.xticks(np.arange(0, data_original.shape[0], step=1200), rotation=-15)
    plt.ion()
    plt.interactive(False)
    # fig.savefig('fig.png')
    plt.subplot(212)
    plt.ylim(75, 105)
    plt.xlim(0, data_original.shape[0])
    plt.yticks(np.arange(70, 110, step=10))
    plt.plot(x, y, label='Sleep data')
    plt.title("Saturation data during sleep")
    plt.legend()
    plt.xticks(np.arange(0, data_original.shape[0], step=1200), rotation=-15)
    #plt.show()
    fig.savefig('Saturation.png')

# to plot the pulse rate
def Pulse(data_original, data, time_low_confidence, time_outbound, time_awake):
    x = []
    y = []
    y2 = []
    y3 = []
    y4 = []
    # print(data_original)
    for i, time, index in zip(data_original['Pulse'], data_original['time'], data_original.index):
        # print(time)
        # y.append(i)
        x.append(time)
        counter_2 = False
        counter_3 = False
        counter_4 = False
        for awake in time_awake:
            # print(awake)
            if time == awake:
                y2.append(i)
                counter_2 = True
        for out in time_outbound:
            if time == out:
                y3.append(i)
                counter_3 = True
        for con in time_low_confidence:
            if con == time:
                y4.append(i)
                counter_4 = True
        if not counter_2:
            y2.append(np.NAN)
        if not counter_3:
            y3.append(np.NAN)
        if not counter_4:
            y4.append(np.NAN)
        if counter_2 == False and counter_3 == False and counter_4 == False:
            y.append(i)
        else:
            y.append(np.NAN)
    # print(x)
    # print(y)
    fig = plt.figure(figsize=(12, 9))
    plt.subplot(211)
    plt.ylim(60, 220)
    plt.xlim(0, data_original.shape[0])
    plt.yticks(np.arange(50, 230, step=15))
    plt.plot(x, y, label='Sleep data')
    plt.plot(x, y2, label='awake data')
    plt.plot(x, y3, label='out of bounds')
    plt.plot(x, y4, label='low confidence')
    plt.title("All Pulse data")
    plt.legend()
    plt.xticks(np.arange(0, data_original.shape[0], step=1200), rotation=-15)
    plt.ion()
    plt.interactive(False)
    #
    plt.subplot(212)
    plt.ylim(75, 105)
    plt.xlim(0, data_original.shape[0])
    plt.yticks(np.arange(50, 230, step=15))
    plt.plot(x, y, label='Sleep data')
    plt.title("Pulse data during sleep")
    plt.legend()
    plt.xticks(np.arange(0, data_original.shape[0], step=1200), rotation=-15)
    #plt.show()
    fig.savefig('Pulse.png')


def generate_report(total_record_time, total_sleep_time, sat, pul, loc, sat_perception, pul_max_10, pul_min_10,filename):
    """Generate the report"""
    content = list()
    content.append(draw_title('Cardiorespiratory Sleep Study Report'))
    content.append(
        draw_text('Total Time Analyzed: {0}      Total sleep time: {1} '.format(total_record_time, total_sleep_time)))
    content.append(draw_little_title('SPO2 Analysis'))

    time_S = ""
    time_P = ""
    for i in loc[0]:
        time_S = time_S + i + "\n"
    for i in loc[1]:
        time_P = time_P + i + "\n"
    data = [
        ('Numerical measures', 'value', 'Time'),
        ('Mean SPO2', '{0}'.format(sat[0]), '/'),
        ('Mode SPO2', '{0}'.format(sat[1]), '/'),
        ('median SPO2', '{0}'.format(sat[2]), '/'),
        ('Standard Deviation SPO2', '{0}'.format(sat[3]), '/'),
        ('Minimum SPO2', '{0}'.format(sat[4]), '{0}'.format(time_S)),
    ]
    content.append(draw_table(*data))
    content.append(
        draw_text('*Numerical measures are calculated by the sleep data. All awake data deleted.'))
    content.append(draw_img('Saturation.png'))
    data_1 = [("SPO2", 'Time Spent', '% of analysis interval')]
    for word in sat_perception:
        sent = "<=" + str(word[0]), str(word[1]), word[2]
        data_1.append(sent)
    content.append(draw_table(*data_1))
    content.append(draw_title(''))
    content.append(draw_little_title('Pulse Analysis'))
    data_2 = [
        ('Numerical measures', 'value', 'Time'),
        ('Mean Pulse', '{0}'.format(pul[0]), '/'),
        ('Mode Pulse', '{0}'.format(pul[1]), '/'),
        ('median Pulse', '{0}'.format(pul[2]), '/'),
        ('Standard Deviation Pulse', '{0}'.format(pul[3]), '/'),
        ('Minimum Pulse', '{0}'.format(pul[4]), '{0}'.format(time_P)),
    ]
    content.append(draw_table(*data_2))
    content.append(
        draw_text('*Numerical measures are calculated by the sleep data. All awake data deleted.'))
    content.append(draw_img('Pulse.png'))
    data_3 = [("Pulse minima", 'Time')]
    for word in pul_min_10:
        sent = str(word[0]), str(word[1])
        data_3.append(sent)
    content.append(draw_table(*data_3))
    content.append((draw_title(" ")))
    data_4  = [("Pulse maxima", 'Time')]
    for word in pul_max_10:
        sent = str(word[0]), str(word[1])
        data_4.append(sent)
    content.append(draw_table(*data_4))
    doc = SimpleDocTemplate(filename+'_report.pdf', pagesize=letter)
    doc.build(content)

def draw_title(title: str):
    # get all styles
    style = getSampleStyleSheet()
    # get the style of the heading
    ct = style['Heading1']
    #ct.fontName = 'Times'
    ct.fontSize = 18
    ct.leading = 50
    # ct.textColor = colors.green     # color
    ct.alignment = 1  # middle
    ct.bold = True
    # create the title
    return Paragraph(title, ct)


def draw_little_title(title: str):
    # get all styles
    style = getSampleStyleSheet()
    # get the style of the heading
    ct = style['Normal']
    ct.fontSize = 15
    ct.leading = 30
    ct.textColor = colors.red
    return Paragraph(title, ct)


def draw_img(path):
    img = Image(path)  # read the image
    img.drawWidth = 480  # set width
    img.drawHeight = 360  # set height
    return img


def draw_table(*args):
    col_width = 120
    style = [
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),  # set the color of text
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # set the grid
    ]
    table = Table(args, colWidths=col_width, style=style)
    return table


def draw_text(text: str):
    style = getSampleStyleSheet()
    ct = style['Normal']
    #ct.fontName = 'Times'
    ct.fontSize = 12
    ct.wordWrap = 'CJK'
    ct.alignment = 1  # Middle
    ct.leading = 25
    return Paragraph(text, ct)


#read_table()
"""date_1 = '2045'
date_2 = '20:43:38'
date1 = datetime.datetime.strptime(date_1, '%H%M')
date2 = datetime.datetime.strptime(date_2, '%H:%M:%S')
date1 = date1 + datetime.timedelta(hours=20)
date = datetime.timedelta(seconds=10000)
table = []
for i in range(8):
    name = str(i), "yes"
    table.append(name)
print(table)
print('date is:{0}'.format(date))
date_3 = date2 - date1
if date1 > date2:
    print(1)
if date2 > date1:
    print(2)
print(date1.hour)
print(date2, date1, date_3)
data = [42, 44, np.NAN, np.NAN, 50, 52]
time = ['20:43:38', '20:43:40', '20:43:42', '20:43:44', '20:43:46', '20:43:48']"""
