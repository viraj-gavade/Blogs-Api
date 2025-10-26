from dotenv import load_dotenv
import os 


load_dotenv()
DB_URL= os.getenv('DB_URL')
SECRETE_KEY = os.getenv('SECRETE_KEY')
ALGORITHM = os.getenv('ALGORITHM')