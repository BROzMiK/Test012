import heapq

def find_top_transactions(transactions, n=3):
    """Find the top N largest transactions using a heap."""
    return heapq.nlargest(n, transactions, key=lambda x: x.amount)

class RunningAverage:
    """Calculate running average with minimal memory usage."""
    def __init__(self):
        self.count = 0
        self.total = 0

    def update(self, value):
        self.count += 1
        self.total += value

    def get_average(self):
        if self.count == 0:
            return 0
        return self.total / self.count
