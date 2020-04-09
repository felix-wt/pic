import numpy as np
import time
from collections import Counter
import sys   
sys.setrecursionlimit(10000)

## 图-邻接表：读取txt中的边的连接情况数据进行邻接表的创建
class graph_table(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.node_list = None
        self.adj_list = None
    def construction(self):
        edge_connection = self.extract_data(self.file_name)   # N * 2 numpy ndarray
        self.node_list = np.unique(edge_connection)  # N,  node_list存储所有(不重复)的node id
        self.adj_list = [[] for i in range(len(self.node_list))]  # 为每个node都创建一个单独的list,它们都存储在大的list中
        for i in range(edge_connection.shape[0]):
            self.adj_list[np.argwhere(self.node_list == edge_connection[i, 0]).item()] \
                .append(np.argwhere(self.node_list == edge_connection[i, 1]).item())  # 邻接表中存放可达node在node_list中的索引值

    def graph_loop_adjmatrix(self, start:int, visited:list, absolute_visited:list, loop_set, current_sequence):
        current_sequence = np.append(current_sequence, self.node_list[start])   ## start, source：从0开始的序号(是self.node_list的索引值)
        visited[start], absolute_visited[start] = 1, 1
        for i in range(len(self.adj_list[start])):
            if visited[self.adj_list[start][i]] != 0:
                possible_loop = current_sequence[np.argwhere(current_sequence == \
                    self.node_list[self.adj_list[start][i]]).item():current_sequence.shape[0]]
                if len(possible_loop) > 2 and len(possible_loop) < 8:         # 发现闭环
                    current_sequence_tmp = self.bit_move(possible_loop, np.argwhere(possible_loop == min(possible_loop)).item())  # 将loop中最小的数循环移动到最前面
                    loop_set.append(tuple(current_sequence_tmp))
            elif visited[self.adj_list[start][i]] == 0:   # 未发现闭环则遍历start为起点的可达节点
                loop_set, current_sequence, visited, _ = self.graph_loop_adjmatrix(self.adj_list[start][i], visited, absolute_visited, loop_set, current_sequence)
            if i < len(self.adj_list[start]) - 1:
                j = np.argwhere(current_sequence == self.node_list[start]).item()
                for k in range(j + 1, current_sequence.shape[0]):
                    visited[np.argwhere(self.node_list == current_sequence[k]).item()] = 0
                current_sequence = np.delete(current_sequence, [m for m in range(j + 1, current_sequence.shape[0])])
        return loop_set, current_sequence, visited, absolute_visited

    @staticmethod
    def extract_data(file_name:str):
        data_np = np.loadtxt(file_name, delimiter=',', dtype='long')
        id_data = np.asarray(data_np[:,0:2])
        id_one_dim = id_data.flatten()
        id_numbers = dict(Counter(id_one_dim))
        id_of_onetimes = []
        for i, data_i in enumerate(id_data):
            if id_numbers.get(data_i[0]) == 1 or  id_numbers.get(data_i[1]) == 1 :
                id_of_onetimes.append(i)
        extracted_id = np.delete(id_data, id_of_onetimes, 0)
        return extracted_id

    @staticmethod
    def bubble_length_first(sequence:list):
        for i in range(len(sequence) - 1):
            for j in range(len(sequence) - i - 1):
                if len(sequence[j]) > len(sequence[j + 1]):
                    sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]
                if len(sequence[j]) == len(sequence[j + 1]):
                    for k in range(len(sequence[j])):
                        if sequence[j][k] < sequence[j + 1][k]:
                            break
                        elif sequence[j][k] == sequence[j + 1][k]:
                            continue
                        else:
                            sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]
                            break
        return sequence

    @staticmethod
    def process_save_result(loop, file_name):
        exam_res_list = list([])
        for i in loop:
            i = str(i).replace(")", '')
            i = str(i).replace("(", '')
            i = str(i).replace(" ", '')
            exam_res_list.append(i)
        loop = exam_res_list.insert(0, len(loop))
        file = open(file_name,'w')
        file.truncate()
        for var in exam_res_list:
            file.writelines(str(var))
            file.write('\n')
        file.close()

    @staticmethod
    def bit_move(l:list, num:int):
        return np.concatenate((l[num % l.shape[0]:], l[:num % l.shape[0]]))

def main(data_file_name:str='/data/test_data.txt', output_file_name='/projects/student/result.txt'):
    a = graph_table(data_file_name)
    a.construction()
    loop = []
    absol_visited = np.zeros(a.node_list.shape[0], dtype='uint')
    for i in range(a.node_list.shape[0]):
        if absol_visited[i] == 1:
            continue
        current_close_loop, _, _, absol_visited = a.graph_loop_adjmatrix(i, np.zeros(a.node_list.shape[0], dtype='uint'), absol_visited, [], np.array([], dtype='uint'))
        loop.extend(current_close_loop)
        loop = list(set(loop))

    loop = a.bubble_length_first(loop)
    a.process_save_result(loop, output_file_name)

main()
