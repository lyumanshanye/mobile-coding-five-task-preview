const tasks = [{ taskId: 1, title: "Prepare" }];

function findTask(taskId) {
  return tasks.find(task => task.taskId === taskId);
}

console.log(findTask(1));
