import os
import sys

# System Variables
os_ = os
sys_ = sys
current_directory = os.getcwd()
base_url = os.environ.get('BASE_URL')
user_agent = os.environ.get('USER_AGENT')
cert = os.environ.get('CERT')
current_directory = os.getcwd()
num_processes = os.cpu_count() or 1

# Sanitation Variables
sanitize = False
reference_column = ''

# HTTP variables
locale = 'gb'
