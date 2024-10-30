Link Dashboard: [DashBoard Tableau](https://public.tableau.com/app/profile/kaio.de.medeiros.gaspar/viz/Livro2_17302512095860/Painel1?publish=yes)

# Fundos Explorer Web Scraper

Este script realiza web scraping no site [Fundos Explorer](https://www.fundsexplorer.com.br) para coletar informações sobre fundos de investimento, incluindo variação de preço, dividendos e patrimônio líquido. Os dados são armazenados em DataFrames e salvos em arquivos `.csv` para análise posterior.

## Dependências

Certifique-se de ter instalado os pacotes necessários antes de rodar o script. Você pode instalar as dependências com o seguinte comando:

- `requests`
- `pandas`
- `beautifulsoup4`

## Passo a Passo para Execução do Código

1. **Clone o Repositório**:
   - Abra o terminal ou prompt de comando.
   - Execute o seguinte comando para clonar o repositório:
     ```bash
     git clone https://github.com/Kaio-Gaspar/web_scraping_fii
     ```
   
2. **Acesse o Diretório do Repositório**:
   - Navegue até o diretório do repositório clonado:
     ```bash
     cd web_scraping_fii
     ```

3. **Instale as Dependências**:
   - Execute o comando abaixo para instalar as bibliotecas necessárias:
     ```bash
     pip install -r requirements.txt
     ```
   
4. **Execute o Script**:
   - Para executar o script, utilize o comando:
     ```bash
     python scrap.py
     ```

5. **Verifique os Resultados**:
   - Após a execução, os dados serão salvos em três arquivos `.csv`:
     - `fundos_investimento.csv`: Contém informações detalhadas dos fundos de investimento.
     - `altas_de_hoje.csv`: Registra os fundos que tiveram altas significativas.
     - `baixas_de_hoje.csv`: Registra os fundos que apresentaram baixas significativas.

## Estrutura do Script

1. **Configurações Iniciais**: Define a URL e os headers para simular uma requisição de navegador.
2. **Coleta de Dados Gerais**: Extrai links, imagens e conteúdo principal da página.
3. **Altas e Baixas de Preços**: Coleta dados de variações diárias nos preços dos fundos.
4. **Informações dos Fundos**: Extração e formatação de dados detalhados dos fundos, como dividendos e patrimônio líquido.
5. **Armazenamento**: Salva os DataFrames em arquivos `.csv` para análise.

## Escolhas de Implementação

- **Requisições HTTP com `requests`**: A escolha de usar a biblioteca `requests` se deve à sua simplicidade e eficácia para realizar requisições HTTP. Essa biblioteca facilita a manipulação de headers e parâmetros, essencial para simular uma requisição de navegador e garantir que a página seja carregada corretamente.

- **Extração de Dados com `BeautifulSoup`**: Optar pelo `BeautifulSoup` para parsing HTML foi uma decisão estratégica. Esta biblioteca permite a navegação e busca eficiente na árvore DOM da página, facilitando a extração de dados específicos, mesmo em estruturas complexas de HTML. Sua facilidade de uso e robustez tornam o processo de scraping mais eficiente.

- **Manipulação de Dados com `pandas`**: A utilização do `pandas` para manipulação e armazenamento de dados é fundamental, pois oferece funcionalidades poderosas para trabalhar com DataFrames. Isso permite que os dados extraídos sejam organizados, filtrados e salvos em formatos acessíveis (como CSV), prontos para análise posterior. O uso do `pandas` facilita a limpeza e transformação de dados, tornando a análise mais fluida.

- **Tratamento de Dados Financeiros**: A formatação e limpeza dos dados financeiros foram implementadas para assegurar que as informações sejam apresentadas de maneira clara e utilizável. Isso inclui a remoção de caracteres indesejados e a conversão de tipos de dados (por exemplo, transformar strings monetárias em números), o que é crucial para análises numéricas.

- **Escalabilidade e Manutenção**: Ao planejar a escalabilidade do sistema, considerou-se a possibilidade de armazenar os dados em um banco de dados SQL. Isso não só melhoraria a organização e a consulta dos dados, mas também permitiria uma análise mais complexa a longo prazo, como a geração de relatórios históricos e tendências.

Essas escolhas foram feitas levando em conta a facilidade de implementação, a robustez do código e a eficiência na manipulação dos dados, garantindo que o scraper seja eficaz e facilmente adaptável a futuras necessidades.

  
## Desafios e Possíveis Melhorias

- **Classes Dinâmicas e Mudanças de Estrutura**: Como o Fundos Explorer pode alterar a estrutura do HTML, especialmente os nomes das classes, seria útil integrar um sistema de monitoramento que detecte essas mudanças. Alternativamente, podemos desenvolver uma abordagem que identifique os elementos dinamicamente para maior robustez.

- **Automação Diária**: Para capturar dados atualizados diariamente, uma melhoria seria agendar a execução automática do script usando `cron` no Linux ou `Task Scheduler` no Windows. Isso permitiria monitorar as variações de preço e dividendos de forma contínua.

- **Execução em Lote**: Implementar uma função que armazene os dados diretamente em um banco de dados SQL permitiria manipulação e análise mais eficiente de grandes volumes de dados ao longo do tempo.

Este script fornece uma base sólida para extração e análise de dados de fundos, com potencial de melhorias para um sistema de monitoramento mais robusto.

ps: Os dados faltantes foram deixados como NaN para evitar a interpretação de valores_nulos = 0 e facilitar o formato dos dados. Pensando em escabilidade essa questão é facilmente manipulada.
