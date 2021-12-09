import numpy as np
import pandas as pd
import json
import os
import string
from collections import Counter
from random import shuffle
import math as mt
from itertools import combinations
import matplotlib.pyplot as plt

os.chdir("/Users/leonardhoh/Desktop/ComputerScience")

#%%loading dataset
with open("TVs-all-merged.json") as f:
    data = json.load(f)
    
    
#%%setting titles to  lower case
def lowercase(title):
    results = title.lower()
    return results

#%%removing interpunction from titles
def removeinterpunction(results):
    results = results.translate(str.maketrans("","", string.punctuation))
    return results 

#%%removing words from titles
def removewords(results):
    results = results.split()
    wordstoremove = ["newegg","amazon", "bestbuy", "best", "buy", "thenerds", "the", "nerds", "com", "neweggcom", "amazoncom", "bestbuycom","thenerdscom","tv"]
    results = [word for word in results if word.lower() not in wordstoremove]
    results = " ".join(results)
    return results

    
#%%cleaning function (strin.split())
def cleantitles(title):
    results = title
    results = lowercase(results)
    results = replaceappinch(results)
    results = removeinterpunction(results)
    results = removewords(results)
    results = splitstring(results)
    return results 


#%%replace apprenthensis with inches
def replaceappinch(results):
    results = results.replace('"', "inch") and results.replace('inches', "inch") and results.replace('-inch', "inch") and results.replace(' inch', "inch") and results.replace(' hz', "hz")  and results.replace('hertz', "hz") and results.replace('-hz', "hz")  and results.replace(' hertz', "hz")
    return results

#%%split the string
def splitstring(results):
    results = results.split()
    return results

#%%extract all numbersandletters
def extractnumberandletter(x):
    removedwordsnumberletter=[]
    for word in x:
        if (any(chr.isalpha() for chr in word) and any(chr.isdigit() for chr in word)) ==False:
            removedwordsnumberletter.append(word)
            
    for word in removedwordsnumberletter:
        x.remove(word)
        
    return x      


#%%Getting all title words and keys from dictionary
titles=[]
keys=[]
featuresMap=[]
shop =[]
for key in data.keys():
    for i in range(0,len(data[key])):
        titles.append(cleantitles(data[key][i]["title"]))
        keys.append(key) 
        shop.append(data[key][i]["shop"])
        featlist = []
        values = [cleantitles(item)[0] for item in data[key][i]['featuresMap'].values()]
        for value in values:
            featlist.append(value)
        featuresMap.append(featlist)



#%%determine list of all brands from features
contains = 'Brand'
brandsfeatures = []
for key in data.keys():
    for i in range(len(data[key])):
            if (contains in data[key][i]['featuresMap'].keys()) == True:
                brandsfeatures.append(data[key][i]['featuresMap']['Brand'])
            else: 
                brandsfeatures.append(0)
numberofwhichbrands = list(Counter(brandsfeatures))  
numberofwhichbrands.remove(0)
              
#%%extracting brands from titles
numberofwhichbrandscleaned = []
for i in range(len(numberofwhichbrands)):
    numberofwhichbrandscleaned.append(lowercase(numberofwhichbrands[i]))
    
    
brandtitles = {}
for i in range(len(titles)):
    brandtitles[i] = 0
    tit = titles[i]
    for brand in numberofwhichbrandscleaned:
        if brand in tit:
            brandtitles[i] = brand
            break
            
#titles and features combinen, die dan nog cleanen, 
#woorden zonder getallen er uit halen, als dat gedaan is, dan pas de brands toevoegen
#checken of we dan goede modelwords hebben 

#%%combinedbrandsandfeatures
combinedbrandsandfeatures =[]
for i in range(len(brandsfeatures)):
    if brandtitles[i] != 0:
        combinedbrandsandfeatures.append(brandtitles[i])
    else:
        combinedbrandsandfeatures.append(brandsfeatures[i])
        

#%%combining titles with features
combinedtitles = []
for i in range(len(titles)):
    combinedtitles.append(titles[i]+featuresMap[i])

                                    


#%%cleaning combined titles with features
combinedtitlescleaned =[]
for i in range(len(combinedtitles)):
    results = extractnumberandletter(combinedtitles[i])
    results = list(dict.fromkeys(results))
    combinedtitlescleaned.append(results)
        
    
    
#%%adding brands to combinedtitlescleaned
for i in range(len(combinedtitlescleaned)):
    combinedtitlescleaned[i].append(brandtitles[i])


     
#%%making dataframes for titles and keys
titles = combinedtitlescleaned
dataframe = pd.DataFrame(list(zip(keys,shop,titles)),
               columns =["keys","shop","titles"])

#%%counting words
countwtitles = pd.Series(Counter([y for x in dataframe['titles'] for y in x]))
countwtitles = countwtitles.to_frame()
countwtitles.columns = ["frequency"]


#%%detect words with high count
removedwords=[]
for ind in countwtitles.index:
     if countwtitles["frequency"][ind] == 1:
         removedwords.append(ind)
        
        
#%%remove words from dataframe
titleslist = pd.Series.tolist(dataframe['titles'])
for i in range(len(titleslist)):
    for word in titleslist[i]:
        if word in removedwords:
            titleslist[i].remove(word)

#%%create modelwordsvector
modelwordswd=[] #12200 words
for i in range(len(titleslist)):
    for word2 in titleslist[i]:
        modelwordswd.append(word2)
        
modelwords=[]
for word in modelwordswd:
    if word not in modelwords:
        modelwords.append(word)

#%%create binary vectors
binarymatrix = np.zeros((len(modelwords),len(titleslist)))

for i in range(len(titleslist)):
    binaryvectori = np.zeros(len(modelwords))
    index =0
    for word in modelwords:
        if word in titleslist[i]:
            binaryvectori[index] = 1
            index += 1
        else:
            index += 1
    binarymatrix[:,i] = binaryvectori
            
    
#%%create matrix random permutations of index's
numberofpermutations = 1000
matrixpermutation = np.zeros((numberofpermutations, len(titleslist)))
permutation = np.array(list(range(len(binaryvectori))))

def createrandompermutations(binaryvectori):
    # function for creating the hash vector/function
    randompermutation = list(range(len(binaryvectori)))
    shuffle(randompermutation)
    return randompermutation

def createsignaturematrix(binaryvectori, numberofpermutations):
    randompermutationmatrix=[]
    for i in range(numberofpermutations):
        randompermutationmatrix.append(createrandompermutations(binaryvectori))
    return randompermutationmatrix

randompermutationmatrix = np.array(createsignaturematrix(binaryvectori, numberofpermutations)).transpose()


#%%creating signature matrix
signaturematrix = np.zeros((numberofpermutations, len(titleslist)))
for i in range(numberofpermutations):
    randomindicevector = randompermutationmatrix[:,i]
    for k in range(len(binarymatrix[0])):
        for j in range(len(randomindicevector)):
            index = np.where(randomindicevector == j)[0][0] 
            if binarymatrix[index,k] == 1:
                signaturematrix[i][k] = randomindicevector[index]
                break
                
            
#%% splitting signaturevector in bands
def splittingsignaturevector(signaturevector,b)  :
    #assertlen(signaturevector)%b==0
    splittedsignaturevector = np.array_split(signaturevector, b)
    splittedsignaturevector = np.array(splittedsignaturevector).transpose()
    return splittedsignaturevector






#%%creating bucket number for certain band
def creatingbucketnumber(bandvector):
    bucketnumber = ''
    for i in range(len(bandvector)):
        bucketnumber += str(round(bandvector[i]))
    return bucketnumber    
        
def calculatingb(numberofpermutations, b):
        while numberofpermutations%b !=0:
                b -= 1
        return round(b)  

#%%creating different lists for plots
diffBandsResults = pd.DataFrame()
listrecall =[]
listprecision =[]
listrecallLSH = []
listprecisionLSH = []
listfraction =[]
listF1 = []
listF1LSH =[]


#%%setting b values and create for loop over b
bands1 = [10, 20, 25, 40, 50, 100, 125, 200, 200, 200, 200, 250, 250, 250,250,250, 500,500,500,500] 
totalpossiblepairs = 1624*1623/2

for b in bands1:
    b = calculatingb(numberofpermutations, b)
    print(b)


    #%%signing signaturevector to bucket
    bucketdic={}
    numberofshuffles = 10
    for k in range(numberofshuffles):
        np.random.shuffle(signaturematrix)
        for i in range(len(signaturematrix[0])):
             splittedsignaturevector = splittingsignaturevector(signaturematrix[:,i],b)
             for bands in range(b):
                 bucketnumber = creatingbucketnumber(splittedsignaturevector[:,bands])
                 if bucketnumber in bucketdic:
                     bucketdic[bucketnumber] += [i]
                 else:
                    bucketdic[bucketnumber] = [i]
    #%%removing from dictionary binary vectors with only zeros
    keywithzero = ""
    for i in range(numberofpermutations):
        keywithzero += "0"
        if keywithzero in bucketdic:
            del bucketdic[keywithzero]
             
    #%%remove keys with length one in bucketdic
    keystoremove = []
    for key in bucketdic:
        if len(bucketdic[key]) == 1:
            keystoremove.append(key)
            
    for key in keystoremove:
        del bucketdic[key]
        
    #%%creating dictionary of candidate pairs
    candidatedic = {}
    for key in bucketdic:
        pairs =list(combinations(bucketdic[key],2))
        for i in range(len(pairs)):
            if pairs[i][0] > pairs[i][1]:
                pairs[i] = pairs[i][1],pairs[i][0]
        candidatedic[pairs[i]] = 1        
    candidatedic = list(candidatedic)        
            
            
    
    #%%determining jaccard similarity between 2 vectors
    def jaccard_binary(x,y):
        intersection = np.logical_and(x, y)
        union = np.logical_or(x, y)
        jacardsimilarity = intersection.sum() / float(union.sum())
        return jacardsimilarity
    
    
    #%%creating vector of similarities
    similarities = np.zeros(len(candidatedic))
    for i in range((len(candidatedic))):
        index1 = candidatedic[i][0]
        index2 = candidatedic[i][1]
        similarities[i] = jaccard_binary(binarymatrix[:,index1],binarymatrix[:,index2])
        
                   
    #%%selected pairs                
    selectedpairs =[]
    threshold = 0.6
    for i in range(len(similarities)):
        
       if similarities[i] >= threshold:
           selectedpairs.append(1)
       else:
           selectedpairs.append(0)
    print('The amount of selected pairs is')
    amountofselectedpairs = sum(selectedpairs)  
    print(amountofselectedpairs)
    print('The amount of total pairs is')
    totalpairs = len(selectedpairs)
    print(totalpairs)  
    
    #%%determining vector of chosen positives
    chosenpositivepairs = []
    for i in range(len(selectedpairs)):
        if selectedpairs[i] ==1:
            chosenpositivepairs.append(candidatedic[i])
            
    #%%ddetermining true value pairs
    listoftruepairs =[]
    for i in list(dataframe.index):
        for j in list(dataframe.index):
            if i>=j:
                continue
            else:
                if dataframe['keys'][i]==dataframe['keys'][j]:
                    pair = tuple([i,j])
                    listoftruepairs.append(pair)  
    #%%determining number of true and false positives for lsh and after Jaccard similarity
    truepositives = len(listoftruepairs) -len((set(listoftruepairs)-set(chosenpositivepairs)))                       
    falsepositives = amountofselectedpairs - truepositives   
    truepositiveslsh =  len(listoftruepairs) -len((set(listoftruepairs)-set(candidatedic))) 
    falsepositiveslsh = len(candidatedic)- truepositiveslsh      
          
    #%%calculating number of false negatives
    totalnumberofduplicates = len(listoftruepairs)    
    falsenegatives= totalnumberofduplicates - truepositives    
    falsenegativeslsh= totalnumberofduplicates - truepositiveslsh  
    
    #%%calculating precision and recall)
    precisionlsh = truepositiveslsh/(truepositiveslsh + falsepositiveslsh)   
    listprecisionLSH.append(precisionlsh)
    recalllsh = truepositiveslsh/(truepositiveslsh + falsenegativeslsh)   
    listrecallLSH.append(recalllsh)      
    F1lsh = 2 *(precisionlsh *recalllsh)/(precisionlsh + recalllsh)  
    listF1LSH.append(F1lsh)
    precision = truepositives/(truepositives + falsepositives)   
    listprecision.append(precision)
    recall = truepositives/(truepositives + falsenegatives)   
    listrecall.append(recall)      
    F1 = 2 *(precision *recall)/(precision + recall)
    listF1.append(F1)
    fraction = len(candidatedic)/totalpossiblepairs
    listfraction.append(fraction)



#%%plotting
diffBandsResults['F1']  = listF1
diffBandsResults['F1LSH'] = listF1LSH
diffBandsResults['precision']  = listprecision
diffBandsResults['recall']  = listrecall
diffBandsResults['precisionLSH'] = listprecisionLSH 
diffBandsResults['recallLSH'] = listrecallLSH
diffBandsResults['fraction'] = listfraction            
     
#%%plotting2   
diffBandsResults.plot.scatter(x='fraction',y='recallLSH')
plt.grid()    

diffBandsResults.plot.scatter(x='fraction',y='precisionLSH')
plt.grid()

diffBandsResults.plot.scatter(x='fraction',y='recall')
plt.grid()

diffBandsResults.plot.scatter(x='fraction',y='precision')
plt.grid()

diffBandsResults.plot.scatter(x='fraction',y='F1')
plt.grid()
  
diffBandsResults.plot.scatter(x='fraction',y='F1LSH')
plt.grid()
    
    
    
    
    
    
    
    
    
    
