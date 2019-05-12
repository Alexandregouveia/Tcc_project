from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
import re
import math

def checkType(inputfile):
    return (re.findall(pattern = r'\.\w*', string = inputfile))[-1]

#Processa planilhas excel
def Processa_xls(inputfile,weights , header, names=False):
    if (header=='on'):
        arq = pd.read_excel(inputfile)
    else:
        arq = pd.read_excel(inputfile,header=None)
        
    arq.iloc[:,-1] = arq.iloc[:,-1].apply(div)
    arq.iloc[:,-2] = arq.iloc[:,-2].apply(div)
    arq = np.asarray(arq)
    out_p = PROMETHEE_II(arq,weights)
    out_t = TOPSIS(arq,weights)
    concat = pd.concat([out_p,out_t["TOPSIS"]],axis=1)
    out_e = euclidian(concat)

    Retorno = out_e.to_json(orient='records')
    return Retorno

#Processa arquivos csv
def Processa_csv(inputfile,weights , header):
    if (header=='on'):
        arq = pd.read_csv(inputfile)
    else:
        arq = pd.read_csv(inputfile,header=None)
        
    arq.iloc[:,-1] = arq.iloc[:,-1].apply(div)
    arq.iloc[:,-2] = arq.iloc[:,-2].apply(div)
    arq = np.asarray(arq)
    out_p = PROMETHEE_II(arq,weights)
    out_t = TOPSIS(arq,weights)
    concat = pd.concat([out_p,out_t["TOPSIS"]],axis=1)
    out_e = euclidian(concat)

    Retorno = out_e.to_json(orient='records')
    return Retorno

#Recebe uma planilha(xls ou xlsx) e retorna um array de json
def xlsToJson(inputfile, header):
    if (header=='on'):
        arq = pd.read_excel(inputfile)
    else:
        arq = pd.read_excel(inputfile,header=None)
    
    Retorno = arq.to_json(orient='records')
    return Retorno

#Recebe csv e retorna um array de json
def csvToJson(inputfile, header):
    if (header=='on'):
        arq = pd.read_csv(inputfile, sep=',')
    else:
        arq = pd.read_csv(inputfile, sep=',', header=None)
    Retorno = arq.to_json(orient='records')
    return Retorno

#Transforma um blob no arquivo original
def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)



#TOPSIS method -Recebe uma numpy array retorna um dataframe
def TOPSIS(array, weights, names=False):
    
    #1 Normaliza os dados
#    norm = normalize(array)
    norm = normaliza(array)
    
    #2 Aplica os pesos
    for i in range (array.shape[1]):
        norm[:,i] = np.multiply(norm[:,i],weights[i])
    #ate aqui ok!
    
    #3 Encontra o maximo e o minimo
    Vp = [np.amax(norm[:,col]) for col in range (norm.shape[1])]
    Vm = [np.amin(norm[:,col]) for col in range (norm.shape[1])]
    
    
    #4 Calcular medida de separação (positiva)
    
    #4.1 lista com o quadrado da distância entre Vij e Vj+
    Sp = [(norm[row,col] - Vp[col])**2 for col in range(norm.shape[1]) for row in range (norm.shape[0])]
    

    #4.2 Transforma a lista anterior em numpy array
    Sp = np.array(Sp)
    Sp = Sp.reshape(norm.shape)

    #4.3 Somatório das alternativas 
    Sp = Sp.sum(axis= 1) 
    
    #4.4 Raiz quadrada dos somatórios
    Sp = [np.sqrt(Sp[row]) for row in range (Sp.shape[0])]
#    print (Sp)

    #5 Calcular medida de separação (negativa)
    
    #5.1 lista com o quadrado da distância entre Vij e Vj+
    Sn = [(norm[row,col] - Vm[col])**2 for col in range(norm.shape[1]) for row in range (norm.shape[0])]

    #5.2 Transforma a lista anterior em numpy array
    Sn = np.array(Sn)
    Sn = Sn.reshape(norm.shape)

    #5.3 Somatório das alternativas 
    Sn = Sn.sum(axis= 1) 

    #5.4 Raiz quadrada dos somatórios
    Sn = [np.sqrt(Sn[row]) for row in range (Sn.shape[0])]
    

    #6 Calcular a aproximidade relativa 
    # p = np.array([Sp[i]/(Sn[i] + Sp[i] ) for i in range (norm.shape[0])])
    c = np.array([Sn[i]/(Sn[i] + Sp[i] ) for i in range (norm.shape[0])])
    
    # c = [math.sqrt(math.pow(n[i],2) + math.pow(p[i],2)) for i in range (norm.shape[0])]
    
    #7 Ordernar resultados
    #7.1 Nomeia as alternativas para serem identificadas após a ordenação
    if (not(names)): # caso não seja passado um nome para as alternativas eles serão gerados aqui
        names = ['Alternativa ' + str(rows + 1) for rows in range (norm.shape[0])]

    df = pd.DataFrame(pd.DataFrame(names))
    df["TOPSIS"] = pd.DataFrame(c)
    
    #7.2 Ordena o dataframe
    # df = df.sort_values(by=["TOPSIS"],ascending=False)
    
    return df
    


def PROMETHEE_II(array, weights, names=False):
    
    # d = [np.subtract(a,b) for a in range (array.shape[0]) for b in range (array.shape[0]) if (not(np.equal(a,b).all()))]
    #Confronta as alternativas
    
    row=[]
    for a in range (array.shape[0]):
        for b in range (array.shape[0]):
            parcial =[]
            # print(array[a],array[b])
            for k in range (array.shape[1]):
                    parcial.append(array[a,k]-array[b,k])
            row.append(parcial)
    # print(row)
    valors = addWeights(np.asarray(row), weights)

    pi=[]
    for row in range(valors.shape[0]):
        pi.append(sum(valors[row])/sum(weights))

    pi = np.asarray(pi)
    rang=  int(math.sqrt(pi.shape[0]))
    pi = np.reshape(pi, (rang, rang)) 
    
    # print(pi.shape)
    #Calculo de sobreclassificação positiva 
    pos=[]
    for i in range (pi.shape[0]):
        pos.append(sum(pi[i,])/(pi.shape[0]-1))

    
    #Calculo de sobreclassificação negativa
    neg=[]
    for i in range (pi.shape[0]):
        neg.append(sum(pi[:,i])/(pi.shape[0]-1))

    #return(neg, pos)
    #Calcula o fluxo final
    final =[]
    for row in range(len(pos)):
        final.append(pos[row] - neg[row])

    final = np.asarray(final)
    final = normalize(final.reshape(1,final.size))
    final = final.reshape(final.size,1)

    if (not(names)): # caso não seja passado um nome para as alternativas eles serão gerados aqui
        names = ['Alternativa ' + str(rows + 1) for rows in range (final.shape[0])]

    df = pd.DataFrame(pd.DataFrame(names))
    df["PROMETHEE"] = pd.DataFrame(final)
    
    #7.2 Ordena o dataframe
    # df = df.sort_values(by=["PROMETHEE"],ascending=False)


    return df

#Função para adicionar pesos ao valores
def addWeights(array, weights):

    # print(weights, type(weights[0]))
    results=[]
    for i in range(array.shape[0]):
        row=[]
        for j in range(array.shape[1]):
            row.append(array[i,j]*weights[j])
        results.append(row)
    return np.asarray(results)


#Função para calcular a média dos resultados
def media(data):
    
    media = np.asarray([(rows['TOPSIS'] + rows['PROMETHEE'])/2 for index,rows in data.iterrows()])

    # df = pd.DataFrame(pd.DataFrame(euclidiana.columns.values))
    data["Media"] = media
    
    
    return data

def normaliza(x):
    sig=0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            sig = sig + math.pow(x[i][j],2)
        
    sig = math.sqrt(sig)
    return np.asanyarray([x[row][col]/sig for col in range(x.shape[1]) for row in range (x.shape[0])]).reshape(x.shape)

    
def euclidian(data):
    
    topMax = data['TOPSIS'].max()
    proMax = data['PROMETHEE'].max()
    
    distEucl = np.asarray([math.sqrt(topMax - (rows["TOPSIS"])**2 + (proMax - rows["PROMETHEE"] )**2)  for index,rows in data.iterrows()])

    data["Euclidiana"] = distEucl
    
    
    return data

def div(x):
    return 10000/x
