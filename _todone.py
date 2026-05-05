todo_path = "."
todo_f = "__todo.todo.txt"

# ---------------------------------------
import os
import sys

def split_into_name_and_num(s):
  if len(s) == 0 or s[-1] != ")":
    return (s, 0)
  for i in range(len(s) - 2, -1, -1):
    if s[i] == "(":
      if s[i + 1] == "0":
        return (s, 0)
      try:
        num = int(s[i + 1:-1])
      except ValueError:
        return (s, 0)
      if num == 0:
        return (s, 0)
      return (s[:i], num)
  return (s, 0)

def rename_no_overwrite(f1, f2):
  num = 1
  while True:
    try:
      os.rename(f1, f2)
    except FileNotFoundError:
      return
    except FileExistsError:
      f2, num = split_into_name_and_num(f2)
      if num == 0:
        f2 += " (1)"
      else:
        f2 += f"({num + 1})"
      continue
    return

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
    rename_no_overwrite(proj_f, proj_f_done)

with open(todo_f, "w") as file:
  file.writelines(not_done_lines)

with open(done_f, "a") as file:
  file.writelines(done_lines)
