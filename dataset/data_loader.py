import os

class DataLoader:
    def __init__(self):
        dir_path = os.path.join(os.getcwd(), 'dataset', 'generated_conversations')
        transcript_paths = {file_name for file_name in os.listdir(dir_path)}
        self.iterator = _TranscriptIterator(transcript_paths, dir_path)
    
    def next(self):
        return self.iterator.next()
    
    def reset(self):
        return self.iterator.reset()
        
    

class _TranscriptIterator:
    def __init__(self, file_names: set, dir_path: str):
        self.files_names = file_names
        self.files_not_visited = file_names.copy()
        self.dir_path = dir_path
    
    def __read_doc(self, file_name: str):
        return open(file_name, 'r').read()
    
    def next(self):
        if len(self.files_not_visited) == 0:
            return None
        file_name = self.files_not_visited.pop()
        return {
            "doc": self.__read_doc(os.path.join(self.dir_path, file_name)),
            "file_name": file_name,
        }
        
    def reset(self):
        self.files_not_visited = self.files_names
    
    