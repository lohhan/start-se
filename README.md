# Sistema de Captação de Investimentos

Este projeto é um sistema de captação de investimentos para empresários, desenvolvido utilizando Django. Ele permite que usuários cadastrados possam tanto captar investimentos para suas próprias empresas quanto investir em outras. Este foi meu primeiro projeto utilizando Django, onde tive a oportunidade de aprender bastante sobre o framework e o desenvolvimento de aplicações web.

## Funcionalidades

- **Cadastro de Usuários**: Os usuários podem criar uma conta e fazer login no sistema.
- **Captação de Investimentos**: Empresários podem criar campanhas de captação de investimentos para suas empresas.
- **Investimento em Campanhas**: Usuários podem visualizar campanhas de outras empresas e investir nelas.

## Tecnologias Utilizadas

- **Django**: Framework principal utilizado para o desenvolvimento do back-end.
- **SQLite**: Banco de dados utilizado para armazenar as informações das campanhas e dos usuários.
- **Bootstrap**: Utilizado para o design e responsividade da interface.
- **HTML/CSS**: Para a estrutura e estilização das páginas.

## Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/lohhan/start-se.git
   
2. Navegue até a pasta do projeto:
   ```bash
    cd start-se
    
3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate

4. Instale as depêndencias:
   ```bash
   pip install -r requirements.txt

5. Execute as migrações:
   ```bash
   python manage.py migrate

6. Inicie o servidor local:
   ```bash
   python manage.py runserver

7. Acesse o sistema em http://127.0.0.1:8000/ no seu navegador.
