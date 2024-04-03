class PostgreSQL():

    def __init__(self):
        pass

    def create_engine(airflow_connection_name='postgres_beepsaude_gcp', db_user=None, db_password=None, db_server_url=None, db_name=None):
        '''
        Função para criar a chave de conexão ao banco de dados.\n
        Caso a conexão seja local (fora do airflow), é necessário incluir usuário e senha.\n
        A conexão padrão é o banco de BI via Airflow.
        '''
        import sqlalchemy
        try:
            from airflow.hooks.base_hook import BaseHook
            connection = BaseHook.get_connection(airflow_connection_name)
            engine_bi = sqlalchemy.create_engine(f"postgresql://{connection.login}:{connection.password}@{connection.host}/{connection.schema}", echo=False)
            return engine_bi
        except ModuleNotFoundError:
            if db_user and db_password:
                engine_bi = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_password}@{db_server_url}/{db_name}", echo=False)
                return engine_bi
            else:
                print('Inclua usuário e senha.')

    def postgres_upsert(self, table, conn, keys, data_iter):
        '''
        Função que permite o pd.to_sql() realizar upsert baseado na chave primária da tabela.\n
        O nome da chave primária deve seguir o padrão "[nome_da_tabela]_pkey".\n
        Esta função deve ser usada da seguinte forma: df.to_sql([...], method=postgres_upsert).
        '''
        from sqlalchemy.dialects.postgresql import insert

        data = [dict(zip(keys, row)) for row in data_iter]

        insert_statement = insert(table.table).values(data)
        upsert_statement = insert_statement.on_conflict_do_update(
            constraint=f"{table.table.name}_pkey",
            set_={c.key: c for c in insert_statement.excluded},
        )
        conn.execute(upsert_statement)
    
    def convert_json_columns(self, df, table_name, table_schema, conn):
        '''
        Função que converte valores do tipo dict no python para string em colunas JSON ou JSONB do banco de dados, evitando erros.
        '''
        import json
        schema_origem = conn.execute(f"SELECT column_name, data_type, udt_name FROM information_schema.columns WHERE table_schema = '{table_schema}' and table_name = '{table_name}'").fetchall()
        for tupla in schema_origem:
            if tupla[1] in ['jsonb', 'json']:
                try:
                    df[tupla[0]] = df[tupla[0]].apply(lambda x: json.dumps(x))
                    df[tupla[0]] = df[tupla[0]].astype(str).replace('NaN', None)
                except KeyError:
                    pass
        return df
    
    
class General():
    
    def __init__(self) -> None:
        pass
    
    def time_print(self, text):
        '''
        Função que printa com o horário antes do texto.
        '''
        from datetime import datetime
        import pytz
        now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
        print(f'[{now}] {text}')
    
    def __convert_to_snake_case(self, match):
        return '_' + match.group(0).lower()

    def rename_columns_camel_case_to_snake_case(self, df):
        '''
        Função que renomeia todas as colunas que estejam em camel case para snake case.\n
        Exemplo: exemploNomeColuna -> exemplo_nome_coluna
        '''
        import re
        for col in df.columns:
            df = df.rename(
                columns={col:re.sub(r'([A-Z][a-z]*)', self.__convert_to_snake_case, col)}
            )
            
    def send_email(self, sender_address, receiver_address, gmail_app_password, subject, mail_content, attach_df_xlsx=False, xlsx_name=None, df=None, attach_pdf=False, pdf=None):
        '''
        Função que envia emails pelo Gmail.\n
        É necessário que o email do remetente esteja habilitado para o disparo (2FA e senha de app).\n
        Os parâmetros "attach_df_xlsx" e "attach_pdf" devem ser "True" caso existam arquivos Excel (dataframe Pandas) ou PDF a anexar.
        '''
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email.mime.application import MIMEApplication
        from email import encoders
        import io
        import os
        
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = ', '.join(receiver_address)
        message['Subject'] = subject 

        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        
        if attach_df_xlsx:
            if df is not None and xlsx_name is not None:
                file_io = io.BytesIO()
                df.to_excel(file_io)
                file_io.seek(0)

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((file_io).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % xlsx_name)

                message.attach(part)
            else:
                print('É necessário passar um dataframe como parâmetro "df" e um nome para o arquivo como "xlsx_name".')
    
        if attach_pdf:
            if pdf is not None:
                with open(pdf, 'rb') as f:
                    attach_pdf = MIMEApplication(f.read(), _subtype='pdf')
                    attach_pdf.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf))
                    message.attach(attach_pdf)
            else:
                print('É necessário passar um arquivo pdf como parâmetro "pdf".')

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, gmail_app_password) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()

        print('Email enviado.')

    def download_metabase_question_result(self, email, password, question_id):
        '''
        Função que retorna um dataframe pandas do resulta de perguntas salvas no Metabase.\n
        O parâmetro "question_id" é o número da pergunta, que aparece como parte do link (url).
        '''
        import requests
        import pandas as pd

        headers = {
            "Content-Type": "application/json"
        }
        
        base_url = "https://dados.beepapp.com.br/api"

        params = {
            "username":email,
            "password":password
        }

        response = requests.post(url=f'{base_url}/session', json=params, headers=headers)

        headers["X-Metabase-Session"] = response.json()["id"]

        # Faça a solicitação à API do Metabase
        response = requests.post(url=f"{base_url}/card/{question_id}/query/json", headers=headers)
        return pd.DataFrame(response.json())
