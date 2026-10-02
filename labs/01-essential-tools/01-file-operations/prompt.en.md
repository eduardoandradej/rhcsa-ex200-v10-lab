On `servera`, working as the `student` user, use the directory:

`/home/student/rhcsa-lab/obj01-01`

The `input` directory already contains the required files. Leave the final environment with the following state:

1. Create `workspace` with the `reports`, `images`, and `notes` subdirectories.
2. Copy all `report-*.txt` files from `input` to `workspace/reports`. The original files must remain in `input`.
3. Move all `image-*.jpg` files from `input` to `workspace/images`.
4. Move `input/notes-old.txt` to `workspace/notes/notes-final.txt`.
5. In `workspace/notes`, create three empty files: `note-1.txt`, `note-2.txt`, and `note-3.txt`.
6. Remove all `.tmp` files from `input`.
7. Do not modify the content of the provided files.

The grader checks the final system state, not the specific command used to reach it.
