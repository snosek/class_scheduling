from backend.schedule import *
from copy import copy


class Population:
    def __init__(
        self,
        population_size: int,
        professors: list[Professor],
        courses: list[Course],
        rooms: list[Room],
        students: list[Students],
    ):
        """
        Generates a population of specified size. Each speciman is a Schedule object with provided data.
        """
        self.professors = professors
        self.courses = courses
        self.rooms = rooms
        self.students = students
        self.population = [
            Schedule(professors, courses, rooms, students)
            for _ in range(population_size)
        ]
        for schedule in self.population:
            schedule.random_schedule()

    def get_fitnesses(self):
        """
        Returns a list of specimen fitness values.
        """
        res = []
        for schedule in self.population:
            schedule.calculate_and_set_fitness()
            res.append(schedule.fitness)
        return res

    def mutation_swap_classes(self):
        """
        Performs a mutation by swapping two random schedule slots.
        """
        # printy beda do usuniecia, uzywalem do testow, moze jednak cos przegapilem i sie przydadza
        for schedule in self.population:
            drawed_student_group = rand.choice(self.students)
            possible_times = MeetingTime.generate_possible_times()
            rand.shuffle(possible_times)
            time1, time2 = possible_times.pop(), possible_times.pop()
            print(drawed_student_group)
            print(time1, time2)
            drawed_classes = []
            # trzyma wylosowane zajecia w formie [zajecia_czas1, zajecia_czas2], jeśli nie ma wylosowanych zajęć to nic nie trzyma
            for time in [time1, time2]:
                drawed_classes += [
                    item for item in schedule.schedule[drawed_student_group.id]
                    if (item.meeting_time.day == time[0] and item.meeting_time.hour == time[1])
                ]
            drawed_lectures = [item for item in drawed_classes if item.category == "lecture"]
            drawed_normal = [item for item in drawed_classes if item.category != "lecture"]
            # najpierw wyklady, coby było git
            for item in drawed_lectures:
                print(f"drawed class bef: {item}")
                other_time = copy([time1, time2])
                other_time.remove([item.meeting_time.day, item.meeting_time.hour])
                other_time = other_time[0]
                for group in item.student_groups:
                    print(group)
                    this_group_other_class = [
                        class_
                        for class_ in schedule.schedule[group.id]
                        if (
                            class_.meeting_time.day == other_time[0]
                            and class_.meeting_time.hour == other_time[1]
                        )
                    ]
                    if this_group_other_class:
                        print(f"groups other bef: {this_group_other_class[0]}")
                        this_group_other_class[0].set_meeting_time(
                            item.meeting_time.day, item.meeting_time.hour
                        )
                        print(f"groups other af: {this_group_other_class[0]}")
                item.set_meeting_time(other_time[0], other_time[1])
                print(f"drawed class af: {item}")
                # poniżej break bo wystarczy raz zmienić plan dla każdej grupy jeśli wylosowaliśmy wykład
                break
            # poniżej jeszcze jeden break, bo jakbyśmy tego nie zrobili, a wylosowany został jakiś niewykład, to byśmy zmienili plany dla jednej grupy rozwalając wszystko
            if drawed_lectures:
                break

            for item in drawed_normal:
                print(f"drawed class bef: {item}")
                other_time = copy([time1, time2])
                other_time.remove([item.meeting_time.day, item.meeting_time.hour])
                other_time = other_time[0]
                drawed_group_other_class = [
                    class_
                    for class_ in schedule.schedule[drawed_student_group.id]
                    if (
                        class_.meeting_time.day == other_time[0]
                        and class_.meeting_time.hour == other_time[1]
                    )
                ]
                if drawed_group_other_class:
                    print(f"drawed other bef: {drawed_group_other_class[0]}")
                    drawed_group_other_class[0].set_meeting_time(
                        item.meeting_time.day, item.meeting_time.hour
                    )
                    print(f"drawed other af: {drawed_group_other_class[0]}")
                item.set_meeting_time(other_time[0], other_time[1])
                print(f"drawed class af: {item}")
                # poniżej break bo wystarczy zamiana raz
                # będąc w tym bloku jesteśmy pewni, że nie wylosowaliśmy wykładu, więc nie ma sytuacji. w której drawed_group_other_class jest wykładem i zmieniamy tylko jego, bez zmiany planów innych grup
                break
