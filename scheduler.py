#from collections import namedtuple # student in Student datatype
from sys import argv
import sys
from queue import *

version = [0, 2, 3]

"""Given number n, returns the appropriate suffix for the ordinal number."""
def get_ordinal(n):
    if (n - 11) % 100 != 0 and n % 10 == 1:
        return "st"
    if (n - 12) % 100 != 0 and n % 10 == 2:
        return "nd"
    if (n - 13) % 100 != 0 and n % 10 == 3:
        return "rd"
    return "th"

def readEnrollment(students, arg):
    file = open(arg)
    practical = ""
    count = 0 # line count
    for line in file:
        count += 1
        if line.startswith("Class List"):
            practical = line[-2:] # to be implemented
            continue
        # Things we want to skip
        if line.find("St Lucia") != -1 or line.startswith("StudentID") or \
                line.startswith("End") or len(line) <= 1:
            continue
        # splitting line on ',' as csv
        items = line.split(',')
        if len(items) > 4 and items[0].isnumeric():
            # We know that we have a number (student ID) and a name
            students[int(items[0])] = items[4].strip()
            continue
        #No conditions meet, we have a problem on this line
        print("""File error: %s
On line %d:
%s

The line is not comma ',' separated or does not have the student number in the 
first column and the student's first name in the 5th column.""" % 
(arg, count, line))
        sys.exit()
    file.close()

#Student = namedtuple("Student", "name class")


# MAIN PROGRAM
if len(argv) == 1: # no arguments given, print usage and exit
    print("""Usage:
scheduler.py class_list [class_list...]""")
    sys.exit()

print("Reading enrollment lists...")

students = {} # student ID -> student name
# Reads each argument given to import all student IDs and names
for i in range(len(argv) - 1):
    readEnrollment(students, argv[i + 1])
print("%d students were found" % len(students))

class InQueue(Queue):
    def __contains__(self, item):
        return item in self.queue
    
    def __str__(self):
        result = ""
        for item in self.queue:
            result += str(item) + ", "
        return result
    
    """Finds index of item in queue, return index value or -1 if not there."""
    def index(self, item):
        for i in range(self.qsize()):
            if self.queue[i] == item:
                return i
        return -1
    
print("""Welcome to the Practical Questions tool!
      
      This program was developed and is maintained by Paul Haley.
      
      Version: %d.%d.%d""" % (version[0], version[1], version[2]))

questions = InQueue(70)
student_number = ""
while (True):
    # Get input
    student_number = input("\nPlease enter your student number: ")
    
    # Give next student if available
    if student_number == "n" or student_number == 'next':
        if questions.empty():
            print("No questions awaiting answers...")
            continue
        print("\aPlease answer the question of: %s" % students[questions.get()])
        continue
    
    # Report size of queue and ETA of tutor
    if student_number == "s" or student_number == "size":
        people = questions.qsize()
        print(("There are currently %d students with questions in the queue." +
              "\nThe estimated wait time is approximately: %G minute(s)") % 
              (people, people * 1.5)) # TODO: make a better time estimator
        continue

    # Help for system
    if student_number == "h" or student_number == "help":
        print("""Practical Questions Help
To queue a question, just type your student number (8 digits) at the prompt 
with no 's'.

Command     Short   Response
help        h       Display this help page
next        n       Pops the next student in the queue and displays their name
size        s       Display the size of the queue and the expected wait time
version     v       Display the version number of the program""")
        continue

    # Display version number
    if student_number == 'v' or student_number == "version":
        print("Practical Questions by Paul Haley\n\n\t Version: %d.%d.%d" % 
                (version[0], version[1], version[2]))
        continue
    
    # Screen dump remaining queue and quit
    if student_number == "exit":
        print(questions)
        sys.exit()
    
    # Invalid student number
    if len(student_number) != 8 or not student_number.isnumeric() or \
            int(student_number[0]) != 4:
        print("Please enter your 8 digit student number with no 's'")
        continue
    
    # Student number already in queue.
    if int(student_number) in questions:
        print("Your number is already in the queue! Your position is %d" % 
              (questions.index(int(student_number)) + 1))
        continue
    
    # Student number unseen, add them
    if int(student_number) not in students.keys():
        print("Your student number is not recognised! If you think this is a" +
              " fault, consult the tutors on duty.")
        continue
    
    # Number is of class student who is not already queued
    questions.put(int(student_number))
    n = questions.qsize()
    print("Your student number as been successfullly added!\n" + 
          "Please wait until a tutor comes. You are %d%s in the queue." % 
          (n, get_ordinal(n)))
    
