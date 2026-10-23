# SNAP Class

SNAP Class is a Streamlit attendance app for teachers and students. Teachers can
create classes, record attendance with face or voice recognition, and review
attendance summaries. Students can register with a face profile, enroll in
classes, and review their attendance.

## Features

### Teacher portal

- Register and sign in with a username and password.
- Create subjects with a subject code, name, and section.
- Share a class join link or QR code with students.
- Take attendance from classroom photos or a classroom audio recording.
- Review detected attendance and confirm or discard it before saving.
- View attendance records summarized by class session.

### Student portal

- Register a profile using the browser camera; recording a voice profile is
  optional.
- Sign in by presenting a registered face to the camera.
- Join a class by entering its subject code or opening a teacher's join link.
- View enrolled subjects and attendance totals, and unenroll from a subject.

## How it works

The app uses Streamlit for its interface and Supabase for persistent data.
Face profiles are generated with dlib and compared against registered student
profiles. Voice profiles and classroom audio are processed using Resemblyzer
and librosa. Teachers review the generated attendance results before the app
writes them to Supabase.

When a student opens a class join link, the app reads the `join-code` query
parameter and offers enrollment in the matching subject. The link and QR code
are generated from the deployed app URL and the subject code.

## Project structure

```text
.
├── app.py                              # Streamlit entry point and portal routing
├── requirements.txt                    # Python dependencies
└── src/
    ├── components/                     # Dialogs, cards, headers, and footers
    ├── database/
    │   ├── config.py                   # Supabase client configuration
    │   └── db.py                       # Database queries and writes
    ├── pipelines/
    │   ├── face_pipeline.py            # Face embeddings and attendance matching
    │   └── voice_pipeline.py           # Voice embeddings and speaker matching
    ├── screens/                        # Home, teacher, and student screens
    └── ui/                             # Shared layout and styles
```

## Requirements

- Python installed on your development machine.
- A Supabase project with the tables and columns described below.
- A browser with camera and microphone access for registration and attendance
  capture.

Python packages are listed in `requirements.txt`, including Streamlit,
Supabase, NumPy, pandas, dlib, scikit-learn, Pillow, librosa, Resemblyzer, and
Segno.

## Run locally

1. Clone the repository and open its root directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Configure the Supabase connection as described in the next section.
5. Start the app:

   ```bash
   streamlit run app.py
   ```

Streamlit prints a local URL in the terminal. Open it in a browser and allow
camera or microphone access when prompted.

## Supabase configuration

The app reads `SUPABASE_URL` and `SUPABASE_KEY` from Streamlit secrets or
environment variables. For local development, create
`.streamlit/secrets.toml` (this directory is ignored by Git) with your own
project values:

```toml
SUPABASE_URL = "https://<your-project-ref>.supabase.co"
SUPABASE_KEY = "<your-supabase-key>"
```

For another environment, set `SUPABASE_URL` and `SUPABASE_KEY` in that
environment's secret manager. Never commit real keys, passwords, access tokens,
student data, or biometric data to the repository. Configure Supabase access
policies and use credentials with only the permissions the app requires.

The code expects the following Supabase tables and fields:

| Table | Fields used by the app |
| --- | --- |
| `teachers` | `teacher_id`, `username`, `password`, `name` |
| `students` | `student_id`, `name`, `face_embedding`, `voice_embedding` |
| `subjects` | `subject_id`, `subject_code`, `name`, `section`, `teacher_id` |
| `subject_students` | `student_id`, `subject_id` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp`, `is_present` |

The application expects the ID fields to identify their corresponding records
and for the relationship fields to link the relevant tables. It stores teacher
passwords as bcrypt hashes. Student face and optional voice embeddings are
stored in the `students` table; attendance entries are stored in
`attendance_logs`. This repository does not include database migrations or a
complete Supabase schema, so configure the database to match the fields and
relationships expected by the queries in `src/database/db.py`.

## Deploy to Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository and choose
   `app.py` as the main file.
3. Add `SUPABASE_URL` and `SUPABASE_KEY` under the app's **Secrets** settings,
   using your own values and never putting them in source control.
4. Deploy and test student and teacher flows.
5. If students should open class links without signing in to Streamlit, set the
   app's visibility to public in its **Sharing** settings. A private app
   requires access to be granted to its viewers.

## Privacy and responsible use

This app processes face images, voice recordings, biometric embeddings, student
identifiers, and attendance records. Obtain appropriate consent before
collecting or using this information, restrict database and app access, and
define retention and deletion practices for your deployment. Do not use real
student or biometric data in development or demonstrations unless you have
authorization. AI-based identification can be inaccurate; teachers should
review attendance results before saving them.

## Limitations

- Face and voice matching are estimates and may produce false matches or miss
  students. Review results before confirming attendance.
- Voice attendance requires enrolled students to have voice profiles.
- The repository does not include database migrations, automated test
  instructions, or a sample dataset.
- A working Supabase project and valid configuration are required for
  registration, enrollment, and attendance storage.
