import json
import requests
from bcb import sgs
import streamlit as st

import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

st.title('Análise das expectativas do boletim focus - Guilherme e Esthevão')
st.sidebar.title('Índice')
indice  = st.sidebar.selectbox('Selecione a sessão desejada', ['Introdução e Objetivos', 'Obtenção dos Dados/Metodologia', 
                                                    'Análise Descritiva (Gráficos)',
                                                    'Modelo preditivo',
                                                    'Conclusão'])
st.sidebar.image("./fgv-logo-1.png", width=200)
upload = st.sidebar.file_uploader('Anexe aqui a base de dados')
pib = []
if upload is not None:
        pib = pd.read_excel(upload, sheet_name = 'PIB')
        ipca = pd.read_excel(upload, sheet_name = 'IPCA')
        cambio = pd.read_excel(upload, sheet_name = 'CAMBIO')         

                            
if indice ==  'Introdução e Objetivos':
    st.header('Introdução e Objetivos')
    st.write('O objetivo principal deste trabalho consiste em conduzir uma análise relativa a acurácia das previsões realizadas por agentes do mercado para o patamar futuro de variáveis macroeconômicas chave, como a inflação (mensurada pelo IPCA), a taxa de câmbio (R\$/US\$) e o crescimento do PIB. Estre trabalho é baseado na _Pesquisa de Expectativas de Mercado_ que, conduzida desde maio de 1999 pelo Banco Central Brasileiro, foi utilizada como parte da transição para o regime de metas para a inflação. O objetivo da PEM é monitorar a evolução das expectativas de mercado para as principais variáveis macroeconômicas, de forma a gerar subsídios para o processo decisório da política monetária.')
    st.write('A pesquisa acompanha as expectativas de mercado para diferentes índices de preços, crescimento do PIB e da produção industrial, taxa de câmbio, taxa Selic, variáveis fiscais e indicadores do setor externo. Em novembro de 2001, foi criada página própria na internet (www.bcb.gov.br/expectativa) para a realização da pesquisa, com acesso restrito a instituições com login e senha específica. Em consequência, o Banco Central pode acompanhar o estado das expectativas de mercado em tempo real.')    
    st.markdown(
"""
Atualmente o Departamento de Estatísticas (Dstat) administra o Sistema Expectativas de Mercado, e seus relatórios são distribuídos a uma lista de e-mails com cerca de 26.000 endereços eletrônicos, que recebem adicionalmente vários relatórios do Banco Central, em português e inglês, além dos comunicados e das Notas produzidas pelo Comitê de Política Monetária, em inglês. Os relatórios sobre expectativas de mercado (Focus) incluem:
- :blue[Focus-Relatório de Mercado]: apresentação de um resumo dos resultados da pesquisa de expectativas de mercado, levantamento diário das previsões de cerca de 130 bancos, gestores de recursos e demais instituições (empresas do setor real, distribuidoras, corretoras, consultorias e outras) para a economia brasileira, publicado toda segunda-feira;
- :blue[Focus-Distribuições de Frequência]: relatório que mostra a evolução das distribuições de frequência das medianas das expectativas de mercado para o IPCA do ano corrente e dos próximos três anos e da Taxa Selic 12 meses à frente coletadas pelo Sistema Expectativas de Mercado, com intervalos de um e três meses, publicado toda primeira segunda-feira de cada mês (caso não seja dia útil, no primeiro dia útil subsequente
- :blue[Focus-Top 5]: classificação mensal/anual das instituições com melhores previsões dentre as participantes da pesquisa de mercado.
"""
)       
    
    
    
elif indice ==  'Obtenção dos Dados/Metodologia':
    st.header('Obtenção dos Dados/Metodologia')
    st.write('Para a obtenção de nossos dados, iremos realizar um WebScrapping da página https://www3.bcb.gov.br/expectativas2/#/consultas que faz parte do Sistema Expectativas de Mercado, do Banco Central Brasileiro. O site do BCB nós permite coletar qual a Mediana, Desvio Padrão, Mínimo e Máximo das expectativas de agentes do mercado para variáveis macroeconômicas como inflação (mensurada pelo IPCA) e taxa de câmbio (R\$/US\$)). Para uma mesmo período futuro, como o primeiro trimestre de 2024, somos capazes de coletar diversos valores para, por exemplo, a mediana das expectativas de uma variável em questão. Isso, pois as previsões para um mesmo período futuro são realizadas em diferentes datas, ou seja, é possível que tenhamos, nos dias 31/12/2022 e 31/01/2023, previsões para o crescimento do PIB no ano de 2023. Em nosso trabalho, coletamos expectativas para o crescimento do PIB de dois meses a frente, do IPCA de 4 meses a frente e do taxa de câmbio também de 4 meses a frente. ')
    st.write('Para exemplificar o que está sendo dito, tomemos como base o dataframe referente ao PIB, que está disponibilizado abaixo. Note que existem 5 colunas: Observado, Mínimo, Mediana, Máximo e Média. Peguemos a primeira linha como exemplo. Esta refere-se ao segundo trimestre de 2011. Nesse caso, temos que o crescimento do PIB do país nesse trimestre foi de 3.66% quando comparado ao primeiro trimestre de 2011. Além disso, 2 meses antes do início desse trimestre a mediana das expectativas indicava um crescimento de 4.07%. A mínima das projeções indicava um crescimento de 2.6% e a máxima das expectativas coletadas pelo Banco Central apontava para um crescimento de 5.62%. A ideia do trabalho é, portanto, comparar essas projeções ao resultado realizado da variável.')
    st.write(pib.head())
    

elif indice ==  'Análise Descritiva (Gráficos)':
    st.header('Análise Descritiva (Gráficos)')
    st.write('Análise dos dados')
    grafico_sem_alt = st.checkbox('Clique aqui para mostrar o gráfico das séries sem alterações')
    if grafico_sem_alt and upload is not None:
        fig, ax = plt.subplots(1, 3)
        fig.set_figwidth(17)
        sns.lineplot(data = pib, ax = ax[0], palette = sns.color_palette("mako_r", 5), linewidth = 2).set(title = 'PIB')
        sns.lineplot(data = ipca, ax = ax[1], palette = sns.color_palette("mako_r", 5), linewidth = 2).set(title = 'IPCA')
        sns.lineplot(data = cambio, ax = ax[2], palette = sns.color_palette("mako_r", 5), linewidth = 2).set(title = 'Câmbio')
        st.pyplot(fig)
    elif upload is None:
        st.markdown(':red[Anexe os arquivos]')
     
    grafico_med = st.checkbox('Clique aqui para mostrar o Gráfico das Séries média móvel com 5 períodos')
    if grafico_med and upload is not None:
        fig, ax = plt.subplots(1, 3)
        fig.set_figwidth(17)
        sns.lineplot(data = pib.rolling(5).mean(), ax = ax[0]).set(title = 'PIB')
        sns.lineplot(data = ipca.rolling(5).mean(), ax = ax[1]).set(title = 'IPCA')
        sns.lineplot(data = cambio.rolling(5).mean(), ax = ax[2]).set(title = 'Câmbio')
        st.pyplot(fig)
    elif upload is None:
        st.markdown(':red[Anexe os arquivos]')
        
        
    grafico_reg = st.checkbox('Clique aqui para mostrar o Gráfico da Regressão Mediana vs Observado')
    if grafico_reg and upload is not None:
        fig, ax = plt.subplots(1, 3)
        fig.set_figwidth(17)
        sns.regplot(data = pib, x = "Mediana", y = "Observado", ax = ax[0]).set(title = 'PIB')
        sns.regplot(data = ipca, x = "Mediana", y = "Observado", ax = ax[1]).set(title = 'IPCA')
        sns.regplot(data = cambio, x = "Mediana", y = "Observado", ax = ax[2]).set(title = 'Câmbio')
        st.pyplot(fig)
    elif upload is None:
        st.markdown(':red[Anexe os arquivos]')  
    
    
    grafico_hist = st.checkbox('Clique aqui para mostrar o Histograma de Distribuições')
    if grafico_hist and upload is not None:
        fig, ax = plt.subplots(1, 3)
        fig.set_figwidth(17)
        sns.histplot(data = pib[["Observado", "Mediana"]], palette = sns.color_palette("mako_r", 2), ax = ax[0]).set(title = 'PIB')
        sns.histplot(data = ipca[["Observado", "Mediana"]], palette = sns.color_palette("mako_r", 2), ax = ax[1]).set(title = 'IPCA')
        sns.histplot(data = cambio[["Observado", "Mediana"]], palette = sns.color_palette("mako_r", 2), ax = ax[2]).set(title = 'Câmbio')
        st.pyplot(fig)
    elif upload is None:
        st.markdown(':red[Anexe os arquivos]')  
    
    analise_des = st.checkbox('Clique aqui para mostrar uma análise descritiva das séries realizadas/observas')
    if analise_des and upload is not None:
        correl = pd.concat([pib.corr().filter(["Observado"], axis = 0),
                   ipca.corr().filter(["Observado"], axis = 0),
                   cambio.corr().filter(["Observado"], axis = 0)], axis = 0)
        correl.index = ["PIB", "IPCA", "Câmbio"]
        st.write(correl[correl.columns[1:]].apply(lambda x: x.apply(lambda x: str(round(100*x, 2)) + "%")))
    elif upload is None:
        st.markdown(':red[Anexe os arquivos]')  
    if grafico_sem_alt and grafico_med and grafico_reg and grafico_hist and analise_des and upload is not None:
        st.markdown(':blue[Análises]')
        st.write('Por meio dos gráficos das séries, é possível analisar como os dados ocorreram e comparar isso com suas expectativas. Em relação ao PIB, as expectativas normalmente seguem um caminho diferente do que ocorre na realidade, principalmente devido à dificuldade de medir isso, visto que há poucas variáveis que ajudam a prever o PIB em tantos períodos anteriormente assim. Como selecionamos a predição do PIB em 2 períodos antes e essa variável demora a sair, é possível perceber que essa predição normalmente erra mais, para todos os níveis (mediana, mínimo, máximo e média)')
        st.write('Quanto ao câmbio e ao IPCA, elas tendem a acertar mais, principalmente pois a frequência dos dados é bem maior e há mais insumos. Por exemplo, as expectativas do PIB são formadas com base na PIM, na PMS e na PMC, que saem 2 meses após o período de referência, enquanto a inflação segue com base em preços de atacado, que saem diariamente, o que aumenta o poder de predição dos agentes do mercado no relatório Focus.')
        st.write('Além disso, também é possível analisar os gráficos de média móvel em 5 períodos e, por meio dela, é fácil perceber que o câmbio tem uma certa defasagem, de modo que as expectativas normalmente seguem muito o que ocorrer e tendem a errar muito, porém são próximas do valor original caso seja acrescentando um intercepto. Além disso, o PIB normalmente é superestimado em épocas de boom e subestimado em épocas de recessão.')
        st.write('Por meio dos gráficos de regressão, é também possível perceber que o PIB é aquele que tem um menor poder preditivo, visto o alto intervalo de confiança e a baixa inclinação desse gráfico, enquanto IPCA e câmbio possuem menor intervalo de confiança e maior intercepto, porém com preferência para câmbio.')
        st.write('Nos resíduos da regressão, é possível perceber que o IPCA é aquele que mais se aproxima de uma normal, pois é a variável que tem um modelo acertivo e é uma variável estacionária, diferentemente de câmbio.')
                 
    
elif indice ==  'Modelo preditivo':
    st.header('Modelo preditivo')
    st.write('Nosso modelo preditivo!')
    if upload is not None:
        pibx_train, pibx_test, piby_train, piby_test = train_test_split(pib[["Mediana", "Minimo", "Maximo", "Maximo", "Média"]],
                                                                        pib["Observado"], test_size = 0.33)

        ipcax_train, ipcax_test, ipcay_train, ipcay_test = train_test_split(ipca[["Mediana", "Minimo", "Maximo", "Maximo", "Média"]],
                                                                            ipca["Observado"], test_size = 0.33)

        cambiox_train, cambiox_test, cambioy_train, cambioy_test = train_test_split(cambio[["Mediana", "Minimo", "Maximo", "Maximo", "Média"]],
                                                                                cambio["Observado"], test_size = 0.33)
        pibx_train_int = sm.add_constant(pibx_train["Minimo"])
        pibx_test_int = sm.add_constant(pibx_test["Minimo"])
        regpib = sm.OLS(piby_train, pibx_train_int).fit()
        reg_pib_display = st.checkbox('Clique aqui para mostrar o resultado da regressão do PIB')
        if reg_pib_display:
            st.markdown('Os resultados para a regressão do :blue[PIB] são:')
            st.write(regpib.summary())
         
        reg_ipca_display = st.checkbox('Clique aqui para mostrar o resultado da regressão do IPCA')
        if reg_ipca_display:
            ipcax_train_int = sm.add_constant(ipcax_train["Média"])
            ipcax_test_int = sm.add_constant(ipcax_test["Média"])
            regipca = sm.OLS(ipcay_train, ipcax_train_int).fit()
            st.markdown('Os resultados para a regressão do :blue[IPCA] são:')
            st.write(regipca.summary())
          
        reg_cambio_display = st.checkbox('Clique aqui para mostrar o resultado da regressão do Câmbio', key = 3)
        if reg_cambio_display:
            cambiox_train_int = sm.add_constant(cambiox_train["Mediana"])
            cambiox_test_int = sm.add_constant(cambiox_test["Mediana"])
            regcambio = sm.OLS(cambioy_train, cambiox_train_int).fit()
            st.markdown('Os resultados para a regressão do :blue[Câmbio] são:')
            st.write(regcambio.summary())

            
        display_histogramas_predict = st.checkbox('Clique aqui para mostrar os histogramas pevistos')   
        if display_histogramas_predict and reg_ipca_display and reg_cambio_display and reg_pib_display:
            st.markdown('Aqui estão os :blue[histogramas]')
            fig, ax = plt.subplots(1, 3)
            fig.set_figwidth(17)
            sns.histplot(data = piby_test - regpib.predict(pibx_test_int),
                         palette = sns.color_palette("mako_r", 2), ax = ax[0]).set(title = 'PIB')
            sns.histplot(data = ipcay_test - regipca.predict(ipcax_test_int),
                         palette = sns.color_palette("mako_r", 2), ax = ax[1]).set(title = 'IPCA')
            sns.histplot(data = cambioy_test - regcambio.predict(cambiox_test_int),
                         palette = sns.color_palette("mako_r", 2), ax = ax[2]).set(title = 'Câmbio')
            st.pyplot(fig)
        elif display_histogramas_predict:
            st.markdown(':red[Rode primeiro as regressões!]')
        
        display_testes = st.checkbox('Clique aqui para mostrar o resultado de alguns testes')
        if display_testes and reg_ipca_display and reg_cambio_display and reg_pib_display:
            st.markdown('Aqui estão os :blue[testes de hipóteses das regressões]!')
            testes = pd.concat([pd.DataFrame([metrics.mean_absolute_error(piby_test, regpib.predict(pibx_test_int)),
              metrics.mean_squared_error(piby_test, regpib.predict(pibx_test_int))**0.5,
              metrics.r2_score(piby_test, regpib.predict(pibx_test_int))]),
            pd.DataFrame([metrics.mean_absolute_error(ipcay_test, regipca.predict(cambiox_test_int)),
                  metrics.mean_squared_error(ipcay_test, regipca.predict(cambiox_test_int))**0.5,
                  metrics.r2_score(ipcay_test, regipca.predict(cambiox_test_int))]),
            pd.DataFrame([metrics.mean_absolute_error(cambioy_test, regcambio.predict(ipcax_test_int)),
                  metrics.mean_squared_error(cambioy_test, regcambio.predict(ipcax_test_int))**0.5,
                  metrics.r2_score(cambioy_test, regcambio.predict(ipcax_test_int))])], axis = 1)

            testes.index = ["MAE", "RMSE", "R²"]
            testes.columns = ["PIB", "IPCA", "Câmbio"]
            st.write(testes)
        elif display_testes:
            st.markdown(':red[Rode primeiro as regressões!]')
        
        display_fit = st.checkbox('Clique aqui para mostrar o fit das regressões:')
        if display_fit and reg_ipca_display and reg_cambio_display and reg_pib_display:
            st.markdown('Aqui está um gráfico dos :blue[fits das regressões]!')
            
            scaler = StandardScaler()
            pib_train_nn = scaler.fit_transform(pibx_train[["Minimo"]])
            pib_test_nn = scaler.fit_transform(pibx_test[["Minimo"]])
            ipca_train_nn = scaler.fit_transform(ipcax_train[["Média"]])
            ipca_test_nn = scaler.fit_transform(ipcax_test[["Média"]])
            cambio_train_nn = scaler.fit_transform(cambiox_train[["Mediana"]])
            cambio_test_nn = scaler.fit_transform(cambiox_test[["Mediana"]])

            model = MLPRegressor(hidden_layer_sizes=(64, 64,64), 
                                 activation="relu" ,
                                 random_state=42, max_iter=2000)

            model.fit(pib_train_nn, piby_train)
            pib_pred = pd.DataFrame(model.predict(pib_test_nn), index = pibx_test.index, columns = ["Predito"])

            model = MLPRegressor(hidden_layer_sizes=(64, 64,64), 
                                 activation="relu" ,
                                 random_state=42, max_iter=2000)

            model.fit(ipca_train_nn, ipcay_train)
            ipca_pred = pd.DataFrame(model.predict(ipca_test_nn), index = ipcax_test.index, columns = ["Predito"])

            model = MLPRegressor(hidden_layer_sizes=(64, 64,64), 
                                 activation="relu" ,
                                 random_state=42, max_iter=2000)

            model.fit(cambio_train_nn, cambioy_train)

            cambio_pred = pd.DataFrame(model.predict(cambio_test_nn), index = cambiox_test.index, columns = ["Predito"])

            regpibpredict = pd.DataFrame(regpib.predict(pibx_test_int), index = pibx_test.index, columns = ["Regressão"])
            regipcapredict = pd.DataFrame(regipca.predict(ipcax_test_int), index = ipcax_test.index, columns = ["Regressão"])
            regcambiopredict = pd.DataFrame(regcambio.predict(cambiox_test_int), index = cambiox_test.index, columns = ["Regressão"])

            fig, ax = plt.subplots(1, 3)
            fig.set_figwidth(17)
            sns.lineplot(data = pd.concat([piby_test, pib_pred, regpibpredict], axis = 1),
                         palette = sns.color_palette("mako_r", 3), linewidth = 2, ax = ax[0]).set(title = 'PIB')
            sns.lineplot(data = pd.concat([ipcay_test, ipca_pred, regipcapredict], axis = 1),
                         palette = sns.color_palette("mako_r", 3), linewidth = 2, ax = ax[1]).set(title = 'IPCA')
            sns.lineplot(data = pd.concat([cambioy_test, cambio_pred, regcambiopredict], axis = 1),
                         palette = sns.color_palette("mako_r", 3), linewidth = 2, ax = ax[2]).set(title = 'Câmbio')
            st.pyplot(fig)
            
            testes = pd.concat([pd.DataFrame([metrics.mean_absolute_error(piby_test, pib_pred),
                                  metrics.mean_squared_error(piby_test, pib_pred)**0.5,
                                  metrics.r2_score(piby_test, pib_pred)]),
                    pd.DataFrame([metrics.mean_absolute_error(ipcay_test, ipca_pred),
                                  metrics.mean_squared_error(ipcay_test, ipca_pred)**0.5,
                                  metrics.r2_score(ipcay_test, ipca_pred)]),
                    pd.DataFrame([metrics.mean_absolute_error(cambioy_test, cambio_pred),
                                  metrics.mean_squared_error(cambioy_test, cambio_pred)**0.5,
                                  metrics.r2_score(cambioy_test, cambio_pred)])], axis = 1)

            testes.index = ["MAE", "RMSE", "R²"]
            testes.columns = ["PIB", "IPCA", "Câmbio"]

            st.markdown('Aqui estão os resultados dos testes das Redes Neurais')
            st.write(testes) 
        if display_fit and reg_ipca_display and reg_cambio_display and reg_pib_display:
            st.markdown(':blue[Análises]')
            st.write('Nos modelos de machine learning, foram feitos modelos de regressão linear e de redes neurais para conseguir predizer o valor da variável observada com base em alguma das predições feitas. No caso do PIB, foi utilizado o mínimo, visto que possui maior correlação, enquanto para o IPCA foi utilizada a média e o câmbio foi utilizada a mediana. Nesse sentido, é possível perceber o que já tínhamos como conclusão, que era um modelo fraco para o PIB (8% de R² e não possível rejeitar que coeficiente seja zero), enquanto do IPCA e câmbio tiveram um maior poder preditivo, com destaque para o câmbio. Entretanto, quando olhamos para a aplicação desse modelo em nossa amostra de teste, ele já performa muito mal, com um rendimento melhor para o PIB (13%), porém um pior rendimento para câmbio e inflação, cujo valor do R² é negativo, o que indica que sua realização apenas fica possível para a amostra como um todo')

            st.write('Também foi feito um modelo de redes neurais, que utiliza a inteligência de máquina para conseguir utilizar os insumos para prever a variável output do nosso modelo. Nesse caso, quando aplicamos o modelo na amostra de treino, todos os resultados ficam melhores comparado à regressão, porém, no caso de teste, o PIB performa muito pior, visto o resultado negativo do R², enquanto os outros modelos têm uma performance melhorada em relação à regressão, apesar de esta ter um resultado positivo para a amostra de treino.')
        
        elif display_fit:
            st.markdown(':red[Rode primeiro as regressões!]')

        else:
            
            st.markdown(':red[Anexe os arquivos]') 
            
else:
        
        st.write('Portanto, é possível perceber que muitas vezes uma regressão simples não é o melhor método para estabelecer causalidade e também é interessante ver que as expecatativas do Focus muitas vezes não têm confirmação na realidade, visto que há muita assimetria de informação nos mercados, o que dificulta a estimação das variáveis reais. Entretanto, há algumas situações em que a regressão performa melhor que outros modelos mais complexos, visto que a amostra de treino pode ser pequena e isso pode impactar na predição, como é o caso do PIB, ao contrário do câmbio e do IPCA.')
    
 












