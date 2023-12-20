class Course:
    def __init__(self, id, name, semester, hours_per_semester, lecturer, professors):
        self.id = id
        self.name = name
        self.semester = semester
        self.hours_per_semester = hours_per_semester
        self.lecturer = lecturer
        self.professors = professors

    def __str__(self):
        return self.name


class Instructor:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class MeetingTime:
    def __init__(self, day, hour):
        self.day = day
        self.hour = hour

    def __str__(self):
        return f"Day: {self.day}, hour: {self.hour}"


class Students:
    def __init__(self, semester, group):
        self.semester = semester
        self.group = group

    def __str__(self):
        return str(self.semester) + str(self.group)


class Room:
    def __init__(self, name, capacity, category):
        self.name = name
        self.category = category  # category "normal" -- normal classes; category "lab" -- laboratories
        self.seating_capacity = capacity

    def __str__(self):
        return self.name


class Class:
    def __init__(self, id, course, category):
        self.id = id
        self.course = course
        self.category = category
        self.instructor = None
        self.meeting_time = None
        self.room = None
        if category == "lecture":
            self.hours_per_semester = self.course.hours_per_semester[0]
        elif category == "practicals":
            self.hours_per_semester = self.course.hours_per_semester[1]
        elif category == "laboratories":
            self.hours_per_semester = self.course.hours_per_semester[2]

    def set_instructor(self, instructor):
        self.instructor = instructor

    def set_meeting_time(self, day, hour):
        self.meeting_time = MeetingTime(day, hour)

    def set_room(self, room):
        self.room = room

    def __str__(self):
        return (
            str(self.course)
            + str(self.room)
            + str(self.instructor)
            + str(self.meeting_time)
        )


class Schedule:
    """ """
