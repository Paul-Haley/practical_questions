#from collections import namedtuple
from sys import argv
import sys
from queue import *

#def readEnrollment(student, arg):
    

#Student = namedtuple("Student", "name class")

#students = {} # student ID -> student name
# Reads each argument given to import all student IDs and names
#for arg in argv:
#    readEnrollment(student, arg)
    
class InQueue(Queue):
    def __contains__(self, item):
        return item in self.queue
    
    def __str__(self):
        result = ""
        for item in self.queue:
            result += str(item) + ", "
        return result
    
# MAIN PROGRAM
print("""Welcome to the Practical Questions tool for %s.
      This program was developed and is maintained by Paul Haley.
      
      Version: 0.1
      """ % argv[1])

questions = InQueue(70)
student_number = ""
while (True):
    # Get input
    student_number = input("\nPlease enter your student number: ")
    
    if student_number == "NEXT":
        if questions.empty():
            print("No questions awaiting answers...")
            continue
        print("\aPlease answer the question of: %s" % questions.get())
        continue
    
    if student_number == "ADMIN DELETE THIS":
        print(questions)
        sys.exit()
    
    if len(student_number) != 8 or not student_number.isnumeric() or int(student_number[0]) != 4:
        print("Please enter your 8 digit student number with no 's'")
        continue
    
    if int(student_number) in questions:
        print("Your number is already in the queue!")
        continue
    
    # Student number unseen, add them
    questions.put(int(student_number))
    print("Your student number as been successfullly add!\n" + 
          "Please wait until a tutor comes. You are %dth in the queue." % 
          questions.qsize())
    
    
