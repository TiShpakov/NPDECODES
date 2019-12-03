# NPDECODES

## General Remarks

* Below, the directory `.` refers to the top level directory of the repository.
* Developers only work in `./developers/<ProblemName>/`. From this, a corresponding directory `./homeworks/<ProblemName>/` for the students can be created automatically using `./scripts/deploy_npde.py`.
* Not only the solutions, but also the corresponding templates need to compile and run without crash. So be careful when setting the solution/template tags in `developers/mastersolution/`.
* The bullets below are only a selection. If you spot additional issues, e.g. ugly or too complicated code, fix it.
* Names of .cc and .h files: For example the files in the folder `./developers/MyHomeworkProblem/mastersolution/` should be called `myhomeworkproblem_main.cc`, `myhomeworkproblem_foo.cc`, `myhomeworkproblem_foo.h`, where foo is a placeholder for any name (summarized: lowercase, split words by _).
* Only in Lehrfem exercises: Use `nostd::span` (C++20) instead of `ForwardIteraters` for iterating over objects contiguous in memory (used e.g. in `Mesh::Entities()`, `SubEntities()`, `DofHandler`).

## Polishing

* Add comments if necessary.
* Only use the `#includes "..."` you need, e.g. for `Eigen::MatrixXd`, `#include "Eigen/Core"` is sufficient (no `#include "Eigen/Dense"` needed). Likewise for the `CMakeLists.txt`: Import/Link only what you need.
* Make the code follow the Google style (see https://google.github.io/styleguide/cppguide.html). In particular, respect the include order (https://google.github.io/styleguide/cppguide.html#Names_and_Order_of_Includes).
* Never store data in the remote repository that is generated by the code anyway (e.g. figures). The repo should only contain source files (and maybe some mesh files).
* Provide unit tests for all functions that the students have to change. If this is not possible for some reason, then point this out in the README.md of the exercise.
* Plotting is done as follows: The C++ code only stores the data in a .csv file (using `std::ofstream`). The plotting is then done by a python script that reads this .csv file. See e.g. BurgersEquation. In particular, remove all the MathGL code.

## Homework Problems

### Setting Up a Homework Problem

Only work in `./developers/<ProblemName>/`. This folder needs to contain at least:
* `CMakeLists.txt` (same for every problem, so just copy-paste it from another problem)
* `mastersolution/` (contains you code, with tags as described below)
* `mastersolution/dependencies.cmake` (contains the info needed by the build system, just mimic the ones from other problems)
Every problem should contain unit test in the directory `mastersolution/test/` containing the following two files:
* `problemname_test.cc` (contains the unit tests for your code)
* `dependencies.cmake` (contains the info needed by the build system, just mimic the ones from other test directories)
In addition, if a problem needs to load meshes, we put them in the folder `./developers/<ProblemName>/meshes/`. Finally, the line `add_subdirectory(<ProblemName>)` has to be added in `./developers/CMakeLists.txt`.

### Solution Tags

In the files of `./developers/mastersolution/` we put the following tags
```
#if SOLUTION
  <only in mastersolution>
#else
  <only in template>
#endif
```
to indicate what belongs to mastersolution and/or template. Based on these tags, the file `./scripts/deploy_npde.py` generates a directory `./homeworks/<ProblemName>/` containg the directories `mastersolution`, `mysolution`, `temaplates` with the corresponding content. The students work exclusively in `./homeworks/<ProblemName>/`.

## TODO

* `BoundaryWave`: mysolution has core dump
* `CoupledSecondOrderBVP`: needs tests and tags
* `ElementMatrixComputation`: unit tests all pass even for template
* `IncidenceMatrices`: wrong file structure and mysolution has core dump
* `LaxWendroffScheme`: unit test of mastersolution takes too long
* `OutputImpedanceBVP`: unit test of mysolution has infinite loop
* `PointEvaluationRhs`: bad includes
* `ProjectionOntoGradients`: completely messed up
* `RadauThreeTimestepping`: mysolution has core dump (and mastersolution takes very long)
* `SDIRKMethodOfLines`: mysolution has core dump
* `SimpleLinearFiniteElements`: bad names of files and classes

## New Problems

Problems PDF: https://www.sam.math.ethz.ch/~grsam/NUMPDE/HOMEWORK/NPDEProblems.pdf

* Problem 4.1: Finite Volumes with Robin Boundary Conditions
* Problem 5.6: Parametric Finite Elements
* Problem 5.7: Stable Evaluation at a Point
* Problem 5.8: Trace Error Estimates **(done already?)**
* Problem 6.6: Non-linear Schrödinger Equation with Cubic Non-Linearity **(Oliver)**
* Problem 7.3: Upwind Quadrature
* Problem 7.4: Exponentially fitted upwind scheme
* Problem 7.5: Transport Problem
* Problem 7.6: Upwind Finite Volume Method 
