

# Define a function to create a to-do list
def create_todo_list():
    speak("What are the tasks you want to add to the to-do list?")
    tasks = []
    while True:
        task = recognize_speech()
        if "stop" in task:
            break
        tasks.append(task)
    speak("Here's your to-do list:")
    for i, task in enumerate(tasks):
        speak(f" {i + 1}. {task};")
    if tasks is not None:
        save_to_file("task", "\n".join(tasks))
    restart_main()