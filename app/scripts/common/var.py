import os 
import get_data

PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_IR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DatabasePath = f'{PRO_DIR}\\..\\DataBase\\Dolby.db'
data=get_data.return_data()

