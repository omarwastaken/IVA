from modules.utils import speak, save_to_file, recognize_speech

# Define a function to create a to-do list
def create_tasks_list(restart_callback):
    speak("What are the tasks you want to add to the tasks list?")
    tasks = []
    while True:
        task = recognize_speech()
        if "stop" in task:
            break
        tasks.append(task)
    speak("Here's your tasks list:")
    for i, task in enumerate(tasks):
        speak(f" {i + 1}. {task};")
    if tasks is not None:
        save_to_file("task", "\n".join(tasks))
    restart_callback()