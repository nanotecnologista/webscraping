import pandas as pd

def dado_mail():
    #Lendo dataframe (df)
    df = pd.read_csv('emails.csv',encoding='utf-8', delimiter=',')

    # Ordenando na ordem crescente e excluindo os repetidos e as outras colunas
    df.sort_values('Email', ascending=True)
    df.drop_duplicates(subset='Email', keep='first')
    df = df['Email']

    # Criando outro dataframe com os dados tratados
    df_second = pd.DataFrame(df)
    df_second.to_csv('emails_01.csv')

    df_second = pd.read_csv('emails_01.csv',encoding='utf-8', delimiter=',')
    
    return (df_second)
dado_mail()