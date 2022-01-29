
class Job:
    """ Data class for each job result

        Attributes:
            title : Listed title from the job board
            link : URL link to the application page
            pay : The hourly rate from the job board
            difficulty: Listed difficulty of applying
    """

    def __init__(self, title: str, link: str, pay: str = "",
                 difficulty: str = ""
                 ):
        self.title: str = title
        self.link: str = link
        self.pay: str = pay
        self.difficulty: str = difficulty

    def __str__(self) -> str:
        return self.title