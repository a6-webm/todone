todo_path = "."
todo_f = "__todo.todo.txt"

# ---------------------------------------
import os
import sys


def wait_for_enter():
  print("<press enter to continue>")
  sys.stdout.flush()
  input()

def get_proj_f(line):
  for word in line.split():
    if word[0] == "+" and word[-3:] == ".md":
      return word[1:]
  return ""

todo_f = os.path.join(todo_path, todo_f)
done_dir = os.path.join(todo_path, "_done")
done_f = os.path.join(done_dir, "_done.txt")

os.makedirs(done_dir, exist_ok=True)

with open(todo_f, "r") as file:
  lines = file.readlines()

done_lines = []
not_done_lines = []
for line in lines:
  if line[0:2] == "x ":
    done_lines.append(line)
  else:
    not_done_lines.append(line)

for line in done_lines:
  proj_f = get_proj_f(line)
  if proj_f:
    proj_f_done = os.path.join(done_dir, proj_f)
    proj_f = os.path.join(todo_path, proj_f)
    try:
      os.rename(proj_f, proj_f_done)
    except e:
      print(e)
      wait_for_enter()

with open(todo_f, "w") as file:
  file.writelines(not_done_lines)

with open(done_f, "a") as file:
  file.writelines(done_lines)
