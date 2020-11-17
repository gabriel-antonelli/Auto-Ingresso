from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from unidecode import unidecode
from time import sleep

opt = Options()
opt.add_argument('--no-sandbox')
opt.headless = True
opt.add_argument('--start-maximized')
driver = webdriver.Chrome(options = opt)

city = input('Digite sua cidade(ex: joao-pessoa): ')
event = input('Para qual evento você deseja comprar ingressos?: ').lower()
unidecode(event)
user_mail = input('Digite seu email: ')
eventtourl = urllib.parse.quote(event)

def sendemail():

    CLIENT_SECRET_FILE = 'src/client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    emailMsg = event.upper() + " já está disponível!\n\n Disponibilidade: \n" + disp + '\n Dias disponíveis: \n \n' + listday + '\n\n Locais disponíveis: \n' + selplace + "\n Para comprar acesse: " + url_current
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = user_mail
    mimeMessage['subject'] = 'Auto-Ingresso: Seu Evento Foi Encontrado!'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)

isRight_movie = False   

while True:

    print('\n...Chegando no site...\n')
    driver.get('https://www.ingresso.com/busca/resultado?city=' + city + '&partnership=home&q=' + eventtourl)
    print('\n...Verificando resultados da busca...\n')
    sleep(3)
    find = driver.find_element_by_css_selector('p.search-result-text').text
    tof = "nenhum resultado" in find

    if tof == True :
        print("\n...Sem resultados!...\n")

    else:
        name = driver.find_element_by_class_name('card-title.ml-tit').text.lower()
        disp = driver.find_element_by_class_name('ml-total-cinemas').text
        print('\nResultado principal de Ingresso.com: ' + name + '\n')
        if isRight_movie == False:
            right_movie = input(name + " é o resultado esperado?(1=SIM)(2=NÃO): ")
            if right_movie == '1':
                isRight_movie = True
        else:
            right_movie = '1'
        sleep(3)

        if right_movie == '2':
            print('\n...Pesquisando no IMDB...\n')
            driver.get('https://www.imdb.com/find?q=' + eventtourl + '&s=tt&ttype=ft&ref_=fn_ft')
            sleep(3)
            imdb_find =  driver.find_element_by_class_name('findHeader').text

            if "No results" in imdb_find:
                print('\n...Sem resultados no IMDB!...\n')

            else:
                other_finds = driver.find_element_by_css_selector('table.findList').text
                print(' \n Não foram achados resultads com o nome: ' + event + '. Você quis dizer: \n\n' + other_finds)
                index = input('\n Escolha uma das opções pela ordem exibida(ex: 2): ')
                event = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[' + index + ']/td[2]/a').text.lower()
                eventtourl = urllib.parse.quote(event)

        elif tof == False and disp != "Fora de Cartaz" and right_movie == '1':
            print("\nEvento encontrado! ")
            print("\nDisponibilidade: \n " + disp)
            sel_event = driver.find_element_by_class_name('ml-lnk[href]').get_attribute('href')
            driver.get(sel_event)
            sleep(3)
            listday = driver.find_element_by_xpath('//*[@id="contentarea-sessionpage"]/div[1]/ing-sessions-tabs/div/div').text
            if listday == '':
                print('\n Sem sessões disponíveis na sua cidade! \n')
            else:    
                print('\nDias disponíveis: \n \n' + listday + '\n')
                sleep(3)
                selplace = driver.find_element_by_xpath('//*[@id="contentarea-sessionpage"]/div[2]/section/div/div').text
                print('\nLocais disponíveis: \n')
                print(selplace)
                url_current = driver.current_url
                sendemail()
                driver.quit()
                break

        else:
            print('\n...Evento ainda não disponível ou fora de cartaz!...\n')
            sleep(30)