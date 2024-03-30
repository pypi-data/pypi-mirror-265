from sqlalchemy import create_engine
import boto3
import json
import yaml
class ReadYMLFile:   
    def __init__(self,ymlfilepathwithname):
        '''
        ymlfilepathwithname: it should contains the path with file name        
        '''
        self.ymlfilepath=ymlfilepathwithname
    
    def read_yml_file(self):
        filename=self.ymlfilepath
        with open(filename,'r') as f:
            yamlfile=yaml.safe_load(f)
        return yamlfile
    
class MySqlConnectWithoutConfig:
    def __init__(self,secret_name_i:str,region_name_i:str,aws_access_key_id_i:str,
                 aws_secret_access_key_i:str,db_name_i:str):
        self.secret_name_o=secret_name_i
        self.region_name_o=region_name_i
        self.aws_access_key_id_o=aws_access_key_id_i
        self.aws_secret_access_key_o=aws_secret_access_key_i
        self.db_name_o=db_name_i
        
    def get_secret(self):
        # Create a Secrets Manager client
        session = boto3.session.Session(aws_access_key_id=self.aws_access_key_id_o,
        aws_secret_access_key=self.aws_secret_access_key_o,region_name=self.region_name_o)
        client = session.client(service_name="secretsmanager", region_name=self.region_name_o)
        return client.get_secret_value(SecretId=self.secret_name_o)["SecretString"]

    def create_engine_conn(self):
        dbname=self.db_name
        secret_value = self.get_secret()
        if secret_value:
            secret_data = json.loads(secret_value)
            rds_user = secret_data["username"]
            rds_pass = secret_data["password"]
            rds_host = secret_data["host"]
            rds_port = secret_data["port"]
            
            engine = create_engine(
                f"mysql+pymysql://{rds_user}:{rds_pass}@{rds_host}:{rds_port}/{dbname}"
            )
        else:
            raise Exception("RDS Connection Failed")
            engine = None
        return engine
    
    def save_data_to_db(self,dataframe,tablefilename:str,ifexists:str="append"):
        '''
        this function will use dataframe.to_sql function to save the dataframe into database    
        dbname: database name where the file to be save 
        dataframe: it should be a DataFrame and 
                    there should not be any "id" column consist int the dataframe
        tablefilename: it will consist the name of file for database table in mysql
        ifexists: it define either want to replace the table to append the table
                    by default it is append,if needed can be change to "replace".
        '''
        engineconnect=self.create_engine_conn()
        start_number = 1 
        dataframe.reset_index(drop=True, inplace=True)
        dataframe.index += start_number
        dataframe.to_sql(name=tablefilename,con=engineconnect,if_exists=ifexists,index=True,index_label='id')
        return {"msg":"file sucessfully inserted"}