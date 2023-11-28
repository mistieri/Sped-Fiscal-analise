import pandas as pd
import glob
import datetime

print(datetime.datetime.now())

data = ''
def FormatarData(variavel, num):
    global data
    data = variavel[num][:2] + '/' + variavel[num][2:4] + '/' + variavel[num][4:]
    return data

listaArquivos = []
listaLinhas = []

path_efd = glob.glob('C:\\SPED\\SPED FISCAL\\*.txt') # Nesta pasta ficarão os arquivos a serem analizados

print(path_efd)

for i in path_efd:
    listaLinhas = []
    dictCabecalho = {}
    dictLinha = {}

    df = open(i,'r', encoding="Latin-1")

    for line in df:
        if '|0000|' in line:
            arq = line.split("|")
            FormatarData(arq, 4)
            dictCabecalho['DT_INI'] = data
            FormatarData(arq, 5)
            dictCabecalho['DT_FIN'] = data
            dictCabecalho['EMPRESA'] = arq[6]
            dictCabecalho['CNPJ'] = arq[7]

        elif '|C100|' in line: #Relação de Danfes
            linha = line.split('|')

            dictLinha['REG'] = linha[1]
            dictLinha['IND_OPER'] = linha[2]
            dictLinha['IND_EMIT'] = linha[3]
            dictLinha['COD_PART'] = linha[4]
            dictLinha['COD_MOD'] = linha[5]
            dictLinha['COD_SIT '] = linha[6]
            dictLinha['SER'] = linha[7]
            dictLinha['NUM_DOC'] = linha[8]
            dictLinha['CHV_NFE'] = linha[9]
            FormatarData(linha, 10)
            dictLinha['DT_DOC'] = data
            FormatarData(linha, 11)
            dictLinha['DT_E_S'] = data
            dictLinha['VL_DOC'] = linha[12]
            dictLinha['VL_BC_ICMS'] = linha[21]
            dictLinha['VL_ICMS'] = linha[22]
            dictLinha['VL_BC_ICMS_ST'] = linha[23]
            dictLinha['VL_ICMS_ST'] = linha[24]
            dictLinha['VL_IPI'] = linha[25]
            dictLinha['VL_PIS'] = linha[26]
            dictLinha['VL_COFINS'] = linha[27]

            listaLinhas.append(dictLinha)
            dictLinha = {}
            
        elif '|C500|' in line: #Energia Elétrica
            linha = line.split('|')

            dictLinha['REG'] = linha[1]
            dictLinha['IND_OPER'] = linha[2]
            dictLinha['IND_EMIT'] = linha[3]
            dictLinha['COD_PART'] = linha[4]
            dictLinha['COD_MOD'] = linha[5]
            dictLinha['COD_SIT '] = linha[6]
            dictLinha['SER'] = linha[7]
            dictLinha['NUM_DOC'] = linha[10]
            FormatarData(linha, 11)
            dictLinha['DT_DOC'] = data
            FormatarData(linha, 12)
            dictLinha['DT_E_S'] = data
            dictLinha['VL_DOC'] = linha[13]
            dictLinha['VL_BC_ICMS'] = linha[19]
            dictLinha['VL_ICMS'] = linha[20]
            dictLinha['VL_BC_ICMS_ST'] = linha[21]
            dictLinha['VL_ICMS_ST'] = linha[22]


            listaLinhas.append(dictLinha)
            dictLinha = {}

     # você pode acrescentar quantos 'Elif' quiser. Cada bloco com um tipo de registro
       
        elif '|E001|' in line:
            break

    listaArquivos.append({'cabecalho': dictCabecalho, 'linhas': listaLinhas})

df = pd.json_normalize(listaArquivos, errors='ignore',record_path= 'linhas',
meta=[
['cabecalho','DT_INI'],
['cabecalho','DT_FIN']])

df.to_csv(r'C:\\SPED\\output\\resultfiscalc100.csv', sep=';', encoding='utf-8', index=False) # Nesta será gerada planilha com o arquivo de saída

print(datetime.datetime.now())
