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
        mutation_probability: float,
        number_of_elites: int,
    ):
        """
        Generates a population of specified size. Each speciman is a Schedule object with provided data.
        """
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.number_of_elites = number_of_elites
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
        self.set_fitnesses()
        self.population = self.sort_by_fitness()

    def set_fitnesses(self):
        """
        Returns a list of specimen fitness values.
        """
        res = []
        for schedule in self.population:
            schedule.calculate_and_set_fitness()
            res.append(schedule.fitness)
        return res

    def mutation_swap_classes(self, schedules: list[Schedule]):
        """
        Performs a mutation by swapping two random schedule slots.
        """
        for schedule in schedules:
            if rand.random() < self.mutation_probability:
                drawed_student_group = rand.choice(self.students)
                possible_times = MeetingTime.generate_possible_times()
                rand.shuffle(possible_times)
                time1, time2 = possible_times.pop(), possible_times.pop()
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
                    other_time = copy([time1, time2])
                    other_time.remove([item.meeting_time.day, item.meeting_time.hour])
                    other_time = other_time[0]
                    for group in item.student_groups:
                        this_group_other_class = [
                            class_ for class_ in schedule.schedule[group.id]
                            if (
                                class_.meeting_time.day == other_time[0]
                                and class_.meeting_time.hour == other_time[1]
                            )
                        ]
                        if this_group_other_class:
                            this_group_other_class[0].set_meeting_time(item.meeting_time.day, item.meeting_time.hour)
                    item.set_meeting_time(other_time[0], other_time[1])
                    # poniżej break bo wystarczy raz zmienić plan dla każdej grupy jeśli wylosowaliśmy wykład
                    break
                # poniżej jeszcze jeden break, bo jakbyśmy tego nie zrobili, a wylosowany został jakiś niewykład, to byśmy zmienili plany dla jednej grupy rozwalając wszystko
                if drawed_lectures:
                    break

                for item in drawed_normal:
                    other_time = copy([time1, time2])
                    other_time.remove([item.meeting_time.day, item.meeting_time.hour])
                    other_time = other_time[0]
                    drawed_group_other_class = [
                        class_ for class_ in schedule.schedule[drawed_student_group.id]
                        if (
                            class_.meeting_time.day == other_time[0]
                            and class_.meeting_time.hour == other_time[1]
                        )
                    ]
                    if drawed_group_other_class:
                        drawed_group_other_class[0].set_meeting_time(item.meeting_time.day, item.meeting_time.hour)
                    item.set_meeting_time(other_time[0], other_time[1])
                    # poniżej break bo wystarczy zamiana raz
                    # będąc w tym bloku jesteśmy pewni, że nie wylosowaliśmy wykładu, więc nie ma sytuacji. w której drawed_group_other_class jest wykładem i zmieniamy tylko jego, bez zmiany planów innych grup
                    break
                

    def sort_by_fitness(self) -> list[Schedule]:
        self.set_fitnesses()
        return sorted(self.population, key = lambda x: x.fitness, reverse = True)

    def genetic_cycle(self):
        new_population = self.population[:self.number_of_elites]
        self.mutation_swap_classes(self.population[self.number_of_elites:])
        new_population.extend(self.population[self.number_of_elites:])
        self.population = self.sort_by_fitness()
        return new_population
    
    def execute(self, number_of_cycles: int):
        self.population = self.sort_by_fitness()
        for j in range(number_of_cycles):
            self.population = self.genetic_cycle()
            print(f"""After {j+1}-th genetic cycle the best result so far is:
                {self.population[0].fitness};
            """)
        return self.population[0]