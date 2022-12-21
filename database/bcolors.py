class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

    @staticmethod
    def colored(message, color):
        return color + message + bcolors.ENDC

    @staticmethod
    def warning(message):
        return bcolors.WARNING + message + bcolors.ENDC

    @staticmethod
    def fail(message):
        return bcolors.FAIL + message + bcolors.ENDC

    @staticmethod
    def ok(message):
        return bcolors.OKGREEN + message + bcolors.ENDC

    @staticmethod
    def okblue(message):
        return bcolors.OKBLUE + message + bcolors.ENDC

    @staticmethod
    def header(message):
        return bcolors.HEADER + message + bcolors.ENDC
