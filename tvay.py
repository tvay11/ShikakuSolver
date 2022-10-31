from ShikakuSolver import *
import time


class PartiallySolvedPuzzle:
    def __init__(self, board, options):
        self.board = board
        self.options = options


class tvay(ShikakuSolver):
    def __init__(self, problem, maxTime, visualizer):
        ShikakuSolver.__init__(self, problem, maxTime, visualizer)

    def solve(self):
        options = {}
        for i in range(self._problem.numRegions()):
            rowOrginal = self._problem.getRegionOrigin(i)[0]
            colOrginal = self._problem.getRegionOrigin(i)[1]
            size = self._problem.getRegionSize(i)
            rectangles = []
            for height in range(1, size + 1):
                if size % height == 0:
                    width = size // height
                    for row in range(0, self._problem.size() - height + 1):
                        for col in range(0, self._problem.size() - width + 1):
                            rows = {x: x for x in range(row, row + height)}
                            cols = {y: y for y in range(col, col + width)}
                            if rowOrginal in rows and colOrginal in cols:
                                if numpy.all(numpy.logical_or(self._problem._known == -1, self._problem._known == i)[row:row + height, col:col + width]):
                                        rectangles.append((row, col, height, width))

            if len(rectangles) == 1:
                options[-i] = rectangles
            else:
                options[i] = rectangles

        root = PartiallySolvedPuzzle(copy.copy(self._problem._known), options)

        if self._visualizer:
            self._visualizer.draw(root.board)

        if self._problem.isGoal(root.board):  # We found the solution
            #print("DONE")
            return root.board

        solution = self.backtrack(root)
        if solution is not None:
            return solution.board
        return None  #

    def backtrack(self, state):
        if not self.timeRemaining():
            return None

        if self._problem.isGoal(state.board):  #
            #print("Done2")
            return state

        if self._visualizer:
            self._visualizer.draw(state.board, state.options)

        regionID = sorted(list(state.options.keys()))[0]
        regionOptions = state.options.pop(regionID)
        regionID = abs(regionID)
        self._numExpansions += 1

        for rectangle in regionOptions:
            consistent = numpy.all(numpy.logical_or(state.board == -1, state.board == regionID)[rectangle[0]:rectangle[0] + rectangle[2],rectangle[1]:rectangle[1] + rectangle[3]])
            if consistent:
                newState = copy.deepcopy(state)
                infer = False
                for row in range(rectangle[0], rectangle[0] + rectangle[2]):
                    for col in range(rectangle[1], rectangle[1] + rectangle[3]):
                        if state.board[row, col] == -1 or state.board[row, col] == regionID:
                            newState.board[row, col] = regionID
                        else:
                            infer = True
                if infer:
                    continue
                loop = False
                if len(regionOptions) >= 1:
                    opt = sorted(list(newState.options.keys()))
                    for key in opt:
                        if len(newState.options.get(key)) > 1:
                            optionKey = state.options.get(key)
                            for rec in optionKey:
                                for row in range(rec[0], rec[0] + rec[2]):
                                    for col in range(rec[1], rec[1] + rec[3]):
                                        changed = False
                                        if newState.board[row, col] == regionID:
                                            newState.options[key].remove(rec)
                                            changed = True
                                            break
                                    if changed:
                                        break
                            count = len(newState.options.get(key))
                            if count == 0:
                                loop = True
                                break

                            if count == 1:
                                newState.options[-key] = newState.options.pop(key)
                if loop == True:
                    continue

                if self._visualizer:
                    self._visualizer.draw(newState.board)

                solution = self.backtrack(newState)
                if solution is not None:
                    return solution
                self._backTracks += 1

        return None

