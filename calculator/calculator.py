import sqlite3
import time
from typing import List, Dict

class GradePortal:
    """Education portal grade processing system using SQLite database."""
    
    def __init__(self):
        self.conn = sqlite3.connect('education_portal.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        
    def setup_database(self):
        self.cursor.executescript('''
            CREATE TABLE student (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone_number INTEGER,
                address TEXT,
            );
            
            CREATE TABLE courses (
                course_id TEXT PRIMARY KEY,
                title TEXT,
                department TEXT,
                credit_hours INTEGER
            );
            
            CREATE TABLE gradings (
                grading_id INTEGER PRIMARY KEY,
                course_id TEXT,
                section_id TEXT,
                grading_type TEXT,
                grading_weight FLOAT
            );
            
            CREATE TABLE scores (
                score_id INTEGER PRIMARY KEY,
                user_id TEXT,
                grading_id INTEGER,
                marks FLOAT
            );
        ''')
        self.conn.commit()
    
    def calculate_student_grades(self, course_id: str) -> List[Dict]:
        """
        Calculate grades for all students in a course.
        This is an inefficient implementation with multiple queries.
        """
        start_time = time.time()
        
        # Inefficient query: Fetches all data and processes in Python
        # Instead of using SQL aggregation functions
        try:
            # Bug: No parameter binding (SQL injection vulnerability)
            self.cursor.execute(f'''
                SELECT DISTINCT s.student_id, s.name 
                FROM students s
                JOIN grades g ON s.student_id = g.student_id
                JOIN assignments a ON g.assignment_id = a.assignment_id
                WHERE a.course_id = '{course_id}'
            ''')
            
            students = self.cursor.fetchall()
            results = []
            
            for student_id, name in students:
                # Inefficient: Makes separate queries for each student
                self.cursor.execute(f'''
                    SELECT a.assignment_type, a.weight, g.score
                    FROM grades g
                    JOIN assignments a ON g.assignment_id = a.assignment_id
                    WHERE g.student_id = '{student_id}'
                    AND a.course_id = '{course_id}'
                ''')
                
                grades = self.cursor.fetchall()
                
                # Inefficient: Processes grades in Python instead of SQL
                final_grade = 0
                for assignment_type, weight, score in grades:
                    final_grade += (score * weight / 100)
                
                results.append({
                    'student_id': student_id,
                    'name': name,
                    'final_grade': round(final_grade, 2)
                })
                
            end_time = time.time()
            print(f"Query execution time: {end_time - start_time:.2f} seconds")
            
            return results
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

def main():
    portal = GradePortal()
    cursor = portal.cursor
    
    # Insert sample data
    cursor.executescript('''
        INSERT OR IGNORE INTO students (student_id, name) VALUES 
        ('S1', 'John Doe'),
        ('S2', 'Jane Smith'),
        ('S3', 'Bob Wilson');
        
        INSERT OR IGNORE INTO courses (course_id, name) VALUES 
        ('CS101', 'Introduction to Programming');
        
        INSERT OR IGNORE INTO assignments (course_id, assignment_type, weight) VALUES 
        ('CS101', 'homework', 30),
        ('CS101', 'tests', 40),
        ('CS101', 'projects', 30);
        
        INSERT OR IGNORE INTO grades (student_id, assignment_id, score) VALUES 
        ('S1', 1, 85),
        ('S1', 2, 92),
        ('S1', 3, 88),
        ('S2', 1, 90),
        ('S2', 2, 85),
        ('S2', 3, 95),
        ('S3', 1, 78),
        ('S3', 2, 88),
        ('S3', 3, 84);
    ''')
    portal.conn.commit()
    
    # Generate grade report
    results = portal.calculate_student_grades('CS101')
    
    print("\nStudent Grades:")
    for result in results:
        print(f"{result['name']} ({result['student_id']}): {result['final_grade']}%")

if __name__ == "__main__":
    main()