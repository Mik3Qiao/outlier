#include <iostream>
using namespace std;

// Define the structure for a binary tree node
struct Node {
    int data;
    Node* left;
    Node* right;
};

// Function to create a new binary tree node with input validation
Node* createNode(int data) {
    Node* newNode = new Node();
    if (newNode == nullptr) {
        cout << "Memory allocation failed\n";
        return nullptr;
    }
    newNode->data = data;
    newNode->left = newNode->right = nullptr;
    return newNode;
}

// Function to check if a binary tree is balanced and calculate its height
int checkBalanceAndHeight(Node* root, bool& isBalanced) {
    if (root == nullptr)
        return 0;

    int leftHeight = checkBalanceAndHeight(root->left, isBalanced);
    if (!isBalanced)
        return 0;

    int rightHeight = checkBalanceAndHeight(root->right, isBalanced);
    if (!isBalanced)
        return 0;

    if (abs(leftHeight - rightHeight) > 1)
        isBalanced = false;

    return max(leftHeight, rightHeight) + 1;
}

// Function to check if a binary tree is balanced
bool isTreeBalanced(Node* root) {
    bool isBalanced = true;
    checkBalanceAndHeight(root, isBalanced);
    return isBalanced;
}

// Example usage:
int main() {
    // Test Case 1: Basic Working Case
    cout << "\nTest 1: Basic working case\n";
    {
        Node* root = createNode(1);
        if (root == nullptr) {
            cout << "Failed to create the root node." << endl;
            return 1;
        }
        root->left = createNode(2);
        root->right = createNode(3);
        cout << "Expected: true (balanced tree)\n";
        if (isTreeBalanced(root)) {
            cout << "Actual: true\n";
        } else {
            cout << "Actual: false\n";
        }
        // Clean up the dynamically allocated memory
        delete root->left;
        delete root->right;
        delete root;
    }

    // Test Case 3: Integer Overflow
    cout << "\nTest 3: Integer overflow\n";
    {
        Node* root = createNode(1);
        if (root == nullptr) {
            cout << "Failed to create the root node." << endl;
            return 1;
        }
        root->left = createNode(2);
        root->left->left = createNode(3);
        // The height calculation can overflow without proper checks
        for(int i = 0; i < 100; i++) {
            Node* node = createNode(i);
            if (node == nullptr) {
                cout << "Failed to create a node." << endl;
                return 1;
            }
            node->right = root;
            root = node;
        }
        cout << "Testing tree with potential integer overflow...\n";
        if (isTreeBalanced(root)) {
            cout << "Result: true (may be incorrect due to overflow)\n";
        } else {
            cout << "Result: false\n";
        }
        // Clean up the dynamically allocated memory
        // (Implement a proper cleanup function to handle the deep tree)
        // For simplicity, we'll just let the program exit and let the OS clean up
    }

    // Test Case 4: Invalid Pointer Handling
    cout << "\nTest 4: Invalid pointer handling\n";
    {
        Node* root = createNode(1);
        if (root == nullptr) {
            cout << "Failed to create the root node." << endl;
            return 1;
        }
        root->left = createNode(2);
        root->right = reinterpret_cast<Node*>(0xDEADBEEF); // Invalid pointer
        cout << "Testing with invalid pointer...\n";
        try {
            if (isTreeBalanced(root)) {
                cout << "Result: true\n";
            } else {
                cout << "Result: false\n";
            }
        } catch(...) {
            cout << "Caught an exception!\n";
        }
        // Clean up the dynamically allocated memory
        delete root->left;
        delete root;
    }

    return 0;
}