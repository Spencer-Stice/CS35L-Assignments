#!/usr/local/cs/bin/python3
import os
import zlib

#Create empty lists to use later
branch_list = []
branch_names = []
sorted_commits = []
CNS = []
commit_stack = []
commit_stack_children = []
unsorted_commits = []
unsorted_commits_parents = []
unsorted_commits_children = []
unsorted_commits_children_marks = []

#Create the CommitNode class
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        self.temp = 0
        self.perm = 0
    def addParent(self, parent_hash):
        self.parents.add(parent_hash)
    def addChild(self, child_hash):
        self.children.add(child_hash)
    def giveTemp(self):
        self.temp = 1
    def givePerm(self):
        self.perm = 1
    def removeTemp(self):
        self.temp = 0
    def removePerm(self):
        self.perm = 0

#Create function to create a new instance of the CommitNode class when called
#Also sets the parents and children properly
def createCNs(current_hash):

    check = 1
    if(len(CNS) > 0):
        for i in range(len(CNS)):
            if CNS[i].commit_hash == current_hash:
                check = 0
                
    #Add commit node to CNS if not already present
    if(check):
        CNS.append(CommitNode(current_hash))
        unsorted_commits.append(current_hash)
        unsorted_commits_parents.append([])
        unsorted_commits_children.append([])
        unsorted_commits_children_marks.append([])

    #Read contents of current node to find parents
    current_length = len(CNS)
    first_chars = current_hash[:2]
    curobj_filepath = os.path.abspath(os.path.join(objs_directory, first_chars))
    curobj_filepath = os.path.abspath(os.path.join(curobj_filepath, current_hash[2:40]))    
    compressed_contents = open(curobj_filepath, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    decompressed_contents = decompressed_contents.decode("utf-8")
    
    #Add parents to current node
    if check == 1:
        while (decompressed_contents.find('parent') != -1):
            parent_index = decompressed_contents.find("parent");
            parent_hash = decompressed_contents[parent_index+7:parent_index+47]
            if check == 1:
                CNS[current_length - 1].addParent(parent_hash)
                unsorted_commits_parents[current_length - 1].append(parent_hash)
            else:
                for i in range(len(CNS)):
                    if CNS[i].commit_hash == current_hash:
                        CNS[i].addParent(parent_hash)
                        unsorted_commits_parents[i].append(parent_hash)

    #Add newly discovered commits to stack with their children
            commit_stack.append(parent_hash)
            commit_stack_children.append([])

            for i in range(len(commit_stack)):
                if commit_stack[i] == parent_hash:
                    commit_stack_children[i].append(current_hash)
            for i in range(len(unsorted_commits)):
                if unsorted_commits[i] == parent_hash:
                    unsorted_commits_children[i].append(current_hash)
                    unsorted_commits_children_marks[i].append(0)
                        
            decompressed_contents = decompressed_contents[parent_index+47:]
    for i in reversed(range(len(commit_stack))):
        if commit_stack[i] == current_hash:
            for j in range(len(commit_stack_children[i])):
                for p in range(len(CNS)):
                    if CNS[p].commit_hash == current_hash:
                        CNS[p].addChild(commit_stack_children[i][j])
                    for p in range(len(unsorted_commits)):
                        if unsorted_commits[p] == current_hash:
                            unsorted_commits_children[p].append(commit_stack_children[i][j])
                            unsorted_commits_children_marks[p].append(0)
            commit_stack.remove(commit_stack[i])
            commit_stack_children.remove(commit_stack_children[i])


#Sort topologically by Kahn's algorithm  
def visit():
    while len(no_edge) > 0:
        n = no_edge[0]
        cur_l = len(sorted_commits)
        for b in range(len(CNS)):
            if CNS[b].commit_hash == n:
                this_one = CNS[b]
        if(len(sorted_commits) > 0):
            sorted_commits.append(this_one)
        else:
            if len(sorted_commits) == 0:
                sorted_commits.append(this_one)
        uo = len(unsorted_commits)
        no_edge.remove(n)
        for a in range(uo):
            if unsorted_commits[a] == n:
                for p in range(len(unsorted_commits_parents[a])):
                    for q in range(len(unsorted_commits)):
                        if unsorted_commits[q] == unsorted_commits_parents[a][p]:
                            done = 1
                            if len(unsorted_commits_children[q]) > 0:
                                for c in range(len(unsorted_commits_children[q])):
                                    if unsorted_commits_children[q][c] == n:
                                        unsorted_commits_children_marks[q][c] = 1
                                for r in range(len(unsorted_commits_children_marks[q])):
                                    if unsorted_commits_children_marks[q][r] == 0:
                                        done = 0
                                        
                            if done == 1:
                                no_edge.append(unsorted_commits[q])

                            
    
    



#Discover the .git directory
current_path = os.getcwd()
git_directory = ""
while True:
    if current_path != '/':
        git_path = current_path + "/.git"
    else:
        git_path = '/.git'
    found = os.path.isdir(git_path)
    if found:
        git_directory = git_path
        break
    elif git_path == '/.git':
        print("Not inside a Git repository")
        exit(1)
    current_path = os.path.join(current_path, os.pardir)
    current_path = os.path.abspath(current_path)
refs_directory = git_directory + '/refs/heads/'
objs_directory = git_directory + '/objects/'
path, dirs, files = next(os.walk(refs_directory))

    
    #Go through each branch and recursively add commit objects
for f in files:
    ref_filepath = os.path.abspath(os.path.join(refs_directory, f))
    ref_hash = open(ref_filepath, 'r').read()
    createCNs(ref_hash[:40])
    while len(commit_stack) > 0:
        c_len = len(commit_stack)
        createCNs(commit_stack[c_len - 1])
    branch_list.append(ref_hash[:40])
    branch_names.append(f)

if len(dirs) > 0:
    for a in dirs:
        new_path = os.path.abspath(os.path.join(refs_directory, a))
        npath, ndirs, nfiles = next(os.walk(new_path))
        for nfile in nfiles:
            ref_filepath = os.path.abspath(os.path.join(new_path, nfile))
            ref_hash = open(ref_filepath, 'r').read()
            createCNs(ref_hash[:40])
            while len(commit_stack) > 0:
                c_len = len(commit_stack)
                createCNs(commit_stack[c_len - 1])
            branch_list.append(ref_hash[:40])
            branch_names.append(a + "/" + nfile)


#Perform topological sort
#Generate list of nodes with no children
no_edge = []
for i in range(len(branch_list)):
    for m in range(len(unsorted_commits)):
        if branch_list[i] == unsorted_commits[m]:
            test = 1
            if len(unsorted_commits_children[m]) == 0:
                for w in range(len(no_edge)):
                    if no_edge[w] == branch_list[i]:
                        test = 0
                if test == 1:
                    no_edge.append(branch_list[i])

visit()
brlm = []
for a in range(len(branch_list)):
    brlm.append(0)
    
        
#Print the results according to the spec
printed_end = 0


for i in range(len(sorted_commits)):
    next_is_parent = 0
    is_a_branch = 0
    branches_here = []
    if i != len(sorted_commits) - 1:
        for a in sorted_commits[i].parents:
            if a == sorted_commits[i + 1].commit_hash:
                next_is_parent = 1
    else:
        next_is_parent = 1
    for j in range(len(branch_list)):
        if sorted_commits[i].commit_hash == branch_list[j]:
            is_a_branch = 1
            branches_here.append(branch_names[j])
    branches_here.sort()
        
    if printed_end == 1:
        if len(sorted_commits[i].children) > 0:
            print_string = "="
            print_string2 = ""
            for g in sorted_commits[i].children:
                print_string2 = print_string2 + g + " "
            final_p = print_string + print_string2
            print(final_p[:-1])
        else:
            print('=')

    if(next_is_parent == 1 and is_a_branch == 0):
        print(sorted_commits[i].commit_hash)
        printed_end = 0
    elif(next_is_parent == 1 and is_a_branch == 1):
        print_string = sorted_commits[i].commit_hash
        #MAKE THIS ORDER RIGHT
        for o in branches_here:
            print_string = print_string + " " + o
        print(print_string)
        printed_end = 0
    elif(next_is_parent == 0 and is_a_branch == 0):
        print(sorted_commits[i].commit_hash)
        print_string = "="
        print_string2 = ""
        #MAKE THIS ORDER RIGHT
        for o in sorted_commits[i].parents:
            print_string2 = print_string2 + o + " "
        print_string2 = print_string2[:-1]
        ps = print_string2 + print_string
        print(ps)
        print()
        printed_end = 1
    else:
        print_string = sorted_commits[i].commit_hash
        #MAKE THIS ORDER RIGHT
        for o in branches_here:
            print_string = print_string + " " + o
        print(print_string)
        print_string = "="
        print_string2 = ""
        #MAKE THIS ORDER RIGHT
        for o in sorted_commits[i].parents:
            print_string2 = print_string2 + o + " "
        print_string2 = print_string2[:-1]
        ps = print_string2 + print_string
        print(ps)
        print()
        printed_end = 1

#I ensured that this script doesn't use any commands outside of python by comparing the strace output
#of this script with a script that uses os.system to run a shell command
#I found that the other script's strace has the trace execve where it calls the shell whereas the only
#execve I found for this script was the first one to run the script. Therefore, this script doesnt execute
#any non-Python commands
