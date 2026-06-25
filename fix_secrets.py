import os
import glob
import re

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return
    
    new_content = content
    # Handle pymysql connections
    new_content = re.sub(
        r"password=os.environ.get('DB_PASSWORD', 'your_password_here')",
        "password=os.environ.get('DB_PASSWORD', 'your_password_here')",
        new_content
    )
    new_content = re.sub(
        r'password=os.environ.get("DB_PASSWORD", "your_password_here")',
        'password=os.environ.get("DB_PASSWORD", "your_password_here")',
        new_content
    )
    new_content = re.sub(
        r"host=os.environ.get('DB_HOST', 'localhost')",
        "host=os.environ.get('DB_HOST', 'localhost')",
        new_content
    )
    new_content = re.sub(
        r"user=os.environ.get('DB_USER', 'root')",
        "user=os.environ.get('DB_USER', 'root')",
        new_content
    )
    new_content = re.sub(
        r"database=os.environ.get('DB_NAME', 'hospital_db')",
        "database=os.environ.get('DB_NAME', 'hospital_db')",
        new_content
    )

    # Handle URI
    new_content = re.sub(
        r"'mysql\+pymysql://remote_user:%40Codevocado%23remote%251@69.62.82.234/wha_chatbot'",
        "os.environ.get('DATABASE_URL', 'mysql+pymysql://user:pass@localhost/db')",
        new_content
    )
    
    new_content = re.sub(
        r"mysql\+pymysql://remote_user:%40Codevocado%23remote%251@69.62.82.234/wha_chatbot",
        "mysql+pymysql://user:pass@localhost/db",
        new_content
    )

    # Handle generic passwords
    new_content = new_content.replace('********', '********')
    new_content = new_content.replace('********', '********')
    
    # Also handle quick_migrate.py root password
    new_content = re.sub(
        r"'user': 'root',\s*'password': ''",
        "'user': os.environ.get('DB_USER', 'root'),\n    'password': os.environ.get('DB_PASSWORD', '')",
        new_content
    )
    
    if new_content != content:
        # We need to make sure os is imported for py files
        if filepath.endswith('.py') and 'os.environ' in new_content and 'import os' not in new_content:
            new_content = 'import os\n' + new_content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')

for root_dir, dirs, files in os.walk('.'):
    # skip node_modules, venv, .git
    if 'node_modules' in root_dir or 'venv' in root_dir or '.git' in root_dir:
        continue
    for file in files:
        if file.endswith(('.py', '.md', '.example', '.jsx', '.json', '.env', '.env.example')):
            process_file(os.path.join(root_dir, file))
