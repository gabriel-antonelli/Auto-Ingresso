# Auto-Ingresso

## Descrição

Ache qualquer filme ou evento no Ingresso.com e receba os dias, locais, horários disponíveis e o link para comprar no seu email, quando e se o evento estiver disponível.

## Requisitos

### Docker
#### No linux:

https://docs.docker.com/engine/install/ubuntu/

#### No Windows:
https://docs.docker.com/docker-for-windows/install/

## Instalação
    docker pull antonelli/auto-ingresso:latest

## Rodando
    docker run -ti antonelli/auto-ingresso:latest

## Exemplo de Uso
    Digite sua cidade(ex: joao-pessoa): jundiai
    Para qual evento você deseja comprar ingressos?: mulher maravilha
    Digite seu email: auto.ingresso@gmail.com
    
    Não foram achados resultads com o nome: mulher maravilha. Você quis dizer: 

    Mulher Maravilha: Linhagem de Sangue (2019)
    Mulher-Maravilha 1984 (2020)
    Mulher-Maravilha (2017)
    Professor Marston e as Mulheres-Maravilhas (2017)

    Escolha uma das opções pela ordem exibida(ex: 2): 2





