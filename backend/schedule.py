import pandas as pd


class Professor:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.preferences = None
        self.class_assignment = None

    def __str__(self):
        return self.name


class Course:
    def __init__(
        self,
        id: int,
        name: str,
        semester: int,
        hours_per_semester: list,
        lecturer: Professor,
        professors: list[Professor],
    ):
        self.id = id
        self.name = name
        self.semester = semester
        self.hours_per_semester = hours_per_semester
        self.lecturer = lecturer
        self.professors = professors

    def __str__(self):
        return self.name

    def create_classes(self) -> list:
        """
        Creates a list of classes in this course.
        """
        classes = []
        for i, type in enumerate(["lecture", "practicals", "laboratories"]):
            hours = self.hours_per_semester[i]
            if hours != 0:
                k = hours//30
                for i in range(k):
                    classes.append(
                        Class(
                            f'{self.name}_{type}_{i+1}',
                            self,
                            type
                            )
                        )

        return classes

class Data:
    def __init__(self, filename: str):
        self.data = pd.read_excel(f"./{filename}")

    def create_professors(self) -> list[Professor]:
        """Creates list of professors from loaded data.

        --------
        Column "kierownik_przedmiotu" sholud contain name and surname of single professor
        Column "realizatorzy_przedmiotu" should contain lists: ['IMIE NAZWISKO_1', 'IMIE NAZWISKO_2', ...].
        """
        professors = []
        professors_names = set(self.data.loc[:, "kierownik_przedmiotu"])

        for i in range(len(self.data)):
            for j in eval(self.data.iloc[i]["realizatorzy_przedmiotu"]):
                professors_names.add(j)

        names_list = list(professors_names)

        for prof_name in names_list:
            professors.append(
                Professor(
                    names_list.index(prof_name),
                    prof_name
                )
            )

        return professors

    def create_courses(self, professors: list[Professor]) -> list[Course]:
        """Create list of Courses from loaded data
        
        --------
        Should be used after create_professors
        """
        courses = []
        for i in range(len(self.data)):
            for j in range(len(professors)):
                if professors[j].name == self.data.iloc[i]["kierownik_przedmiotu"]:
                    lecturer = professors[j]

            set_of_prof_names = set(eval(self.data.iloc[i]["realizatorzy_przedmiotu"]))
            list_of_profs = []

            for k in range(len(professors)):
                if professors[k].name in set_of_prof_names:
                    list_of_profs.append(professors[k])

            courses.append(
                Course(
                    i,
                    str(self.data.iloc[i]["nazwa_przedmiotu"]).replace(" ", "_"),
                    self.data.iloc[i]["semestr"],
                    [
                        self.data.iloc[i]["W"],
                        self.data.iloc[i]["Ć"],
                        self.data.iloc[i]["L"],
                    ],
                    lecturer,
                    list_of_profs,
                )
            )

        return courses



class MeetingTime:
    def __init__(self, day: int, hour: int):
        self.day = day
        self.hour = hour

    def __str__(self):
        return f"Day: {self.day}, hour: {self.hour}"


class Students:
    def __init__(self, semester: int, group: int):
        self.semester = semester
        self.group = group

    def __str__(self):
        return str(self.semester) + str(self.group)


class Room:
    def __init__(self, name: str, capacity: str, category: str):
        self.name = name
        self.category = category  # category "normal" -- normal classes; category "lab" -- laboratories
        self.seating_capacity = capacity

    def __str__(self):
        return self.name


class Class:
    def __init__(self, name: str, course: Course, category: str):
        self.name = name # jednak daję imię zamiast ID bo tak chyba wystarczy, a łatwiej rozróżnić zajęcia: Analiza_1_ćwiczenia_1 i Analiza_1_ćwiczenia_2 po nazwie
        self.course = course
        self.category = category
        self.professor = None
        self.meeting_time = None
        self.room = None
        if category == "lecture":
            self.professor = course.lecturer
        # to co niżej jest w mojej ocenie niepotrzebne:
        # -- z perspektywy jednych zajęc, po co dawać godziny w całym semestrze jedne zajęcia to blok 2h w planie czyli 30 godzin w sem.
        # if category == "lecture":
        #     self.hours_per_semester = self.course.hours_per_semester[0]
        # elif category == "practicals":
        #     self.hours_per_semester = self.course.hours_per_semester[1]
        # elif category == "laboratories":
        #     self.hours_per_semester = self.course.hours_per_semester[2]

    def set_professor(self, professor: Professor):
        self.instructor = professor

    def set_meeting_time(self, day: int, hour: int):
        self.meeting_time = MeetingTime(day, hour)

    def set_room(self, room: Room):
        self.room = room

    def __str__(self):
        return (
            str(self.name)
            + ", "
            + str(self.course)
            + ", "
            + str(self.category)
            + ", "
            + str(self.room)
            + ", "
            + str(self.professor)
            + ", "
            + str(self.meeting_time)
            + ", "
        )


class Schedule:
    def __init__(self):
        self.data = None
        self.classes = []
        self.number_of_conflicts = 0
        self.fitness = -1

    def get_classes(self):
        return self.classes

    def get_number_of_conflicts(self):
        return self.number_of_conflicts

    def initialize(self):
        """ """
