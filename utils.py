import os

def getenv(key):
    """_getenv_
    Top get environment/secret MYSECRET:
        1. Try to read from environment $MYSECRET
        2. If not found and environment MYSECRET_FILE is set, read from the contents of the filename specified by MYSECRET_FILE
        3. Otherwise get the value from the contents of the file $ENVIRONMENT/MYSECRET
    
    Set environment variable in:
        1. -e parameter to docker run
        2. .env file
        3. In file contents pointed at by environment variable $ENVIRONMENT/MYSECRET
        4. In docker-compose.yaml as follows:    
            ...
                    environment:
                    MYSECRET_FILE: /run/secrets/mysecret
            ...
            secrets:            
              mysecret:
                file: ."${ENVIRONMENT}/MYSECRET"

            and put secret into file "${ENVIRONMENT}/MYSECRET" where ENVIRONMENT an entry in the environment or .env file pointing to the folder containing the file MYSECRET
            
            
    
    Args:
        key (_type_): _environment variable_
    """
    value = os.getenv(key)                                                                      # Default to environment variable
    if value == None:                                                                           # Try reading from a file if not set
        key_file = os.getenv(f"{key}_FILE") or os.path.join(os.getenv("ENVIRONMENT"), key)      # in docker secrets file or os secrets file
        with open(key_file) as f:
            value = f.readline().strip('\n')                                                    # Make sure not to include trailing newline if there is one    
    return value