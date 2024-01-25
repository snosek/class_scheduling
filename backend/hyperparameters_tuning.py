import optuna
from genetic_algorithm import *
from math import floor

rooms = [
    Room("B9-F1", 60, "normal"),
    Room("B9-F2", 60, "normal"),
    Room("B9-F3", 60, "normal"),
    Room("B9-F4", 60, "normal"),
    Room("B9-F5", 60, "normal"),
    Room("B9-F6", 30, "normal"),
    Room("B9-F7", 60, "normal"),
    Room("B9-F8", 60, "normal"),
    Room("B9-F9", 60, "normal"),
    Room("B9-F10", 150, "normal"),
    Room("B9-51", 30, "laboratories"),
    Room("B9-52", 60, "normal"),
    Room("B9-53", 30, "laboratories"),
    Room("B14-1.11", 60, "normal"),
    Room("B14-1.12", 30, "laboratories"),
    Room("B14-2.1", 30, "laboratories"),
    Room("B14-2.2", 30, "laboratories"),
    Room("B14-2.3", 30, "laboratories"),
]

program = Data("program.xlsx")

professors = program.create_professors()

courses = program.create_courses(professors)

MS_sem_1_gr_1 = Students(0, 1, 1, "matematyka stosowana")
MS_sem_1_gr_2 = Students(1, 1, 2, "matematyka stosowana")
MS_sem_2_gr_1 = Students(2, 2, 1, "matematyka stosowana")
MS_sem_2_gr_2 = Students(3, 2, 2, "matematyka stosowana")
MS_sem_3_gr_1 = Students(4, 3, 1, "matematyka stosowana")
MS_sem_3_gr_2 = Students(5, 3, 2, "matematyka stosowana")
MS_sem_4_gr_1 = Students(6, 4, 1, "matematyka stosowana")
MS_sem_4_gr_2 = Students(7, 4, 2, "matematyka stosowana")
MS_sem_5_gr_1 = Students(8, 5, 1, "matematyka stosowana")
MS_sem_6_gr_1 = Students(9, 6, 1, "matematyka stosowana")

students = [
    MS_sem_1_gr_1, MS_sem_1_gr_2, MS_sem_2_gr_1, MS_sem_2_gr_2,
    MS_sem_3_gr_1, MS_sem_3_gr_2, MS_sem_4_gr_1, MS_sem_4_gr_2,
    MS_sem_5_gr_1, MS_sem_6_gr_1, 
]

def objective(trial):
    population_size = trial.suggest_int("population_size", 50, 500, step = 10)
    mutation_probability = trial.suggest_float("mutation_probability", 0.1, 1, step = 0.05)
    elites_percentage = trial.suggest_float("number_of_elites", 0.05, 0.2, step = 0.05)
    pairs_percentage = trial.suggest_float("number_of_pairs", 0.4, 1, step = 0.1)
    number_of_class_swaps = trial.suggest_int("number_of_class_swaps", 1, 15, step = 1)
    number_of_room_swaps = trial.suggest_int("number_of_room_swaps", 1, 15, step = 1)

    pop = Population(
        population_size,
        professors,
        courses,
        rooms,
        students,
        mutation_probability,
        floor(population_size * elites_percentage),
        floor(population_size/2 * pairs_percentage), 
        number_of_class_swaps,
        number_of_room_swaps,
    )

    pop.population = pop.sort_by_fitness_and_soft_fitness(pop.population)

    pop.execute(100)
    
    return pop.population[0].fitness + pop.population[0].soft_fitness

study = optuna.create_study(direction = "maximize")

study.optimize(objective, n_trials = 100)

print(study.best_trial.value)
print(study.best_trial.value)