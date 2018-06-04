#---------Numero de pessoas com e sem def por mês-----------#
import numpy as np
import matplotlib.pyplot as plt

n=12 #numero de colunas
ind=np.arange(n) #localização das colunas
largura=.3 #largura das colunas
plt.subplot(111)
#
'''
para o numero de pessoas precisa-se fazer uma função para calcular
número de pessoas, com e sem def, andaram em meses especificios,
mostrando os momentos no ano em que a trilha esta mais calma ou agitada
'''
cDef=[1,2,3,4,5,6,7,8,9,10,11,12]
sDef=[1,2,3,4,5,6,7,8,9,10,11,12]

cDplot=plt.bar(ind, cDef, largura,
	color='r',
	#error_kw=dict(elinewidth=6),
	ecolor='red')
sDplot=plt.bar(ind+largura, sDef, largura,
	color='g',
	#error_kw=dict(elinewidth=6),
	ecolor='green')

plt.ylabel('numero de pessoas')
plt.title('numero de usuarios em trilhas\ndurante meses no ano')
plt.xticks(ind+largura,('jan','fev','mar','abr','mai','jun','jul',
	'ago','set','out','nov','dez'))
plt.ylim(0,15)

plt.legend((cDplot[0],sDplot[0]),('com deficiencia','sem deficiencia'))#legendas para plots

def autolabel(rects):
	#anexar dados aos titulos
	for rect in rects:
		height=rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2.,1.05*height,'%d'%int(height),
			ha='center',va='bottom')
autolabel(cDplot)
autolabel(sDplot)

plt.show()
