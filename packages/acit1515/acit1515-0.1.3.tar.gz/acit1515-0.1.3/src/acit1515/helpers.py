class Transcript:
    def __init__(self, firstname: str, lastname: str, grades: dict[str, str]):
        self.firstname = firstname
        self.lastname = lastname
        self.grades = grades

    def print_grades(self, enumerated = False):
        obj_str = ''
        for i, grade in enumerate(self.grades):
            if enumerated:
                obj_str += f'{i + 1}. '
            obj_str += f'{grade["course"]}: {grade["mark"]}\n'
        return obj_str[:-1]

    def to_string(self, enumerated = False):
        obj_str = f'{self.firstname} {self.lastname}\n'
        obj_str += self.print_grades(enumerated)
        return obj_str
    
