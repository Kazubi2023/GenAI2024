from aws_conn import AWSBedrockConnection
from dataset import DataLoader

import os

class MeetingComprehender(object):
    def __init__(self):
        self.conn = AWSBedrockConnection()
        self.data_laoder = DataLoader()
        
    def comprehend(self, save_to: str = "output/summaries"):
        document = self.data_laoder.next()
        while document is not None:
            transcript, file_name = document['doc'], document['file_name']
            output = self.conn.query_model(transcript, task="summary")['output']
            print(f'Generated SUMMARY for {file_name}.')
            self.__save_to_(save_to, file_name, output)
            document = self.data_laoder.next()
            
            
    def __save_to_(self, dir_name: str, file_name: str, content: str):
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, "w") as f:
            print(f"SAVE output to {file_path}")
            f.writelines(content)