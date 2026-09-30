import { useEffect, useState } from "react"

function App() {

  const [task, setTask] = useState("")
  const [tasks, setTasks] = useState([])


  // GET TASKS
  useEffect(() => {

    fetch("http://127.0.0.1:8000/tasks")
      .then((response) => response.json())
      .then((data) => {
        setTasks(data)
      })

  }, [])


  // ADD TASK
  async function addTask() {

    if (task.trim() === "") {
      return
    }

    const response = await fetch(
      "http://127.0.0.1:8000/tasks",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          name: task
        })
      }
    )

    const newTask = await response.json()

    setTasks([...tasks, newTask])

    setTask("")
  }


  // COMPLETE TASK
  async function completeTask(id) {

    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${id}`,
      {
        method: "PUT"
      }
    )

    const updatedTask = await response.json()

    setTasks(
      tasks.map((item) =>
        item.id === id ? updatedTask : item
      )
    )
  }


  // DELETE TASK
  async function deleteTask(id) {

    await fetch(
      `http://127.0.0.1:8000/tasks/${id}`,
      {
        method: "DELETE"
      }
    )

    setTasks(
      tasks.filter((item) => item.id !== id)
    )
  }


  return (

    <div>

      <h1>Task Manager</h1>

      <input
        type="text"
        placeholder="Enter your task"
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />

      <button onClick={addTask}>
        Add Task
      </button>


      <h2>My Tasks</h2>


      {tasks.map((item) => (

        <div key={item.id}>

          <span
            style={{
              textDecoration:
                item.completed
                  ? "line-through"
                  : "none"
            }}
          >

            {item.name}

          </span>


          <button
            onClick={() =>
              completeTask(item.id)
            }
          >

            {item.completed
              ? "Undo"
              : "Complete"}

          </button>


          <button
            onClick={() =>
              deleteTask(item.id)
            }
          >

            Delete

          </button>

        </div>

      ))}

    </div>

  )
}

export default App