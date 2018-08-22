from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
import re

def checkType(inputfile):
    return (re.findall(pattern = r'\.\w*', string = inputfile))[-1]

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



#TOPSIS method
def TOPSIS(weights, array, names=False):
    
    #1 Normaliza os dados
    norm = normalize(array)

    #2 Aplica os pesos
    for i in range (array.shape[1]):
        norm[:,i] = np.multiply(norm[:,i],weights[i])
    
    #3 Encontra o maximo e o minimo
    Vp = [np.amax(norm[:,col]) for col in range (norm.shape[1])]
    Vm = [np.amin(norm[:,col]) for col in range (norm.shape[1])]

    #4 Calcular medida de separação (positiva)
    #4.1 lista com o quadrado da distância entre Vij e Vj+
    Sn = [(norm[row,col] - Vp[col])**2 for col in range(norm.shape[1]) for row in range (norm.shape[0])]
    
    #4.2 Transforma a lista anterior em numpy array
    Sn = np.array(Sn)
    Sn = Sn.reshape(norm.shape)

    #4.3 Somatório das alternativas 
    Sn = Sn.sum(axis= 1) 
    
    #4.4 Raiz quadrada dos somatórios
    Sn = [np.sqrt(Sn[row]) for row in range (Sn.shape[0])]


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
    c = np.array([Sn[i]/(Sn[i] + Sn[i]) for i in range (norm.shape[0])])

    

    #7 Ordernar resultados
    #7.1 Nomeia as alternativas para serem identificadas após a ordenação
    if (not(names)): # caso não seja passado um nome para as alternativas eles serão gerados aqui
        names = ['Alternativa' + str(rows) for rows in range (norm.shape[0])]

    df = pd.DataFrame(pd.DataFrame(names))
    df = df.append(c)
    
    #7.2 Ordena o dataframe
    df = df.sort_values(by=[1],ascending=False)

    return df


def PROMETHEE_II(array, weights, names=False):
    
    d = [np.subtract(a,b) for a in range (array.shape()[0]) for b in range (array.shape()[0]) if (not(np.equal(a,b).all()))]
    
    return 0