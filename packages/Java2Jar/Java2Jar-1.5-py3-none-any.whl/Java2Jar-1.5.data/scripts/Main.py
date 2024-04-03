import os
import subprocess

def ConvertJavaToJar(javafile):
    # Compile Java file to JAR
    print(f"Converting {javafile}.java to {javafile}.jar ...")
    compilation_result = subprocess.run(["javac", f"{javafile}.java"], capture_output=True, text=True)

    if compilation_result.returncode == 0:
        jar_result = subprocess.run(["jar", "cfe", f"{javafile}.jar", "Main", f"{javafile}.class"], capture_output=True, text=True)
        if jar_result.returncode == 0:
            print("Conversion completed successfully.")
        else:
            print("Error occurred while creating JAR file.")
            print(jar_result.stderr)
    else:
        print("Compilation process failed. Please check your Java file for errors.")
        print(compilation_result.stderr)

while True:
    # Prompt user for the name of the Java file
    javafile = input("Enter the name of the Java file (not including extension, just the name): ")
    
    # Check if the Java file exists
    if os.path.exists(f"{javafile}.java"):
        ConvertJavaToJar(javafile)
    else:
        print("File not found. Please make sure the file exists.")