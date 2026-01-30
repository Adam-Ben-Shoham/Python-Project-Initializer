from project_orchestrator import ProjectOrchestrator
import os

# 1. Setup your test data
# Make sure these paths are correct for YOUR computer!
test_input = {
    'project_name': 'Meitar',
    'root_dir': r"C:\Users\mada2\Desktop",  # Use an 'r' before the string for Windows paths
    'ide_choice': 'PyCharm',
    'py_interpreter': r'C:\Users\mada2\AppData\Local\Programs\Python\Python312\python.exe',  # Path to your global python.exe
    'ide_path': r'C:\Program Files\JetBrains\PyCharm 2025.2.3\bin\pycharm64.exe',
    'init_git': True,
    'project_type': 'Automation',
    'install_libs': True
}


def run_test():
    print("🚀 Starting Project Creation Test...")

    try:
        # Initialize the Orchestrator
        orchestrator = ProjectOrchestrator(test_input)

        # Run the build
        orchestrator.create_project()

        print("\n✨ TEST SUCCESSFUL!")
        print(f"Project created at: {orchestrator.final_path}")

    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {e}")


if __name__ == "__main__":
    run_test()