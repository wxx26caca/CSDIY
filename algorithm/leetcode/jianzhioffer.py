"""
剑指 offer 参考解法
"""
import collections
from heapq import *
import math
import queue

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class ComplexNode:
    def __init(self, x, next, random):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    # 剑指 offer 03. 数组中重复的数字
    # 方法：哈希表/原地交换
    def findRepeatNumber(self, nums: [int]):
        dic = set()
        for num in nums:
            if num in dic:
                return num
            dic.add(num)
        return -1
    
    def findRepeatNumber2(self, nums: [int]):
        i = 0
        while i < len(nums):
            if nums[i] == i:
                i += 1
                continue
            if nums[nums[i]] == nums[i]:
                return nums[i]
            nums[nums[i]], nums[i] = nums[i], nums[nums[i]]
        return -1
    
    # 剑指 offer 04. 二维数组中的查找
    # 方法：标志数
    def findNumberIn2DArray(self, matrix: List[List[int]], target: int):
        i, j = len(matrix) - 1, 0
        while i >=0 and j < len(matrix[0]):
            if matrix[i][j] > target:
                i -= 1
            elif matrix[i][j] < target:
                j += 1
            else:
                return True
        return False
    
    # 剑指 offer 05. 替换空格
    # 方法：遍历添加/原地修改
    def replaceSpace(self, s: str):
        res = []
        for c in s:
            if c == ' ':
                res.append("%20")
            else:
                res.append(c)
        return "".join(res)

    def replaceSpace2(self, s: str):
        pass

    # 剑指 offer 06. 从尾到头打印链表
    # 方法：递归法/辅助栈法
    def reversePrint(self, head: ListNode):
        return self.reversePrint(head.next) + [head.val] if head else []
    
    def reversePrint2(self, head: ListNode):
        stack = []
        while head:
            stack.append(head.val)
            head = head.next
        return stack[::-1]

    # 剑指 offer 07. 重建二叉树
    # 方法：分治法
    def buildTree(self, preorder: List[int], inorder: List[int]):
        def recur(root, left, right):
            if left > right:
                return
            node = TreeNode(preorder[root])
            i = dic[preorder[root]]
            node.left = recur(root + 1, left, i - 1)
            node.right = recur(i - left + root + 1, i + 1, right)
            return node

        dic, preorder = {}, preorder
        for i in range(len(inorder)):
            dic[inorder[i]] = i
        return recur(0, 0, len(inorder) - 1)
    
    # 剑指 offer 09. 用两个栈实现队列
    # 方法：栈，队列
    class CQueue:
        def __init__(self):
            self.A = []
            self.B = []
        
        def appendTail(self, value: int):
            self.A.append(value)
        
        def deleteHead(self):
            if self.B:
                return self.B.pop()
            if not self.A:
                return -1
            while self.A:
                self.B.append(self.A.pop())
            return self.B.pop()
    
    # 剑指 offer 10-1. 斐波那契数列
    # 方法：动态规划
    def fib(self, n: int):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a % 1000000007
    
    # 剑指 offer 10-2. 青蛙跳台阶问题
    # 方法：动态规划
    def numWays(self, n: int):
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return a % 1000000007
    
    # 剑指 offer 11. 旋转数组的最小数字
    # 方法：二分法
    def minArray(self, numbers: List[int]):
        i, j = 0, len(numbers) - 1
        while i < j:
            m = (i + j) // 2
            if numbers[m] > numbers[j]:
                i = m + 1
            elif numbers[m] < numbers[j]:
                j = m
            else:
                j -= 1
        return numbers[i]
    
    # 剑指 offer 12. 矩阵中的路径
    # 方法：DFS + 剪枝
    def exist(self, board: List[List[int]], word: str):
        def dfs(i, j, k):
            if not 0 <= i < len(board) or not 0 <= j < len(board[0]) or board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            board[i][j] = ''
            res = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)
            board[i][j] = word[k]
            return res
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if dfs(0, 0, 0):
                    return True
        return False
    
    # 剑指 offer 13. 机器人的运动范围
    # 方法：DFS/BFS
    def movingCount_DFS(self, m: int, n: int, k: int):
        def dfs(i, j, si, sj):
            if i >=m or j >=n or k < si + sj or (i, j) in visited:
                return 0
            visited.add((j, j))
            return 1 + dfs(i+1, j, si + 1 if (i+1)%10 else si-8, sj) + dfs(i, j+1, si, sj + 1 if (j+1)%10 else sj -8)
        
        visited = set()
        return dfs(0, 0, 0, 0)
    
    def movingCount_BFS(self, m: int, n: int, k: int):
        queue, visited = [(0, 0, 0, 0)], set()
        while queue:
            i, j, si, sj = queue.pop(0)
            if i >=m or j >= n or k < si + sj or (i, j) in visited:
                continue
            visited.add((i, j))
            queue.append((i + 1, j, si + 1 if (i + 1) % 10 else si - 8, sj))
            queue.append((i, j + 1, si, sj + 1 if (j + 1) % 10 else sj - 8))
        return len(visited)

    # 剑指 offer 14-1. 剪绳子 Ⅰ
    # 方法：数学推导/动态规划
    def cuttingRope(self, n: int):
        if n <= 3:
            return n - 1
        a, b = n //3, n % 3
        if b == 0:
            return int(math.pow(3, a))
        if b == 1:
            return int(math.pow(3, a - 1) * 4)
        return int(math.pow(3, a) * 2)
    
    def cuttingRope2(self, n: int):
        if n <= 3:
            return n - 1
        dp = [0] * (n+1)
        for i in range(2, n+1):
            for j in range(i):
                dp[i] = max(dp[i], j*(i-j), j*dp[i-j])
        return dp[n]
    
    # 剑指 offer 14-2. 剪绳子 Ⅱ
    # 方法：数学推导/贪心
    def cuttingRope3(self, n: int):
        if n <= 3:
            return n - 1
        a, b, p, x, rem = n // 3 - 1, n % 3, 1000000007, 3, 1
        while a > 0:
            if a % 2:
                rem = (rem * x) % p
            x = x ** 2 % p
            a //= 2
        if b == 0:
            return (rem * 3) % p
        if b == 1:
            return (rem * 4) % p
        return (rem * 6) % p
    
    def cuttingRope4(self, n: int):
        if n <= 3:
            return n - 1
        res = 1
        while n > 4:
            res = res * 3 % 1000000007
            n -= 3
        return res * n % 1000000007
    
    # 剑指 offer 15. 二进制中 1 的个数
    # 方法：位运算
    def hammingWeight(self, n: int):
        res = 0
        while n:
            res += n & 1
            n >>= 1
        return res
    
    def hanmingWeight2(self, n: int):
        res = 0
        while n:
            res += 1
            n &= n - 1 # 消去最右边的 1
        return res
    
    # 剑指 offer 16. 数值的整数次方
    # 方法：快速幂
    def myPow(self, x: float, n: int):
        if x == 0:
            return 0
        res = 1
        if n < 0:
            x, n = 1 / x, -n
        while n:
            if n & 1: # n % 2 == 1
                res *= x
            x *= x # x = x ^ 2
            n >>= 1 # n = n // 2
        return res
    
    # 剑指 offer 17. 打印从 1 到最大的 n 位数
    # 方法：分治/全排列
    def printNumbers(self, n: int):
        res = []
        for i in range(1, 10 ** n):
            res.append(i)
        return res
    
    def printNumbers2(self, n: int):
        # 考虑大数越界
        def dfs(x):
            if x == n: # 终止条件：已经固定所有位
                res.append(''.join(num)) # 拼接 num 并添加到 res 尾部
                return
            for i in range(10): # 遍历 0-9
                num[x] = str(i) # 固定第 x 位为 i
                dfs(x + 1) # 开启固定第 x + 1 位
        num = ['0'] * n # 起始数字定义为 n 个 0 组成的字符列表
        res = [] # 数字字符串列表
        dfs(0) # 开启全排列递归
        return ','.join(res) # 拼接所有数字字符串，用逗号隔开并返回
    
    # 剑指 offer 18. 删除链表的节点
    # 方法：双指针
    def deleteNode(self, head: ListNode, val: int):
        if head.val == val:
            return head.next
        pre, cur = head, head.next
        while cur and cur.val != val:
            pre, cur = cur, cur.next
        if cur:
            pre.next = cur.next
        return head
    
    # 剑指 offer 19. 正则表达式匹配
    # 方法：动态规划
    def isMatch(self, s: str, p: str):
        m, n = len(s) + 1, len(p) + 1
        dp = [[False] * n for _ in range(m)]
        dp[0][0] = True
        for j in range(2, n, 2):
            dp[0][j] = dp[0][j - 2] and p[j - 1] == '*'
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i][j - 2] or dp[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.') if p[j - 1] == '*' else dp[i - 1][j - 1] and (p[j - 1] == '.' or s[i - 1] == p[j - 1])
        return dp[-1][-1]
    
    def isMatch2(self, s: str, p: str):
        m, n = len(s) + 1, len(p) + 1
        dp = [[False] * n for _ in range(m)]
        dp[0][0] = True
        for j in range(2, n, 2):
            dp[0][j] = dp[0][j - 2] and p[j - 1] == '*'
        for i in range(1, m):
            for j in range(1, n):
                if p[j - 1] == '*':
                    if dp[i][j - 2]:
                        dp[i][j] = True
                    elif dp[i - 1][j] and s[i - 1] == p[j - 2]:
                        dp[i][j] = True
                    elif dp[i - 1][j] and p[j - 2] == '.':
                        dp[i][j] = True
                else:
                    if dp[i - 1][j - 1] and s[i - 1] == p[j - 1]:
                        dp[i][j] = True
                    elif dp[i - 1][j - 1] and p[j - 1] == '.':
                        dp[i][j] = True
        return dp[-1][-1]

    # 剑指 offer 20. 表示数值的字符串
    # 方法：有限状态机
    def isNumber(self, s: str):
        states = [
            {' ': 0, 's': 1, 'd': 2, '.': 4}, # 0. start with 'blank'
            {'d': 2, '.': 4},                 # 1. 'sign' before 'e'
            {'d': 2, '.': 3, 'e': 5, ' ': 8}, # 2. 'digit' before 'dot'
            {'d': 3, 'e': 5, ' ': 8},         # 3. 'digit' after 'dot'
            {'d': 3},                         # 4. 'digit' after 'dot' ('blank' before 'dot')
            {'s': 6, 'd': 7},                 # 5. 'e'
            {'d': 7},                         # 6. 'sign' after 'e'
            {'d': 7, ' ': 8},                 # 7. 'digit' after 'e'
            {' ': 8}                          # 8. end with 'blank'
        ]
        p = 0
        for c in s:
            if '0' <= c <= '9':
                t = 'd'
            elif c in "+-":
                t = 's'
            elif c in 'eE':
                t = 'e'
            elif c in '. ':
                t = c
            else:
                t = '?'
            if t not in states[p]:
                return False
            p = states[p][t]
        return p in (2, 3, 7, 8)

    # 剑指 offer 21. 调整数组顺序使得奇数位于偶数前面
    # 方法: 双指针
    def exchange(self, nums: List[int]):
        i, j = 0, len(nums) - 1
        while i < j:
            while i < j and nums[i] & 1 == 1:
                i += 1
            while i < j and nums[j] & 1 == 0:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        return nums
    
    # 剑指 offer 22. 链表中倒数第 k 个节点
    # 方法：双指针
    def getKthFromEnd(self, head: ListNode, k: int):
        former, latter = head, head
        for _ in range(k):
            former = former.next
        while former:
            former, latter = former.next, latter.next
        return latter
    
    # 剑指 offer 24. 反转链表
    # 方法：迭代/递归
    def reverseList(self, head: ListNode):
        cur, pre = head, None
        while cur:
            cur.next, pre, cur = pre, cur, cur.next
        return pre
    
    def reverseList2(self, head: ListNode):
        def recur(cur, pre):
            if not cur:
                return pre
            res = recur(cur.next, cur)
            cur.next = pre
            return res
        return recur(head, None)
    
    # 剑指 offer 25. 合并两个排序的链表
    # 方法：dummy node
    def mergeTwoLists(self, l1: ListNode, l2: ListNode):
        cur = dummy = ListNode(0)
        while l1 and l2:
            if l1.val < l2.val:
                cur.next, l1 = l1, l1.next
            else:
                cur.next, l2 = l2, l2.next
            cur = cur.next
        cur.next = l1 if l1 else l2
        return dummy.next
    
    # 剑指 offer 26. 树的子结构
    # 方法：先序遍历 + 判断
    def isSubStructure(self, A: TreeNode, B: TreeNode):
        def recur(A, B):
            if not B:
                return True
            if not A or A.val != B.val:
                return False
            return recur(A.left, B.left) and recur(A.right, B.right)
        
        return bool(A and B) and (recur(A, B) or self.isSubStructure(A.left, B) or self.isSubStructure(A.right, B))
    
    # 剑指 offer 27. 二叉树的镜像
    # 方法：递归/辅助栈
    def mirrorTree(self, root: TreeNode):
        if not root:
            return True
        root.left, root.right = self.mirrorTree(root.right), self.mirrorTree(root.left)
        return root
    
    def mirrorTree2(self, root: TreeNode):
        if not root:
            return True
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
            node.left, node.right = node.right, node.left
        return root
    
    # 剑指 offer 28. 对称的二叉树
    # 方法：递归
    def isSymmetric(self, root: TreeNode):
        def recur(L, R):
            if not L and not R:
                return True
            if not L or not R or L.val != R.val:
                return False
            return recur(L.left, R.right) and recur(L.right, R.left)
        
        return recur(root.left, root.right) if root else True
    
    # 剑指 offer 29. 顺时针打印矩阵
    # 方法：模拟，设定边界
    def spiralOrder(self, matrix: List[List[int]]):
        if not matrix:
            return []
        left, right, top, bottom, result = 0, len(matrix[0]) - 1, 0, len(matrix) - 1, []
        while True:
            for i in range(left, right + 1):
                result.append(matrix[top][i])
            top += 1
            if top > bottom:
                break

            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1
            if left > right:
                break

            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
            if top > bottom:
                break

            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
            if left > right:
                break
        return result
    
    # 剑指 offer 30. 包含 min 函数的栈
    # 方法：两个栈
    class MinStack:
        def __init__(self):
            self.A, self.B = [], []
        
        def push(self, x):
            self.A.append(x)
            if not self.B or self.B[-1] >= x:
                self.B.append(x)
        
        def pop(self):
            if self.A.pop() == self.B[-1]:
                self.B.pop()
        
        def top(self):
            return self.A[-1]
        
        def min(self):
            return self.B[-1]

    # 剑指 offer 31. 栈的压入、弹出序列
    # 方法：模拟
    def validateStackSequence(self, pushed: List[int], poped: List[int]):
        stack, i = [], 0
        for num in pushed:
            stack.append(num)
            while stack and stack[-1] == poped[i]:
                stack.pop()
                i += 1
        return not stack
    
    # 剑指 offer 32. 从上到下打印二叉树ⅠⅡⅢ
    # 方法：层序遍历 BFS (按树的层打印；每一层打印到一行；打印顺序交替变化)
    def levelOrder1(self, root: TreeNode):
        if not root:
            return []
        res, queue = [], collections.deque()
        queue.append(root)
        while queue:
            node = queue.popleft()
            res.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return res
    
    def levelOrder2(self, root: TreeNode):
        if not root:
            return []
        res, queue = [], collections.deque()
        queue.append(root)
        while queue:
            tmp = []
            for _ in range(len(queue)):
                node = queue.popleft()
                tmp.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(tmp)
        return res
    
    def levelOrder3(self, root: TreeNode):
        if not root:
            return []
        res, queue = [], collections.deque()
        queue.append([root])
        while queue:
            tmp = collections.deque()
            for _ in range(len(queue)):
                node = queue.popleft()
                if len(res) % 2:
                    tmp.appendleft(node.val)
                else:
                    tmp.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(list(tmp))
        return res

    # 剑指 offer 33. 二叉搜索树的后序遍历序列
    # 方法：递归分治/单调栈
    def verifyPostorder(self, postorder: [int]):
        def recur(i, j):
            if i >= j:
                return True
            p = i
            while postorder[p] < postorder[j]:
                p += 1
            m = p
            while postorder[p] > postorder[j]:
                p += 1
            return p == j and recur(i, m - 1) and recur(m, j - 1)
        return recur(0, len(postorder) - 1)
    
    def verfiyPostorder2(self, postorder: [int]):
        stack, root = [], float("INF")
        for i in range(len(postorder) - 1, -1, -1):
            if postorder[i] > root:
                return False
            while (stack and postorder[i] < stack[-1]):
                root = stack.pop()
            stack.append(postorder[i])
        return True
    
    # 剑指 offer 34. 二叉树中和为某一值的路径
    # 方法：回溯法
    def pathSum(self, root: TreeNode, sum: int):
        res, path = [], []
        def recur(root, target):
            if not root:
                return
            path.append(root.val)
            target -= root.val
            if target == 0 and not root.left and not root.right:
                res.append(list(path))
            recur(root.left, target)
            recur(root.right, target)
            path.pop()
        recur(root, sum)
        return res
    
    # 剑指 offer 35. 复杂链表的复制
    # 方法：哈希表/拼接与拆分
    def copyRandomList(self, head: ComplexNode):
        if not head:
            return
        dic = {}
        cur = head
        while cur:
            dic[cur] = ComplexNode(cur.val)
            cur = cur.next
        cur = head
        while cur:
            dic[cur].next = dic.get(cur.next)
            dic[cur].random = dic.get(cur.random)
            cur = cur.next
        return dic[head]
    
    def copyRandomList2(self, head: ComplexNode):
        if not head:
            return
        cur = head
        while cur:
            tmp = ComplexNode(cur.val)
            tmp.next = cur.next
            cur.next = tmp
            cur = tmp.next
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next
        cur = res = head.next
        pre = head
        while cur.next:
            pre.next = pre.next.next
            cur.next = cur.next.next
            pre = pre.next
            cur = cur.next
        pre.next = None
        return res
    
    # 剑指 offer 36. 二叉搜索树与双向链表
    # 方法：中序遍历
    def treeToDoublyList(self, root: TreeNode):
        def dfs(cur):
            if not cur:
                return
            dfs(cur.left)
            if self.pre:
                self.pre.right, cur.left = cur, self.pre
            else:
                self.head = cur
            self.pre = cur
            dfs(cur.right)
        if not root:
            return
        self.pre = None
        dfs(root)
        self.head.left, self.pre.right = self.pre, self.head
        return self.head
    
    # 剑指 offer 37. 序列化二叉树
    # 方法：层序遍历 BFS
    class Codec:
        def serialize(self, root):
            if not root:
                return "[]"
            res, queue = [], collections.deque()
            queue.append(root)
            while queue:
                node = queue.popleft()
                if node:
                    res.append(str(node.val))
                    queue.append(node.left)
                    queue.append(node.right)
                else:
                    res.append("null")
            return '[' + ','.join(res) + ']'
            
        def deserialize(self, data):
            if data == "[]":
                return
            vals, i = data[1:-1].split(','), 1
            root = TreeNode(int(vals[0]))
            queue = collections.deque()
            queue.append(root)
            while queue:
                node = queue.popleft()
                if vals[i] != "null":
                    node.left = TreeNode(int(vals[i]))
                    queue.append(node.left)
                i += 1
                if vals[i] != "null":
                    node.right = TreeNode(int(vals[i]))
                    queue.append(node.right)
                i += 1
            return root

    # 剑指 offer 38. 字符串的排列(全排列)
    # 方法：回溯法
    def premutation(self, s: str):
        c, res = list(s), []
        def dfs(x):
            if x == len(c) - 1:
                res.append(''.join(c))  # 添加排列方案
                return
            dic = set()
            for i in range(x, len(c)):
                if c[i] in dic:  # 重复，因此剪枝
                    continue
                dic.add(c[i])
                c[i], c[x] = c[x], c[i]  # 交换，将 c[i] 固定在第 x 位
                dfs(x+1)                 # 开启固定第 x + 1 位字符
                c[i], c[x] = c[x], c[i]  # 恢复交换
        dfs(0)
        return res
    
    # 剑指 offer 39. 数组中出现次数超过一半的数字
    # 方法：哈希表统计法/数组排序法/摩尔投票法（票数正负抵消）
    def majoriryElement(self, nums: List[int]):
        votes = 0
        for num in nums:
            if votes == 0:
                x = num
            votes += 1 if num == x else -1
        return x
    
    # 剑指 offer 40. 最小的 k 个数
    # 方法：排序/基于快排的数组划分
    def getLeastNumbers(self, arr: List[int], k: int):
        def quick_sort(arr, l, r):
            if l >= r:
                return
            i, j = l, r
            while i < j:
                while i < j and arr[j] >= arr[l]:
                    j -= 1
                while i < j and arr[i] <= arr[l]:
                    i += 1
                arr[i], arr[j] = arr[j], arr[i]
            arr[l], arr[i] = arr[i], arr[l]
            quick_sort(arr, l, i - 1)
            quick_sort(arr, i + 1, r)
        quick_sort(arr, 0, len(arr) - 1)
        return arr[:k]
    
    def getLeastNumbers2(self, arr: List[int], k: int):
        if k >= len(arr):
            return arr
        def quick_sort(l, r):
            i, j = l, r
            while i < j:
                while i < j and arr[j] >= arr[l]:
                    j -= 1
                while i < j and arr[i] <= arr[l]:
                    i += 1
                arr[i], arr[j] = arr[j], arr[i]
            arr[l], arr[i] = arr[i], arr[l]
            if k < i:
                return quick_sort(l, i - 1)
            if k > i:
                return quick_sort(i + 1, r)
            return arr[:k]
        return quick_sort(0, len(arr) - 1)
    
    # 剑指 offer 41. 数据流中的中位数
    # 方法：优先队列/堆
    class MedianFinder:
        def __init__(self):
            self.A = [] # 小顶堆，保存较大的一半
            self.B = [] # 大顶堆，保存较小的一半
        
        def addNum(self, num):
            if len(self.A) != len(self.B):
                heappush(self.A, num)
                heappush(self.B, -heappop(self.A))
            else:
                heappush(self.B, -num)
                heappush(self.A, -heappop(self.B))
        
        def findNumber(self):
            return self.A[0] if len(self.A) != len(self.B) else (self.A[0] - self.B[0]) / 2.0
    
    # 剑指 offer 42. 连续子数组的最大和
    # 方法：动态规划
    def maxSubArray(self, nums: List[int]):
        for i in range(1, len(nums)):
            nums[i] += max(nums[i-1], 0)
        return max(nums)
    
    def maxSubArray2(self, nums: List[int]):
        n = len(nums)
        dp = [0] * (n + 1)
        res = nums[0]
        for i in range(1, n):
            dp[i] = max(nums[i-1], dp[i-1] + nums[i])
            res = max(res, dp[i])
        return res
    
    # 剑指 offer 43. 1 ~ n 整数中 1 出现的次数
    # 方法：分析(逐位分析)
    def countDigitOne(self, n: int):
        digit, res = 1, 0
        high, cur, low = n // 10, n % 10, 0
        while high != 0 or cur != 0:
            if cur == 0:
                res += high * digit
            elif cur == 1:
                res += high * digit + low + 1
            else:
                res += (high + 1) * digit
            low += cur * digit # 将 cur 加入 low ，组成下轮 low
            cur = high % 10    # 下轮 cur 是本轮 high 的最低位
            high //= 10        # 将本轮 high 最低位删除，得到下轮 high
            digit *= 10        # 位因子每轮 × 10
        return res
    
    # 剑指 offer 44. 数字序列中某一位的数字
    # 方法：迭代 + 求整/求余
    def findNthDigit(self, n: int):
        digit, start, count = 1, 1, 9
        while n > count: # 确定所求数位的所在数字的位数
            n -= count
            start *= 10
            digit += 1
            count = 9 * start * digit
        num = start + (n - 1) // digit # 确定所求数位所在的数字
        return int(str(num)[(n - 1) % digit]) # 确定所求数位在 num 的哪一数位
    
    # 剑指 offer 45. 把数组排成最小的数
    # 方法：自定义排序
    def minNumber(self, nums: List[int]):
        def quick_sort(l, r):
            if l >= r:
                return
            i, j = l, r
            while i < j:
                while strs[j] + strs[l] >= strs[l] + strs[j] and i < j:
                    j -= 1
                while strs[i] + strs[l] <= strs[l] + strs[i] and i < j:
                    i += 1
                strs[i], strs[j] = strs[j], strs[i]
            strs[i], strs[l] = strs[l], strs[i]
            quick_sort(l, i - 1)
            quick_sort(i + 1, r)
        strs = [str(num) for num in nums]
        quick_sort(0, len(strs) - 1)
        return ''.join(strs)
    
    # 剑指 offer 46. 把数字翻译成字符串
    # 方法：动态规划/数字取余
    # dp[i] = dp[i - 1] + dp[i - 2] ([10,25]) or dp[i - 1] ([0, 10) or (25,99])
    def translateNum(self, num: int):
        s = str(num)
        a = b = 1
        for i in range(2, len(s) + 1):
            tmp = s[i - 2:i]
            c = a + b if "10" <= tmp <= "25" else a
            b = a
            a = c
        return a

    # 剑指 offer 47. 礼物的最大价值
    # 方法：动态规划
    # dp[i, j] = max(dp[i, j - 1], dp[i - 1, j]) + grid(i, j)
    def maxValue(self, grid: List[List[int]]):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i == 0 and j == 0:
                    continue
                if i == 0:
                    grid[i][j] += grid[i][j - 1]
                elif j == 0:
                    grid[i][j] += grid[i - 1][j]
                else:
                    grid[i][j] += max(grid[i - 1][j], grid[i][j - 1])
        return grid[-1][-1]
    
    # 剑指 offer 48. 最长不含重复字符串的子字符串
    # 方法：动态规划/双指针+哈希表
    # dp[j] = dp[j - 1] + 1 (dp[j - 1] < j - i) or j - i (dp[j - 1] >= j - i)
    def lengthOfLongestSubStrings(self, s: str):
        dic = {}
        res = tmp = 0
        for j in range(len(s)):
            i = dic.get(s[j], -1) # 获取索引 i
            dic[s[j]] = j         # 更新哈希表
            tmp = tmp + 1 if tmp < j - i else j - i # dp[j - 1] -> dp[j]
            res = max(res, tmp)   # max(dp[j - 1], dp[j])
        return res

    # 剑指 offer 49. 丑数(只包含质因子 2、3 和 5 的数称作丑数)
    # 方法：动态规划
    def nthUglyNumber(self, n: int):
        dp, a, b, c = [1] * n, 0, 0, 0
        for i in range(1, n):
            n2, n3, n5 = dp[a] * 2, dp[b] * 3, dp[c] * 5
            dp[i] = min(n2, n3, n5)
            if dp[i] == n2:
                a += 1
            if dp[i] == n3:
                b += 1
            if dp[i] == n5:
                c += 1
        return dp[-1]
    
    # 剑指 offer 50. 第一个只出现一次的字符
    # 方法：哈希表/有序哈希表
    def firstUniqChar(self, s: str):
        dic = {}
        for c in s:
            dic[c] = not c in dic
        for c in s:
            if dic[c]:
                return c
        return ' '
    
    def firstUniqChar2(self, s: str):
        dic = collections.OrderedDict()
        for c in s:
            dic[c] = not c in dic
        for k, v in dic.items():
            if v:
                return k
        return ' '
    
    # 剑指 offer 51. 数组中的逆序对
    # 方法：归并排序
    def reversePairs(self, nums: List[List[int]]):
        def merge_sort(l, r):
            if l >= r:
                return 0
            m = (l + r) // 2
            res = merge_sort(l, m) + merge_sort(m + 1, r)
            i, j = l, m + 1
            tmp[l:r + 1] = nums[l:r + 1]
            for k in range(l, r + 1):
                if i == m + 1:
                    nums[k] = tmp[j]
                    j += 1
                elif j == r + 1 or tmp[i] <= tmp[j]:
                    nums[k] = tmp[i]
                    i += 1
                else:
                    nums[k] = tmp[j]
                    j += 1
                    res += m - i + 1
            return res
        tmp = [0] * len(nums)
        return merge_sort(0, len(nums) - 1)

    # 剑指 offer 52. 两个链表的第一个公共节点
    # 方法：双指针
    def getIntersectionNode(self, headA: ListNode, headB: ListNode):
        A, B = headA, headB
        while A != B:
            A = A.next if A else headB
            B = B.next if B else headA
        return A
    
    # 剑指 offer 53. 在排序数组中查找数字出现的次数，查找递增数组里0~n-1中缺失的数字
    # 方法：二分法
    def search(self, nums: [int], target: int):
        def helper(tar):
            i, j = 0, len(nums) - 1
            while i <= j:
                m = (i + j) // 2
                if nums[m] <= tar:
                    i = m + 1
                else:
                    j = m - 1
            return i
        return helper(target) - helper(target - 1)
    
    def missingNumber(self, nums: List[int]):
        i, j = 0, len(nums) - 1
        while i <= j:
            m = (i + j) // 2
            if nums[m] == m:
                i = m + 1
            else:
                j = m - 1
        return i
    
    # 剑指 offer 54. 二叉搜索树的第 k 大节点
    # 方法：中序遍历+提前返回
    def kthLargest(self, root: TreeNode, k: int):
        def dfs(root):
            if not root:
                return
            dfs(root.right)
            if self.k == 0:
                return
            self.k -= 1
            if self.k == 0:
                self.res = root.val
            dfs(root.left)
        
        self.k = k
        dfs(root)
        return self.res

    # 剑指 offer 55. 二叉树的深度，平衡二叉树
    # 方法：DFS/BFS; 先序遍历+判断深度/先序遍历+剪枝
    def maxDepth(self, root: TreeNode):
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right))
    
    def maxDepth2(self, root: TreeNode):
        if not root:
            return 0
        queue, res = [root], 0
        while queue:
            tmp = []
            for node in queue:
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            queue = tmp
            res += 1
        return res
    
    def isBalanced(self, root: TreeNode):
        if not root:
            return True
        return abs(depth(root.left) - depth(root.right)) <= 1 and self.isBalanced(root.left) and self.isBalanced(root.right)
        
        def depth(root):
            if not root:
                return 0
            return max(depth(root.left), depth(root.right)) + 1
    
    def isBalanced2(self, root: TreeNode):
        def recur(root):
            if not root:
                return 0
            left = recur(root.left)
            if left == 1:
                return -1
            right = recur(root.right)
            if right == 1:
                return -1
            return max(left, right) + 1 if abs(left - right) <= 1 else -1
        return recur(root) != -1

    # 剑指 offer 56. 数组中数字出现的次数 Ⅰ(只出现一次的两个数字)，Ⅱ(除了一个出现一次外，其它都出现了三次)
    # 方法：位运算; 有限状态机/遍历统计
    def singleNumber(self, nums: List[int]):
        x, y, n, m = 0, 0, 0, 1
        for num in nums:    # 遍历异或
            n ^= num
        while n & m == 0:   # 循环左移，计算 m，利用位运算分开数组
            m <<= 1
        for num in nums:    # 遍历 nums 分组
            if num & m:     
                x ^= num    # 当 num & m != 0 时
            else:
                y ^= num    # 当 num & m == 0 时
        return x, y         # 返回只出现一次的两个数字
    
    def singleNumber2(self, nums: List[int]):
        ones, twos = 0, 0
        for num in nums:
            ones = ones ^ num & ~twos
            twos = twos ^ num & ~ones
        return ones
    
    def singleNumber3(self, nums: List[int]):
        counts = [0] * 32
        for num in nums:
            for j in range(32):
                counts[j] += num & 1
                num >>= 1
        res, m = 0, 3
        for i in range(32):
            res <<= 1
            res |= counts[32 - i] % m
        return res if counts[31] % m == 0 else ~(res ^ 0xffffffff)

    # 剑指 offer 57. 找到排序数组中和为 s 的两个数字，和为 s 的连续正数序列
    # 方法：双指针; 滑动窗口
    def twoSum(self, nums: List[int], target: int):
        i, j = 0, len(nums) - 1
        while i < j:
            s = nums[i] + nums[j]
            if s > target:
                j -= 1
            elif s < target:
                i += 1
            else:
                return nums[i], nums[j]
        return []
    
    def findContinuousSequence(self, target: int):
        i, j, res = 1, 2, []
        while i < j:
            j = (-1 + (1 + 4 * (2 * target + i * i - i)) ** 0.5) / 2  # 一元二次方程组的解
            if i < j and j == int(j):
                res.append(list(range(i, int(j) + 1)))
            i += 1
        return res
    
    def findContinuousSequence2(self, target: int):
        i, j, s, res = 1, 2, 3, []
        while i < j:
            if s == target:
                res.append(list(range(i, j + 1)))
            if s >= target:
                s -= i
                i += 1
            else:
                j += 1
                s += j
        return res
    
    # 剑指 offer 58. 翻转单词顺序(单词内字符顺序不变），左旋转字符串
    # 方法：双指针
    def reverseWord(self, s: str):
        s = s.strip()                     # 删除首尾空格
        i = j = len(s) - 1
        res = []
        while i >= 0:
            while i >= 0 and s[i] != ' ': # 搜索首个空格
                i -= 1
            res.append(s[i + 1: j + 1])   # 添加单词
            while s[i] == ' ':            # 跳过单词间空格
                i -= 1
            j = i                         # j 指向下一个单词的尾字符
        return ' '.join(res)              # 拼接并返回
    
    def reverseLeftWord(self, s: str, n: int):
        res = []
        for i in range(n, len(s)):
            res.append(s[i])
        for i in range(n):
            res.append(s[i])
        return ''.join(res)
    
    def reverseLeftWord2(self, s: str, n: int):
        res = ""
        for i in range(n, len(s)):
            res += s[i]
        for i in range(n):
            res += s[i]
        return res
    
    # 剑指 offer 59. 滑动窗口的最大值，队列的最大值
    # 方法：单调队列;
    def maxSlidingWindow(self, nums: List[int], k: int):
        deque = collections.deque()
        res, n = [], len(nums)
        for i, j in zip(range(1 - k, n + 1 - k), range(n)):
            if i > 0 and deque[0] == nums[i - 1]:  # 若 i > 0 且 队首元素 deque[0] == 被删除元素 nums[i−1] ：则队首元素出队；
                deque.popleft()
            while queue and deque[-1] < nums[j]:   # 删除 deque 内所有 <nums[j] 的元素，以保持 deque 递减；
                deque.pop()
            deque.append(nums[j])                  # 将 nums[j] 添加至 deque 尾部；
            if i >= 0:
                res.append(deque[0])               # 将窗口最大值（即队首元素 deque[0] ）添加至列表 res
        return res
    
    class MaxQueue:
        def __init__(self):
            self.queue = queue.Queue()
            # 使用双向队列原因：维护递减列表需要元素队首弹出、队尾插入、队尾弹出操作皆为 O(1) 时间复杂度。
            self.deque = queue.deque()

        def max_value(self):
            return self.deque[0] if self.deque else -1

        def push_back(self, value: int):
            #  若入队一个比队列某些元素更大的数字 x ，则为了保持此列表递减，需要将双向队列尾部所有小于 x 的元素弹出。
            self.queue.put(value)
            while self.deque and self.deque[-1] < value:
                self.deque.pop()
            self.deque.append(value)

        def pop_front(self):
            # 若出队的元素是最大元素，则双向队列需要同时将首元素出队，以保持队列和双向队列的元素一致性。
            if self.queue.empty():
                return -1
            val = self.queue.get()
            if val == self.deque[0]:
                self.queue.popleft()
            return val
    
    # 剑指 offer 60. n 个骰子的点数(朝上一面点数之和 s 的所有可能值出现的概率)
    # 方法：暴力法/动态规划
    # dp[i][j] 代表前 i 个骰子的点数和为 j 的概率, 由于 dp[i] 仅由 dp[i−1] 递推得出，为降低空间复杂度，只建立两个一维数组 dp , tmp 交替前进即可。
    def dicesProbability(self, n: int):
        dp = [1 / 6] * 6
        for i in range(2, n+1):
            tmp = [0] * (5 * i + 1)
            for j in range(len(dp)):
                for k in range(6):
                    tmp[j + k] += dp[j] / 6
            dp = tmp
        return dp

    # 剑指 offer 61. 判断任意 5 张扑克牌是不是一个顺子
    # 方法：集合+遍历/排序+遍历
    def isStraight(self, nums: List[int]):
        repeat = set()
        ma, mi = 0, 14
        for num in nums:
            if num == 0:
                continue       # 遇到大小王跳过
            ma = max(ma, num)  # 最大牌
            mi = min(mi, num)  # 最小牌
            if num in repeat:  
                return False   # 如果有重复牌，提前返回
            repeat.add(num)    # 添加牌到 set
        return ma - mi < 5     # 最大牌 - 最小牌 < 5 即可构成顺子
    
    def isStraight2(self, nums: List[int]):
        joker = 0
        nums.sort()
        for i in range(4):
            if nums[i] == 0:
                joker += 1
            elif nums[i] == nums[i + 1]:
                return False
        return nums[4] - nums[joker] < 5
    
    # 剑指 offer 62. 圆圈中最后剩下的数字(从 0...n-1 中每次删 m 个数字)
    # 方法：数学/动态规划(约瑟夫环问题)
    # dp[i] = (dp[i-1]+m)%i, dp[1]=0
    def lastRemaining(self, n: int, m: int):
        x = 0
        for i in range(2, n+1):
            x = (x + m) % i
        return x

    # 剑指 offer 63. 股票的最大利润(只买卖一次)
    # 方法：动态规划
    # dp[i] = max(dp[i-1], prices[i] - min(prices[0:i]))
    def maxProfit(self, prices: List[int]):
        cost, profit = float("inf"), 0
        for price in prices:
            cost = min(cost, price)
            profit = max(profit, price - cost)
        return profit
    
    # 剑指 offer 64. 求 1+2+...+n
    # 方法：平均计算/迭代/递归/逻辑运算巧用短路计算
    def sumNums(self, n):
        return (1 + n) * n // 2
    
    def sumNums2(self, n):
        res = 0
        for i in range(1, n+1):
            res += i
        return res
    
    def sumNums3(self, n):
        if n == 1:
            return 1
        n += sumNums3(n - 1)
        return n
    
    class Sum:
        def __init__(self):
            self.res = 0
        def sumNums(self, n):
            n > 1 and self.sumNums(n-1)
            self.res += n
            return self.res
    
    # 剑指 offer 65. 不用加减乘除做加法
    # 方法：位运算
    """ 
    java
    class Solution{
        public int add(int a, int b){
            while(b != 0){             // 当进位为 0 时跳出
                int c = (a & b) << 1;  // c = 进位
                a ^= b;                // a = 非进位和
                b = c;                 // b = 进位
            }
            return a;
        }
    } 
    """
    def add(self, a: int, b: int):
        x = 0xffffffff
        a, b = a & x, b & x
        while b != 0:
            a, b = (a ^ b), (a & b) << 1 & x
        return a if a <= 0x7fffffff else ~(a ^ x)
    
    # 剑指 offer 66. 构建乘积数组
    # 方法：表格分区
    def constructArr(self, a: List[int]):
        b, tmp = [1] * len(a), 1
        for i in range(1, len(a)):
            b[i] = b[i - 1] * a[i - 1]       # 计算左下方三角
        for i in range(len(a) - 2, -1, -1):
            tmp *= a[i + 1]                  # 计算右上方三角
            b[i] *= tmp                      # 下三角 * 上三角
        return b
    
    # 剑指 offer 67. 把字符串转换成整数
    # 
    def strToInt(self, str: str):
        str = str.strip()
        if not str:
            return 0
        res, i, sign = 0, 1, 1
        int_max, int_min, bndry = 2 ** 31 - 1, -2 ** 31, 2 ** 31 // 10
        if str[0] == '-':
            sign = -1
        elif str[0] != '+':
            i = 0
        for c in str[i:]:
            if not '0' <= c <= '9':
                break
            if res > bndry or res == bndry and c > '7':
                return int_max if sign == 1 else int_min
            res = 10 * res + ord(c) - ord('0')
        return sign * res
    
    # 剑指 offer 68. 二叉搜索树的最近公共祖先，二叉树的最近公共祖先
    # 方法：迭代
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode):
        while root:
            if root.val < p.val and root.val < q.val:
                root = root.right
            elif root.val > p.val and root.val > q.val:
                root = root.left
            else:
                break
        return root
    
    def lowestCommonAncestor2(self, root: TreeNode, p: TreeNode, q: TreeNode):
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor2(root.left, p, q)
        right = self.lowestCommonAncestor2(root.right, p, q)
        if not left and not right:
            return
        if not left:
            return right
        if not right:
            return left
        return root