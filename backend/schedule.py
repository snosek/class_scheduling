import os
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

    def generate_possible_times():
        """
        Generates a list of possible times in the format [day, hour].
        """
        possible_times = []
        for day in range(5):
            for hour in range(6):
                possible_times.append(MeetingTime(day, hour))
        return possible_times

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        else:
            return self.day == other.day and self.hour == other.hour

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

    def set_meeting_time(self, meeting_time: MeetingTime):
        self.meeting_time = meeting_time

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
            this_course_students = []
            for student_group in students:
                if (
                    student_group.semester == course.semester
                    and student_group.subject == course.subject
                ):
                    this_course_students.append(student_group)
            self.classes += course.create_classes(this_course_students)
        self.number_of_conflicts = 0
        self.number_of_early_hours = 0
        self.number_of_late_hours = 0
        self.number_of_free_days = 0
        self.number_of_course_conflicts = 0
        self.number_of_free_periods = 0
        self.length_of_free_periods = 0
        self.fitness = -1
        self.schedule = []


    def random_schedule(self) -> None:
        """
        Generate a random schedule for all groups. Prevents conflicts within groups, may generate conflicts for rooms and professors
        """
        rooms_lab = [room for room in self.rooms if room.category == "laboratories"]
        rooms_normal = [room for room in self.rooms if room.category == "normal"]
        for student_group in self.students:
            temp = []
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
                    item.set_meeting_time(drawed_meeting_time)
                    if item.category == "laboratories":
                        item.set_room(rand.choice(rooms_lab))
                    else:
                        item.set_room(rand.choice(rooms_normal))
                else:
                    possible_times.remove(item.meeting_time)
                temp.append(item)
            for item in group_classes:
                drawed_meeting_time = possible_times.pop()
                item.set_meeting_time(drawed_meeting_time)
                if item.category == "laboratories":
                    item.set_room(rand.choice(rooms_lab))
                else:
                    item.set_room(rand.choice(rooms_normal))
                temp.append(item)
            self.schedule.append(temp)

    def calculate_and_set_number_of_conflicts(self) -> None:
        """
        Calculate number of conflicts in this schedule. Set number_of_conflicts attribute as calculated value.
        """
        conflicts = 0
        for i, class_1 in enumerate(self.classes):
            for j in range(i+1, len(self.classes)):
                if (
                    class_1.professor == self.classes[j].professor
                    or class_1.room == self.classes[j].room
                ) and class_1.meeting_time == self.classes[j].meeting_time:
                    conflicts += 1
        self.number_of_conflicts = conflicts - len(self.classes)

    def calculate_and_set_number_of_early_and_late_hours(self) -> None:
        """
        Calculate number of early and late hours (at 8-10 and 18-20) in this schedule.
        Set those numbers as number_of_early_hours and number_of_late_hours attributes.
        """
        early_hours = 0
        late_hours = 0

        for class_ in self.classes:
            if class_.meeting_time.hour == 0:
                # wykład może być u kilku grup i dlatego jest tak jak niżej
                early_hours += len(class_.student_groups)
            elif class_.meeting_time.hour == 5:
                late_hours += len(class_.student_groups)

        self.number_of_early_hours = early_hours
        self.number_of_late_hours = late_hours

    def calculate_and_set_number_of_free_days(self) -> None:
        """
        Calculate number of free days for student groups in this schedule.
        Set number_of_free_days attrubute as calculated value.
        """
        free_days = 0

        for group_plan in self.schedule:
            class_times = [[class_.meeting_time.day, class_.meeting_time.hour] for class_ in group_plan]

            for day in [0,1,2,3,4]:
                taken_hours = 0
                for hour in [0,1,2,3,4,5]:
                    if [day,hour] in class_times:
                        taken_hours += 1
                        break
                if taken_hours == 0:
                    free_days += 1
        
        self.number_of_free_days = free_days

    def calculate_and_set_number_of_free_periods(self) -> None:
        """
        Calcualate number of free periods and their cumulative length.
        Set those calculated values as appropriate attributes.
        """
        free_periods = 0
        free_periods_length = 0

        for group_plan in self.schedule:
            class_times = [[class_.meeting_time.day, class_.meeting_time.hour] for class_ in group_plan]

            for day in [0, 1, 2, 3, 4]:
                hour = 0
                while hour <= 5:
                    if [day, hour] in class_times:
                        this_period_length = 0
                        this_period = 0
                        for next_period_hour in range(hour+1, 6):
                            if [day, next_period_hour] in class_times:
                                if this_period_length != 0:
                                    this_period += 1
                                hour = next_period_hour-1
                                break
                            else:
                                this_period_length +=1
                                hour = next_period_hour-1
                        if this_period == 1:
                            free_periods += 1
                            free_periods_length += this_period_length
                    hour += 1
        
        self.number_of_free_periods = free_periods
        self.length_of_free_periods = free_periods_length
                
    def calculate_and_set_number_of_course_conflicts(self):
        """
        Calculate number of practicals/laboratories/lectures within every course assigned to a specific group
        that happen at the same day.
        Set calculated vale as course_conflicts attribute.
        --------
        Within one course a student group shouldn't have two practicals at the same day.
        It also applies to laboratories and lectures.
        Although having laboratories and practicals and lecture in the same day is acceptable.
        """
        subject_conflicts = 0

        for student_group in self.students:
            for course in self.courses:
                if student_group.subject == course.subject \
                    and student_group.semester == course.semester:
                    group_labs_from_subject = [class_ for class_ in self.schedule[student_group.id]
                                                if (class_.course == course and class_.category == "laboratories")]
                    group_practicals_from_subject = [class_ for class_ in self.schedule[student_group.id]
                                                    if (class_.course == course and class_.category == "practicals")]

                    N = len(group_labs_from_subject)
                    for i in range(N):
                        for j in range(i+1, N):
                            if group_labs_from_subject[i].meeting_time.day == group_labs_from_subject[j].meeting_time.day:
                                subject_conflicts += 1
                    
                    M = len(group_practicals_from_subject)
                    for i in range(M):
                        for j in range(i+1, M):
                            if group_practicals_from_subject[i].meeting_time.day == group_practicals_from_subject[j].meeting_time.day:
                                subject_conflicts += 1
                
                course_lectures = [class_ for class_ in self.classes 
                                   if (class_.course == course and class_.category == "lecture")]
                
                K = len(course_lectures)
                for i in range(K):
                    for j in range(i+1, K):
                        if course_lectures[i].meeting_time.day == course_lectures[j].meeting_time.day:
                            subject_conflicts += 1

        
        self.number_of_course_conflicts = subject_conflicts

    def calculate_and_set_fitness(self):
        self.calculate_and_set_number_of_conflicts()
        self.fitness = 1.0 / (self.number_of_conflicts + 1)

    def visualize_rooms(self, file_name: str) -> None:
        """
       
        """
        if os.path.exists(f"{file_name}_rooms.xlsx"):
            os.remove(f"{file_name}_rooms.xlsx")
            writer = pd.ExcelWriter(f"{file_name}_rooms.xlsx", engine="xlsxwriter")
            workbook = writer.book
            worksheet = workbook.add_worksheet("Arkusz_1")
            worksheet.write(0, 0, " ")
            writer.close()
        else:
            writer = pd.ExcelWriter(f"{file_name}_rooms.xlsx", engine="xlsxwriter")
            workbook = writer.book
            worksheet = workbook.add_worksheet("Arkusz_1")
            worksheet.write(0, 0, " ")
            writer.close()

        for i, room in enumerate(self.rooms):
            df = pd.DataFrame(index=[0, 1, 2, 3, 4, 5], columns=[0, 1, 2, 3, 4])
            for class_ in self.classes:
                if class_.room == room:
                    df[class_.meeting_time.day][class_.meeting_time.hour] = class_.name
            df.columns = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek")
            df.index = ("8-10", "10-12", "12-14", "14-16", "16-18", "18-20")
            # Zapis do arkusza kalkulacyjnego
            with pd.ExcelWriter(
                f"{file_name}_rooms.xlsx", mode="a", engine="openpyxl"
            ) as writer:
                df.to_excel(writer, sheet_name=f"{room.name}_{room.category}")



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

    def visualize_professors(self, file_name: str) -> None:
        """
        
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

        for i, professor in enumerate(self.professors):
            professor_schedule = [class_ for class_ in self.classes if class_.professor == professor]
            df = pd.DataFrame(index=[0, 1, 2, 3, 4, 5], columns=[0, 1, 2, 3, 4])
            for lecture in professor_schedule:
                df[lecture.meeting_time.day][lecture.meeting_time.hour] = lecture.name
            df.columns = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek")
            df.index = ("8-10", "10-12", "12-14", "14-16", "16-18", "18-20")
            
            with pd.ExcelWriter(
                f"{file_name}.xlsx", mode="a", engine="openpyxl"
            ) as writer:
                df.to_excel(
                    writer, sheet_name=f"{professor.name}_{i + 1}"
                )


"""
Spotkanie 15.01:
-- DONE Fitness w klasie Schedule 

-- DONE Osobna klasa do algorytmu genetycznego:
    -- Mutacje (w obrębie całego planu tj. obiektu klasy Schedule): 
        1. DONE Wybranie losowych "okienek" w planie i zamiana ich miejscami -- UWAGA NA WYKŁADY
        2. Zamiana całych dni miejscami -- UWAGA NA WYKŁAD
        3. DONE Zmiana miejsca i godziny jednych zajęć na losowy (inny pokój) w wolnym czasie 
        4. ...
    -- Crossovers (w obrębie dwóch obiektów klasy Schedule): 
        0. DONE Z pierwszego rodzica bierzemy tylko część semestrów a zdrugiego reszt 
        1. Wybieramy zajęcia, zapamiętujemy miejsca w obu planach i zamieniamy te miejsca w obu planach
        2. Z pierwszego rodzica wybieramy losowo trochę zajęć i wpisujemy je do planu dziecka. Póżniej z planu drugiego rodzica wykreślamy wybrane już zajęcia a pozostałe umieszczamy losowo w planie dziecka.
    -- Selekcja:
        DONE Zostawienie n najlepszych osobników

-- DONE Dokończenie wizualizacji danych
"""

"""
Spotkanie 22.01:
-- Dodanie kolejnej funkcji fitness i aktualizacja sortowania
    -- Wygenerowanie najlepszego planu

-- Przygotowanie pliku do prezentacji:
    -- prezentacja wszytkich metod i klas

-- Poprawienie jakości wizualizacji (szerokość kolumn)
    
"""
