import pandas as pd


class Data:
    def __init__(self, filename: str):
        self.data = pd.read_excel(f"./{filename}")

    def create_courses(self):
        courses = []
        for i in range(len(self.data)):
            courses.append(
                Course(
                    i,
                    str(self.data.iloc[i]["nazwa_przedmiotu"]),
                    self.data.iloc[i]["semestr"],
                    [
                        self.data.iloc[i]["W"],
                        self.data.iloc[i]["Ć"],
                        self.data.iloc[i]["L"],
                    ],
                    None,   # None, bo chyba lepiej najpierw wczytać samych profesorów żeby nie było problemu z ID
                    None,
                )
            )
        return courses


class Professor:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

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
        professors: list,
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
        # do poprawienia -- problem z różnymi id
        """
        Creates a list of classes in this course.
        """
        classes = []
        for i, type in enumerate(["lecture", "practicals", "laboratories"]):
            if self.hours_per_semester[i] != 0:
                classes.append(Class(i, self, type))
            else:
                classes.append(None)
        return classes


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
    def __init__(self, id: int, course: Course, category: str):
        self.id = id
        self.course = course
        self.category = category
        self.professor = None
        self.meeting_time = None
        self.room = None
        if category == "lecture":
            self.hours_per_semester = self.course.hours_per_semester[0]
            self.professor = course.lecturer
        elif category == "practicals":
            self.hours_per_semester = self.course.hours_per_semester[1]
        elif category == "laboratories":
            self.hours_per_semester = self.course.hours_per_semester[2]

    def set_professor(self, professor: Professor):
        self.instructor = professor

    def set_meeting_time(self, day: int, hour: int):
        self.meeting_time = MeetingTime(day, hour)

    def set_room(self, room: Room):
        self.room = room

    def __str__(self):
        return (
            str(self.course)
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
