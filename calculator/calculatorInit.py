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
        self.cursor.execute('''
                SELECT stu.s_id, stu.s_name, fg.a_id, fg.final_grade, 
                    assign.t_type, assign.t_per, assign.m_id, 
                    m.module_name AS m_title,
                    q.quiz_score,
                    a.status as attendance_status,
                    s.section_name
                FROM students stu
                JOIN final_grades fg ON stu.s_id = fg.s_id
                JOIN assignments assign ON fg.a_id = assign.a_id 
                JOIN modules m ON assign.m_id = m.m_id
                JOIN sections s ON m.section_id = s.section_id
                LEFT JOIN quizzes q ON m.m_id = q.m_id
                LEFT JOIN attendance a ON (stu.s_id = a.s_id AND m.m_id = a.m_id)
                WHERE assign.m_id = \''''+m_id+'\'''')
        
        all_records = self.cursor.fetchall()
        
        s_dict = {}
        
        for record in all_records:
            s_id = record[0]
            s_name = record[1]
            a_id = record[2]
            final_grade = record[3]
            t_type = record[4]
            t_per = record[5]
            m_id = record[6]
            m_title = record[7]
            

            if s_id not in s_dict:
                s_dict[s_id] = {
                    's_name': s_name,
                    'scores': [],
                    'm_title': m_title
                }
            

            scores = s_dict[s_id]['scores']
            temp_scores = []
            for score in scores:
                temp_scores.append(score)
            temp_scores.append((t_type, t_per, final_grade))
            s_dict[s_id]['scores'] = temp_scores
        
        final_results = []
        
        student_ids = list(s_dict.keys())
        for s_id in student_ids:
            learner_data = s_dict[s_id]
            total_score = 0
            

            scores = learner_data['scores']
            for i in range(len(scores)):
                t_type, t_per, final_grade = scores[i]
                total_score += (final_grade * t_per / 100)
            

            result_entry = {
                's_id': s_id,
                's_name': learner_data['s_name'],
                'm_title': learner_data['m_title'],
                'total_score': round(total_score, 2)
            }
            final_results.append(result_entry)
        
        return final_results


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