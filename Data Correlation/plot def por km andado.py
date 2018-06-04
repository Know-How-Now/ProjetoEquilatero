import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

grupos=5

comDef=[10,20,45,12,9]
cD_std=[2,3,4,1,2]
semDef=[12,21,39,13,8]
sD_std=[3,5,2,3,3]

fig, ax=plt.subplots()

index=np.arange(grupos)
largura=.4

opacidade=.3
errorCon={'ecolor':'.3'}

rects1=ax.bar(index,comDef,largura,alpha=opacidade,color='b',
	error_kw=errorCon, label='Com deficiencia')
rects2=ax.bar(index+largura,semDef,largura,alpha=opacidade,color='r',
        error_kw=errorCon,label='Sem deficiencia')
ax.set_xlabel('Km andados')
ax.set_ylabel('numero de pessoas')
ax.set_title('Kms andados por numero de pessoas com ou sem deficiencia')
ax.set_xticks(index+largura/2)
ax.set_xticklabels(('1kms','2kms','5kms','7kms','10kms'))
ax.legend()

fig.tight_layout()
plt.show()
