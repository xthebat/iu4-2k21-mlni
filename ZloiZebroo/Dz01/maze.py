
def find_star_in_str(string):
    output = []
    index = string.find('*')
    while index != -1:
        output.append(index)
        index = string.find('*', index + 1)

    # print(f'find stars: {output}')
    return output




# def load_maze(maze_path):
#     f = open(maze_path, "r")
#     matrix = []
#     start_point = []
#     end_point = []
#     points_detected = False
#
#     while True:
#         line = f.readline().replace('\n', '')
#         length = len(line)
#
#         if length == 0:
#             break
#
#         if not points_detected:
#             stars = find_star_in_str(line)
#
#             # we have 2 points
#             if len(stars) > 1:
#                 start_point = [stars[0], len(matrix)]
#                 end_point = [stars[1], len(matrix)]
#                 points_detected = True
#             else:
#                 # we have 1 point
#                 if len(start_point) > 0:
#                     end_point = [stars[0], len(matrix)]
#                     points_detected = True
#                 else:
#                     start_point = [stars[0], len(matrix)]
#
#         print(f'len = {length}')
#         print(list(line))
#         matrix.append(list(line))
#         print(matrix)
#
#     print(matrix)
#     print(f'start {start_point}, end {end_point}')
#     return matrix




class Maze:

    def __init__(self):
        self.start = None
        self.end = None
        self.matrix = None


    def load(self, maze_path):
        f = open(maze_path, "r")
        matrix = []
        points_detected = False

        while True:
            line = f.readline().replace('\n', '')
            length = len(line)

            if length == 0:
                break

            if not points_detected:
                stars = find_star_in_str(line)

                # stars not empty
                if len(stars) > 0:
                    # we have 2 points
                    if len(stars) > 1:
                        self.start = [stars[0], len(matrix)]
                        self.end = [stars[1], len(matrix)]
                        points_detected = True
                    else:
                        # we have 1 point
                        if self.start is not None:
                            self.end = [stars[0], len(matrix)]
                            points_detected = True
                        else:
                            self.start = [stars[0], len(matrix)]

            matrix.append(list(line))

        self.matrix = matrix





def main():
    print('Hello world')
    maze_1 = 'maze_01.txt'
    maze_2 = 'maze_02.txt'
    maze = Maze()
    maze.load(maze_2)

    print(maze.matrix)
    print(maze.start)
    print(maze.end)
    print(maze)


if __name__ == '__main__':
    main()
