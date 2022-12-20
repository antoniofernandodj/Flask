from src.libraries.routing import path
from src.views import view


url_rules = [
    path('/', view.Jobs.as_view('jobs')),
    path('/login/', view.Login.as_view('login')),
    path('/new-job/', view.NewJob.as_view('new_job')),
    path('/del-job/<int:index>/<string:user>', view.DelJob.as_view('del_job')),
    path('/reset/', view.ResetToDefault.as_view('reset')),
    path('/logout/', view.Logout.as_view('logout')),
    path('/run-cron/', view.RunCron.as_view('run_cron')),
    path('/long-request/', view.LongRequest.as_view('long_request'))
]
