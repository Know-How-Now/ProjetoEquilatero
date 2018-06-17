#------------Numero de pessoas que passaram por uma km específica----------#
import matplotlib.pyplot as plt
import numpy as np
cDef=12#criar função para computar numero de pessoas com defiencia que passaram por km(x)
sDef=10#idem pra pessoas sem def

fig,ax=plt.subplots(figsize=(6,3),subplot_kw=dict(aspect='equal'))

segmentos=[cDef,sDef]
grupos=['com deficiência','sem deficiência']
cores=['r','g']

def func(pct,allvals):
	absolute=int(pct/100.*np.sum(allvals))
	return "{:.1f}%\n({:d})".format(pct,absolute)
wedges, texts, autotexts=ax.pie(segmentos,autopct=lambda pct: func(pct,segmentos),
	textprops=dict(color='w'),colors=cores)

ax.legend(wedges, grupos,
	title='numero de pessos',
	loc='lower right',
	bbox_to_anchor=(1,0))
plt.setp(autotexts,weight='bold')

'''
plt.pie(segmentos,
	labels=grupos,
	startangle=90,
	shadow=True,
	autopct='%1.1f')
'''
ax.set_title('numero de pessoas que andaram até 10km')
#plt.legend()
plt.show()
