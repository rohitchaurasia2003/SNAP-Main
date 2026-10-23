from src.database.config import require_supabase
import bcrypt


def check_teacher_exists(username):
    client = require_supabase()
    response = client.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def create_teacher(username, password, name):
    client = require_supabase()
    data = { "username" : username, "password": hash_pass(password), "name": name}
    response = client.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    client = require_supabase()
    response = client.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    client = require_supabase()
    response = client.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    client = require_supabase()
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = client.table('students').insert(data).execute()
    return response.data

def create_subject(subject_code, name, section, teacher_id):
    client = require_supabase()
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = client.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    client = require_supabase()
    response = client.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    client = require_supabase()
    data = {'student_id': student_id, "subject_id": subject_id}
    response= client.table('subject_students').insert(data).execute()
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    client = require_supabase()
    response= client.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    client = require_supabase()
    response = client.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    client = require_supabase()
    response = client.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    client = require_supabase()
    response = client.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    client = require_supabase()
    response = client.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data