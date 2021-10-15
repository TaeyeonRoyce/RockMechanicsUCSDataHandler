import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

from math import pi

from pandas.core.indexing import is_label_like

##시트 선택
sheetList = ["u-1 ucs"]
#"u-1 ucs" ,"u-2 ucs","u-3 ucs","u-4 ucs","u-5 ucs"
ghResult=[]
xlResult=[]
compactData = []
## 데이터 영역 선택
## head="row-2", usecols= ["column1, colum2, ... "]
for sheetName in sheetList:
    data = pd.read_excel('UCSData.xlsx', sheet_name = sheetName, header= 7, usecols=[0,1,2,3,4,5,6])
    dataToNumpy = pd.DataFrame.to_numpy(data)

    times = list(np.array(data['s'].tolist()))

    #초기 직경
    initDiameter = dataToNumpy[0][6]

    #횡/축 방향 변형률(1)과 그에 따른 직경, 축응력
    lateralStrain_1 =  list(np.array(data['microstrain'].tolist()))
    axialStrain_1 =  list(np.array(data['mm/mm'].tolist()))

    axialStress_1 = []
    lateralStrain_mm_1 = []
    axialStrain_mm_1 = []

    reslut_1 = []

    #횡/축 방향 변형률(2)과 그에 따른 직경, 축응력
    lateralStrain_2 =  list(np.array(data['mm/mm.1'].tolist()))
    axialStrain_2 =  list(np.array(data['mm/mm.2'].tolist()))

    axialStress_2 = []
    lateralStrain_mm_2 = []
    axialStrain_mm_2 = []

    reslut_2 = []

    #하중
    axialForce =  list(np.array(data['kN'].tolist()))


    def calculate_1(D, lateralStrain, axialStrain, axialLoad):
        for i in range(len(lateralStrain)):
            reslut = []
            #직경
            diameter = round(D*((1-lateralStrain[i]/1000000)),5)
            #축 응력
            axialStress = round((4*(axialLoad[i]*1000))/(pi*((diameter/1000)**2))/1000000,5)
            reslut.append(axialStress)
            axialStress_1.append(axialStress)

            reslut.append(axialStrain[i]/1000)
            axialStrain_mm_1.append(axialStrain[i]/1000)

            reslut.append(lateralStrain[i]/1000)
            lateralStrain_mm_1.append(lateralStrain[i]/1000)

            reslut_1.append(reslut)
            


    def calculate_2(D, lateralStrain,axialStrain, axialLoad):
        for i in range(len(lateralStrain)):
            reslut = []
            #직경
            diameter = round(D*((1-lateralStrain[i]/1000000)),5)
            #축 응력
            axialStress = round((4*(axialLoad[i]*1000))/(pi*((diameter/1000)**2))/1000000,5)
            reslut.append(axialStress)
            axialStress_2.append(axialStress)

            reslut.append(axialStrain[i]/100)
            axialStrain_mm_2.append(axialStrain[i]/100)

            reslut.append(lateralStrain[i]/100)
            lateralStrain_mm_2.append(lateralStrain[i]/100)

            reslut_2.append(reslut)


    calculate_1(initDiameter,lateralStrain_1,axialStrain_1,axialForce)
    calculate_2(initDiameter,lateralStrain_2,axialStrain_2,axialForce)
    ghResult.append([axialStress_1,axialStrain_mm_1,lateralStrain_mm_1])
    ghResult.append([axialStress_2,axialStrain_mm_2,lateralStrain_mm_2])

#     df_1 = pd.DataFrame(reslut_1,columns=['Axial Stress', 'Axial Strain', 'Lateral Strain'])
#     df_2 = pd.DataFrame(reslut_2,columns=['Axial Stress', 'Axial Strain', 'Lateral Strain'])
#     xlResult.append(df_1)
#     xlResult.append(df_2)

# writer = pd.ExcelWriter('DataResult.xlsx', engine='openpyxl')
# xlResult[0].to_excel(writer, sheet_name= sheetList[0] + "1" )
# xlResult[1].to_excel(writer, sheet_name= sheetList[0] + "2" )
# xlResult[2].to_excel(writer, sheet_name= sheetList[1] + "1" )
# xlResult[3].to_excel(writer, sheet_name= sheetList[1] + "2" )
# xlResult[4].to_excel(writer, sheet_name= sheetList[2] + "1" )
# xlResult[5].to_excel(writer, sheet_name= sheetList[2] + "2" )
# xlResult[6].to_excel(writer, sheet_name= sheetList[3] + "1" )
# xlResult[7].to_excel(writer, sheet_name= sheetList[3] + "2" )
# xlResult[8].to_excel(writer, sheet_name= sheetList[4] + "1" )
# xlResult[9].to_excel(writer, sheet_name= sheetList[4] + "2" )
# writer.save()

def compactingData(data, compactRange):
    compactedData = [[],[],[],[],[],[],[]]
    stressSum = 0
    axialStrainSum = 0
    lateralStrainSum = 0
    cnt = 1
    isAxialEnd = False
    isLaterEnd = False
    for i in range(len(data[0])):
        stressSum += data[0][i]
        axialStrainSum += data[1][i]
        lateralStrainSum += data[2][i]
        if len(compactedData[1]) > 1 and (compactedData[1][-1] - compactedData[1][-2] < -0.5):
            isAxialEnd = True
        if len(compactedData[2]) > 1 and (compactedData[2][-1] - compactedData[2][-2] > 0.2):
            isLaterEnd = True
        if (i > 10000) and i < len(data[0]) - 2 and abs(data[0][i]-data[0][-1])*3 < abs(data[0][i]-data[0][-1]):
            if axialStrainSum > 0 and isAxialEnd == False:
                compactedData[0].append(stressSum/cnt)
                compactedData[1].append(axialStrainSum/cnt)
            if lateralStrainSum < 0 and isLaterEnd == False:
                compactedData[2].append(lateralStrainSum/cnt)
                compactedData[3].append(stressSum/cnt)
            stressSum = 0
            axialStrainSum = 0
            lateralStrainSum = 0
            cnt = 1
        elif cnt == compactRange or i == len(data[0])-1:
            if axialStrainSum > 0 and isAxialEnd == False:
                compactedData[0].append(stressSum/cnt)
                compactedData[1].append(axialStrainSum/cnt)
            if lateralStrainSum < 0 and isLaterEnd == False:
                compactedData[2].append(lateralStrainSum/cnt)
                compactedData[3].append(stressSum/cnt)
            
            stressSum = 0
            axialStrainSum = 0
            lateralStrainSum = 0
            cnt = 1 
        else: 
            cnt += 1
        
    maxPoint = compactedData[0].index(max(compactedData[0]))
    maxStress = max(compactedData[0])
    compactedData[4].append(maxStress)
    for i in range(len(compactedData[0])):
        if compactedData[0][i] >= maxStress*0.4:
            compactedData[5].append([compactedData[1][i],compactedData[0][i]])
            compactedData[6].append([compactedData[2][i],compactedData[0][i]])
            break
    for i in range(len(compactedData[0])):
        if compactedData[0][i] >= maxStress*0.6:
            compactedData[5].append([compactedData[1][i],compactedData[0][i]])
            compactedData[6].append([compactedData[2][i],compactedData[0][i]])
            break 
    # compactedData[5].append([compactedData[1][int(maxPoint*0.4)],compactedData[0][int(maxPoint*0.4)]])
    # compactedData[5].append([compactedData[1][int(maxPoint*0.9)],compactedData[0][int(maxPoint*0.9)]])
    # compactedData[6].append([compactedData[2][int(maxPoint*0.4)],compactedData[0][int(maxPoint*0.4)]])
    # compactedData[6].append([compactedData[2][int(maxPoint*0.9)],compactedData[0][int(maxPoint*0.9)]])
    return compactedData



ucsTestResultData = compactingData(ghResult[0],1)
ucsTestAxialStrain = ucsTestResultData[1]
ucsTestAxialStress = ucsTestResultData[0]
ucsTestLateralStrain = ucsTestResultData[2]
ucsTestAxialStressToLateralStrain = ucsTestResultData[3]
ucs = ucsTestResultData[4]
ucsLinearAxialStrain = ucsTestResultData[5]
ucsLinearLateralStrain = ucsTestResultData[6]

fig, ax = plt.subplots()
ax.spines['left'].set_position(('data', 0))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)  

ax.plot(ucsTestAxialStrain,ucsTestAxialStress,label='Stress-Axial Strain')
ax.plot(ucsTestLateralStrain,ucsTestAxialStressToLateralStrain, label='Stress-Lateral Strain')
plt.title("Axial Stress - Axial Strain Curve")
plt.grid(True)
plt.rcParams['font.size'] = 10
plt.legend(loc='upper right', ncol=1)
plt.show()

a= ucsLinearAxialStrain
b= ucsLinearLateralStrain
print(a)
print(b)
youngsModulusA = round((a[1][1]-a[0][1])/(a[1][0]- a[0][0]),5)
youngsModulusL = abs(round((b[1][1]-b[0][1])/(b[1][0]- b[0][0]),5))
possionRatio = round(youngsModulusA/youngsModulusL,5)
print(ucs, youngsModulusA, possionRatio)
# print(ucs)
    

