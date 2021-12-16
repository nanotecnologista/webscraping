import requests
import getpass
import sys
import json
import re #regex
import csv

def get_issues(username, repo, auth):
    """ nome de usuário e repo devem ser strings
    auth deve ser uma tupla de nome de usuário e senha.
    eventualmente, vamos trocá-lo para usar um token oauth"""

    tmpl = "https://api.github.com/repos/{username}/{repo}/issues?per_page=100"
    url = tmpl.format(username=username, repo=repo)
    return _getter(url, auth)

def _getter(url, auth):
    """  Pagination utility.  Obnoxious. """

    link = dict(next=url)
    while 'next' in link:
        response = requests.get(link['next'], auth=auth)

        # E .. se não obtivermos bons resultados, basta sair.
        if response.status_code != 200:
            raise IOError(
                "Non-200 status code %r; %r; %r" % (
                    response.status_code, url, response.json()))

        for result in response.json():
            yield result

        link = _link_field_to_dict(response.headers.get('link', None))


def _link_field_to_dict(field):
    """ Utilitário para separar o campo de cabeçalho Link do github.
    É meio feio."""

    if not field:
        return dict()

    return dict([
        (
            part.split('; ')[1][5:-1],
            part.split('; ')[0][1:-1],
        ) for part in field.split(', ')
    ])


def pega_link():
    username = 'usuario'
    password = 'token'
    auth = (username, password)
    usuario = input('Qual o usuario?\n')
    repositorio = input('Repositório:\n')
    tipoVaga = input('Qual o tipo da Vaga?\n')
    with open('emails.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Título', 'Tags'])
        for count, issue in enumerate(get_issues(usuario, repositorio, auth)):
            print(str(count) + ': ', end='')
            for label in issue['labels']:
                if(tipoVaga == label['name']):
                    texto = issue['body']
                    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', texto)
                    if (match):
                        email = match[0]
                        titulo = (issue['title'])
                        tags = ''
                        for i, tag in enumerate(issue['labels']):
                            if(i != 0):
                                tags += ', '
                            tags += tag['name']
                        print('Título: ' + titulo + '\n e-mail: ' + email)
                        writer.writerow([email, titulo, tags])
                    break
    return True
pega_link()