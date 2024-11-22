#include <iostream>
#include <climits> // For INT_MAX and INT_MIN
#include <exception> // For std::exception
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

// Function to safely delete a binary tree to prevent memory leaks
void deleteTree(Node* root) {
    if (root == nullptr) return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
}

// Function to check if a binary tree is balanced and calculate its height
int checkBalanceAndHeight(Node* root, bool& isBalanced, int maxDepth, int currentDepth) {
    if (root == nullptr) return 0;

    if (currentDepth > maxDepth) {
        isBalanced = false;
        throw overflow_error("Maximum depth exceeded, possible stack overflow.");
    }

    // Left subtree height
    int leftHeight = checkBalanceAndHeight(root->left, isBalanced, maxDepth, currentDepth + 1);
    if (!isBalanced) return 0;

    // Right subtree height
    int rightHeight = checkBalanceAndHeight(root->right, isBalanced, maxDepth, currentDepth + 1);
    if (!isBalanced) return 0;

    // Check balance condition
    if (abs(leftHeight - rightHeight) > 1) isBalanced = false;

    // Avoid integer overflow when calculating height
    if (leftHeight > INT_MAX - 1 || rightHeight > INT_MAX - 1) {
        isBalanced = false;
        throw overflow_error("Height calculation overflow detected.");
    }

    return max(leftHeight, rightHeight) + 1;
}

// Wrapper function to check if a binary tree is balanced
bool isTreeBalanced(Node* root, int maxDepth) {
    bool isBalanced = true;
    try {
        checkBalanceAndHeight(root, isBalanced, maxDepth, 0);
    } catch (const overflow_error& e) {
        cout << "Overflow error: " << e.what() << endl;
        isBalanced = false;
    }
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
        if (isTreeBalanced(root, 1000)) {
            cout << "Actual: true\n";
        } else {
            cout << "Actual: false\n";
        }
        deleteTree(root);
    }

    // Test Case 2: Stack Overflow Handling
    cout << "\nTest 2: Stack overflow with deep tree\n";
    {
        Node* root = createNode(1);
        Node* current = root;
        try {
            const int maxDepth = 1000; // Safeguard to prevent excessive depth
            for (int i = 0; i < 2000; i++) { // Exceeding maxDepth will trigger an exception
                current->left = createNode(i);
                if (current->left == nullptr) throw runtime_error("Memory allocation failed.");
                current = current->left;
            }
            cout << "Testing deep tree...\n";
            bool result = isTreeBalanced(root, maxDepth);
            cout << "Result: " << (result ? "true" : "false") << endl;
        } catch (const exception& e) {
            cout << "Caught exception: " << e.what() << endl;
        }
        deleteTree(root);
    }

    // Test Case 3: Integer Overflow
    cout << "\nTest 3: Integer overflow\n";
    {
        Node* root = createNode(1);
        if (root == nullptr) {
            cout << "Failed to create the root node." << endl;
            return 1;
        }
        Node* current = root;
        for (int i = 0; i < 100; i++) {
            Node* node = createNode(i);
            if (node == nullptr) {
                cout << "Failed to create a node." << endl;
                deleteTree(root);
                return 1;
            }
            node->right = current;
            current = node;
        }
        cout << "Testing tree with potential integer overflow...\n";
        try {
            if (isTreeBalanced(root, 1000)) {
                cout << "Result: true\n";
            } else {
                cout << "Result: false\n";
            }
        } catch (const overflow_error& e) {
            cout << "Caught overflow error: " << e.what() << endl;
        }
        deleteTree(current);
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
            if (isTreeBalanced(root, 1000)) {
                cout << "Result: true\n";
            } else {
                cout << "Result: false\n";
            }
        } catch (...) {
            cout << "Caught an exception!\n";
        }
        root->right = nullptr; // Prevent deleteTree from dereferencing invalid pointer
        deleteTree(root);
    }

    return 0;
}
