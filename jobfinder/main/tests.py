from django.test import TestCase

from classes.totaljobs import TotalJobsSearch
from classes.indeed import IndeedSearch
from classes.monster import MonsterSearch

# Create your tests here.


def main() -> None:
    """ Testing function used for debugging the file.

        Returns:
            None
    """

    test = 3
    if test == 1:
        new = IndeedSearch(location="Newark", title="warehouse",
                           job_type="temporary", radius="5"
                           )
    elif test == 2:
        new = TotalJobsSearch(location="Newark", title="retail",
                              job_type="part-time", radius="0"
                              )
    elif test == 3:
        new = MonsterSearch(location="Newark", title="retail", radius="5")
    else:
        new = IndeedSearch(location="Newark", title="warehouse",
                           job_type="temporary", radius="5"
                           )

    for i in new.get_links():
        print(i)


if __name__ == "__main__":
    main()
