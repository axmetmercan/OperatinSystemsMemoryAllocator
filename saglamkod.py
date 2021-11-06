import sys


class MemoryPartition(object):
    def __init__(self):
        self.size_of_block = None
        self.isAllocated = False
        self.allocated_size = None
        self.has_new_next = False
        self.remaining_size = None
        self.index_of = None


class Procces(object):
    def __init__(self):
        self.size_of_process = None


def readfile(file_name):
    with open(file_name, "r") as file:
        Lines = file.readlines()
        processes = Lines[0].strip("\n").split(",")
        free_memory_spaces = Lines[1].strip("\n").split(",")

        processes = map(int, processes)
        processes = list(processes)

        free_memory_spaces = map(int, free_memory_spaces)
        free_memory_spaces = list(free_memory_spaces)

        return processes, free_memory_spaces


def first_fit(proc_list, mem_list):
    final = ""
    for proc in proc_list:
        for mem in mem_list:
            if (proc.size_of_process <= mem.size_of_block and mem.isAllocated != True):
                mem.allocated_size = proc.size_of_process
                mem.isAllocated = True
                mem.remaining_size = mem.size_of_block - proc.size_of_process
                if mem.remaining_size != 0:
                    new_mem = MemoryPartition()
                    new_mem.size_of_block = mem.remaining_size
                    index_mem = mem_list.index(mem)
                    # print(index_mem)
                    mem_list.insert(index_mem + 1, new_mem)
                break

        output = str(proc.size_of_process) + " => "
        for mem in mem_list:
            if (mem.isAllocated):
                output = output + str(mem.allocated_size) + "* "
            else:
                output = output + str(mem.size_of_block) + " "
            # print(mem.size_of_block, end=" | ")
        output += "\n"
        final += output
    return final


def best_fit(proc_list, mem_list, ):
    final = ""
    for proc in proc_list:
        initial_available_memory_size = sys.maxsize
        initial_available_memory_index = None
        for mem in mem_list:
            if mem.size_of_block >= proc.size_of_process and mem.isAllocated != True:
                if mem.size_of_block < initial_available_memory_size:
                    initial_available_memory_size = mem.size_of_block
                    initial_available_memory_index = mem_list.index(mem)

        if initial_available_memory_index:
            mem = mem_list[initial_available_memory_index]
            mem.allocated_size = proc.size_of_process
            mem.isAllocated = True
            mem.remaining_size = mem.size_of_block - proc.size_of_process
            if mem.remaining_size != 0:
                new_mem = MemoryPartition()
                new_mem.size_of_block = mem.remaining_size
                index_mem = mem_list.index(mem)
                mem_list.insert(index_mem + 1, new_mem)

        # break
        output = str(proc.size_of_process) + " => "
        for mem in mem_list:
            if (mem.isAllocated):
                output = output + str(mem.allocated_size) + "* "
            else:
                output = output + str(mem.size_of_block) + " "
            # print(mem.size_of_block, end=" | ")
        output += "\n"
        final += output
    return final


def worst_fit(proc_list, mem_list):
    final = ""
    error = ""
    for proc in proc_list:
        initial_available_memory_size = - sys.maxsize - 1
        initial_available_memory_index = None
        for mem in mem_list:
            if mem.size_of_block >= proc.size_of_process and mem.isAllocated != True:
                if mem.size_of_block >= initial_available_memory_size:
                    initial_available_memory_size = mem.size_of_block
                    initial_available_memory_index = mem_list.index(mem)

        # print(initial_available_memory_index)
        if initial_available_memory_index != None:
            mem = mem_list[initial_available_memory_index]
            mem.allocated_size = proc.size_of_process
            mem.isAllocated = True
            mem.remaining_size = mem.size_of_block - proc.size_of_process
            if mem.remaining_size != 0:
                new_mem = MemoryPartition()
                new_mem.size_of_block = mem.remaining_size
                index_mem = mem_list.index(mem)
                mem_list.insert(index_mem + 1, new_mem)
        else:
            error = ("not allocated  must wait")

        # break
        output = str(proc.size_of_process) + " => " + error
        if "not allocated  must wait" not in output:
            for mem in mem_list:
                if (mem.isAllocated):
                    output = output + str(mem.allocated_size) + "* "
                else:
                    output = output + str(mem.size_of_block) + " "

        output += "\n"
        final += output
    print(final)
    return final


def append_mem_list():
    memory = []
    for i in readfile("memory.txt")[0]:
        mem_block = MemoryPartition()
        mem_block.size_of_block = i
        mem_block.index_of = readfile("memory.txt")[0].index(i)
        memory.append(mem_block)
    return memory


def append_poc_list():
    processes_list = []
    for i in readfile("memory.txt")[1]:
        process = Procces()
        process.size_of_process = i
        processes_list.append(process)
    return processes_list


if __name__ == '__main__':

    first_fit(append_poc_list(), append_mem_list())
    best_fit(append_poc_list(), append_mem_list())
    worst_fit(append_poc_list(), append_mem_list())
    with open("output.txt", "w") as output_file:
        output_file.write(
            "First-Fit Memory Allocation\n-----------------------------------------------------------------------------------------------\nstart  => ")
        for mem in append_mem_list():
            output_file.write(str(mem.size_of_block) + " ")
        output_file.write("\n")
        output_file.write(first_fit(append_poc_list(), append_mem_list()))

        output_file.write(
            "Best-Fit Memory Allocation\n-----------------------------------------------------------------------------------------------\nstart  => ")
        for mem in append_mem_list():
            output_file.write(str(mem.size_of_block) + " ")
        output_file.write("\n")
        output_file.write(best_fit(append_poc_list(), append_mem_list()))

        output_file.write(
            "Worst-Fit Memory Allocation\n-----------------------------------------------------------------------------------------------\nstart  => ")
        for mem in append_mem_list():
            output_file.write(str(mem.size_of_block) + " ")
        output_file.write("\n")
        output_file.write(worst_fit(append_poc_list(), append_mem_list()))
