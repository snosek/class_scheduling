import pandas as pd
import random as rand


class Professor:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.preferences = None
        self.class_assignment = None

    def __str__(self):
        return self.name


class Students:
    def __init__(self, semester: int, group: int, subject: str):
        self.semester = semester
        self.group = group
        self.subject = subject
        self.class_assignment = []

    def __str__(self):
        return f"Kierunek {self.subject} Semestr {self.semester} Grupa {self.group}"


class Course:
    def __init__(
        self,
        id: int,
        name: str,
        semester: int,
        subject: str,
        hours_per_semester: list,
        lecturer: Professor,
        professors: list[Professor],
    ):
        self.id = id
        self.name = name
        self.semester = semester
        self.subject = subject
        self.hours_per_semester = hours_per_semester
        self.lecturer = lecturer
        self.professors = professors

    def __str__(self):
        return self.name

    def create_classes(self, students: list[Students]) -> list:
        """
        Creates a list of classes in this course with regard to number of student groups. Assign professors to created classes.

        --------
        students: list[Students] - a list of student groups assigned to this course
        """
        classes = []
        for i, type in enumerate(["lecture", "practicals", "laboratories"]):
            if type != "lecture":
                index = 0
                for student_grp in students:
                    index % len(self.professors)
                    hours = self.hours_per_semester[i]
                    if hours != 0:
                        k = hours // 30
                        for i in range(k):
                            classes.append(
                                Class(
                                    f"{self.name}_{type}_{i+1}_grp_{student_grp.group}",
                                    self,
                                    type,
                                    self.professors[index],
                                    [student_grp],
                                )
                            )
                    index += 1
            else:
                hours = self.hours_per_semester[i]
                if hours != 0:
                    k = hours // 30
                    for i in range(k):
                        classes.append(
                            Class(
                                f"{self.name}_{type}_{i+1}",
                                self,
                                type,
                                self.lecturer,
                                students,
                            )
                        )

        return classes


class Data:
    def __init__(self, filename: str):
        self.data = pd.read_excel(f"./{filename}")

    def create_professors(self) -> list[Professor]:
        """Creates list of professors from loaded data.

        --------
        Column "kierownik_przedmiotu" should contain name and surname of single professor
        Column "realizatorzy_przedmiotu" should contain lists: ['IMIE NAZWISKO_1', 'IMIE NAZWISKO_2', ...].
        """
        professors = []
        professors_names = set(self.data.loc[:, "kierownik_przedmiotu"])

        for i in range(len(self.data)):
            for j in eval(self.data.iloc[i]["realizatorzy_przedmiotu"]):
                professors_names.add(j)

        names_list = list(professors_names)

        for prof_name in names_list:
            professors.append(Professor(names_list.index(prof_name), prof_name))

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
                    self.data.iloc[i]["kierunek"],
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
    def __init__(self, day: [0, 1, 2, 3, 4], hour: [0, 1, 2, 3, 4, 5]):
        """
        Creates meeting time.
        "hour" is an integer from 0 to 5, because there's 6 possible slots for a 2–hour class in a day.
        """
        self.day = day
        self.hour = hour

    def __str__(self):
        return f"Day: {self.day}, hour: {self.hour}"


class Room:
    def __init__(self, name: str, capacity: int, category: str):
        self.name = name
        self.category = category  # category "normal" - normal classes; category "laboratories" - laboratories
        self.seating_capacity = (
            capacity  # 1 means 1 group can fit in; 2 means 2 groups etc.
        )

    def __str__(self):
        return self.name


class Class:
    def __init__(
        self,
        name: str,
        course: Course,
        category: str,
        professor: Professor,
        student_groups: list[Students],
    ):
        self.name = name  # jednak daję imię zamiast ID bo tak chyba wystarczy, a łatwiej rozróżnić zajęcia: Analiza_1_ćwiczenia_1 i Analiza_1_ćwiczenia_2 po nazwie
        self.course = course
        self.category = category
        self.professor = professor
        self.meeting_time = None
        self.room = None
        self.student_groups = student_groups  # list grup dla których prowadzone są te zajęcia

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
            + str(self.room)
            + ", "
            + str(self.professor)
            + ", "
            + str(self.meeting_time)
        )


class Schedule:
    def __init__(
        self,
        professors: list[Professor],
        courses: list[Course],
        rooms: list[Room],
        students: list[Students],
    ):
        """
        08.01.2024
        -- przechodzimy przez wszystkie zajęcia po kolei i losujemy/wybieramy ich miejsca w planie (tj. Room i MeetingTime)
        """
        self.rooms = rooms
        self.professors = professors
        self.courses = courses
        self.students = students
        self.classes = []
        for course in self.courses:
            self.classes += course.create_classes(self.students)
        self.number_of_conflicts = 0
        self.fitness = -1

    # może warto generować plan oddzielnie dla każdej grupy studenckiej, wtedy możnaby łatwo na tym etapie uniknąć konfliktów w MeetingTime w obrębie jednej grupy
    def random_schedule(self):
        """
        Generates randomized schedule.
        """
        rooms_lab = [room for room in self.rooms if room.category == "laboratories"]
        rooms_normal = [room for room in self.rooms if room.category == "normal"]
        for item in self.classes:
            item.set_meeting_time(rand.randint(0, 4), rand.randint(0, 5))
            if item.category == "laboratories":
                item.set_room(rand.choice(rooms_lab))
            else:
                item.set_room(rand.choice(rooms_normal))
