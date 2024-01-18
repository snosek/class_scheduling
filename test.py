from backend.schedule import *

rooms = [
    Room("B9-F3", 60, "normal"),
    Room("B9-F6", 30, "normal"),
    Room("B9-F7", 60, "normal"),
    Room("B9-F8", 60, "normal"),
    Room("B9-51", 30, "laboratories"),
    Room("B9-52", 60, "normal"),
    Room("B9-53", 30, "laboratories"),
    Room("B14-1.12", 30, "laboratories"),
]
program = Data("program_testowy.xlsx")
professors = program.create_professors()
courses = program.create_courses(professors)
<<<<<<< HEAD
MS_sem_1_gr_1 = Students(0, 1, 1, "matematyka stosowana")
MS_sem_1_gr_2 = Students(1, 1, 2, "matematyka stosowana")
MS_sem_2_gr_1 = Students(2, 2, 1, "matematyka stosowana")
MS_sem_2_gr_2 = Students(3, 2, 2, "matematyka stosowana")
=======
MS_sem_1_gr_1 = Students(1, 1, "matematyka stosowana")
MS_sem_1_gr_2 = Students(1, 2, "matematyka stosowana")
MS_sem_2_gr_1 = Students(2, 1, "matematyka stosowana")
MS_sem_2_gr_2 = Students(2, 2, "matematyka stosowana")
>>>>>>> main
MS = [MS_sem_1_gr_1, MS_sem_1_gr_2, MS_sem_2_gr_1, MS_sem_2_gr_2]

schedule1 = Schedule(professors, courses, rooms, MS)
schedule1.random_schedule()

for i in range(len(MS)):
    print(f"{MS[i]}:")
    for item in schedule1.schedule[i]:
        print(item)
    print(" ")

schedule1.calculate_and_set_number_of_conflicts()
print(schedule1.number_of_conflicts) 

<<<<<<< HEAD
schedule1.visualize_groups("plan_dla_studentow")
=======

schedule1.visualize_group()
>>>>>>> main
