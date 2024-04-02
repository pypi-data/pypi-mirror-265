class Course:
    def __init__(self, name, duration, link):
        self.name = name 
        self.duration = duration
        self.link = link

    def __str__(self):
        return f"{self.name} [{self.duration} Horas] ({self.link})"

courses = [
    Course("Introuccion a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalizacion de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introduccion al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

for course in courses:
    print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course:

    return None 

