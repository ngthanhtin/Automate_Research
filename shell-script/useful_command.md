Change name of all files in a directory using format:

```ls | cat -n | while read n f; do mv "$f" $(printf "%06d.png" "$n"); done```

o find several files (in the example, PNG images) with specific name format and do whatever you want to do with them (in the example, convert them to JPG images), use the following example which uses command line tool find:

```find . -type f -name "*.png" -not -name "*heatmaps.png" -print | while read f; do
  mogrify -format jpg $f
done
```

Delete folders inside the path which name includes name_desired:

```rm -rf `find . -maxdepth <num> -type d -name "<name_desired>"`
```
