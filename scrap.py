import requests
import pandas as pd
from bs4 import BeautifulSoup

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Descrição Geral do Bloco
# Este código realiza web scraping em duas páginas do site Fundsexplorer,
# coletando dados financeiros, como variação de preço de fundos e dividendos.
# Em seguida, organiza essas informações em DataFrames para análise posterior.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ## Parte 1: Configurações Iniciais @@@@@@@@@@
# Definição da URL e cabeçalhos para a requisição HTTP
url = 'https://www.fundsexplorer.com.br/'
fundos_url = 'https://www.fundsexplorer.com.br/funds'

# Cabeçalho para simular uma requisição vinda de um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# ## Parte 2: Acessando a Página Principal e Coletando Dados Gerais @@@@@@@@@@
# Faz a requisição HTTP e analisa se a resposta foi bem-sucedida
response = requests.get(url, headers=headers)

# Verificação do status da resposta
if response.status_code == 200:
    print("Acesso bem-sucedido!")

    # Analisando o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai o título da página
    title = soup.title.string if soup.title else "Título não encontrado"
    print("Título da Página:", title)

    # Coleta e exibe os primeiros 5 links encontrados na página
    links = [a['href'] for a in soup.find_all('a', href=True)]
    print("\n 5 Primeiros links encontrados:")
    for link in links[5:10]:
        print(link)

    # Extrai o conteúdo principal (primeiro parágrafo)
    main_content = soup.find('p').get_text() if soup.find('p') else "Conteúdo principal não encontrado"
    print("\nConteúdo Principal(primeiro):", main_content)

    # Coleta e exibe as URLs das primeiras 5 imagens encontradas
    image_urls = [img['src'] for img in soup.find_all('img', src=True)]
    print("\nURLs das 5 primeiras imagens:")
    for img_url in image_urls[:5]:
        print(img_url)

    # ## Parte 3: Coletando Dados de Altas e Baixas de Preços @@@@@@@@@@
    # Extrai divs que contêm informações de altas e baixas de preços de fundos
    altas_div = soup.find('div', class_='tab1')
    baixas_div = soup.find('div', class_='tab2')

    # Coleta dados das altas (preços, nomes de fundos, variação percentual)
    if altas_div:
        precos_cotacao_hoje_altas = [b.get_text(strip=True) for b in altas_div.find_all('b')]
        fundos_cotacao_hoje_altas = [a.get_text(strip=True) for a in altas_div.find_all('a')]
        porcentagem_do_fundo_altas = [span.get_text(strip=True) for span in altas_div.find_all('span')]

        # print("\nDados das Altas:")
        # print(precos_cotacao_hoje_altas)
        # print(fundos_cotacao_hoje_altas)
        # print(porcentagem_do_fundo_altas)
    else:
        print("Div com as altas não encontrada.")

    # Coleta dados das baixas (preços, nomes de fundos, variação percentual)
    if baixas_div:
        precos_cotacao_hoje_baixas = [b.get_text(strip=True) for b in baixas_div.find_all('b')]
        fundos_cotacao_hoje_baixas = [a.get_text(strip=True) for a in baixas_div.find_all('a')]
        porcentagem_do_fundo_baixas = [span.get_text(strip=True) for span in baixas_div.find_all('span')]

        # print("\nDados das Baixas:")
        # print(precos_cotacao_hoje_baixas)
        # print(fundos_cotacao_hoje_baixas)
        # print(porcentagem_do_fundo_baixas)
    else:
        print("Div com as baixas não encontrada.")

    # Cria DataFrames para armazenar e organizar os dados de altas e baixas
    df_baixas_de_hoje = pd.DataFrame({
        'Fundos': fundos_cotacao_hoje_baixas,
        'Preço': precos_cotacao_hoje_baixas,
        'Variação': porcentagem_do_fundo_baixas
    })

    df_altas_de_hoje = pd.DataFrame({
        'Fundos': fundos_cotacao_hoje_altas,
        'Preço': precos_cotacao_hoje_altas,
        'Variação': porcentagem_do_fundo_altas
    })

    # print("\nDataFrame de Altas de Hoje:")
    # print(df_altas_de_hoje)

    # print("\nDataFrame de Baixas de Hoje:")
    # print(df_baixas_de_hoje)

else:
    print(f'Deu ruim: Código de status {response.status_code}')

# ## Parte 4: Acessando a Página de Fundos e Coletando Informações dos Fundos @@@@@@@@@@
# Faz requisição HTTP para página com dados dos fundos
response_fundos = requests.get(fundos_url, headers=headers)

if response_fundos.status_code == 200:

    # Analisando conteúdo HTML da resposta
    soup = BeautifulSoup(response_fundos.content, 'html.parser')

    # Encontra divs com dados de cada fundo
    titulo_fundo_div = soup.find_all('div', class_='tickerBox link-tickers-container')

    # Inicializa listas para armazenar dados dos fundos
    titulos_fundo_lista = []
    categorias_titulo_lista = []
    dividendos_lista = []
    patrimonio_liquido_lista = []
    descricao_fundo_lista = []

    # Extrai informações de cada fundo na lista
    for div in titulo_fundo_div:
        dividendo = div.find_all('div', "tickerBox__info__box")[0].get_text()
        dividendos_lista.append(dividendo)

        patrimonio_liquido = div.find_all('div', "tickerBox__info__box")[1].get_text(strip=False)
        patrimonio_liquido_lista.append(patrimonio_liquido)

        categoria_titulo = [categoria.get_text(strip=True) for categoria in div.find_all('span')]
        categorias_titulo_lista.append(categoria_titulo)

        titulos = [titulo.get_text(strip=True) for titulo in div.find_all('a')]
        titulos_fundo_lista.append(titulos)

        descricao_fundo = div.find_all('div', "tickerBox__desc")[0].get_text(strip=False)
        descricao_fundo_lista.append(descricao_fundo)

    # print(f'Tamanho da lista de títulos: {len(titulos_fundo_lista)}')
    # print(f'Tamanho da lista de dividendos_lista: {len(dividendos_lista)}')
    # print(f'Tamanho da lista de patrimônio líquido: {len(patrimonio_liquido_lista)}')
    # print(f'Tamanho da lista de categorias: {len(categorias_titulo_lista)}')

    # ## Parte 5: Criando e Formatando o DataFrame dos Fundos @@@@@@@@@@
    # Cria DataFrame com os dados coletados
    df_fundos = pd.DataFrame({
        'Título': titulos_fundo_lista,
        'Dividendos': dividendos_lista,
        'Patrimônio Líquido': patrimonio_liquido_lista,
        'Categoria': categorias_titulo_lista,
        'Descrição': descricao_fundo_lista
    })

    # Limpeza de caracteres e substituições para melhorar a formatação dos dados
    df_fundos = df_fundos.replace({',':'.', '-':'',r'\[':'', r'\]':''}, regex=True)
    df_fundos = df_fundos.drop(index=464, axis=0)

    # Função para converter valores financeiros com sufixo
    def converter_patrimonio(valor):
        if valor.endswith('B'):  # Bilhão
            return float(valor[:-1]) * 1_000_000_000
        elif valor.endswith('M'):  # Milhão
            return float(valor[:-1]) * 1_000_000
        elif valor.endswith('K'):  # Mil
            return float(valor[:-1]) * 1_000

    # Aplicação de funções para formatação
    df_fundos['Título'] = [
        ', '.join(titulo) if isinstance(titulo, list) else str(titulo)
        for titulo in df_fundos['Título']
    ]

    df_fundos['Categoria'] = [
        ', '.join(categoria_titulo) if isinstance(categoria_titulo, list) else str(categoria_titulo)
        for categoria_titulo in df_fundos['Categoria']
    ]

    # Converte patrimônio líquido usando a função definida
    df_fundos['Patrimônio Líquido'] = df_fundos['Patrimônio Líquido'].apply(converter_patrimonio)

    # Converte colunas numéricas para tipos apropriados
    pd.to_numeric(df_fundos['Dividendos'])
    pd.to_numeric(df_fundos['Patrimônio Líquido'])

    # print("\nDataFrame de Fundos Formatado:")
    # print(df_fundos.head())

    # Salva o DataFrame de Fundos em um arquivo CSV
    df_fundos.to_csv('dados/fundos_investimento.csv', index=False, encoding='utf-8', sep=';')

    # Salva o DataFrame das Altas de Hoje em um arquivo CSV
    df_altas_de_hoje.to_csv('dados/altas_de_hoje.csv', index=False, encoding='utf-8')

    # Salva o DataFrame das Baixas de Hoje em um arquivo CSV
    df_baixas_de_hoje.to_csv('dados/baixas_de_hoje.csv', index=False, encoding='utf-8')


else:
    print(f'Erro: Código de status {response_fundos.status_code}')

