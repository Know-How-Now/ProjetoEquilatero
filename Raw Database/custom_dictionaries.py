import pandas as pd

# ----------[DDD de Todos Estados e Regiões do Brasil]---------- #
ddd_data_string = '11,São Paulo,São Paulo e Região Metropolitana / Jundiaí e Aglomeração Urbana / São Roque-Mairinque / Itu-Salto / Bragança Paulista-Atibaia,12,São Paulo,São José dos Campos e Vale do Paraíba,13,São Paulo,Santos/Baixada Santista/Vale do Ribeira,14,São Paulo,Bauru/Marília/Jaú/Botucatu,15,São Paulo,Sorocaba e Itapetininga,16,São Paulo,Ribeirão Preto/Araraquara/São Carlos,17,São Paulo,São José do Rio Preto/Barretos,18,São Paulo,Presidente Prudente/Araçatuba/Assis,19,São Paulo,Campinas e Região Metropolitana/Piracicaba,21,Rio de Janeiro,Rio de Janeiro/ Região Metropolitana e Teresópolis,22,Rio de Janeiro,Campos dos Goytacazes/Nova Friburgo/Macaé/Cabo Frio,24,Rio de Janeiro,Petrópolis/Volta Redonda/Angra dos Reis,27,Espírito Santo,Vitória e Região Metropolitana,28,Espírito Santo,Mesoreregião Sul do Espírito Santo,31,Minas Gerais,Belo Horizonte/ Região Metropolitana e Vale do Aço,32,Minas Gerais,Juiz de Fora/São João Del Rei,33,Minas Gerais,Governador Valadares/Teófilo Otoni/Caratinga/Manhuaçu,34,Minas Gerais,Uberlândia e Triângulo Mineiro,35,Minas Gerais,Poços de Caldas/Pouso Alegre/Varginha,37,Minas Gerais,Divinópolis/Itaúna,38,Minas Gerais,Montes Claros/Diamantina/Noroeste de Minas,41,Paraná,Curitiba e Região Metropolitana,42,Paraná,Ponta Grossa/Guarapuava,43,Paraná,Londrina/Apucarana,44,Paraná,Maringá/Campo Mourão/Umuarama,45,Paraná,Cascavel/Foz do Iguaçu,46,Paraná,Francisco Beltrão/Pato Branco,47,Santa Catarina,Joinville/Blumenau/Itajaí/Balneário Camboriú,48,Santa Catarina,Florianópolis e Região Metropolitana/Criciúma/Tubarão,49,Santa Catarina,Chapecó/Lages/Caçador,51,Rio Grande do Sul,Porto Alegre e Região Metropolitana/Santa Cruz do Sul/Litoral Norte,53,Rio Grande do Sul,Pelotas/Rio Grande,54,Rio Grande do Sul,Caxias do Sul/Passo Fundo,55,Rio Grande do Sul,Santa Maria/Uruguaiana/Santana do Livramento/Santo Ângelo,61,Distrito Federal/Goiás,Abrangência em todo o Distrito Federal e municípios goianos da Região Integrada de Desenvolvimento do Distrito Federal e Entorno,62,Goiás,Goiânia e Região Metropolitana/Anápolis/Niquelândia/Porangatu,63,Tocantins,Abrangência em todo o estado,64,Goiás,Rio Verde/Itumbiara/Caldas Novas/Catalão,65,Mato Grosso,Cuiabá e Região Metropolitana,66,Mato Grosso,Rondonópolis/Sinop,67,Mato Grosso do Sul,Abrangência em todo o estado,68,Acre,Abrangência em todo o estado,69,Rondônia,Abrangência em todo o estado,71,Bahia,Salvador e Região Metropolitana,73,Bahia,Itabuna/Ilhéus,74,Bahia,Juazeiro,75,Bahia,Feira de Santana/Alagoinhas,77,Bahia,Vitória da Conquista/Barreiras,79,Sergipe,Abrangência em todo o estado,81,Pernambuco,Recife e Região Metropolitana/Caruaru,82,Alagoas,Abrangência em todo o estado,83,Paraíba,Abrangência em todo o estado,84,Rio Grande do Norte,Abrangência em todo o estado,85,Ceará,Fortaleza e Região Metropolitana,86,Piauí,Teresina e Região Metropolitana/Parnaíba,87,Pernambuco,Petrolina/Garanhuns/Serra Talhada/Salgueiro,88,Ceará,Juazeiro do Norte/Sobral,89,Piauí,Picos/Floriano,91,Pará,Belém/Região Metropolitana,92,Amazonas,Manaus/Região Metropolitana/Parintins,93,Pará,Santarém/Altamira,94,Pará,Marabá,95,Roraima,Abrangência em todo o estado,96,Amapá,Abrangência em todo o estado,97,Amazonas,Abrangência no interior do estado,98,Maranhão,São Luís e Região Metropolitana,99,Maranhão,Imperatriz/Caxias'
ddd_data_list = ddd_data_string.split(',')

ddd_list = ddd_data_list[0::3]
ddd_state_list = ddd_data_list[1::3]
ddd_region_list = ddd_data_list[2::3]

ddd_labels = ['DDD','State','Region']
ddd_columns = [ddd_list, ddd_state_list, ddd_region_list]

ddd_zipped = list(zip(ddd_labels, ddd_columns))
ddd_dict = dict(ddd_zipped)

ddd_data_df = pd.DataFrame(ddd_dict)

ddd_data_df = pd.DataFrame(ddd_dict)

def ddd_df_read(label_index):
    for i, row in ddd_data_df.iterrows():
        print(row[label_index])

# ----------[Track Hashtags]---------- #
track_hashtags_string = 'Poucos obstaculos,Muitos obstaculos,Poucos obstaculos,Desnivel positivo,Desnivel negativo,Mata Aberta,Mata Fechada,Piso Regular,Piso Irregular,Riachos,Alta insolacao,Baixa insolacao,Cachoeira,Riachos,Rios,Escaladas'
track_hashtags_list = track_hashtags_string.split(',')

track_traits_1_list = track_hashtags_list[0::2]
track_traits_2_list = track_hashtags_list[1::2]