from pathlib import Path
from os import path

file = path.join(str(Path(__file__).parent),
    '.venv', 'bin', 'activate_this.py'
)

exec(open(file).read(), {'__file__': file})

from src import create_app
from src.urls import url_rules

app = create_app()

# run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
