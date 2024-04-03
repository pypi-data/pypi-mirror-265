import os

def ConvertJavaToJar(javafile):
    # Compile Java file to JAR
    #Remember not to remove any generated files
    print(f"Converting {javafile}.java to {javafile}.jar ...")
    compilation_result = os.system(f"javac {javafile}.java")

    
    if compilation_result == 0:
        os.system(f"jar cfe {javafile}.jar Main {javafile}.class")
    else:
        print("Compilation process failed. Please check your Java file for errors.")

while True:
    # Prompt user for the name of the Java file
    javafile = input("Enter the name of the Java file (not including extension, just the name): ")
    
    # Check if the Java file exists
    if os.path.exists(f"{javafile}.java"):
        ConvertJavaToJar(javafile)
    else:
        print("File not found. Please make sure the file exists.")
