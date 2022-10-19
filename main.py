from src import app
from src.controller import url_rules

#register all urls from url_routes
for r in url_rules:
    app.add_url_rule(rule=r.get('route'), view_func=r.get('func'), methods=r.get('methods'))

#run app
if __name__ == '__main__':
    app.run(debug=True)