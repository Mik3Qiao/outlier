#include <iostream>
#include <queue>
using namespace std;

// Define the structure for a binary tree node
struct Node {
    int data;
    Node* left;
    Node* right;
};

// Function to create a new binary tree node
Node* createNode(int data) {
    Node* newNode = new Node();
    if (!newNode) {
        cout << "Memory error\n";
        return NULL;
    }
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

bool isTreeBalanced(Node* root, int& height) {
    if (root == NULL) {
        height = 0;
        return true; // empty tree is balanced
    }

    int leftHeight = 0;
    int rightHeight = 0;

    if (!isTreeBalanced(root->left, leftHeight)) {
        return false;
    }

    if (!isTreeBalanced(root->right, rightHeight)) {
        return false;
    }

    height = max(leftHeight, rightHeight) + 1;

    if (abs(leftHeight - rightHeight) > 1) {
        return false;
    }

    return true;
}

// Helper function to get the height of a tree
int getHeight(Node* root) {
    if (root == NULL) {
        return 0;
    }

    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);

    return max(leftHeight, rightHeight) + 1;
}

// Example usage:
int main() {
    // Test Case 1: Basic Working Case
    cout << "\nTest 1: Basic working case\n";
    {
        Node* root = createNode(1);
        root->left = createNode(2);
        root->right = createNode(3);
        cout << "Expected: true (balanced tree)\n";
        int height = 0;
        cout << "Actual: " << (isTreeBalanced(root, height) ? "true" : "false") << "\n";
        // Memory leak: No cleanup!
    }

    // // Test Case 2: Stack Overflow with Deep Tree
    // cout << "\nTest 2: Stack overflow with deep tree\n";
    // {
    //     Node* root = createNode(1);
    //     Node* current = root;
    //     // Create a very deep tree to force stack overflow
    //     try {
    //         for(int i = 2; i <= 1000000; i++) {
    //             current->left = createNode(i);
    //             current = current->left;
    //         }
    //         cout << "Testing deep tree...\n";
    //         int height = 0;
    //         bool result = isTreeBalanced(root, height);
    //         cout << "Should not reach here due to stack overflow\n";
    //     } catch(const std::exception& e) {
    //         cout << "Caught exception: " << e.what() << "\n";
    //     }
    //     // Memory leak: No cleanup!
    // }

    // Test Case 3: Integer Overflow
    cout << "\nTest 3: Integer overflow\n";
    {
        Node* root = createNode(1);
        root->left = createNode(2);
        root->left->left = createNode(3);
        // The height calculation can overflow without proper checks
        for(int i = 0; i < 100; i++) {
            Node* node = createNode(i);
            node->right = root;
            root = node;
        }
        cout << "Testing tree with potential integer overflow...\n";
        int height = 0;
        bool result = isTreeBalanced(root, height);
        cout << "Result: " << (result ? "true" : "false") << " (may be incorrect due to overflow)\n";
        // Memory leak: No cleanup!
    }

    // Test Case 4: Invalid Pointer Handling
    cout << "\nTest 4: Invalid pointer handling\n";
    {
        Node* root = createNode(1);
        root->left = createNode(2);
        root->right = reinterpret_cast<Node*>(0xDEADBEEF); // Invalid pointer
        cout << "Testing with invalid pointer...\n";
        try {
            int height = 0;
            bool result = isTreeBalanced(root, height);
            cout << "Result: " << (result ? "true" : "false") << "\n";
        } catch(...) {
            cout << "Program should crash before catching\n";
        }
        // Memory leak: No cleanup even if we somehow get here!
    }

    return 0;
}
