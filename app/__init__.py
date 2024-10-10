import os
import sys

os_ = os
sys_ = sys
current_directory = os.getcwd()
base_url = os.environ.get('BASE_URL')
user_agent = os.environ.get('USER_AGENT')
current_directory = os.getcwd()
num_processes = os.cpu_count() or 1
sanitize = False