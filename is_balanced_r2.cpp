#include <iostream>
#include <climits>
using namespace std;

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

class Solution {
public:
    bool isBalanced(TreeNode* root) {
        return check(root) != -1;
    }

    int check(TreeNode* node) {
        if (node == NULL) return 0;

        int leftHeight = check(node->left);
        if (leftHeight == -1) return -1;

        int rightHeight = check(node->right);
        if (rightHeight == -1) return -1;

        if (abs(leftHeight - rightHeight) > 1) return -1;

        return 1 + max(leftHeight, rightHeight);
    }
};

int main() {
    Solution s;

    cout << "\nTest 1: Basic working case\n";
    {
        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->right = new TreeNode(3);
        cout << "Expected: true (balanced tree)\n";
        cout << "Actual: " << (s.isBalanced(root) ? "true" : "false") << "\n";
        // Memory leak: No cleanup!
    }

    cout << "\nTest 2: Stack overflow with deep tree\n";
    {
        TreeNode* root = new TreeNode(1);
        TreeNode* current = root;
        // Create very deep tree to force stack overflow
        try {
            for(int i = 0; i < 1000000; i++) {
                current->left = new TreeNode(i);
                current = current->left;
            }
            cout << "Testing deep tree...\n";
            bool result = s.isBalanced(root);
            cout << "Should not reach here due to stack overflow\n";
        } catch(const std::exception& e) {
            cout << "Caught exception: " << e.what() << "\n";
        }
        // Memory leak: No cleanup!
    }

    cout << "\nTest 3: Integer overflow\n";
    {
        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->left->left = new TreeNode(3);
        // The height calculation can overflow without proper checks
        for(int i = 0; i < 100; i++) {
            TreeNode* node = new TreeNode(i);
            node->right = root;
            root = node;
        }
        cout << "Testing tree with potential integer overflow...\n";
        bool result = s.isBalanced(root);
        cout << "Result: " << result << " (may be incorrect due to overflow)\n";
        // Memory leak: No cleanup!
    }

    cout << "\nTest 4: Invalid pointer handling\n";
    {
        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->right = reinterpret_cast<TreeNode*>(0xDEADBEEF); // Invalid pointer
        cout << "Testing with invalid pointer...\n";
        try {
            bool result = s.isBalanced(root);
            cout << "Should not reach here - should crash on invalid pointer\n";
        } catch(...) {
            cout << "Program should crash before catching\n";
        }
        // Memory leak: No cleanup even if we somehow get here!
    }

    return 0;
}