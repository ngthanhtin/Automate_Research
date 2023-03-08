Change name of all files in a directory using format:

`ls | cat -n | while read n f; do mv "$f" $(printf "%06d.png" "$n"); done`
