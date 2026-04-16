import os
import subprocess

SCRIPTS_DIR = 'scripts'

def main():
    scripts = sorted(
        f for f in os.listdir(SCRIPTS_DIR)
        if f.endswith('.py')
    )

    for script in scripts:
        script_path = os.path.join(SCRIPTS_DIR, script)
        print(f'Running {script_path}...')

        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        if result.stderr:
            print(f'Error in {script}:\n{result.stderr}')

        if result.returncode != 0:
            print(f'{script} failed. Stopping execution.')
            break

if __name__ == '__main__':
    main()