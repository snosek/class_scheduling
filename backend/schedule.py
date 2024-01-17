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
    def __init__(self, id: int, semester: int, group: int, subject: str):
        self.id = id
        self.semester = semester
        self.group = group
        self.subject = subject
        self.class_assignment = []
        self.size = 0

    def __str__(self):
        return f"Kierunek {self.subject} Semestr {self.semester} Grupa {self.group}"

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
                    index = index % len(self.professors)
                    hours = self.hours_per_semester[i]
                    if hours != 0:
                        k = hours // 30
                        for j in range(k):
                            classes.append(
                                Class(
                                    f"{self.name}_{type}_{j+1}_grp_{student_grp.group}",
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
                    for j in range(k):
                        classes.append(
                            Class(
                                f"{self.name}_{type}_{j+1}",
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

<<<<<<< Updated upstream
=======
    def generate_possible_times():
        possible_times = []
        for day in range(5):
            for hour in range(6):
                possible_times.append([day, hour])
        return possible_times

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        else:
            return self.day == other.day and self.hour == other.hour

>>>>>>> Stashed changes
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
        # jednak daję imię zamiast ID bo tak chyba wystarczy, a łatwiej rozróżnić zajęcia: Analiza_1_ćwiczenia_1 i Analiza_1_ćwiczenia_2 po nazwie
        self.name = name
        self.course = course
        self.category = category
        self.professor = professor
        self.meeting_time = None
        self.room = None
        # lista grup dla których prowadzone są te zajęcia
        self.student_groups = student_groups

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
        self.rooms = rooms
        self.professors = professors
        self.courses = courses
        self.students = students
        self.classes = []
        for course in self.courses:
<<<<<<< Updated upstream
            self.classes += course.create_classes(self.students)
=======
            this_course_students = []
            for student_group in students:
                if (
                    student_group.semester == course.semester
                    and student_group.subject == course.subject
                ):
                    this_course_students.append(student_group)
            self.classes += course.create_classes(this_course_students)
        # poniżej trójwymiarowa macierz zajęć w formacie classes_matrix[student_groups.ids][days][hours]
        # chyba jednak niepotrzebna
        self.classes_matrix = [
            [[None for _ in range(6)] for _ in range(5)] for _ in self.students
        ]
>>>>>>> Stashed changes
        self.number_of_conflicts = 0
        self.fitness = -1
        self.schedule = []

<<<<<<< Updated upstream
    # może warto generować plan oddzielnie dla każdej grupy studenckiej, wtedy możnaby łatwo na tym etapie uniknąć konfliktów w MeetingTime w obrębie jednej grupy
    def random_schedule(self):
=======
    def random_schedule(self) -> None:
        """
        Generate a random schedule for all groups. Prevents conflicts within groups, may generate conflicts for rooms and professors
        """
>>>>>>> Stashed changes
        rooms_lab = [room for room in self.rooms if room.category == "laboratories"]
        rooms_normal = [room for room in self.rooms if room.category == "normal"]
        for student_group in self.students:
            temp = []
<<<<<<< Updated upstream
            group_classes = [item for item in self.classes if student_group in item.student_groups]
            possible_times = []
            for day in range(5):
                for hour in range(6):
                    possible_times.append([day, hour])
            rand.shuffle(possible_times)
=======
            group_classes = [
                item
                for item in self.classes
                if (student_group in item.student_groups) and item.category != "lecture"
            ]
            group_lectures = [
                item
                for item in self.classes
                if (student_group in item.student_groups) and item.category == "lecture"
            ]
            possible_times = MeetingTime.generate_possible_times()
            rand.shuffle(possible_times)

            # najpierw wykłady by zapobiec "przekładaniu" zajęć na inne miejsce w kolejnych losowaniach dla grup
            for item in group_lectures:
                if item.meeting_time == None:
                    drawed_meeting_time = possible_times.pop()
                    item.set_meeting_time(
                        drawed_meeting_time[0], drawed_meeting_time[1]
                    )
                    if item.category == "laboratories":
                        item.set_room(rand.choice(rooms_lab))
                    else:
                        item.set_room(rand.choice(rooms_normal))
                else:
                    possible_times.remove(
                        [item.meeting_time.day, item.meeting_time.hour]
                    )
                temp.append(item)
                # ponizej raczej niepotrzebne
                for id in [group.id for group in item.student_groups]:
                    self.classes_matrix[id][item.meeting_time.day][
                        item.meeting_time.hour
                    ] = item

>>>>>>> Stashed changes
            for item in group_classes:
                drawed_meeting_time = possible_times.pop()
                item.set_meeting_time(drawed_meeting_time[0], drawed_meeting_time[1])
                if item.category == "laboratories":
                    item.set_room(rand.choice(rooms_lab))
                else:
                    item.set_room(rand.choice(rooms_normal))
                temp.append(item)
                self.classes_matrix[student_group.id][item.meeting_time.day][
                    item.meeting_time.hour
                ] = item
            self.schedule.append(temp)
<<<<<<< Updated upstream

        """
    def random_schedule(self):
        
        Generates randomized schedule.
        
        rooms_lab = [room for room in self.rooms if room.category == "laboratories"]
        rooms_normal = [room for room in self.rooms if room.category == "normal"]
        for item in self.classes:
            item.set_meeting_time(rand.randint(0, 4), rand.randint(0, 5))
            if item.category == "laboratories":
                item.set_room(rand.choice(rooms_lab))
            else:
                item.set_room(rand.choice(rooms_normal))
"""
=======

    def calculate_and_set_number_of_conflicts(self) -> None:
        """
        Calculate number of conflicts in this schedule. Set number_of_conflicts attribute as calculated value.
        """
        conflicts = 0
        for class_1 in self.classes:
            for class_2 in self.classes:
                if (
                    class_1.professor == class_2.professor
                    or class_1.room == class_2.room
                ) and class_1.meeting_time == class_2.meeting_time:
                    conflicts += 1
        self.number_of_conflicts = conflicts - len(self.classes)

    def calculate_and_set_fitness(self):
        self.calculate_and_set_number_of_conflicts()
        self.fitness = 1.0 / (self.number_of_conflicts + 1)

    # używane w mutacji, bo tak chyba prościej xd
    # znow, chyba niepotrzebne, ale zobaczymy
    def update_from_matrix(self):
        for group in self.classes_matrix:
            for dayid, day in enumerate(group):
                for hourid, class_ in enumerate(day):
                    if class_ is not None:
                        class_.set_meeting_time(dayid, hourid)
                        print(class_.meeting_time == MeetingTime(dayid, hourid))

    def visualize_groups(self, file_name: str) -> None:
        """
        Check if file_name.xlsx already exists. If it does remove it and create a new empty one, otherwise create a new empty one.
        Fill an excel spreadsheet with schedules for all student groups.
        """
        if os.path.exists(f"{file_name}.xlsx"):
            os.remove(f"{file_name}.xlsx")
            writer = pd.ExcelWriter(f"{file_name}.xlsx", engine="xlsxwriter")
            workbook = writer.book
            worksheet = workbook.add_worksheet("Arkusz_1")
            worksheet.write(0, 0, " ")
            writer.close()
        else:
            writer = pd.ExcelWriter(f"{file_name}.xlsx", engine="xlsxwriter")
            workbook = writer.book
            worksheet = workbook.add_worksheet("Arkusz_1")
            worksheet.write(0, 0, " ")
            writer.close()

        for i, group_plan in enumerate(self.schedule):
            df = pd.DataFrame(index=[0, 1, 2, 3, 4, 5], columns=[0, 1, 2, 3, 4])
            for lecture in group_plan:
                df[lecture.meeting_time.day][lecture.meeting_time.hour] = lecture.name
            df.columns = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek")
            df.index = ("8-10", "10-12", "12-14", "14-16", "16-18", "18-20")
            # dałem zapisanie do excela bo nie umiem zrobić żeby się ładnie wyświetalało xd
            # jeśli zostajemy przy czymś takim, to można jakoś automatycznie formatować pliki by ładnie wyglądały
            group = self.students[i]
            with pd.ExcelWriter(
                f"{file_name}.xlsx", mode="a", engine="openpyxl"
            ) as writer:
                df.to_excel(
                    writer, sheet_name=f"{group.subject}_{group.semester}_{group.group}"
                )


"""
Spotkanie 15.01:
-- DONE Fitness w klasie Schedule 

-- Osobna klasa do algorytmu genetycznego:
    -- Mutacje (w obrębie całego planu tj. obiektu klasy Schedule): 
        1. DONE Wybranie losowych "okienek" w planie i zamiana ich miejscami -- UWAGA NA WYKŁADY
        2. Zamiana całych dni miejscami -- UWAGA NA WYKŁAD
        3. Zmiana miejsca i godziny jednych zajęć na losowy (inny pokój) w wolnym czasie 
        4. ...
    -- Crossovers (w obrębie dwóch obiektów klasy Schedule): 
        1. Wybieramy zajęcia, zapamiętujemy miejsca w obu planach i zamieniamy te miejsca w obu planach
        2. Z pierwszego rodzica wybieramy losowo trochę zajęć i wpisujemy je do planu dziecka. Póżniej z planu drugiego rodzica
            wyrkeślamy wybrane już zajęcia a pozostałe umieszczamy losowo w planie dziecka.
    -- Selekcja:
        Zostawienie n najlepszych osobników

-- Dokończenie wizualizacji danych
"""
>>>>>>> Stashed changes
