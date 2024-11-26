import sqlite3
import time
from typing import List, Dict

class GradePortal:
    
    def __init__(self):
        self.conn = sqlite3.connect('education_portal.db')
        self.cursor = self.conn.cursor()
        self.init_db()
        
    def init_db(self):
        self.cursor.executescript('''
            DROP TABLE IF EXISTS students;
            DROP TABLE IF EXISTS modules;
            DROP TABLE IF EXISTS assignments;
            DROP TABLE IF EXISTS final_grades;
            DROP TABLE IF EXISTS quizzes; 
            DROP TABLE IF EXISTS attendance;
            DROP TABLE IF EXISTS sections;
            
            CREATE TABLE students (
                s_id TEXT PRIMARY KEY,
                s_name TEXT,
                student_email TEXT,
                student_avatar TEXT,
                student_dob TEXT,
                student_balance INTEGER
            );
            
            CREATE TABLE sections (
                section_id TEXT PRIMARY KEY,
                section_name TEXT
            );
            
            CREATE TABLE modules (
                m_id TEXT PRIMARY KEY,
                module_name TEXT,
                module_percent Integer,
                section_id TEXT
            );
            
            CREATE TABLE assignments (
                a_id INTEGER PRIMARY KEY,
                m_id TEXT,
                t_type TEXT,
                t_per FLOAT
            );
            
            CREATE TABLE quizzes (
                quiz_id INTEGER PRIMARY KEY,
                m_id TEXT,
                quiz_score FLOAT
            );
            
            CREATE TABLE attendance (
                attendance_id INTEGER PRIMARY KEY,
                s_id TEXT,
                m_id TEXT,
                status TEXT
            );
            
            CREATE TABLE final_grades (
                final_grades_id INTEGER PRIMARY KEY,
                s_id TEXT,
                a_id INTEGER,
                final_grade FLOAT
            );
        ''')
        self.conn.commit()

    def get_grades(self, m_id: str) -> List[Dict]:
        """
        Retrieve grades for a specific module.
        
        Args:
            m_id (str): Module ID to get grades for
            
        Returns:
            List[Dict]: List of dictionaries containing student grades
            
        Raises:
            sqlite3.Error: If there's a database error
            ValueError: If module_id is invalid or empty
        """
        if not m_id or not isinstance(m_id, str):
            raise ValueError("Invalid module ID provided")

        try:

            query = """
                SELECT 
                    stu.s_id, 
                    stu.s_name, 
                    m.module_name AS m_title,
                    SUM(fg.final_grade * assign.t_per / 100) AS total_score
                FROM 
                    students stu
                JOIN 
                    final_grades fg ON stu.s_id = fg.s_id
                JOIN 
                    assignments assign ON fg.a_id = assign.a_id
                JOIN 
                    modules m ON assign.m_id = m.m_id
                WHERE 
                    assign.m_id = ?
                GROUP BY 
                    stu.s_id, stu.s_name, m.module_name
            """
            

            self.cursor.execute(query, (m_id,))
            all_records = self.cursor.fetchall()
            

            final_results = []
            for record in all_records:
                result_entry = {
                    's_id': record[0],
                    's_name': record[1],
                    'm_title': record[2],
                    'total_score': round(record[3], 2) if record[3] is not None else 0.0
                }
                final_results.append(result_entry)
            
            return final_results
            
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


def main():
    portal = GradePortal()
    cursor = portal.cursor

    cursor.executescript('''
        INSERT OR IGNORE INTO students (s_id, s_name, student_email, student_avatar, student_dob, student_balance) VALUES 
        ('S1', 'John Doe', 'john@example.com', 'avatar1.png', '1995-05-15', 500),
        ('S2', 'Jane Smith', 'jane@example.com', 'avatar2.png', '1997-08-22', 700),
        ('S3', 'Bob Wilson', 'bob@example.com', 'avatar3.png', '1998-03-12', 300);

        INSERT OR IGNORE INTO sections (section_id, section_name) VALUES 
        ('SEC1', 'Morning Session');

        INSERT OR IGNORE INTO modules (m_id, module_name, module_percent, section_id) VALUES 
        ('CS101', 'Introduction to Programming', 100, 'SEC1');

        INSERT OR IGNORE INTO assignments (a_id, m_id, t_type, t_per) VALUES 
        (1, 'CS101', 'homework', 30),
        (2, 'CS101', 'tests', 40),
        (3, 'CS101', 'projects', 30);

        INSERT OR IGNORE INTO quizzes (quiz_id, m_id, quiz_score) VALUES 
        (1, 'CS101', 85),
        (2, 'CS101', 90);

        INSERT OR IGNORE INTO attendance (attendance_id, s_id, m_id, status) VALUES 
        (1, 'S1', 'CS101', 'present'),
        (2, 'S2', 'CS101', 'present'),
        (3, 'S3', 'CS101', 'absent');

        INSERT OR IGNORE INTO final_grades (final_grades_id, s_id, a_id, final_grade) VALUES 
        (1, 'S1', 1, 85),
        (2, 'S1', 2, 92),
        (3, 'S1', 3, 88),
        (4, 'S2', 1, 90),
        (5, 'S2', 2, 85),
        (6, 'S2', 3, 95),
        (7, 'S3', 1, 78),
        (8, 'S3', 2, 88),
        (9, 'S3', 3, 84);
    ''')
    portal.conn.commit()

    # Generate grade report
    final_grades = portal.get_grades('CS101')

    print("\nStudent Grades:")
    for result in final_grades:
        print(f"{result['s_name']} ({result['s_id']}): {result['total_score']}%")

if __name__ == "__main__":
    main()