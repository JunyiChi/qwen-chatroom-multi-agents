def print_file_info(file_name):
    try:
        f=open(file_name, 'r')
    except:
        print(f"File {file_name} does not exist.")
    finally:
        f.close()
def append_to_file(file_name,data):
    f=open(file_name, 'a')
    f.write(data)
    f.flush()
    f.close()