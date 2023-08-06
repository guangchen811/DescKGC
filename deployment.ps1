# Change directory to 'docs' folder and generate Sphinx API documentation for AutoKGC
Set-Location "docs"
sphinx-apidoc --module-first -f -o source ..\AutoKGC
Set-Location ".."

# Change directory to 'docs' folder, clean the previous build, and create HTML documentation
Set-Location "docs"
./make.bat clean
./make.bat html
Set-Location ".."

# Copy the contents of the 'docs/build' folder to the remote server using SCP
scp -r .\docs\build\* ecs-user@39.107.102.44:~/build