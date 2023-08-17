import os

def getenv(key):
    """_getenv_
    Given environment variable KEY:
        1. Try to read from environment
        2. If not found and environment KEY_FILE is set, read from the contents of the filename specified by KEY_FILE
    
    Set environment variable in:
        1. -e parameter to docker run
        2. .env file
        3. In docker-compose.yaml as follows:    
            ...
                    environment:
                    MYSECRET_FILE: /run/secrets/mysecret_key
            ...
            secrets:            
              mysecret_key:
                file: ./secrets/MYSECRET_KEY

            and put secret into file ./secrets/MYSECRET_KEY
    
    Args:
        key (_type_): _environment variable_
    """
    print(f'getenv({key})...')
    value = os.getenv(key)# Default to environment variable
    if value == None:        
        key_file = os.getenv(f"{key}_FILE") or f'.{os.sep}secrets{os.sep}{key}'    # or secret in docker secrets file or os secrets file
        print(f'Unset, key file is {key_file}')
        with open(key_file) as f:
            value = f.readline().strip('\n')
    return value