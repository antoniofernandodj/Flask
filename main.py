from src import create_app
from src.urls import url_rules

app = create_app()

#run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
