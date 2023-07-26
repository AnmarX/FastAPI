import subprocess

# List of shell scripts to run
scripts_to_run = [
    "./script1.sh",
    "./script2.sh",
    "./script3.sh",
    # Add more scripts as needed
]

def run_shell_script(script_path):
    try:
        subprocess.run(script_path, shell=True, check=True)
        print(f"Script {script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running script {script_path}. Return code: {e.returncode}")
        # Optionally, you can handle the error or perform other actions here

def main():
    for script in scripts_to_run:
        run_shell_script(script)

if __name__ == "__main__":
    main()
