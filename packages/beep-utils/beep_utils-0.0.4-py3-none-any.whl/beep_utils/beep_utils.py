class PostgreSQL():
    
    def __init__(self):
        pass

    def create_engine(db_user=None, db_password=None, db_name=None):
        '''
        Função para criar a chave de conexão ao banco de dados.\n
        Caso a conexão seja local (fora do airflow), é necessário incluir usuário e senha.
        '''
        import sqlalchemy
        try:
            from airflow.hooks.base_hook import BaseHook
            connection = BaseHook.get_connection("postgres_beepsaude_gcp")
            engine_bi = sqlalchemy.create_engine(f"postgresql://{connection.login}:{connection.password}@{connection.host}/{connection.schema}", echo=False)
            return engine_bi
        except ModuleNotFoundError:
            if db_user and db_password:
                engine_bi = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_password}@data-services.beepapp.com.br/{db_name}", echo=False)
                return engine_bi
            else:
                print('Inclua usuário e senha.')

    def postgres_upsert(table, conn, keys, data_iter):
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
    
    def convert_json_columns(df, table_name, table_schema, conn):
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
    
    def time_print(text):
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
        Função que renomeia todas as colunas que estejam em camel case para snake case.
        Exemplo: exemploNomeColuna -> exemplo_nome_coluna
        '''
        import re
        for col in df.columns:
            df = df.rename(
                columns={col:re.sub(r'([A-Z][a-z]*)', self.__convert_to_snake_case, col)}
            )
