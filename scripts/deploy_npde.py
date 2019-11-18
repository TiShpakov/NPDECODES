#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import tempfile
import zipfile
import shutil


def copy(file, indir, outdir):
    """
    Aggressively copy file to outdir. File can be a directory and can
    already exists.

    :param file: file (or directory) name
    :param indir: the directory which contains file
    :param outdir: the destination to where file copies to
    :return:
    """
    print("Moving '{}' to '{}'".format(indir + file, outdir + file))
    if file == "":
        shutil.copytree(indir, outdir)
        # Recursively copy an entire directory tree rooted at indir
        # to a directory named outdir and return the destination directory.
    elif file[-1] == "/":
        # if the solution needed to copy is a directory, delete the same directory in outdir (if has)
        # then use copytree to copy the directory
        try:
            shutil.rmtree(outdir + file)  # Delete an entire directory tree
        except:
            pass
        shutil.copytree(indir + file, outdir + file)
    else:
        # copy the file
        shutil.copy2(indir + file, outdir + file)
        """
        shutil.copy(src, dst, *, follow_symlinks=True)
        Copies the file scr to the file or directory dst. src and dst should be strings. If dst specifies a directory, 
        the file will be copied into dst using the base filename from src. Returns the path to the newly created file.
        """


def deploy(filename, indir, outdir, handle_unifdef, with_solution=False):
    """
    Parse a file trough "unifdef" and remove SOLUTIONS ifdef code blocks.
    Must have "unifdef" program. Can toggle if SOLUTIONS is true or false.

    :param filename:  e.g. "1dwaveabsorbingbc.cc"
    :param indir:     "../homeworks/1DWaveAbsorbingBC/mastersolution_tagged"
    :param outdir:    "../homeworks/1DWaveAbsorbingBC/templates"
    :param parse_unifdef: deal with #if ... block if true
    :param with_solution: keep block in #if SOLUTION if true
    :return:
    """
    # if is_cpp(indir + filename) or is_hpp(indir + filename):
    if handle_unifdef:
        cmd = ["unifdef"]
        # if with_internal:
        #     cmd.append("-DINTERNAL=1")
        # else:
        #     cmd.append("-DINTERNAL=0")
        if with_solution:
            cmd.append("-DSOLUTION=1")
        else:
            cmd.append("-DSOLUTION=0")

        cmd.append(indir + filename)

        print("Preparing " + outdir.split('/')[-2] + " for '{}'".format(filename))
        # print("Preparing templates/ for '{}'".format(filename))
        print(" ".join(cmd))

        f = open(outdir + filename, "w")
        subprocess.call(cmd, stdout=f)  # run the command described by cmd
        f.close()
    else:
        copy(filename, indir, outdir)


def mkdir(dir):
    """
    Aggressively create a directory if non existing.
    """
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def is_cpp(file):
    """
    Returns True if file looks like a C++ file (header of .cpp)
    """
    # return "cpp" == file.split(".")[-1]
    return file.split(".")[-1] in ["cpp", "cc", "c"]


def is_hpp(file):
    """
    Returns True if file looks like a C++ file (header of .cpp)
    """
    return file.split(".")[-1] in ["hpp", "h"]


def is_py(file_path):
    """
    :param file_path: the path of a file
    :return: true if file is a python file(ends with .py)
    """
    return file_path.split(".")[-1] == "py"


def is_cmake(file_path):
    """
    :param file_path: the path of a file
    :return: true if file with suffix .cmake
    """
    return file_path.split(".")[-1] == "cmake"


def generate_templates_and_mysolution(problem_dir):
    """
    First create templates and mysolution directory,
    then copy the files in "mastersolution_tagged" to them
    (remove "#if SOLUTION" block, that is, -DSOLUTION=0).
    Then create "mastersolution" directory, copy the files in "mastersolution_tagged" with the solution(-DSOLUTION=1)

    :param problem_dir: "../homeworks/problem_name/"
    """
    mkdir(problem_dir + "templates/")  # "../homeworks/problem_name/templates"
    mkdir(problem_dir + "mysolution/")
    mkdir(problem_dir + "mastersolution/")
    fileInMastersolution = os.listdir(problem_dir + 'mastersolution_tagged/')
    for file in fileInMastersolution:
        file_path = problem_dir + 'mastersolution_tagged/' + file
        if is_cpp(file_path) or is_hpp(file_path) or is_cmake(file_path) or is_py(file_path):
            handle_unifder = True
        else:
            handle_unifder = False
        deploy(file, problem_dir + 'mastersolution_tagged/', problem_dir + 'mastersolution/',
               handle_unifder, with_solution=True)
        deploy(file, problem_dir + 'mastersolution_tagged/', problem_dir + 'templates/',
               handle_unifder, with_solution=False)
        deploy(file, problem_dir + 'mastersolution_tagged/', problem_dir + 'mysolution/',
               handle_unifder, with_solution=False)


def parse_json(filename):
    """
    Parse a JSON description of the Assignment bundles.
    """
    this_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(this_dir)  # change the current working directory to this_dir

    f = open(filename, 'r')

    obj = json.load(f)

    assignment_dir = obj["assignment_dir"]  # "../Assignments/Codes"
    working_dir = obj["working_dir"]  # "./" current directory
    if not assignment_dir.endswith("/"):
        assignment_dir += "/"
    if not working_dir.endswith("/"):
        working_dir += "/"

    print("Looking for files in '{}'".format(assignment_dir))

    for problem in obj["Problems"]:
        # for every problem folder, rename the "mastersolution" to "mastersolution_tagged" (if not exists)
        problem_dir = assignment_dir + problem
        if not os.path.exists(problem_dir + "mastersolution_tagged"):
            os.rename(problem_dir + "mastersolution", problem_dir + "mastersolution_tagged")
        generate_templates_and_mysolution(problem_dir)


if __name__ == "__main__":
    try:
        subprocess.call(["unifdef", "--help"])
    except FileNotFoundError:
        print("You must install 'unifdef'.")
        exit(-1)

    parse_json("assignment_list.json")

