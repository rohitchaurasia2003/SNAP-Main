import bcrypt

from src.database.config import supabase


def _require_supabase():
    if supabase is None:
        raise RuntimeError(
            'Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets or environment variables.'
        )


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    _require_supabase()
    response = supabase.table('teachers').select('username').eq('username', username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    _require_supabase()
    data = {'username': username, 'password': hash_pass(password), 'name': name}
    response = supabase.table('teachers').insert(data).execute()
    return response.data


def teacher_login(username, password):
    _require_supabase()
    response = supabase.table('teachers').select('*').eq('username', username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    _require_supabase()
    response = supabase.table('students').select('*').execute()
    return response.data
