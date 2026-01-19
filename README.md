Matrix Calculator 

This application is used to perform matrix and linear algebra calculations
in a simple and structured way.
The main purpose of this application is to provide calculation features for:

matrix operations
vector operations
system of linear equations (SPL)

through an interactive graphical user interface.

This application focuses on separating user interface, calculation logic,
and application state to make the code easier to understand and maintain.

------------------------------------------------------------

How to use this application

Before using this application, make sure you already have:
- Python 3.10 or above
- NumPy
- PyQt5

You need to install the required libraries before running the application.
All calculations are performed locally and do not require an internet connection.

After that, you can start using the calculator through the GUI.
You can select the type of calculation, matrix size, and input values
based on your needs.

Each calculation process consists of:
- operation type   -> matrix / vector / SPL
- input            -> numerical values entered by user
- computation      -> processed using NumPy
- output           -> result displayed on the screen

------------------------------------------------------------

Matrix Operations

The application supports the following matrix operations:

matrix addition
matrix subtraction
matrix multiplication
matrix transpose
matrix determinant
matrix inverse (if applicable)

------------------------------------------------------------

Vector Operations

The application also provides basic vector calculations, including:

vector addition
vector subtraction
scalar multiplication
basic vector computation

------------------------------------------------------------

System of Linear Equations (SPL)

For SPL calculations, the application allows users to:

input coefficient matrix
input constant vector
solve the system using matrix-based methods
identify solution type (unique, infinite, or no solution)

------------------------------------------------------------

Running the Application

Step 1
Install required dependencies:

pip install numpy PyQt5

------------------------------------------------------------

Step 2
Run the application from the project directory:

python core/app.py

The application window will open automatically.

------------------------------------------------------------

Application Execution (GUI)

Step 3
Using the graphical interface, you can:
- choose calculation category
- input matrix or vector values
- execute calculation
- view results instantly

All interactions are handled through the GUI
and no command-line input is required after the application starts.

------------------------------------------------------------

Calculation Behavior

- all calculations are performed using NumPy
- invalid matrix dimensions are rejected
- determinant and inverse are restricted to valid matrices
- SPL solutions are classified as:
  - unique solution
  - infinite solutions
  - no solution
- user input is treated as runtime data and not stored permanently

------------------------------------------------------------

Project Purpose

This project is part of the Linear Algebra / Programming course.
The implementation is intended to help students understand:
- matrix and vector computation
- system of linear equations
- numerical computation using Python
- GUI-based application development

------------------------------------------------------------

Author

Devi Maulani
D4 Teknik Informatika
Politeknik Negeri Bandung

------------------------------------------------------------

License

This project is licensed for educational and non-commercial use.
You are allowed to use, modify, and develop this project further
for learning purposes.

If this project is reused, modified, or developed further,
please include proper attribution by citing the original author
and this repository as the source.

------------------------------------------------------------

Warning

This project is developed for educational purposes only.
All features provided in this application are simplified versions
of real mathematical tools. 
