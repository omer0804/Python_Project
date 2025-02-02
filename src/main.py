import subprocess
import os

def run_script(script_name):
    project_dir = os.path.dirname(os.path.dirname(__file__))
    venv_python = os.path.join(project_dir, '.venv', 'Scripts', 'python.exe')
    script_path = os.path.join(project_dir, 'src', script_name)
    try:
        subprocess.run([venv_python, script_path], check=True)
        print(f"{script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    run_script('data_cleaner.py')
    run_script('data_analysis.py')
    run_script('data_visualizer.py')