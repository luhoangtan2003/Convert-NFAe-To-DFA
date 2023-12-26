import copy

class DFA:
    def __init__(self):
        self.Q = list()
        self.Σ = set()
        self.Q0 = set()
        self.F = list()
        self.δ = dict()

    def Show_DFA(self):
        print("DFA(Q,Σ,δ,Q0,F)\n")
        print("Q:")
        for q in self.Q:
            print(f"    {q}\n")
        print("Σ:\n    ",list(self.Σ))
        print("δ:")
        for q, c in self.δ:
            print(f"    ({set(q)}, {c}) => {self.δ[q,c]}\n")
        print("Q0:\n    ",self.Q0)
        print("F:\n    ",self.F)

class NFAε:
    def __init__(self):
        self.Q = set()
        self.Σ = set()
        self.δ = dict()
        self.Q0 = None
        self.F = set()

    def Import(self):
        with open("Graph_1.txt", 'r') as File:
            Lines = File.readlines()
            Temp = Lines.pop(0)
            Temp = Temp.split()
            self.Q0 = Temp[0]
            self.F.update(Temp[1:])
            for Item in Lines:
                Line = Item.split()
                self.δ[Line[0],Line[1]] = set(Line[2:])
                self.Q.add(Line[0])
                self.Q.update(Line[2:])
                if Line[1] != 'ε':
                    self.Σ.add(Line[1])

    def Show_NFAε(self):
        print("NFAε(Q,Σ,δ,Q0,F)\n")
        print("Q:\n    ",list(self.Q))
        print("Σ:\n    ",list(self.Σ))
        print("δ:")
        for q, a in self.δ:
            print(f"    ({q}, {a}) = {self.δ[q,a]}\n")
        print("Q0:\n    ",self.Q0)
        print("F:\n    ",list(self.F))

    def ε_closure(self, States):
        Result = set()
        Queue = list()
        for State in States:
            Queue.append(State)
            Result.add(State)
        while len(Queue) != 0:
            q = Queue.pop(0)
            if(q,'ε') in self.δ:
                for Value in self.δ[(q,'ε')]:
                    if Value not in Result:
                        Result.add(Value)
                        Queue.append(Value)
        return Result

    def Move(self, States, c):
        Result = set()
        for q in States:
            if(q, c) in self.δ:
                for Value in self.δ[(q, c)]:
                    Result.add(Value)
        return Result

    def Convert(self):
        IsOpen = list()
        Closed = list()
        Result = DFA()
        Start = self.ε_closure({self.Q0})
        IsOpen.append(Start)
        print("Chuyển đổi từ NFAε sang DFA\n")
        print(f"    Trạng thái bắt đầu DFA: ε_closure({self.Q0}) = {Start}\n")
        while len(IsOpen) != 0:
            q = IsOpen.pop(0)
            Closed.append(q)
            for c in self.Σ:
                Next = self.ε_closure(self.Move(q,c))
                if Next not in IsOpen and Next not in Closed and len(Next) != 0:
                    IsOpen.append(Next)
                print(f"    ε_closure(δ({q}, {c})) = ε_closure({self.Move(q, c)}) = {Next}\n")
                if len(Next) != 0:
                    Result.δ[tuple(q),c] = Next
        Result.Q = copy.deepcopy(Closed)
        Result.Q0 = copy.deepcopy(Start)
        for State_End in Closed:
            if any(e in State_End for e in self.F):
                Result.F.append(State_End)
        Result.Σ = copy.deepcopy(self.Σ)
        return Result

if __name__ == "__main__":
    Nfaε = NFAε()
    Nfaε.Import()
    Nfaε.Show_NFAε()
    print("\n\n\n")
    Dfa = Nfaε.Convert()
    print("\n\n\n")
    Dfa.Show_DFA()