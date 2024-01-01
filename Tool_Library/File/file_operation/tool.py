from pathlib import Path
def write_file(text: str, file_path: str = './') -> str:
        '''write file to disk
        '''
        write_path = (
            Path(file_path)
        )
        try:
            write_path.parent.mkdir(exist_ok=True, parents=False)
            with write_path.open("w", encoding="utf-8") as f:
                f.write(text)
            return f"File written successfully to {file_path}."
        except Exception as e:
            return "Error: " + str(e)

def read_file(file_path: str) -> str:
        '''read file from disk
        '''
        read_path = (
            Path(file_path)
        )
        try:
            with read_path.open("r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            return "Error: " + str(e)
    

if __name__ == '__main__':
    print(write_file(file_path ='Tools/File/file_operation/output',text ="hello world"))
    print(read_file(file_path ='Tools/File/file_operation/output'))