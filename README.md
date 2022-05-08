# Trips Data Ingestion Challenge

### Description 

This challenge will evaluate your proficiency in Data Engineering, and your knowledge in Software development as well. 

### Assignment 

Your task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination. 

This CSV file gives you a small sample of the data your solution will have to handle. We would like to have some visual reports of this data, but in order to do that, we need the following features. 

We do not need a graphical interface. Your application should preferably be a REST API, or a console application. 

### Mandatory Features
- [x] There must be an automated process to ingest and store the data. 
- [x] Trips with similar origin, destination, and time of day should be grouped together. ● Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region. 
- [x] Develop a way to inform the user about the status of the data ingestion without using a polling solution. 
- [x] The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable. 
- [x] Use a SQL database.

### Bonus features 
- [x] Containerize your solution. 
- [x] Sketch up how you would set up the application using any cloud provider (AWS, Google Cloud, etc). 
- [x] Include a .sql file with queries to answer these questions: 
- [x] From the two most commonly appearing regions, which is the latest datasource? ○ What regions has the "cheap_mobile" datasource appeared in? 

### Deliverables 

Your project should be stored in a public GitHub repository. When you are done, send us the link to your repo. 

It’s not necessary to host this application anywhere (although you can if you like). Just make sure your repo has a README.md which contains any instructions we might need for running your project. 


### Observations/Recommendation
● If you will integrate your solution with any cloud platform, you must provide an account
(user/password) to us to test it.
● Please detail your code so that we can understand your reasoning and its use regardless
of platform expertise.
● We recommend recording a video explaining how it works and steps of execution.

## 💻 Architecture

IMAGE PENDING

For this challenge, I've builded a architecture that uses a docker-compose to create a container with python scripts that attend the challenge requirements, a Redis server to enqueue jobs and a PostgreSQL database to store data. 

### Running the ingestion process

To run the files ingestion, the user must put files in 'files_to_ingest' directory. After this, run the below commands in root directory:

```
docker-compose up -d
docker-compose exec ingest_app python app.py trips.csv
```

If you wish to ingest more than one file, just add it after the script path. The files must be separated by comma.

When you run the exec command, the script will execute the follow steps:

1. Get the files list to ingest
2. For each file, will add the ingestion job to Redis queue using the [RQ library](https://python-rq.org/).

The ingestion job will execute the follow steps:

1. Read the CSV file passed as argument and create a pandas dataframe with the file data
2. Save this panda dataframe to 'trips' table in PostgreSQL. I decided to use the [to_sql](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) pandas function, because it will create the table if does not exist.

I decided to use Redis with the RQ library because it gave me the possibility to enqueue jobs to be processed in the background with workers.
In order to simplify the running of this challenge, I've set to jobs run synchronously. But asynchronously it can be set just changing one parameter to True.

### Showing reports results

To show the queries results, just run the below command after did the ingestion process.
```
docker-compose exec myapp ingest_app metrics.py
```




Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você instalou a versão mais recente de `<linguagem / dependência / requeridos>`
* Você tem uma máquina `<Windows / Linux / Mac>`. Indique qual sistema operacional é compatível / não compatível.
* Você leu `<guia / link / documentação_relacionada_ao_projeto>`.

## 🚀 Instalando <nome_do_projeto>

Para instalar o <nome_do_projeto>, siga estas etapas:

Linux e macOS:
```
<comando_de_instalação>
```

Windows:
```
<comando_de_instalação>
```

## ☕ Usando <nome_do_projeto>

Para usar <nome_do_projeto>, siga estas etapas:

```
<exemplo_de_uso>
```

Adicione comandos de execução e exemplos que você acha que os usuários acharão úteis. Fornece uma referência de opções para pontos de bônus!

## 📫 Contribuindo para <nome_do_projeto>
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com <nome_do_projeto>, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars3.githubusercontent.com/u/31936044" width="100px;" alt="Foto do Iuri Silva no GitHub"/><br>
        <sub>
          <b>Iuri Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://s2.glbimg.com/FUcw2usZfSTL6yCCGj3L3v3SpJ8=/smart/e.glbimg.com/og/ed/f/original/2019/04/25/zuckerberg_podcast.jpg" width="100px;" alt="Foto do Mark Zuckerberg"/><br>
        <sub>
          <b>Mark Zuckerberg</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://miro.medium.com/max/360/0*1SkS3mSorArvY9kS.jpg" width="100px;" alt="Foto do Steve Jobs"/><br>
        <sub>
          <b>Steve Jobs</b>
        </sub>
      </a>
    </td>
  </tr>
</table>


## 😄 Seja um dos contribuidores<br>

Quer fazer parte desse projeto? Clique [AQUI](CONTRIBUTING.md) e leia como contribuir.

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#nome-do-projeto)<br>
