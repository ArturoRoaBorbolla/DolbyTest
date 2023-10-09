import subprocess

def generate_requirements_file():
    try:
        subprocess.check_call(['pipreqs', '.'])
        print("requirements.txt file has been generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements.txt: {e}")

def install_required_libraries():
    try:
        with open('requirements.txt') as f:
            libraries = f.read().splitlines()
            with open('pip_output.txt', 'w') as output_file:
                for lib in libraries:
                    try:
                        subprocess.check_call(['pip', 'install', lib])
                    except subprocess.CalledProcessError as e:
                        print(f"Error installing '{lib}': {e}\n")
                        output_file.write(f"Error installing '{lib}': {e}\n")
                output_file.write("All libraries have been successfully installed.")
        print("All libraries have been successfully installed.")
    except FileNotFoundError:
        print("The 'requirements.txt' file was not found. Make sure the file exists and contains the required libraries.")

generate_requirements_file()
install_required_libraries()
