# -*- coding: utf-8 -*-
"""
Created on Mon May  7 21:33:03 2018

@author: Minh Ta & Son Nguyen
"""

import json
from pprint import pprint
from pylab import *
import matplotlib.pyplot as plt
    
ranged_heroes = [3, 5, 6, 9, 11, 10, 13, 15, 17, 20, 21, 22, 25, 31, 26, 27, 30, 
               33, 34, 35, 36, 37, 39, 40, 43, 45, 46, 47, 48, 50, 52, 53, 56, 58,
               59, 63, 64, 65, 66, 68, 72, 74, 75, 76, 79, 86, 87, 90, 91, 92, 
               94, 101, 110, 105, 111, 112, 113, 119]
melee_heroes = [1, 2, 4, 7, 8, 12, 14, 16, 18, 19, 23, 28, 29, 32, 38, 41, 42,
                44, 51, 54, 55, 57, 60, 61, 62, 67, 69, 70, 71, 73, 77, 78, 81,
                82, 83, 84, 85, 88, 89, 93, 96, 97, 98, 99, 100, 102, 103, 104,
                106, 107, 108, 114, 120]
hybrid_heroes = [49, 80, 95, 109]

stre_heroes = [102, 73, 2, 38, 78, 99, 96, 81, 51, 69, 49, 107, 7, 103, 
    59, 91, 23, 104, 54, 77, 97, 60, 57, 110, 14, 16, 28, 71, 18, 29, 98,
    19, 100, 108, 85, 42, 83]
agil_heroes = [1, 113, 4, 62, 61, 56, 6, 106, 41, 72, 8, 80, 48, 94, 82, 9, 
    114, 10, 89, 88, 120, 44, 12, 15, 32, 11, 93, 35, 67, 46, 95, 70, 
    20, 40, 47, 63, 109]
intel_heroes = [68, 3, 65, 66, 5, 55, 119, 50, 43, 87, 58, 33, 74, 64, 90, 52,
    31, 25, 26, 53, 36, 84, 111, 76, 13, 45, 39, 86, 79, 27, 75, 101, 17,
    105, 34, 92, 37, 21, 112, 30, 22]

with open('realData.json') as f:
    data = json.load(f)

#for Strength-Agility-Intelligence Filter
def theFunction(start, end):    
    #initialize match
    match = {}
    winRate = {}
    totalMatches = {}
    for stre in range(0, 6):
        for agil in range (0, 6 - stre):
            intel = 5 - stre - agil
            comb = str(stre) + str(agil) + str(intel)
            if (comb) not in match:
                match[comb] = [0, 0]
                winRate[comb] = 0
                
    for i in range(start, end, 10):
        win = [0, 0, 0]
        lost = [0, 0, 0]
        
        for j in range(0, 10):
            if data[i + j]["win"] == True:
                if data[i + j]["hero_id"] in stre_heroes:
                    win[0] = win[0] + 1
                if data[i + j]["hero_id"] in agil_heroes:
                    win[1] = win[1] + 1
                if data[i + j]["hero_id"] in intel_heroes:
                    win[2] = win[2] + 1
            else:
                if data[i + j]["hero_id"] in stre_heroes:
                    lost[0] = lost[0] + 1
                if data[i + j]["hero_id"] in agil_heroes:
                    lost[1] = lost[1] + 1
                if data[i + j]["hero_id"] in intel_heroes:
                    lost[2] = lost[2] + 1  
        combWin = str(win[0]) + str(win[1]) + str(win[2])
        combLost = str(lost[0]) + str(lost[1]) + str(lost[2])
        match[combWin][0] = match[combWin][0] + 1
        match[combLost][1] = match[combLost][1] + 1
    
    for stre in range(0, 6):
        for agil in range (0, 6 - stre):
            intel = 5 - stre - agil
            comb = str(stre) + str(agil) + str(intel)
            if (comb) in match:
                totalMatches[comb] = match[comb][0] + match[comb][1]
                if (totalMatches[comb] != 0):
                    winRate[comb] = '{0:.4g}'.format(match[comb][0] / totalMatches[comb])
                else:
                    winRate[comb] = 0
    totalMatchesSorted = sorted(totalMatches, key = totalMatches.get, reverse=True)
    top10 = {}
    for i in range(10):
        top10[totalMatchesSorted[i]] = winRate[totalMatchesSorted[i]]
    return match, winRate, top10, totalMatchesSorted

#for Melee-Ranged Filter
def theFunction2(start, end):
    match = {}
    winRate = {}
    totalMatches = {}
    for melee in range(0, 6):
        ranged = 5 - melee
        comb = str(melee) + str(ranged)
        if (comb) not in match:
            match[comb] = [0, 0]
            winRate[comb] = 0
                
    for i in range(start, end, 10):
        win = [0, 0]
        lost = [0, 0]
        
        for j in range(0, 10):
            if data[i + j]["win"] == True:
                if data[i + j]["hero_id"] in melee_heroes:
                    win[0] = win[0] + 1
                if data[i + j]["hero_id"] in ranged_heroes or data[i + j]["hero_id"] in hybrid_heroes:
                    win[1] = win[1] + 1
            else:
                if data[i + j]["hero_id"] in melee_heroes:
                    lost[0] = lost[0] + 1
                if data[i + j]["hero_id"] in ranged_heroes or data[i + j]["hero_id"] in hybrid_heroes:
                    lost[1] = lost[1] + 1
        combWin = str(win[0]) + str(win[1])
        combLost = str(lost[0]) + str(lost[1])
        match[combWin][0] = match[combWin][0] + 1
        match[combLost][1] = match[combLost][1] + 1
    
    for melee in range(0, 6):
        ranged = 5 - melee
        comb = str(melee) + str(ranged)
        if (comb) in match:
            totalMatches[comb] = match[comb][0] + match[comb][1]
            if (totalMatches[comb] != 0):
                winRate[comb] = '{0:.4g}'.format(match[comb][0] / totalMatches[comb])
            else:
                winRate[comb] = 0
    return match, winRate

def graph(match, winRate):    
    sortedWR = sorted(winRate, key = winRate.get, reverse=True)
    x = []
    y = []
    for i in range(5):
        y.append(sortedWR[i])
        x.append(float(winRate[sortedWR[i]]) * 100)
    for i in range(len(sortedWR) - 5, len(sortedWR)):
        y.append(sortedWR[i])
        x.append(float(winRate[sortedWR[i]]) * 100)
    figure()
    graph = barh(range(len(x)), x, color = [red,red,red,red,red, blue,blue,blue,blue,blue])
    xlim(20,80)
    yticks(range(len(y)), y)
    gca().invert_yaxis()
    axvline(x=50, color=verLineColor)
    xlabel("Winrate (%)")
    ylabel("Team combination (S A I)")
    addValue(graph)
    legend((graph[0], graph[5]), ('Top 5', 'Bottom 5'))
    show()
    
def graphAll(match, winRate, xleftlim, xrightlim, sort):
    if sort == True:
        sortedWR = sorted(winRate, key = winRate.get, reverse=True)
    else:    
        sortedWR = list(winRate.keys())
    x = []
    y = []
    for i in range(len(sortedWR)):
        y.append(sortedWR[i])
        x.append(float(winRate[sortedWR[i]]) * 100)
    figure()
    graph = barh(range(len(x)), x, color = barColor)
    xlim(xleftlim, xrightlim)
    yticks(range(len(y)), y)
    gca().invert_yaxis()
    axvline(x=50, color=verLineColor)
    xlabel("Winrate (%)")
    ylabel("Team combination (S A I)")
    addValue(graph)
    show()
    
def graphAllByCombination(match, winRate, xleftlim, xrightlim, comb):
    x = []
    for i in range(len(list(winRate.keys()))):
        x.append(float(winRate[comb[i]]) * 100)
    figure()
    graph = barh(range(len(x)), x, color = barColor)
    xlim(xleftlim, xrightlim)
    yticks(range(len(comb)), comb)
    gca().invert_yaxis()
    axvline(x=50, color=verLineColor)
    xlabel("Winrate (%)")
    ylabel("Team combination (S A I)")
    addValue(graph)
    show()
    
def addValue(graph):
    for rect in graph:
        width = rect.get_width()
        text(1.01 * width, rect.get_y() + rect.get_height()/2,
                '%.2f' % float(width))
        

def compare(start, end, string):
    match = {}
    winRate = {}
    totalMatches = {}
    for i in range(start, end, 10):
        win = [0, 0, 0]
        lost = [0, 0, 0]
        check = False
        for j in range(0, 10):
            if data[i + j]["win"] == True:
                if data[i + j]["hero_id"] in stre_heroes:
                    win[0] = win[0] + 1
                if data[i + j]["hero_id"] in agil_heroes:
                    win[1] = win[1] + 1
                if data[i + j]["hero_id"] in intel_heroes:
                    win[2] = win[2] + 1
            else:
                if data[i + j]["hero_id"] in stre_heroes:
                    lost[0] = lost[0] + 1
                if data[i + j]["hero_id"] in agil_heroes:
                    lost[1] = lost[1] + 1
                if data[i + j]["hero_id"] in intel_heroes:
                    lost[2] = lost[2] + 1  
        combWin = str(win[0]) + str(win[1]) + str(win[2])
        combLost = str(lost[0]) + str(lost[1]) + str(lost[2])
        if(combWin == string or combLost == string):
            check = True
        if(check):
            if(combWin == combLost):
                continue
            if(combWin == string):
                if(combLost in match):
                    match[combLost][1] = match[combLost][1] + 1
                else:
                    match[combLost] = [0,1]
            else:
                if(combWin in match):
                    match[combWin][0] = match[combWin][0] + 1
                else:
                    match[combWin] = [1,0]      
 
    keys = list(match.keys())  
    for i in range(len(keys)):
        key = keys[i]
        totalMatches[key] = match[key][0] + match[key][1]
        winRate[key] = '{0:.4g}'.format(match[key][1]/totalMatches[key])
    
    totalMatchesSorted = sorted(totalMatches, key = totalMatches.get, reverse=True)
    
    
    winRateSortByTotal = {}
    for i in range(len(totalMatchesSorted)):
        key = totalMatchesSorted[i]
        winRateSortByTotal[key] = '{0:.4g}'.format(match[key][1]/totalMatches[key])
    return match, winRate, winRateSortByTotal

def winRateOverTime(start, end, interval, string):
    winRate = []
    for i in range(0, int ((end-start)/(interval*10))):
        winLost = [0, 0]
        for j in range(start + 10 * interval * i, start + 10 * interval * (i + 1), 10):
            win = [0, 0, 0]
            lost = [0, 0, 0]
            check = False
            for k in range(0, 10):
                if data[k + j]["win"] == True:
                    if data[k + j]["hero_id"] in stre_heroes:
                        win[0] = win[0] + 1
                    if data[k + j]["hero_id"] in agil_heroes:
                        win[1] = win[1] + 1
                    if data[k + j]["hero_id"] in intel_heroes:
                        win[2] = win[2] + 1
                else:
                    if data[k + j]["hero_id"] in stre_heroes:
                        lost[0] = lost[0] + 1
                    if data[k + j]["hero_id"] in agil_heroes:
                        lost[1] = lost[1] + 1
                    if data[k + j]["hero_id"] in intel_heroes:
                        lost[2] = lost[2] + 1  
            combWin = str(win[0]) + str(win[1]) + str(win[2])
            combLost = str(lost[0]) + str(lost[1]) + str(lost[2])
            if(combWin == string or combLost == string):
                check = True
            if(check):
                if(combWin == combLost):
                    continue
                if(combWin == string):
                    winLost[0] = winLost[0] + 1
                else:
                    winLost[1] = winLost[1] + 1
        if winLost[0] + winLost[1] == 0:
            winRate.append(0)
        else:
            winRate.append(100 * winLost[0] / (winLost[0] + winLost[1]))
    return winRate

def graphWROverTime(start, end, interval, wrot):
    figure()
    plot(range(len(wrot)), wrot, color = barColor)
    ylim(30, 70)
    axhline(y=50, color=verLineColor)
    xticks(range(int((end-start)/interval / 10)), range(start, end, interval * 10))
    gca().locator_params(nbins=6, axis='x')
    xlabel("Matches")
    ylabel("Winrate (%)")
    show()
    
red = "#f6546a"
blue = "#4B92DB"

barColor = blue
verLineColor = "black"
#419740 is the number of games before 7.0
matchAll, winAll, top10All, matchNumSortAll = theFunction(0, len(data))
#graph(matchAll, winAll)
#graphAll(matchAll, winAll, 30, 70, True)
#graphAll(matchAll, top10All, 30, 70, False)
#
#comb = ['212', '122', '113', '221', '311', '203', '023', '302', '131', '032']
#matchb47, winb47, top10b47, matchNumSortb47 = theFunction(len(data) - 419740, len(data))
#graphAllByCombination(matchb47, top10b47, 30, 70, comb)
#
#matchaf7, winaf7, top10af7, matchNumSortaf7 = theFunction(0, len(data) - 419740)
#graphAllByCombination(matchaf7, top10af7, 30, 70, comb)
#
#113, 122, 212
match311, win311, total311 = compare(0, len(data),'311')
match113, win113, total113 = compare(0, len(data),'113')
match221, win221, total221 = compare(0, len(data),'221')
match122, win122, total122 = compare(0, len(data),'122')
match212, win212, total212 = compare(0, len(data),'212')

wrot311 = winRateOverTime(0, len(data), 1000, '311')
graphWROverTime(0, len(data), 1000, wrot311)
##sort by winrate
#graphAll(match311, win311, 0, 100, True)
#graphAll(match113, win113, 0, 100, True)
#graphAll(match221, win221, 0, 100, True)
#graphAll(match122, win122, 0, 100, True)
#graphAll(match212, win212, 0, 100, True)


##graph by popularity
#graphAll(match311, total311, 0, 100, False)
#graphAll(match113, total113, 0, 100, False)
#graphAll(match221, total221, 0, 100, False)
#graphAll(match122, total122, 0, 100, False)
#graphAll(match212, total212, 0, 100, False)
#print(winRate)
#print(sorted(winRate, key = winRate.get, reverse=True))
theFunction2(0, len(data))

        