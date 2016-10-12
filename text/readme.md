Need to install xelatex, latexmk and biber

To compile run:
```
latexmk -xelatex -shell-escape main.py
```

This should take care of running biber. If not then run 
```
biber ./main.bcf
```

To clean the folder run 
```
latexmk -c
```

What happened to the build and aux folders? They didn't really work too well with latexmk so they were removed.
