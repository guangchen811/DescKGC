cd docs; sphinx-apidoc --module-first -f -o source ../AutoKGC; cd ..
cd docs; make clean; make html; cd ..
scp -r ./docs/build/* ecs-user@39.107.102.44:~/build