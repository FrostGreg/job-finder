from dataclasses import dataclass


@dataclass
class Job:
    """ Data class for each job result

        Attributes:
            title : Listed title from the job board
            link : URL link to the application page
            pay : The hourly rate from the job board
            difficulty: Listed difficulty of applying
    """

    title: str
    link: str
    pay: str = ""
    difficulty: str = ""

    def __hash__(self):
        return hash(self.title + self.link)