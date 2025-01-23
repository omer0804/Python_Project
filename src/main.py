import subprocess
import os

def run_script(script_name):
    venv_python = os.path.join('C:\\Users\\USER\\Desktop\\Advanced Python Course\\Python Project\\.venv\\Scripts\\python.exe')
    script_path = os.path.join('C:\\Users\\USER\\Desktop\\Advanced Python Course\\Python Project\\src', script_name)
    try:
        subprocess.run([venv_python, script_path], check=True)
        print(f"{script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    run_script('data_cleaner.py')
    run_script('data_analysis.py')
    run_script('data_visualizer.py')