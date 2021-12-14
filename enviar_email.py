from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import dados_mail

destinatarios = dados_mail.dado_mail()

def create_email():
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    file_attachment = [r'/teste/curriculo.pdf']

    #mensagem de e-mail
    emailMsg = """Pois é, encontrei sua vaga fazendo webscraping.
Me chamo Júlia, sou estudante de Análise e Desenvolvimento de Sistemas, cursando o segundo semestre.
Sou apaixonada por tecnologia e uma entusiasta da área.
Quer saber um pouco mais sobre como descobri essa vaga?
É só acessar meu perfil no github: https://github.com/nanotecnologista

Em anexo, também estou enviando o meu currículo. E, muito embora eu não tenha tido tanta experiência na área,
ainda consigo destacar inovações/melhorias"""
    
    for destinatario in destinatarios:
        #Mensagem de email
        mimeMessage = MIMEMultipart()
        mimeMessage['from'] = 'Julia Ingrid <julia.ingridsantos.7@gmail.com' 
        mimeMessage['to'] = destinatario
        mimeMessage['subject'] = 'Vaga Remota - Encontrei essa vaga fazendo webscraping'
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        
        # Serve para incluir um arquivo ou mais...
        for attachment in file_attachment:
            content_type, encoding = mimetypes.guess_type(attachment)
            main_type, sub_type = content_type.split('/', 1)
            file_name = os.path.basename(attachment)
        
            f = open(attachment, 'rb')
        
            myFile = MIMEBase(main_type, sub_type)
            myFile.set_payload(f.read())
            myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
            encoders.encode_base64(myFile)
        
            f.close()
        
            mimeMessage.attach(myFile)
        
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        
        message = service.users().messages().send(
            userId='me',
            body={'raw': raw_string}).execute()
        
        print(message)
